from turtle import pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def correlationMatrix(dataset):
    """
    Function to visualize the correlation of a given dataset

    :param dataset:  object of class DataSet
    :return: A plot with the visualization of the correlation matrix
    """
    df=pd.DataFrame(dataset.data)

    correlation=df.corr()
    ax = plt.axes()
    sns.heatmap(correlation, ax = ax,cmap="YlGnBu",center=0.5)
    ax.set_title('Correlation Plot')
    plt.show()

def entropyPlot(dataset):
    """
     Function to visualize the entropy of a given dataset
    :param dataset: object of class DataSet
    :return: A plot with the visualization
    """
    return

def rocPlot(dataset, vIndex,classIndex):
    """
    Function to visualize the ROC curve of a given DataSet
    :param dataset: DataSet class vector
    :param vIndex: index of the continuous variable to compute the AUC
    :param classIndex: index of the class
    :return: A plot with the curve
    """
    valor = np.array(dataset.data[vIndex])
    valor = np.sort(valor)
    etiqueta = np.array(dataset.data[classIndex])
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