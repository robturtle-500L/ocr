import numpy as np
import math

import os
import json


NUM_PIXELS = 400
NN_FILE_NAME = 'nn.json'
TRAINING_SET_FILE_NAME = 'training_set.csv'
TEST_SET_FILE_NAME = 'test_set.csv'

OUTPUTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
OUTPUT_SIZE = len(OUTPUTS)


def _rand_initialize_weights(size_in, size_out):
    return [((x * 0.12) - 0.06) for x in np.random.rand(size_out, size_in)]


class Functions(object):
    def __init__(self):
        self.sigmoid = np.vectorize(self.sigmoid_scalar)
        self.sigmoid_prime = np.vectorize(self.sigmoid_prime_scalar)

    def sigmoid_scalar(self, z):
        return 1 / (1 + math.e ** -z)

    def sigmoid_prime_scalar(self, z):
        return self.sigmoid(z) * (1 - self.sigmoid(z))


class TrainData(object):
    PIXEL_WIDTH = 20

    def __init__(self, label, y0):
        self.label = int(label)
        self.y0 = y0

    def __str__(self):
        return 'TrainData(label={}, len(y0)={})'.format(self.label, len(self.y0))

    def __repr__(self):
        return str(self)


class OCRNeuralNetwork(object):
    def __init__(self, num_hidden_nodes):
        self.num_hidden_nodes = num_hidden_nodes
        self.samples = []
        self.functions = Functions()
        self._resume()

    def _resume(self):
        if (not os.path.isfile(NN_FILE_NAME)):
            self.theta1 = _rand_initialize_weights(
                NUM_PIXELS, self.num_hidden_nodes)
            self.theta2 = _rand_initialize_weights(
                self.num_hidden_nodes, OUTPUT_SIZE)
            self.input_layer_bias = _rand_initialize_weights(
                1, self.num_hidden_nodes)
            self.hidden_layer_bias = _rand_initialize_weights(1, OUTPUT_SIZE)
            self.is_trained = False
        else:
            self.is_trained = True
            self._load_neural_network()

        if os.path.isfile(TRAINING_SET_FILE_NAME):
            self._load_samples(TRAINING_SET_FILE_NAME)

    def add_sample(self, label, y0):
        self.samples.append(TrainData(label, y0))

    def train(self, training_indexes=None, learning_rate=0.1):
        if training_indexes is None:
            training_indexes = range(len(self.samples))
        size = len(training_indexes)
        for i, data in enumerate([self.samples[i] for i in training_indexes]):
            print("training sample: {}/{}".format(i + 1, size))
            # Step 2. forward propagation
            y1 = np.dot(np.mat(self.theta1), np.mat(data.y0).T)
            sum1 = y1 + np.mat(self.input_layer_bias)
            y1 = self.functions.sigmoid(sum1)

            y2 = np.dot(np.array(self.theta2), y1)
            y2 = np.add(y2, self.hidden_layer_bias)
            y2 = self.functions.sigmoid(y2)

            # Step 3. back propagation
            actual_vals = [0] * 10
            actual_vals[data.label] = 1
            output_errors = np.mat(actual_vals).T - np.mat(y2)
            hidden_errors = np.multiply(
                np.dot(np.mat(self.theta2).T,
                       output_errors), self.functions.sigmoid_prime(sum1))

            self.theta1 += learning_rate * \
                np.dot(np.mat(hidden_errors), np.mat(data.y0))
            self.theta2 += learning_rate * \
                np.dot(np.mat(output_errors), np.mat(y1).T)
            self.hidden_layer_bias += learning_rate * output_errors
            self.input_layer_bias += learning_rate * hidden_errors
        self.save_neural_network()

    def predict(self, test):
        y1 = np.dot(np.mat(self.theta1), np.mat(test).T)
        y1 = y1 + np.mat(self.input_layer_bias)
        y1 = self.functions.sigmoid(y1)

        y2 = np.dot(np.array(self.theta2), y1)
        y2 = np.add(y2, self.hidden_layer_bias)
        y2 = self.functions.sigmoid(y2)

        results = y2.T.tolist()[0]
        print(results)
        return results.index(max(results))

    def save_neural_network(self):
        weights = {
            "theta1": [mat.tolist()[0] for mat in self.theta1],
            "theta2": [mat.tolist()[0] for mat in self.theta2],
            "b1": self.input_layer_bias[0].tolist()[0],
            "b2": self.hidden_layer_bias[0].tolist()[0]
        }
        with open(NN_FILE_NAME, 'w') as f:
            json.dump(weights, f)

    def _load_neural_network(self):
        with open(NN_FILE_NAME) as f:
            nn = json.load(f)
        self.theta1 = [np.array(i) for i in nn['theta1']]
        self.theta2 = [np.array(i) for i in nn['theta2']]
        self.input_layer_bias = [np.array(nn['b1'][0])]
        self.hidden_layer_bias = [np.array(nn['b2'][0])]

    def _load_samples(self, path=TRAINING_SET_FILE_NAME):
        with open(path) as f:
            for line in f:
                label, y0 = line.split(':')
                label = int(label)
                y0 = json.loads(y0)
                self.add_sample(label, y0)
