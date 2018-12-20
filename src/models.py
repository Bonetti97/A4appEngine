from google.appengine.ext import db
from google.appengine.api import images

import webapp2

class Comic (db.Model):
    idComic=db.IntegerProperty()#Queremos que los valores los ponga Google App Engine directamente
    nombre=db.StringProperty()
    descripcion=db.StringProperty()
    fechaCreacion=db.DateTimeProperty(auto_now_add=True)#con el auto_now_add creo que es un atributo cuyo valor se añade solo con el time actual.
    
    #Dado que un comic tiene muchas entregas y una entrega es para un solo comic, la relación entre Comic y Entrega es de 1 a muchos y va en Entrega.
    #Esta es la relación 1 a muchos entre usuario y comic.
    usuario=db.ReferenceProperty(Usuario,collection_name="listaComics")
    
    
    

class Entrega (db.Model):
    idEntrega = db.IntegerProperty()#Queremos que los valores los ponga Google App Engine directamente
    nombre = db.StringProperty()
    #archivo = db.LinkProperty()#esto es un enlace url->HAY que cambiar la imagen
    imagen=db.BlobProperty()
    fechaCreacion =db.DateTimeProperty(auto_now_add=True)
    #Ahora creamos la relación con Comic.
    idComic = db.ReferenceProperty(Comic,collection_name="listaEntrega")
    #El collection_name es el nombre del atributo en Comic para esta relacion
    

class Usuario (db.Model):
    idUsuario =db.IntegerProperty()
    nombreUsuario=db.StringProperty()
    permiso=db.IntegerProperty()
    #Tiene una lista de comics y una lista de comentarios.Estas relaciones son de 1 a muchos.
    
    #Lista de comics que al ser de una relación de 1 a muchos va en comic.

class Comentario (db.Model):
    idComentario=db.IntegerProperty()
    titulo=db.StringProperty()
    contenido=db.StringProperty()
    #Un comentario sólo puede pertenecer a un cómic o a una entrega según decidamos a quien comentamos.Entonces de 1 a muchos
    
    #Un comentario es de un usuario.
    usuario=db.ReferenceProperty(Usuario,collection_name="listaComentariosUsuario")
    #Los comentarios van a ir en las entregas
    entrega=db.ReferenceProperty(Entrega,collection_name="listaComentariosEntrega")





class Photo(db.Model):
    title = db.StringProperty()
    full_size_image = db.BlobProperty()
    


class Thumbnailer(webapp2.RequestHandler):
    def get(self):
        if self.request.get("id"):
            photo = Photo.get_by_id(int(self.request.get("id")))

            if photo:
                img = images.Image(photo.full_size_image)#crea un objeto de la entidad Imagen
                img.resize(width=80, height=100)#le pone sus medidas
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)#Creo que está metiendo la imagen en el objeto response.
                return

        # Either "id" wasn't provided, or there was no image with that ID
        # in the datastore.
        self.error(404)
    
    
    