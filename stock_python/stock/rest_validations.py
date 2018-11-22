# coding=utf_8
# Son las validaciones de los servicios rest, se validan los parametros obtenidos desde las llamadas externas rest

import utils.errors as error
#import articles.crud_service as crud
import stock.crud_service as crud
import utils.schema_validator as schemaValidator
import numbers


# Son validaciones sobre las propiedades que pueden actualizarse desde REST
STOCK_UPDATE_SCHEMA = {
    
    "cantStock": {
        "type": numbers.Integral,
        "min": 0
        }
}


def validateAddStockParams(params):
    """
    Valida los parametros para crear un objeto.\n
    params: dict<propiedad, valor> Article
    """
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(STOCK_UPDATE_SCHEMA, params)


def validateEditStockParams(articleId, params):
    """
    Valida los parametros para actualizar un objeto.\n
    params: dict<propiedad, valor> Article
    """
    if (not articleId):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(STOCK_UPDATE_SCHEMA, params)


def validateStockExist(articleId):
    stock = crud.getStock(articleId)
    if("enabled" not in stock or not stock["enabled"]):
        raise error.InvalidArgument("_id", "Inválido")
