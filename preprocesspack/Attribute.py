import math

import numpy as np
import sklearn
from preprocesspack import utils
#from utils import discretizeEF, discretizeEW, entropy


class Attribute:
    def __init__(self, vector, name=""):
        """
            Basic constructor of the Attribute class
        :param vector: Numeric vector containing the information of the attribute
        :param name: Character indicating the name given to the attribute
        """
        if (isinstance(vector, list) or isinstance(vector, np.ndarray)):
            if (len(vector) >= 1):

                self.vector = vector
                self.name = name
                self.size = len(vector)
                self.type = type(vector[0])
                if (type(vector[0])== str):
                    self.vector=self.getCatAsInt()

            else:
                raise ValueError("The vector parameter must have at least one element")
        else:
            raise TypeError("The vector parameter must be a list or a numpy array")

    def isCategorical(self):
        if(type(self.vector[0]) is tuple):
            return True
        else:
            return False

    def discretize(self, num_bins, typeDisc):
        """
        This function applies equal width discretization to an Attribute
        :param num_bins: Numeric value indicating the number of intervals
        :param typeDisc: a Character indicating the type of discretization:  "EW"(Equal Width) or "EF"(Equal Frequency)
        :return:  An Attribute with the factor containing the equal width discretization
        """

        if (type(self.vector[0]) is tuple):
            return Attribute(self.vector, self.name)
        else:
            if (typeDisc == "EF"):
                vector = utils.discretizeEF(self.vector, num_bins)[0]
            else:
                vector = utils.discretizeEW(self.vector, num_bins)[0]
            return Attribute(vector, self.name)

    def entropy(self):
        if (type(self.vector[0]) is tuple or (type(self.vector[0]) is int)):
            return utils.entropy(self.vector)
        else:
            return None

    def normalize(self):
        """
        Function to normalize a given Attribute.
        :return: A normalized attribute. If the attribute is categorical it will return a copy of the original attribute
        """
        vector = self.vector.copy()
        if (type(self.vector[0]) is tuple):
            return Attribute(vector, self.name)
        else:
            # valor = min(self.vector)
            # vector = (np.array(vector))
            # vector = vector - valor
            # vector = vector / valor
            mod = math.sqrt(np.sum(np.power(self.vector, 2)))
            vector=np.divide(vector,mod)
            return Attribute(vector, self.name)

    def standardize(self):
        """
        Function to standardize a given Attribute
        :return: A standardized attribute. If the attribute is categorical it will return a copy of the original attribute
        """
        vector = self.vector.copy()
        if (type(self.vector[0]) is tuple):
            return Attribute(vector, self.name)
        else:
            media = np.mean(vector)
            desviacion = np.std(vector)
            estandarizado = (vector - media) / desviacion
            return Attribute(estandarizado, self.name)

    def variance(self):
        """
        Function to compute the variance of a given Attribute
        :return: A real number containing the variance of the attribute
        """
        if (self.isCategorical()):
            return None
        else:
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

    def printAttribute(self):
        print(self.name)
        for i in self.vector:
            print(i)

    def getCatAsInt(self):
        if(self.isCategorical()):
            elements = set(self.vector)
            diccionario = dict(zip(elements, range(0, len(elements))))
            return [diccionario[x] for x in self.vector]
        else:
            return self.vector

def computeCorrelation(x,y,discretizationType="EW",num_bins=3):
    """
    This function computes the correlation between two vectors

    :param x: a vector
    :param y: a vector
    :param discretizationType: if x and y are a mix of continuous and discrete variables a discretization is computed
    in the continuous one. This parameter indicates the discretization type to compute: equal width "EW"
    (default) or equal frequency "EF"
    :param num_bins: if x and y are a mix of continuous and discrete variables a discretization is computed
    in the continuous one. This parameter indicates the number of intervals to use in the discretization.
    It's the  of y/3 by default
    :return: A real number with the correlation between both vectors
    """
    xVector = x.getVector()
    yVector = y.getVector()
    if(x.isCategorical()==False and y.isCategorical()==True):
        if(discretizationType=="EW"):
            xVector=utils.discretizeEW(x.getVector(),num_bins)[0]
            xDisc=Attribute(xVector)

        else:
            xVector=utils.discretizeEF(x.getVector(),num_bins)[0]
            xDisc=Attribute(xVector)


        return sklearn.metrics.mutual_info_score(xDisc.getCatAsInt(), y.getCatAsInt())

    if (x.isCategorical() == True and y.isCategorical() == False):

        if (discretizationType == "EW"):
            yVector = utils.discretizeEW(y.getVector(), num_bins)[0]
            yDisc=Attribute(yVector)

        else:
            yVector = utils.discretizeEF(y.getVector(), num_bins)[0]
            yDisc=Attribute(yVector)

        return sklearn.metrics.mutual_info_score(x.getCatAsInt(), yDisc.getCatAsInt())


    if (x.isCategorical() == True and y.isCategorical() == True):

        return sklearn.metrics.mutual_info_score(x.getCatAsInt(), y.getCatAsInt())
    else:
        return np.corrcoef(xVector,yVector)[0][1]


