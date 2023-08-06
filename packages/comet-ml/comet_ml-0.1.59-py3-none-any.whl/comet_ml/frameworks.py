'''

Comet

'''
from keras.callbacks import Callback

'''
Extends keras Callback. Provides automatic logging and tracking with Comet
'''


class EmptyKerasCallback(Callback):
    def __init__(self):
        pass

    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_batch_begin(self, batch, logs=None):
        pass

    def on_batch_end(self, batch, logs=None):
        pass

    def on_train_begin(self, logs=None):
        pass


class KerasCallback(Callback):
    def __init__(self, experiment, log_params=True,log_metrics=True):
        '''
        Create a new experiment and submit source code.
        :param api_key: User's API key. Required.
        '''
        super(Callback, self).__init__()
        # Inits the experiment with reference to the name of this class. Required for loading the correct
        # script file
        self.experiment = experiment
        self.log_params = log_params
        self.log_metrics = log_metrics


    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):

        if self.log_metrics:
            self.experiment.log_epoch_end(epoch)
            if logs:
                for name, val in logs.items():
                    self.experiment.log_metric(name, val)


    def on_batch_begin(self, batch, logs=None):
        pass

    def on_batch_end(self, batch, logs=None):
        '''
        Logs training metrics.
        '''
        if logs and self.log_metrics:
            for name, val in logs.items():
                self.experiment.log_metric(name, val)

    def on_train_begin(self, logs=None):
        '''
        Sets model graph.
        '''

        self.experiment.set_model_graph(self.model.to_json())

        if self.log_params:
            if logs:
                for k, v in logs.items():
                    self.experiment.log_parameter(k, v)

            if self.params:
                for k, v in self.params.items():
                    if k is not 'metrics':
                        self.experiment.log_parameter(k, v)


