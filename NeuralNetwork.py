import numpy as np

class NeuralNetwork:
    def __init__(self, network_architecture):
        # network architecture is an array
        #  for example [100,10,10,4]  has 100 inputs two hidden layers of size 10 and 4 outputs
        self.network_architecture = network_architecture
        self.network_len = len(network_architecture)        # network length is minumum 2 which correspond to input and output layers
        self.inputs = network_architecture[0]               # first index is the input layer size
        self.outputs = network_architecture[-1]             # last index is the output layer size
        self.parameters = {}                                # this parameters will be filled with initializeNetwork function

    # function to initialize random weights and biases to the network
    def initializeNetwork(self):
        for i in range(self.network_len-1):
            # layerSize and nextLayerSize are sized determined by the user and will be used for creating the weight matrices
            layerSize = self.network_architecture[i]
            nextLayerSize = self.network_architecture[i+1]

            # initialize weights between -1 and 1 and biases as zero
            self.parameters["W" + str(i+1)] = np.random.uniform(-1,1,[layerSize, nextLayerSize])
            #self.parameters["b" + str(i+1)] = np.zeros([1, nextLayerSize])

    # if input Z is less than zero returns zero if its not it returns Z
    def reLU(self,Z):
        return np.maximum(0,Z)

    # takes input X and gets the dot product sequantially through the network until output(prediction) is produced
    def forwardProp(self, X):
        A = X
        for i in range(1, len(self.parameters)//2 + 1):
            Z = np.dot(A, self.parameters["W" + str(i)]) # + self.parameters["b" + str(i)]
            A = self.reLU(Z)
        # returns the argmax of the output array which can be indexes 0,1,2,3
        # these will correspond to up, down, left and right directions for the snake
        return np.argmax(A)

