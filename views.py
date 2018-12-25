#coding=utf-8
import os
import webapp2
import jinja2

from models import Comic, Entrega

from google.appengine.ext import ndb

from google.appengine.ext import gql
from google.appengine.api import images
import datetime #esto lo vamos a usar para pasar de string a fecha.
from google.appengine.api import users


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))



class BaseHandler(webapp2.RequestHandler):

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))
    
        
        
class login(BaseHandler):
    def get(self):
        self.render_template('login.html', {})
        

class showComics(BaseHandler):
  
    def get(self):
        
        lista=Comic.query()
        self.render_template('comics.html', {'listaComic': lista})

class AddComic(BaseHandler):

    def get(self):
        self.render_template('newComic.html', {})
        
    def post(self):
        imagenPortada=self.request.get('portadaComic')
        
        com = Comic(nombre=self.request.get('nombreComic'),portada=imagenPortada)
                        
        com.put()#el método ENTIDAD.put() añade un nuevo OBJETO del tipo de la entidad en el dataStore
        
    
        return webapp2.redirect('/')
    

class Image(webapp2.RequestHandler):
    def get(self):
        Comic_key = ndb.Key(urlsafe=self.request.get('img_id'))
        comi = Comic_key.get()
        if comi.portada:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(comi.portada)
        else:
            self.response.out.write('No image')
# [END image_handler]
    
    
class EditComic(BaseHandler):

    def get(self, comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        self.render_template('editarComic.html', {'comic': com})
        
    def post(self,comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        nombreNuevo = self.request.get('nombreComic')
        com.nombre=nombreNuevo
        com.put()
        
        return webapp2.redirect('/')  
    
class DeleteComic(BaseHandler):

    def get(self, comicID):
        print comicID
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        com.key.delete()
        return webapp2.redirect('/')


class BuscarFechaMayor(BaseHandler):
    def get(self):
        fechaString=self.request.get('busquedaFechaMayor')
        fechaDate=datetime.datetime.strptime(fechaString,'%Y-%m-%d')
        q=Comic.gql("WHERE fechaCreacion >:fech",fech=fechaDate)
        #query=Comic.query("fechaCreacion >"+fecha)#strftime castea de string a tipo date.
        print q
        #cos=Controller().listaFechaMayor(fecha)
        self.render_template('comics.html', {'listaComic': q})


class showEntregasComic(BaseHandler):
    def get(self,comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        
        listaEntregas=Entrega.query(Entrega.idComic==com.key)
       
        self.render_template('entregasComicPrueba.html', {'listaEntregas': listaEntregas,'comicID': comicID})


class AddEntrega(BaseHandler):

    def get(self, comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        self.render_template('newEntrega.html', {'comic':com})
        
    def post(self,comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        
        imagenPortada=self.request.get('imagenEntrega')
        
        entr = Entrega(nombre=self.request.get('nombreEntrega'),imagen=imagenPortada,idComic=com.key)
                        
        entr.put()#el método ENTIDAD.put() añade un nuevo OBJETO del tipo de la entidad en el dataStore
        
        listaEntregas=Entrega.query(Entrega.idComic==com.key)
    
        return webapp2.redirect('/entregasComic/'+comicID)
        #self.render_template('entregasComicPrueba.html', {'listaEntregas': listaEntregas,'comicID': comicID})
        
class DeleteEntrega(BaseHandler):

    def get(self, entregaID):
       
        entrega_id= int (entregaID)
        en=Entrega.get_by_id(entrega_id)
        en.key.delete()
        return webapp2.redirect('/')
    
class EditEntrega(BaseHandler):

    def get(self, entregaID):
        entrega_id= int (entregaID)
        en=Entrega.get_by_id(entrega_id)
        self.render_template('editarEntrega.html', {'entrega': en})
        
    def post(self,entregaID):
        entrega_id= int (entregaID)
        en=Entrega.get_by_id(entrega_id)
        nombreNuevo = self.request.get('nombreEntrega')
        en.nombre=nombreNuevo
        en.put()
        
        return webapp2.redirect('/')  
