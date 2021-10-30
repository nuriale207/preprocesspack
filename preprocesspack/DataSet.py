import numpy as np

from preprocesspack import Attribute

import pandas as pd
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
            self.data=[]
            self.name = name
            self.size = len(data)

    def addAttribute(self,attribute):

        if (isinstance(attribute, Attribute.Attribute)):
            self.data.append(attribute)
        elif(isinstance(attribute,list) or isinstance(attribute,np.ndarray)):
            attr= Attribute.Attribute(attribute)
            self.data.append(attr)

    def printDataSet(self):
        for attr in self.data:
            print(attr.getVector())

    def normalize(self):
        """
        Function to normalize a DataSet
        :return: A normalized DataSet
        """
        ds=DataSet([],name=self.name)
        for attr in self.data:
            ds.addAttribute(attr.normalize())
        return ds

    def standardize(self):
        """
        Function to standardize a DataSet
        :return: A standardized DataSet
        """
        ds = DataSet([], name=self.name)
        for attr in self.data:
            ds.addAttribute(attr.standardize())
        return ds

    def variance(self):
        """
        This function computes the variance of a given DataSet
        :return: A vector containing the variance of each column data
        """
        var=[attr.variance() for attr in self.data]
        return var

    def entropy(self):
        """
        Function to compute the entropy of a given DataSet
        :return: A vector containing the entropy of each column data if the data is discrete. None otherwise

        """
        entropy = [attr.entropy() for attr in self.data]
        return entropy


    def discretize(self,num_bins,type,columns):
        """
        This function computes the dicretization of a given DataSet
        :param num_bins: Numeric value indicating the number of intervals. Default: half the length of the data
        :param type: a String indicating the type of discretization: Default "EW"(Equal Width) or "EF"(Equal Frequency)
        :param columns: Numeric vector indicating the columns in which the discretization must be applied.
        :return: A dataSet with discrete ds. NA otherwise
        """
        ds = DataSet([], name=self.name)

        for i in columns:
            attr=self.data[i].discretize(num_bins=num_bins, typeDisc=type)
            ds.addAttribute(attr)

        return ds
     
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

        valor = np.array(self.data[vIndex].getVector())
        valor = np.sort(valor)
        etiqueta = np.array(self.data[classIndex].getVector())
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


    def asDataFrame(self):
        matriz=[]
        for attr in self.data:
            if(attr.isCategorical()==False):
                matriz.append(attr.getVector())

        return pd.DataFrame(matriz)

def loadDataSet(path,sep=","):
    """
    Function to read a CSV file and save it into a DataSet
    :param path: path to the CSV file
    :param header: logical indicating if the first row of data corresponds to the names
    :param sep: the character separator of the data
    :return: A DataSet containing the data of the CSV file.
    """
    df = pd.read_csv(path,sep=sep)
    print(df)
    ds=DataSet([])
    for column in df:
        attr=Attribute.Attribute(list(df[column]),name=column)
        ds.addAttribute(attr)
    return ds
