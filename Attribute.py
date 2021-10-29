import numpy as np

from utils import discretizeEF, discretizeEW, entropy


class Attribute:
    def __init__(self,vector,name=""):
        """
            Basic constructor of the Attribute class
        :param vector: Numeric vector containing the information of the attribute
        :param name: Character indicating the name given to the attribute
        """
        if (isinstance(vector,list) or isinstance(vector,np.ndarray)):
            self.vector=vector
            self.name=name
            self.size=len(vector)
            self.type=type(vector[0])
        else:
            raise TypeError("The data parameter must be a list or a numpy array")


    def discretize(self, num_bins, type):
        """
        This function applies equal width discretization to an Attribute
        :param num_bins: Numeric value indicating the number of intervals
        :param type: a Character indicating the type of discretization:  "EW"(Equal Width) or "EF"(Equal Frequency)
        :return:  An Attribute with the factor containing the equal width discretization
        """
        if(type=="EF"):
            self.vector= discretizeEF(self.vector, num_bins)
        else:
            self.vector = discretizeEW(self.vector, num_bins)

    def entropy(self):
        if(type(self.vector[0])=="factor" and self.vector[0]=="integer"):
            return None
        else:
            return entropy(self.vector)

    def normalize(self):
        """
        Function to normalize a given Attribute
        :return: A normalized attribute
        """
        valor = min(self.vector)
        self.vector = (np.array(self.vector))
        self.vector = self.vector - valor
        self.vector = self.vector / valor

    def standardize(self):
        """
        Function to standardize a given Attribute
        :return: A standardized attribute
        """
        media = np.mean(self.vector)
        desviacion = np.std(self.vector)
        estandarizado = (self.vector - media) / desviacion
        self.vector= estandarizado

    def variance(self):
        """
        Function to compute the variance of a given Attribute
        :return: A real number containing the variance of the attribute
        """
        return np.var(self.vector)

    def getName(self):
        """
        Function to get the name of the Attribute
        :return: A string containing the name of the attribute.
        """
        return self.name

    def getVector(self):
        """
        Function to get the list that contain the Attribute
        :return:A vector containing the information of the attribute.
        """
        return self.vector


