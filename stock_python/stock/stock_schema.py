# coding=utf_8

import numbers
import datetime
import utils.schema_validator as validator
import utils.errors as errors
import bson.objectid as bson
#import stock.route
#from requests import get

# Validaciones generales del esquema, se valida solo lo que el usuario puede cambiar
STOCK_DB_SCHEMA = {
    "idProducto": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    
    
    "cantStock": {
        "required": True,
        "type": numbers.Integral,
        "min": 0
        },

    "nombreProducto": {
        "required": True,
        "type": str,
        "maxLen": 1024
        },
  



}


def newStock():
    """
    Crea un nuevo articulo en blanco.\n
    return dict<propiedad, valor> Articulo
    """
    
    #base = "http://127.0.0.1:3002/v1/articles/"
    #consumir = get(base+articleId).json()
    return {
        "idProducto": "", #consumir["_id"] que viene por url,
        "nombreProducto": "",
        "cantStock": "",
        "updated": datetime.datetime.utcnow(),
        "created": datetime.datetime.utcnow(),
        "enabled": True
    }


def validateSchema(document):
    err = validator.validateSchema(STOCK_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
