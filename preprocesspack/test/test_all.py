import sys
sys.path.append("..")

from preprocesspack import Attribute,DataSet,graphics,utils


def test_all():
    ##Atributo numerico
    attr=Attribute.Attribute(vename="age",vector=[34,16,78,90,12])

