import numpy as np

class NeuralNetwork:
    def __init__(self, network_architecture):
        # network architecture is an array
        #  for example [100,10,10,4]  has 100 inputs two hidden layers of size 10 and 4 outputs
        self.network_architecture = network_architecture
        self.network_len = len(network_architecture)        # network length is minumum 2 which correspond to input and output layers
        self.inputs = network_architecture[0]               # first index is the input layer size
        self.outputs = network_architecture[-1]             # last index is the output layer size
        self.parameters = {}

    def initializeNetwork(self):
        for i in range(self.network_len-1):
            layerSize = self.network_architecture[i]
            nextLayerSize = self.network_architecture[i+1]
            self.parameters["W" + str(i+1)] = np.random.uniform(-1,1,[layerSize, nextLayerSize])
            self.parameters["b" + str(i+1)] = np.zeros([1, nextLayerSize])

    def reLU(self,Z):
        return np.maximum(0,Z)

    def forwardProp(self, X):
        A = X
        for i in range(1, len(self.parameters)//2 + 1):
            Z = np.dot(A, self.parameters["W" + str(i)]) + self.parameters["b" + str(i)]
            A = self.reLU(Z)

        return np.argmax(A)

