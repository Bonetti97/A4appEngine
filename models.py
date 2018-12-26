#coding=utf-8
from google.appengine.ext import db

from google.appengine.ext import ndb

from google.appengine.api import images

import webapp2



class Usuario (ndb.Model):
    
    id = ndb.StringProperty()
    nombre=ndb.StringProperty()
    

class Comic (ndb.Model):

    nombre=ndb.StringProperty()
    portada=ndb.BlobProperty()
    fechaCreacion=ndb.DateTimeProperty(auto_now_add=True)#con el auto_now_add creo que es un atributo cuyo valor se añade solo con el time actual.
    usuario = ndb.KeyProperty(Usuario)
    #Dado que un comic tiene muchas entregas y una entrega es para un solo comic, la relación entre Comic y Entrega es de 1 a muchos y va en Entrega.
    #Esta es la relación 1 a muchos entre usuario y comic.
    

class Entrega (ndb.Model):
    nombre = ndb.StringProperty()
    
    imagen=ndb.BlobProperty()
    #fechaCreacion =ndb.DateTimeProperty(auto_now_add=True)
    #Ahora creamos la relación con Comic.
    idComic = ndb.KeyProperty(Comic)
    #El collection_name es el nombre del atributo en Comic para esta relacion
    




class Comentario (ndb.Model):
    
    
    contenido=ndb.StringProperty()
    entrega = ndb.KeyProperty(Entrega)
    usuario = ndb.KeyProperty(Usuario)
    #Un comentario sólo puede pertenecer a un cómic o a una entrega según decidamos a quien comentamos.Entonces de 1 a muchos
    
    #Un comentario es de un usuario.
    #usuario=db.ReferenceProperty(Usuario,collection_name="listaComentariosUsuario")
    #Los comentarios van a ir en las entregas
   





