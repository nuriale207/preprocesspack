import numpy as np

import Attribute


class DataSet:
    def __init__(self,data,name=""):
        """
            Basic constructor of the Dataset class. This function creates an object of class DataSet

            :param data: List containing Attribute objects
            :param name: Character with the name of the dataset
            """
        if (isinstance(data,list) or isinstance(data,np.ndarray)):
            self.data=data
            self.name=name
            self.size=len(data)
        else:
            raise TypeError("The data parameter must be a list or a numpy array")

    def addAttribute(self,attribute):
        if (isinstance(attribute,Attribute)):
            self.data.append(attribute)
        elif(isinstance(attribute,list) or isinstance(attribute,np.ndarray)):
            attr=Attribute(attribute)

    def normalize(self):
        """
        Function to normalize a DataSet
        :return: A normalized DataSet
        """
        for attr in self.data:
            attr.normalize()

    def standardize(self):
        """
        Function to standardize a DataSet
        :return: A standardized DataSet
        """
        for attr in self.data:
            attr.standardize()

    def variance(self):
        """
        This function computes the variance of a given DataSet
        :return: A vector containing the variance of each column data
        """
        var=[attr.variance for attr in self.data]
        return var

    def entropy(self):
        """
        Function to compute the entropy of a given DataSet
        :return: A vector containing the entropy of each column data if the data is discrete. None otherwise

        """
        entropy = [attr.entropy for attr in self.data]
        return entropy


    def discretize(self,num_bins,type,columns):
        """
        This function computes the dicretization of a given DataSet
        :param num_bins: Numeric value indicating the number of intervals. Default: half the length of the data
        :param type: a String indicating the type of discretization: Default "EW"(Equal Width) or "EF"(Equal Frequency)
        :param columns: Numeric vector indicating the columns in which the discretization must be applied. By default the discretization of every column will be computed
        :return: A vector containing the entropy of each column data if the data is discrete. NA otherwise
        """
        for i in columns:
            self.data[i].discretize(num_bins=num_bins,type=type)
     
    def getNames(self):
        """
        This function returns the names of the columns of a given DataSet

        :return: A vector containing the name of each column data.
        """
        return [attr.getName() for attr in self.data]

    def rocAuc(self,vIndex, classIndex):
        """
        Function to compute the AUC-ROC of the DataSet
        :param vIndex: index of the continuous variable to compute the AUC
        :param classIndex: index of the class
        :return: The value of the AUC-ROC
        """

        valor = np.array(self.data[vIndex])
        valor = np.sort(valor)
        etiqueta = np.array(self.data[classIndex])
        TPR = []
        FPR = []
        for i in range(len(valor)):
            predicciones = valor >= valor[i]
            TP = 0
            TN = 0
            FN = 0
            FP = 0
            for j in range(len(predicciones)):
                if (etiqueta[j] == predicciones[j] and predicciones[j] == True):
                    TP = TP + 1;
                elif (etiqueta[j] == predicciones[j] and predicciones[j] == False):
                    TN = TN + 1
                elif (etiqueta[j] == 1 and predicciones[j] == 0):
                    FN = FN + 1
                else:
                    FP = FP + 1
            TPR.append(TP / (TP + FN))
            FPR.append(FP / (FP + TN))
        dFPR = np.diff(FPR)
        dTPR = np.diff(TPR)
        dFPR = np.append(dFPR, 0)
        dTPR = np.append(dTPR, 0)
        AUC = sum(TPR * dFPR) + sum(dTPR * dFPR) / 2

        return AUC

