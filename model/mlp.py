import numpy as np
import func


class Dense:

    def __init__(self, units, input_dim=None, activation=func.linear):

        self.input_dim = input_dim + 1
        self.units = units

        self.activation = Activation(activation)
        self.d_activation = func.functions[activation]

        self.weights = np.random.random((input_dim, units))
        self.dw = np.zeros(self.weights.shape)

        self.output = None

        self.dropout = None
        self.batch_normalization = None

    def propagate_forward(self, input_data):
        self.output = self.activation.function(input_data, self.weights)

    def modify_weights(self, learning_rate, delta):
        self.weights -= learning_rate*np.dot(self.output.T, delta)

    def add(self, activation=None, dropout=None, batch_normalization=None):

        if activation is not None:
            self.activation = activation
            self.d_activation = func.functions[activation]

        if dropout is not None:
            self.dropout = dropout

        if batch_normalization is not None:
            self.batch_normalization = batch_normalization


class Activation:

    def __init__(self, activation_function):
        self.activation_function = activation_function

    def function(self, input_data, weights):
        return self.activation_function(input_data*weights)


class Dropout:

    def __init__(self):
        pass


class BatchNorm:

    def __init__(self):
        pass


class Sequential:

    def __init__(self):
        self.layers = []
        self.learning_rate = None

    def add(self, layer):

        if type(layer) is Activation:
            self.layers[-1].add(activation=layer)

        elif type(layer) is Dropout:
            self.layers[-1].add(dropout=layer)

        elif type(layer) is BatchNorm:
            self.layers[-1].add(batch_normalization=layer)

        else:
            self.layers.append(layer)

    def fit(self, x_train, y_train, epochs=100, batch_size=32):

        data_set = [(x_train[index], y_train[index]) for index in range(len(x_train))]

        for epoch in range(epochs):

            for data_index, element in enumerate(data_set[::batch_size]):

                deltas = []

                if data_index == 0:
                    continue

                data = data_set[data_index-batch_size:data_index, 0]
                input_data = data[0]

                for layer in self.layers:
                    layer.propagate_forward(input_data)
                    input_data = layer.output

                error = -(data[1] - self.layers[-1].output)

                delta = np.multiply(error, self.layers[-1].d_activation(np.dot(self.layers[-2].output,
                                                                               self.layers[-1].weights)))
                deltas.append(delta)
                for layer_index, layer in enumerate(self.layers[-2:0:-1]):
                    delta = np.dot(deltas[0], layer.weights.T) * \
                            layer.d_activation(np.dot(self.layers[layer_index - 1].output,
                                                      self.layers[layer_index - 1].weights))
                    deltas.insert(0, delta)

                for layer in self.layers:
                    layer.modify_weights()

    def compile(self, loss, optimizer):
        pass

    def predict(self, batch):
        pass


def main():
    model = Sequential()
    model.add(Dense(units=4, input_dim=4))


if __name__ == "__main__":
    main()
