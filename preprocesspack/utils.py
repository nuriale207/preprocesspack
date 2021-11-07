import math
from datetime import datetime


def __discretizePoints(x,cut_points):
    """
    Function to discretize a vector given a list of cutpoints.
    This function dicretizes a vector given the list of points to cut
    :param x: a vector composed by real numbers
    :param cut_points:a list with the points at which the vector has to be cut
    :return: A factor with the discretization
    """
    vCat = [1] * len(x)

    for i in range(0, len(x)):
        for j in range(0, len(cut_points)):
            if (float(x[i]) >= cut_points[j][0] and float(x[i]) <= cut_points[j][1]):
                vCat[i] = cut_points[j]
    return (vCat)

def discretizeEW(x,num_bins):
    """
    Function to apply equal width discretization to a vector. This function applies equal width discretization to a vector
    :param x: a vector composed by real numbers
    :param num_bins: number of intervals
    :return: A factor with the equal width discretization
    """
    width = (max(x) - min(x)) / num_bins
    puntosCorte = []
    limiteIn = -math.inf
    for i in range(1, num_bins + 1):
        limiteFin = min(x) + width * i
        if (i < num_bins):
            puntosCorte.append((limiteIn, limiteFin))
            limiteIn = limiteFin
        else:
            puntosCorte.append((limiteIn, math.inf))

    vCat=__discretizePoints(x,puntosCorte)

    return (vCat, set(puntosCorte))


def discretizeEF(x, num_bins):
    """
    Function to apply equal frequency discretization to a vector.  This function applies equal frequency discretization to a vector
    :param x: a vector composed by real numbers
    :param num_bins: number of intervals
    :return: A factor with the equal frequency discretization
    """
    n = len(x)
    numXintervalo = math.floor(n / num_bins)
    vectorOrdenado = x
    vectorOrdenado.sort
    puntosCorte = []
    limiteInf = -math.inf
    limiteSup = 0
    if (numXintervalo > 1):
        for i in range(n):

            if i != 0 and (i % numXintervalo == 0 or i == n - 1):
                limiteSup = vectorOrdenado[i]
                print(i)
                if (i == n - 1):
                    puntosCorte.append((limiteInf, math.inf))
                    limiteInf = limiteSup
                else:
                    puntosCorte.append((limiteInf, limiteSup))

                    limiteInf = limiteSup
            elif len(puntosCorte) == num_bins:
                break
    else:
        for i in range(num_bins):
            limiteSup = vectorOrdenado[i]
            if (i == (num_bins - 1)):
                limiteSup = vectorOrdenado[i]
                puntosCorte.append((limiteInf, math.inf))
            else:
                puntosCorte.append((limiteInf, limiteSup))
                limiteInf = limiteSup

    vCat =__discretizePoints(x,puntosCorte)

    return (vCat, set(puntosCorte))


def entropy(x):
    """
     Function to compute the entropy of a given vector.
    :param x: a vector composed by discrete variables
    :return: A real number
    """
    cuenta=dict(zip(x,(map(lambda el: x.count(el),x))))
    n=len(x)
    nCuenta=len(cuenta)
    entropia=0
    for i in range(nCuenta):
        probabilidad=list(cuenta.values())[i]/n
        if(probabilidad>0):
            entropia=entropia+((-1)*probabilidad*math.log2(probabilidad))
    return entropia


def writeLog(file_path, text):
    """
    Function to save a log text into a file
    :param file_path: a string with the path where the text has to be saved
    :param text: a string that contains the text to write
    :return:
    """
    today = datetime.now()

        # Write data in file
    with open(file_path, 'w') as outfile:
        outfile.writelines(str(today) + " " + text)
        print("Data correctly saved in: " + file_path)


