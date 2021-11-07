import numpy as np

from preprocesspack import Attribute

import pandas as pd


class DataSet:
    def __init__(self, data, name=""):
        """
            Basic constructor of the Dataset class. This function creates an object of class DataSet

            :param data: List containing Attribute objects
            :param name: Character with the name of the dataset
            """
        if (isinstance(data, list) or isinstance(data, np.ndarray)):
            self.data = data
            self.name = name
            self.size = len(self.data)
        else:
            self.data = []
            self.name = name
            self.size = len(self.data)

    def addAttribute(self, attribute):

        if (isinstance(attribute, Attribute.Attribute)):
            self.data.append(attribute)
        elif (isinstance(attribute, list) or isinstance(attribute, np.ndarray)):
            attr = Attribute.Attribute(attribute)
            self.data.append(attr)

    def printDataSet(self):

        names=""
        for j in range(len(self.data)):
            attr=self.data[j]
            name=attr.getName()
            if(len(name)>8):
                name=name[0:8]
            else:
                cuantos=8-len(name)
                name=name+" "*cuantos
            names=names+name+"\t"
        print(names)
        texto=""
        for i in range(self.data[0].size):
           for j in range(len(self.data)):
               attr=self.data[j]

               texto=texto+str(attr.getVector()[i])+"\t"+"\t"
           texto=texto+"\n"

        print (texto)


    def normalize(self,columns=None):
        """
        Function to normalize a DataSet
        :return: A normalized DataSet
        """
        ds = self
        if(columns is None):
            columns=range(len(self.data))
        for i in columns:
            attr=self.data[i]
            ds.data[i]=attr
        return ds

    def standardize(self,columns=None):
        """
        Function to standardize a DataSet
        :return: A standardized DataSet
        """
        if (columns is None):
            columns = range(len(self.data))

        ds = self
        for i in columns:
            attr=self.data[i]
            ds.data[i]=attr
        return ds

    def variance(self):
        """
        This function computes the variance of a given DataSet
        :return: A vector containing the variance of each column data
        """
        var = [attr.variance() for attr in self.data]
        return var

    def entropy(self):
        """
        Function to compute the entropy of a given DataSet
        :return: A vector containing the entropy of each column data if the data is discrete. None otherwise

        """
        entropy = [attr.entropy() for attr in self.data]
        return entropy

    def discretize(self, num_bins, type, columns=None):
        """
        This function computes the dicretization of a given DataSet
        :param num_bins: Numeric value indicating the number of intervals. Default: half the length of the data
        :param type: a String indicating the type of discretization: Default "EW"(Equal Width) or "EF"(Equal Frequency)
        :param columns: Numeric vector indicating the columns in which the discretization must be applied.
        :return: A dataSet with discrete ds. NA otherwise
        """
        if (columns is None):
            columns = range(len(self.data))

        ds = self

        for i in columns:
            attr = self.data[i].discretize(num_bins=num_bins, typeDisc=type)
            ds.data[i]=attr

        return ds

    def getNames(self):
        """
        This function returns the names of the columns of a given DataSet

        :return: A vector containing the name of each column data.
        """
        return [attr.getName() for attr in self.data]

    def rocAuc(self, vIndex, classIndex):
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

    def asDataFrame(self, includeCategorical=True,transpose=True):
        """
        Function to convert a given DataSet in a DataFrame object
        :param includeCategorical: Boolean indicating if the DataFrame will include categorical attributes
        :param transpose: Boolean indicating if the resulting DataFrame has to be transposed
        :return: a DataFrame object with the DataSet information
        """
        matriz = []
        for attr in self.data:
            if attr.isCategorical() == False and includeCategorical == False:
                matriz.append(attr.getVector())
            else:
                matriz.append(attr.getVector())
        if(transpose):
            return pd.DataFrame(matriz).transpose()
        else:
            return pd.DataFrame(matriz)

    def correlation(self):
        """
        Function to compute the correlation matrix between the Attribute pairs of the dataset

        :return:A matrix containing the correlation between attribute pairs.

        """
        correlation=np.zeros((len(self.data),len(self.data)))
        for i in range(len(self.data)):
            v1=self.data[i]
            for j in range(i,len(self.data)):
                v2=self.data[j]
                valor=Attribute.computeCorrelation(v1,v2)
                correlation[i][j]=valor
                correlation[j][i]=valor
        return correlation

    def filter(self,threshold,FUN=None,inverse=False):
        """
         This function returns the filtered DataSet without the unnecessary attributes
        :param FUN: function by which filter the data, it has to return a value per attribute. FUN=correlation by default
        :param threshold: integer value that indicates the limit from which to remove the attribute
        :param inverse:  If TRUE the attribute has to be below the threshold to remove ir.By default FALSE
        :return:A DataSet without the filtered attributes
        """
        data=self
        if(FUN==None):
            cor=self.correlation()
            elimino=set()
            for i in range(len(self.data)):
                for j in range(i,len(self.data)):
                    if (i != j and cor[i][j] >= threshold and inverse==False):
                        elimino.add(i)

                    elif (i != j and cor[i][j] <threshold and inverse):
                        elimino.add(i)
            for id in elimino:
                del data.data[id]
        else:
            result=[FUN(attr.getVector()) for attr in self.data]
            if(inverse):
                elementos=list(filter(lambda x: x > 3, result))
            else:
                elementos=list(filter(lambda x: x < 3, result))
            for elem in elementos:
                data.data.remove(elem)
        return data


def loadDataSet(path, sep=","):
    """
    Function to read a CSV file and save it into a DataSet
    :param path: path to the CSV file
    :param header: logical indicating if the first row of data corresponds to the names
    :param sep: the character separator of the data
    :return: A DataSet containing the data of the CSV file.
    """
    df = pd.read_csv(path, sep=sep)
    ds = DataSet([])
    for column in df:
        attr = Attribute.Attribute(list(df[column]), name=column)
        ds.addAttribute(attr)
    return ds


def saveDataSet(ds, path, sep=","):
    """
    Function to save the DataSet object in a CSV file
    :param ds: DataSet object to save
    :param path: String with the path indicating where to save the DataSet
    :param sep: A character containing the separator of the data, by default ','
    :return:
    """
    df = ds.asDataFrame()
    df.to_csv(path, sep=sep,header=ds.getNames(),index=False)
