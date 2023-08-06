"""comet-ml"""
from __future__ import print_function

import atexit
import inspect
import os
import os.path
import sys
import uuid

from pkg_resources import DistributionNotFound, get_distribution

from .comet import (Message, RestServerConnection, StdLogger, Streamer, config,
                    file_uploader, server_address)

try:
    __version__ = get_distribution('comet_ml').version
except DistributionNotFound:
    __version__ = 'Please install comet with `pip install comet_ml`'

__author__ = 'Gideon <Gideon@comet.ml>'
__all__ = ['Experiment']


class Experiment(object):
    '''
    An instance of experiment. Takes the values from the different
    implementations and unifies them for the server. Basically submits stuff
    to the Streamer queue.
    '''

    def __init__(self, api_key, project_name=None, log_code=True, auto_param_logging=True, auto_metric_logging=True):
        '''
        Init a new experiment.
        :param api_key: key used to send data to server.
        '''
        config.experiment = self

        self.project_name = project_name
        if api_key is None:
            self.api_key = os.getenv("COMET_API_KEY", None)
        else:
            self.api_key = api_key

        if self.api_key is None:
            raise ValueError("Comet.ml requires an API key. Please provide as the first argument to Experiment("
                             "api_key) or as an environment variable named COMET_API_KEY ")

        self.auto_param_logging = auto_param_logging
        self.auto_metric_logging = auto_metric_logging

        # Generate a unique identifier for this experiment.
        self.id = self._generate_guid()
        self.alive = False
        is_github = False

        global streamer
        global logger
        global run_id
        global project_id

        def _generate_experiment_url():
            project_name_str = self.project_name

            if (project_name_str is None):
                project_name_str = "General"

            return "go to https://www.comet.ml/User/%s?focus=%s to view your run." % (project_name_str, self.id)

        self.experiment_url = _generate_experiment_url()

        try:
            # This init the streamer and logger for the first time.
            # Would only be called once.
            if (streamer is None and logger is None):
                # Get an id for this run
                try:
                    run_id, ws_server_address, project_id, is_github = RestServerConnection.get_run_id(self.api_key,
                                                                                                       self.project_name)
                    full_ws_url = ws_server_address + "?apiKey=" + api_key + "&runId=" + run_id
                except ValueError:
                    print("Failed to establish connection to Comet server. Please check you internet connection. Your "
                          "experiment would not be logged")
                    return

                # Initiate the streamer
                streamer = Streamer(full_ws_url)
                # Overwride default sys.stdout and feed to streamer.
                logger = StdLogger(streamer, run_id, project_id)
                # Start streamer thread.
                streamer.start()

            self.streamer = streamer
            logger.set_api_key(self.api_key)

            self.alive = True

        except Exception as e:
            print('%s \n comet.ml error: run will not be logged' % e)

        # This allows different implementations to provide the correct source code with logging
        # our library code.
        try:
            if self.__in_notebook():
                self.set_notebook_name()
            else:
                self.filename = self._get_filename()
                self.set_filename(self.filename)

            self.set_pip_packages()
            self.set_cmd_args()

            if log_code:
                # only report code if user asked us
                self.set_code(self._get_source_code())

                if is_github:
                    # if user asked to log code and he has a github project linked. sync that.
                    file_uploader.upload_repo_start_process(project_id, self.id, self.filename,
                                                            server_address + "repoRoot", server_address + "uploadFiles")

        except Exception as e:
            print('%s \n comet.ml error: failed to set run metadata (code/pip/file-name)' % e)

        print(self.experiment_url)

    def _create_message(self):
        return Message(self.api_key, self.id, run_id, project_id)

    def log_other(self, key, value):
        if self.alive:
            message = self._create_message()
            message.set_log_other(key, value)
            self.streamer.put_messge_in_q(message)

    def log_html(self, html):
        if self.alive:
            message = self._create_message()
            message.set_html(html)
            self.streamer.put_messge_in_q(message)

    def log_step_end(self, step):
        if self.alive:
            message = self._create_message()
            message.set_param("curr_step", step)
            self.streamer.put_messge_in_q(message)

    def log_accuracy(self, acc):
        self.log_metric("accuracy", acc)

    def log_f1(self, val):
        self.log_metric("f1", val)

    def log_f1_micro(self, val):
        self.log_metric("f1_micro", val)

    def log_f1_macro(self, val):
        self.log_metric("f1_macro", val)

    def log_f1_weighted(self, val):
        self.log_metric("f1_weighted", val)

    def log_f1_samples(self, val):
        self.log_metric("f1_samples", val)

    def log_neg_log_loss(self, val):
        self.log_metric("neg_log_loss", val)

    def log_roc_auc(self, val):
        self.log_metric("roc_auc", val)

    def log_precision(self, val):
        self.log_metric("precision", val)

    def log_recall(self, val):
        self.log_metric("recall", val)

    def log_auc(self, val):
        self.log_metric("auc", val)

    def log_adjusted_mutual_info_score(self, val):
        self.log_metric("adjusted_mutual_info_score", val)

    def log_adjusted_rand_score(self, val):
        self.log_metric("adjusted_rand_score", val)

    def log_completeness_score(self, val):
        self.log_metric("completeness_score", val)

    def log_fowlkes_mallows_score(self, val):
        self.log_metric("fowlkes_mallows_score", val)

    def log_homogeneity_score(self, val):
        self.log_metric("homogeneity_score", val)

    def log_mutual_info_score(self, val):
        self.log_metric("mutual_info_score", val)

    def log_average_precision(self, val):
        self.log_metric("average_precision", val)

    def log_normalized_mutual_info_score(self, val):
        self.log_metric("normalized_mutual_info_score", val)

    def log_v_measure_score(self, val):
        self.log_metric("v_measure_score", val)

    def log_explained_variance(self, val):
        self.log_metric("explained_variance", val)

    def log_neg_mean_absolute_error(self, val):
        self.log_metric("neg_mean_absolute_error", val)

    def log_neg_mean_squared_error(self, val):
        self.log_metric("neg_mean_squared_error", val)

    def log_neg_mean_squared_log_error(self, val):
        self.log_metric("neg_mean_squared_log_error", val)

    def log_neg_median_absolute_error(self, val):
        self.log_metric("neg_median_absolute_error", val)

    def log_r2(self, val):
        self.log_metric("r2", val)

    def log_loss(self, loss):
        self.log_metric("loss", loss)

    def log_step(self, step):
        self.log_parameter("curr_step", step)

    def log_epoch_end(self, epoch_cnt):
        '''
        Logs that the current epoch finished + number. required for progress bars.
        :param epoch_cnt: integer
        '''
        if self.alive:
            message = self._create_message()
            message.set_param("curr_epoch", epoch_cnt)
            self.streamer.put_messge_in_q(message)

    def log_metric(self, name, value):
        """
        Logs a metric (i.e accuracy, f1). Required for training visualizations.
        :param name: Metric name - String
        :param value: Metric value - float
        """
        if self.alive:
            message = self._create_message()
            message.set_metric(name, value)
            self.streamer.put_messge_in_q(message)

    def log_parameter(self, name, value):
        '''
        Logs an hyper parameters
        :param name: Parameter name - String
        :param value: Parameter value - String
        '''
        if self.alive:
            message = self._create_message()
            message.set_param(name, value)
            self.streamer.put_messge_in_q(message)

    def set_num_of_epocs(self, num):
        pass

    def log_epoch_ended(self):
        pass

    def log_current_epoch(self, value):
        if self.alive:
            message = self._create_message()
            message.set_metric('curr_epoch', value)
            self.streamer.put_messge_in_q(message)

    def log_multiple_params(self, dic, prefix=None):
        if self.alive:
            for k, v in dic.items():
                if prefix is not None:
                    k = prefix + "_" + str(k)

                self.log_parameter(k, v)

    def log_dataset_hash(self, data):
        try:
            import hashlib
            data_hash = hashlib.md5(str(data).encode('utf-8')).hexdigest()
            self.log_parameter("dataset_hash", data_hash[:12])
        except:
            print('failed to create dataset hash')

    def set_code(self, code):
        '''
        Sets the current experiment script's code. Should be called once per experiment.
        :param code: String
        '''
        if self.alive:
            message = self._create_message()
            message.set_code(code)
            self.streamer.put_messge_in_q(message)

    def set_model_graph(self, graph):
        '''
        Sets the current experiment computation graph.
        :param graph: JSON
        '''
        if self.alive:

            if type(graph).__name__ == "Graph":  # Tensorflow Graph Definition
                from google.protobuf import json_format
                graph_def = graph.as_graph_def()
                graph = json_format.MessageToJson(graph_def)

            message = self._create_message()
            message.set_graph(graph)
            self.streamer.put_messge_in_q(message)

    def set_filename(self, fname):
        if self.alive:
            message = self._create_message()
            message.set_filename(fname)
            self.streamer.put_messge_in_q(message)

    def set_notebook_name(self):
        self.set_filename("Notebook")

    def set_pip_packages(self):
        if self.alive:
            try:
                import pip
                installed_packages = pip.get_installed_distributions()
                installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                                  for i in installed_packages])
                message = self._create_message()
                message.set_installed_packages(installed_packages_list)
                self.streamer.put_messge_in_q(message)
            except:  # TODO log/report error
                pass

    def set_cmd_args(self):
        if self.alive:
                args = Experiment._get_cmd_args_dic()
                if args is not None:
                    for k,v in args:
                        message = self._create_message()
                        message.set_param(k,v)
                        self.streamer.put_messge_in_q(message)

    @staticmethod
    def _get_cmd_args_dic():
        if len(sys.argv) > 1:
            try:
                return Experiment._parse_cmd_args(sys.argv[1:])
            except ValueError as e:
                print(e)
                return Experiment._parse_cmd_args_naive(sys.argv[1:])


    @staticmethod
    def _parse_cmd_args_naive(to_parse):
        vals = {}
        if len(to_parse) > 1:
            for i, arg in enumerate(to_parse):
                vals["run_arg_%s" % i] = str(arg)

        return vals


    @staticmethod
    def _parse_cmd_args(input):

        def guess_type(s):
            import ast
            try:
                value = ast.literal_eval(s)
                return value

            except ValueError:
                return str(s)

        results = {}

        current_key = None
        for word in input:
            word = word.strip()
            prefix = 0

            if word[0] == '-':
                prefix = 1
                if len(word) > 1 and word[1] == '-':
                    prefix = 2

                if current_key is not None:
                    # if we found a new key but haven't found a value to the previous
                    # key it must have been a boolean argument.
                    results[current_key] = True

                current_key = word[prefix:]


            else:
                word = word.strip()
                if current_key is None:
                    # we failed to parse the string. We think this is a value but we don't know what's the key.
                    # fallback to naive parsing.
                    raise ValueError("Failed to parse argv arguments")
                else:
                    word = guess_type(word)
                    results[current_key] = word
                    current_key = None

        if current_key is not None:
            # last key was a boolean
            results[current_key] = True

        return results

    def keras_callback(self):
        if self.alive:
            from comet_ml.frameworks import KerasCallback
            return KerasCallback(self, log_params=self.auto_param_logging, log_metrics=self.auto_metric_logging)
        else:
            from comet_ml.frameworks import EmptyKerasCallback
            return EmptyKerasCallback()

    def _get_source_code(self):
        '''
        Inspects the stack to detect calling script. Reads source code from disk and logs it.
        '''

        class_name = self.__class__.__name__

        for frame in inspect.stack():
            if class_name in frame[4][0]:  # 4 is the position of the calling function.
                path_to_source = frame[1]
                if os.path.isfile(path_to_source):
                    with open(path_to_source) as f:
                        return f.read()
                else:
                    print("Failed to read source code file from disk: %s" % path_to_source, file=sys.stderr)

    def _get_filename(self):

        if (len(sys.argv) > 0):
            pathname = os.path.dirname(sys.argv[0])
            abs_path = os.path.abspath(pathname)
            filename = os.path.basename(sys.argv[0])
            full_path = os.path.join(abs_path, filename)
            return full_path
        else:
            return None

    @staticmethod
    def _generate_guid():
        return str(uuid.uuid4()).replace("-","")

    @staticmethod
    def __in_notebook():
        """
        Returns ``True`` if the module is running in IPython kernel,
        ``False`` if in IPython shell or other Python shell.
        """
        return 'ipykernel' in sys.modules


def on_exit_dump_messages():
    if streamer is not None:
        streamer.waitForFinish()


streamer = None
logger = None
run_id = None
project_id = None

atexit.register(on_exit_dump_messages)