# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
import datetime

import stock.stock_schema as schema

import utils.json_serializer as json


def getStock(articleId):
    """
    Obtiene un articulo. \n
    articleId: string ObjectId\n
    return dict<propiedad, valor> Articulo\n
    """
    """
    @api {get} /v1/articles/:articleId Buscar Artículo
    @apiName Buscar Artículo
    @apiGroup Articulos

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "_id": "{id de articulo}"
            "name": "{nombre del articulo}",
            "description": "{descripción del articulo}",
            "image": "{id de imagen}",
            "price": {precio actual},
            "stock": {stock actual}
            "updated": {fecha ultima actualización}
            "created": {fecha creación}
            "enabled": {activo}
        }

    @apiUse Errors

    """
    try:
        result = db.stock.find_one({"_id": bson.ObjectId(articleId)})
        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return result
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")


def addStock(params):
    """
    Agrega un articulo.\n
    params: dict<propiedad, valor> Articulo\n
    return dict<propiedad, valor> Articulo
    """
    """
    @api {post} /v1/articles/ Crear Artículo
    @apiName Crear Artículo
    @apiGroup Articulos

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "name": "{nombre del articulo}",
            "description": "{descripción del articulo}",
            "image": "{id de imagen}",
            "price": {precio actual},
            "stock": {stock actual}
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "_id": "{id de articulo}"
            "name": "{nombre del articulo}",
            "description": "{descripción del articulo}",
            "image": "{id de imagen}",
            "price": {precio actual},
            "stock": {stock actual}
            "updated": {fecha ultima actualización}
            "created": {fecha creación}
            "enabled": {si esta activo}
        }

    @apiUse Errors

    """
    return _addOrUpdateStock(params)


def updateStock(articleId,name, params):
    """
    Actualiza un articulo. \n
    articleId: string ObjectId\n
    params: dict<propiedad, valor> Articulo\n
    return dict<propiedad, valor> Articulo\n
    """
    """
    @api {post} /v1/articles/:articleId Actualizar Artículo
    @apiName Actualizar Artículo
    @apiGroup Articulos

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "name": "{nombre del articulo}",
            "description": "{descripción del articulo}",
            "image": "{id de imagen}",
            "price": {precio actual},
            "stock": {stock actual}
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "_id": "{id de articulo}"
            "name": "{nombre del articulo}",
            "description": "{descripción del articulo}",
            "image": "{id de imagen}",
            "price": {precio actual},
            "stock": {stock actual}
            "updated": {fecha ultima actualización}
            "created": {fecha creación}
            "enabled": {si esta activo}
        }

    @apiUse Errors

    """



    params["nombreProducto"] = name
    params["idProducto"] = articleId
    return _addOrUpdateStock(params)


def delStock(articleId):
    """
    Marca un articulo como invalido.\n
    articleId: string ObjectId
    """
    """
    Elimina un articulo : delArticle(articleId: string)

    @api {delete} /articles/:articleId Eliminar Artículo
    @apiName Eliminar Artículo
    @apiGroup Articulos

    @apiUse AuthHeader

    @apiSuccessExample {json} 200 Respuesta
        HTTP/1.1 200 OK

    @apiUse Errors

    """
    stock = getStock(articleId)
    stock["updated"] = datetime.datetime.utcnow()
    stock["enabled"] = False
    db.stock.save(stock)


def _addOrUpdateStock(params):
    """
    Agrega o actualiza un articulo. \n
    params: dict<property, value>) Articulo\n
    return dict<propiedad, valor> Articulo
    """
    isNew = True
    stock = schema.newStock()

    if ("_id" in params):
        isNew = False
        stock = getStock(params["_id"])

    #art = params["idProducto"]
    #if(art == articleId):    
        #idNew = False
        #result = db.stock.find_one({"articleId": bson.ObjectId(idProducto)})
        #stock = getStock(params["_id"])
    # Actualizamos los valores validos a actualizar
    
    stock.update(params)

    
    stock["updated"] = datetime.datetime.utcnow()

    schema.validateSchema(stock)


    if (not isNew):
        del stock["_id"]
        r = db.stock.replace_one({"_id": bson.ObjectId(params["_id"])}, stock)
        stock["_id"] = params["_id"]
    else:
        stock["_id"] = db.stock.insert_one(stock).inserted_id
    return stock
