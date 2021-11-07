import sys


sys.path.append("..")

from preprocesspack import Attribute,DataSet,graphics,utils


def test_all():
    ##ATTRIBUTE
    ##Numeric Attribute
    attr=Attribute.Attribute(name="age",vector=[34,16,78,90,12])
    attrContinuous=Attribute.Attribute(name="age",vector=[1.2,3.4,6.7,8.9,4.7])

    ##Categorized Attribute
    #attrCat=Attribute.Attribute(name="age",vector=[34,16,78,90,12])

    attrCatEF=attr.discretize(3,"EF")
    attrCatEW=attr.discretize(3,"EW")


    print (attrCatEF.vector)
    print (attrCatEW.vector)
    print (attr.vector)

    ##Normalized Attribute

    attrNorm=attr.normalize()
    attrStd=attr.standardize()

    attrCatStd=attrCatEW.standardize()
    attrCatNorm=attrCatEF.standardize()
    print(attrNorm.vector)
    print(attrStd.vector)
    print(attr.vector)

    print(attrCatStd.vector)
    print(attrCatNorm.vector)
    ##Attribute entropy
    print(attrCatEF.entropy())
    print (attr.entropy())
    print(attrContinuous.entropy())

    ##Attribute variance
    print (attrStd.variance())
    print (attr.variance())
    print (attrCatEF.variance())

    ##GetName and getVector
    print(attr.discretize(4,"EF").getVector())
    print(attr.discretize(4,"EF").getName())

    ##DATASET
    dataset=DataSet.DataSet([],name="students")

    print(dataset.data)
    print(dataset.name)

    dataset.addAttribute(attr)
    dataset.addAttribute(attrContinuous)
    dataset.addAttribute(attrCatEW)
    dataset.addAttribute([0,1,0,1,1])

    dataset.printDataSet()

    ##NORMALIZE DATASET

    dsNorm=dataset.normalize()
    dsNorm.printDataSet()

    ##STANDARDIZE DATASET
    dsStd=dataset.standardize()
    dsStd.printDataSet()

    ## VARIANCE
    print (dsStd.variance())

    ## ENTROPY
    print (dsStd.entropy())

    ##DISCRETIZATION
    print ("Discretization")
    dsDisc=dataset.discretize(3,"EW",[0,1,2,3])
    dsDisc.printDataSet()

    ##ROC AUC
    dataset.printDataSet()
    print(dataset.rocAuc(1,3))


    ##GET NAMES
    print(attr.isCategorical())
    print(dataset.getNames())

    ##CORRELATION MATRIX
    #graphics.correlationMatrix(dataset)

    ##ENTROPY PLOT
    #graphics.entropyPlot(dataset)

    ##ROC CURVE PLOT
    #graphics.rocPlot(dataset,1,3)

    ##LOAD DATASET
    ds=DataSet.loadDataSet("datos.csv")

    ds.printDataSet()
    attr.printAttribute()


    dataset.printDataSet()
    #graphics.correlationPlot(dataset)
    DataSet.saveDataSet(dataset,"pruebaGuardar.csv")

    loadedDS=DataSet.loadDataSet("pruebaGuardar.csv")
    print (loadedDS)
    print (Attribute.computeCorrelation(attrNorm,attrCatEW))
    print (Attribute.computeCorrelation(attrCatEF,attrCatEW))
    print (Attribute.computeCorrelation(attrNorm,attrStd))
    dataset.printDataSet()

    loadedDS.printDataSet()
    attr.printAttribute()

test_all()