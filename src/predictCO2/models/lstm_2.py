"""
Created by: Tapan Sharma
Date: 14/07/20
"""
import tensorflow
from tensorflow.python.keras.callbacks import TensorBoard

from predictCO2.models.nn_template import NN_Template
from tensorflow.keras import layers, models, optimizers, backend


tensorflow.get_logger().setLevel('INFO')


class LSTM_2(NN_Template):

    def __init__(self, config, num_features, num_outputs):
        """
        Initializer for LSTM RNN.
        :param config: Configuration file containing parameters
        """
        super(LSTM_2, self).__init__(config)
        self.n_feats = num_features
        self.n_ops = num_outputs
        self.build_model()
        self.prediction_tolerance = 1e-1

    def build_model(self):
        """
        Builds the model as specified in the model configuration file.
        """
        self.model = models.Sequential()
        for layer in self.config['model']['layers']:
            neurons = layer['neurons'] if 'neurons' in layer else None
            dropout_rate = layer['rate'] if 'rate' in layer else None
            activation = layer['activation'] if 'activation' in layer else None
            return_seq = layer['return_seq'] if 'return_seq' in layer else None
            input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
            input_dim = self.n_feats

            if layer['type'] == 'dense':
                self.model.add(layers.Dense(neurons, activation=activation))
            if layer['type'] == 'flatten':
                self.model.add(layers.Flatten())
            if layer['type'] == 'lstm':
                self.model.add(
                    layers.LSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
            if layer['type'] == 'dropout':
                self.model.add(layers.Dropout(dropout_rate))
        self.model.compile(loss=self.config['model']['loss'],
                           optimizer=optimizers.Adam(self.config['model']['learning_rate']),
                           metrics=[self.soft_acc])


    def train(self, features, labels):
        pass
