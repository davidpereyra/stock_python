# coding=utf_8

import flask
# import articles.crud_service as crud
# import articles.find_service as find
import stock.crud_service as crud
import stock.find_service as find
import utils.json_serializer as json
import utils.errors as errors
import utils.security as security
#import articles.rest_validations as restValidator
import stock.rest_validations as restValidator
import numbers

from requests import get

def init(app):
    """
    Inicializa las rutas para Stock\n
    app: Flask
    """

    @app.route('/v1/stock/<articleId>/', methods=['POST'])
    def updateStock(articleId):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateAddStockParams(params)

            base = "http://127.0.0.1:3002/v1/articles/"
            consumir = get(base+articleId).json()

            if consumir["_id"]:
                #result = crud.addStock(params)
                articleId = consumir["_id"]
                nombreProducto = consumir["name"]
                result = crud.updateStock(articleId,nombreProducto,params)
            
                return json.dic_to_json({
                    "articleId": articleId,
                    #"cantStock": params["cantStock"],
                    "resultado" : result
                }) 
            else:
                error = "el _id no pertenece a un articulo del catalogo"
                return error
        except Exception as err:
            return errors.handleError(err)


    @app.route('/v1/stock/<articleId>/', methods=['GET'])
    def getStock(articleId):
        try:
            return json.dic_to_json(crud.getStock(articleId))
        except Exception as err:
            return errors.handleError(err)


    @app.route('/v1/stock/consume/<articleId>', methods=['POST'])
    def consume(articleId):
        base = "http://127.0.0.1:3002/v1/articles/"
        consumir = get(base+articleId).json()

        return consumir["_id"]
