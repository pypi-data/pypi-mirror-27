'''
Author: Gideon Mendels

This module contains the main components of comet.ml client side

'''
from __future__ import print_function
import inspect
import threading
import sys, os

from six.moves.queue import Queue

import requests
import json
import uuid

import time

import websocket

import comet_ml
from comet_ml import config
from comet_ml import sklearn_logger
from comet_ml import keras_logger
from comet_ml import file_uploader
from comet_ml.json_encoder import NestedEncoder

DEBUG = False

"""
A static class that handles the connection with the server.
"""
server_address = os.environ.get('COMET_URL_OVERRIDE', 'https://www.comet.ml/clientlib/logger/')


class RestServerConnection(object):
    def __init__(self):
        pass

    @staticmethod
    def get_run_id(api_key, project_name):
        """
        Gets a new run id from the server.
        :param api_key: user's API key
        :return: run_id - String
        """
        endpoint_url = server_address + "add/run"
        headers = {'Content-Type': 'application/json;charset=utf-8'}

        try:
            version_num = comet_ml.__version__
        except NameError:
            version_num = None

        payload = {"apiKey": api_key, "local_timestamp": int(time.time() * 1000), "projectName": project_name,
                   "libVersion": version_num}
        r = requests.post(url=endpoint_url, data=json.dumps(payload), headers=headers)

        if r.status_code != 200:
            raise ValueError(r.content)

        res_body = json.loads(r.content.decode('utf-8'))
        run_id_server = res_body["runId"]
        ws_server = res_body["ws_url"]

        if "project_id" in res_body:
            project_id = res_body["project_id"]
        else:
            project_id = None

        if "githubEnabled" in res_body:
            is_github = res_body['githubEnabled']
        else:
            is_github = False

        if "msg" in res_body:
            print(res_body["msg"])

        return run_id_server, ws_server, project_id, is_github

    @staticmethod
    def send_message(message):
        """
        Sends a json with stdout/metric/code to the server.
        :param message: A message object containing the values to send
        :return: True if request was sucessful.
        """
        global run_id

        if message.stdout is not None:
            base_url = server_address + "add/stdout"
        else:
            base_url = server_address + "add/data"

        headers = {'Content-Type': 'application/json;charset=utf-8'}
        r = requests.post(url=base_url, data=message.to_json(), headers=headers)

        if r.status_code != 200:
            raise ValueError(r.content + ",to address %s With request: %s" % (base_url, message))

        if run_id is None:
            run_id = json.loads(r.content)['message']

        return True


class WebSocketConnection(threading.Thread):
    def __init__(self, server_address):
        threading.Thread.__init__(self)
        self.priority = 0.2
        self.daemon = True

        if DEBUG:
            websocket.enableTrace(True)

        self.address = server_address
        self.ws = self.connect_ws(self.address)

    def is_connected(self):
        if self.ws.sock is not None:
            return self.ws.sock.connected
        else:
            return False

    def connect_ws(self, server_address):
        ws = websocket.WebSocketApp(server_address,
                                    on_message=WebSocketConnection.on_message,
                                    on_error=WebSocketConnection.on_error,
                                    on_close=WebSocketConnection.on_close)
        ws.on_open = WebSocketConnection.on_open
        return ws

    def run(self):
        while True:
            try:
                self.ws.run_forever()
            except Exception as e:
                if sys is not None and DEBUG:
                    print(e, file=sys.stderr)

    def send(self, messages):
        """ Encode the messages into JSON and send them on the websocket
        connection
        """
        data = self._encode(messages)
        self._send(data)

    def _encode(self, messages):
        """ Encode a list of messages into JSON
        """
        messagesArr = []
        for message in messages:
            payload = {}
            # make sure connection is actually alive
            if message.stdout is not None:
                payload["stdout"] = message
            else:
                payload["log_data"] = message

            messagesArr.append(payload)

        data = json.dumps(messagesArr, cls=NestedEncoder, allow_nan=False)
        return data

    def _send(self, data):
        if self.ws.sock:
            self.ws.send(data)
            return
        else:
            self.wait_for_connection()

    def wait_for_connection(self):

        if not self.is_connected():
            num_tries = 0

            while not self.is_connected() and num_tries < 5:
                time.sleep(2)
                num_tries += 1

            if not self.is_connected():
                raise ValueError("Could not connect to server after multiple tries. ")

        return True

    @staticmethod
    def on_open(ws):
        if DEBUG:
            print("Socket connection open")

    @staticmethod
    def on_message(ws, message):
        if DEBUG:
            print(message)

    @staticmethod
    def on_error(ws, error):
        error_type_str = type(error).__name__
        ignores = ['WebSocketBadStatusException', 'error', 'WebSocketConnectionClosedException',
                   'ConnectionRefusedError', 'BrokenPipeError']

        if not DEBUG and error_type_str in ignores:
            return

        print(error)

    @staticmethod
    def on_close(ws):
        if DEBUG:
            print("### closed ###")


'''
This class extends threading.Thread and provides a simple concurrent queue
and an async service that pulls data from the queue and sends it to the server.
'''


class Streamer(threading.Thread):
    def __init__(self, ws_server_address):
        threading.Thread.__init__(self)
        self.daemon = True
        self.messages = Queue()
        self.counter = 0
        self.ws_connection = WebSocketConnection(ws_server_address)
        self.ws_connection.start()
        self.ws_connection.wait_for_connection()

    def put_messge_in_q(self, message):
        '''
        Puts a message in the queue
        :param message: Some kind of payload, type agnostic
        '''
        if message is not None:
            self.messages.put(message)

    def close(self):
        '''
        Puts a None in the queue which leads to closing it.
        '''
        self.messages.put(None)
        self.messages.join()

    def run(self):
        '''
        Continuously pulls messages from the queue and sends them to the server.
        '''
        self.ws_connection.wait_for_connection()

        while True:
            try:
                if self.ws_connection is not None and self.ws_connection.is_connected():
                    messages = self.getn(1)

                    if messages is None:
                        break

                    self.ws_connection.send(messages)

            except Exception as e:
                if sys is not None:
                    print(e, file=sys.stderr)
        return

    def getn(self, n):
        msg = self.messages.get() # block until at least 1
        self.counter += 1
        msg.set_offset(self.counter)
        result = [msg]
        try:
            while len(result) < n:
                anotherMsg = self.messages.get(block=False)  # dont block if no more messages
                self.counter += 1
                anotherMsg.set_offset(self.counter)
                result.append(anotherMsg)
        except:
            pass
        return result

    def waitForFinish(self):
        print("uploading stats to Comet before program termination (may take several seconds)")

        import time
        startTime = time.time()

        while not self.messages.empty():
            now = time.time()
            if (now - startTime > 30):
                break
        if config.experiment is not None:
            if config.experiment.alive:
                print(config.experiment.experiment_url)
            else:
                print("failed to log run in comet.ml")
        else:
            print("failed to log run in comet.ml")

'''
A class the overwrites sys.stdout with itself.
The class prints everything as normal to console but also submits
every line to Streamer
'''


class StdLogger(object):
    # todo: this doesn't log the output from C libs (tensorflow etc)
    def __init__(self, streamer, run_id, project_id):
        '''
        :param streamer: An instance of Streamer() to allow sending to server.
        '''
        self.terminal = sys.stdout
        self.streamer = streamer
        self.api_key = None
        self.run_id = run_id
        self.project_id = project_id
        sys.stdout = self

    def write(self, line):
        '''
        Overrides the default IO write(). Writes to console + queue.
        :param line: String printed to stdout, probably with print()
        '''
        self.terminal.write(line)
        payload = Message(api_key=self.api_key, experiment_key=None, run_id=self.run_id, project_id=self.project_id)
        payload.set_stdout(line)
        self.streamer.put_messge_in_q(payload)

    def flush(self):
        self.terminal.flush()

    def set_api_key(self, key):
        self.api_key = key

    def isatty(self):
        return False


INFINITY = float('inf')


def fix_special_floats(value, _inf=INFINITY, _neginf=-INFINITY):
    """ Fix out of bounds floats (like infinity and -infinity) and Not A
    Number.
    Returns either a fixed value that could be JSON encoded or the original
    value.
    """

    # Check if the value is Nan, equivalent of math.isnan
    if value != value:
        return "NaN"
    elif value == _inf:
        return "Infinity"
    elif value == _neginf:
        return "-Infinity"

    return value



class Message(object):
    def __init__(self, api_key, experiment_key, run_id, project_id):
        self.apiKey = api_key
        self.experimentKey = experiment_key
        self.runId = run_id
        self.projectId = project_id
        self.local_timestamp = int(time.time() * 1000)

        # The following attributes are optional
        self.metric = None
        self.param = None
        self.graph = None
        self.code = None
        self.stdout = None
        self.offset = None
        self.fileName = None
        self.html = None
        self.installed_packages = None
        self.log_other = None

    def set_log_other(self, key, value):
        self.log_other = {"key": key, "val": value}

    def set_installed_packages(self, val):
        self.installed_packages = val

    def set_offset(self, val):
        self.offset = val

    def set_metric(self, name, value):
        safe_value = fix_special_floats(value)
        self.metric = {"metricName": name, "metricValue": safe_value}

    def set_html(self, value):
        self.html = value

    def set_param(self, name, value):
        safe_value = fix_special_floats(value)
        self.param = {"paramName": name, "paramValue": safe_value}

    def set_graph(self, graph):
        self.graph = graph

    def set_code(self, code):
        self.code = code

    def set_stdout(self, line):
        self.stdout = line

    def set_filename(self, fname):
        self.fileName = fname

    def to_json(self):
        json_re = json.dumps(self.repr_json(), sort_keys=True, indent=4, cls=NestedEncoder)
        return json_re

    def repr_json(self):
        return self.__dict__

    def __str__(self):
        return self.to_json()

    def __len__(self):
        return len(self.to_json())
