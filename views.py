#coding=utf-8
import os
import webapp2
from google.appengine.ext import webapp
from google.appengine.api import users
import jinja2
import comicAPI


import json

from models import Comic, Entrega,Comentario,Usuario

from google.appengine.ext import ndb

from google.appengine.ext import gql
from google.appengine.api import images
from google.appengine.api import urlfetch
import datetime #esto lo vamos a usar para pasar de string a fecha.
from google.appengine.api import users
import random


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
    
        

class showComics(BaseHandler):
  
    def get(self):
        user = users.get_current_user()

        if user:
        
            lista=Comic.query()
            self.render_template('comics.html', {'listaComic': lista, 'currentUserID' : user.user_id()})
        else:
            self.redirect(users.create_login_url(self.request.uri)) 
  
  

class AddComic(BaseHandler):

    def get(self):
        
        user = users.get_current_user()

        if user:
        
            self.render_template('newComic.html', {})
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
        
    def post(self):
        user = users.get_current_user()
        imagenPortada=self.request.get('portadaComic')
        usuario  = Usuario.query(Usuario.id==user.user_id())
        usuario = usuario.get().key
        com = Comic(nombre=self.request.get('nombreComic'),portada=imagenPortada, usuario=usuario)
                        
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

class ImagenEntrega(webapp2.RequestHandler):
    def get(self):
        Entrega_key = ndb.Key(urlsafe=self.request.get('img_id'))
        comi = Entrega_key.get()
        if comi.imagen:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(comi.imagen)
        else:
            self.response.out.write('No image')
    
    
class EditComic(BaseHandler):

    def get(self, comicID):
        
        user = users.get_current_user()

        if user:
        
            comic_id= int (comicID)
            com=Comic.get_by_id(comic_id)
            self.render_template('editarComic.html', {'comic': com})
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
        
        
    def post(self,comicID):
        comic_id= int (comicID)
        com=Comic.get_by_id(comic_id)
        nombreNuevo = self.request.get('nombreComic')
        com.nombre=nombreNuevo
        com.put()
        
        return webapp2.redirect('/')  
    
class DeleteComic(BaseHandler):

    def post(self, comicID):
        
        user = users.get_current_user()

        if user:
        
            comic_id= int (comicID)
            com=Comic.get_by_id(comic_id)
            com.key.delete()
            return webapp2.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
            

class BuscarFechaMayor(BaseHandler):
    def post(self):
        
        user = users.get_current_user()

        if user:
        
            fechaString=self.request.get('busquedaFechaMayor')
            fechaDate=datetime.datetime.strptime(fechaString,'%Y-%m-%d')
            q=Comic.gql("WHERE fechaCreacion >:fech",fech=fechaDate)
        #query=Comic.query("fechaCreacion >"+fecha)#strftime castea de string a tipo date.
        #cos=Controller().listaFechaMayor(fecha)
            self.render_template('comics.html', {'listaComic': q})
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
        
class comicsPorUsuario(BaseHandler):
    def post(self):
        
        user = users.get_current_user()

        if user:
            iduser= user.user_id()
            us = Usuario.query(Usuario.id==iduser)

            q=Comic.query(Comic.usuario==us.get().key)
            
            self.render_template('comics.html', {'listaComic': q , 'currentUserID' : iduser})
        else:
            self.redirect(users.create_login_url(self.request.uri))     
        
        


class showEntregasComic(BaseHandler):
    def get(self,comicID):
        
        
        user = users.get_current_user()

        if user:
        
            comic_id= int (comicID)
            com=Comic.get_by_id(comic_id)
        
            listaEntregas=Entrega.query(Entrega.idComic==com.key)
       
            self.render_template('entregasComic.html', {'listaEntregas': listaEntregas,'comicID': comicID, 'currentUserID' : user.user_id(), 'comicCompleto' : com})
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
class Comentarios(BaseHandler):
    def get(self,entregaID):
          
        user = users.get_current_user()
        
        if user:
        
            entrega_id= int (entregaID)
            en=Entrega.get_by_id(entrega_id)
            
            listaComentarios=Comentario.query(Comentario.entrega==en.key)
       
            self.render_template('comentarios.html', {'listaComentarios': listaComentarios,'entregaID': entregaID,'currentUserID' : user.user_id() })
        else:
            self.redirect(users.create_login_url(self.request.uri))        
        
        
class AddComentario(BaseHandler):

    def post(self, entregaID):
        
        user = users.get_current_user()

        if user:
            com = self.request.get('nuevoComentario')
            entrega_id= int (entregaID)
            en=Entrega.get_by_id(entrega_id)
            usuarioAux = Usuario.query(Usuario.id==user.user_id())
            comentario = Comentario(contenido=com,entrega=en.key,usuario=usuarioAux.get().key)
            comentario.put()
            return webapp2.redirect('/comentarios/'+entregaID)

           
        else:
            self.redirect(users.create_login_url(self.request.uri))



class AddEntrega(BaseHandler):

    def get(self, comicID):
        
        user = users.get_current_user()

        if user:
        
            comic_id= int (comicID)
            com=Comic.get_by_id(comic_id)
            self.render_template('newEntrega.html', {'comic':com})
        else:
            self.redirect(users.create_login_url(self.request.uri))

        
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

    def post(self, entregaID):
        user = users.get_current_user()

        if user:
            entrega_id= int (entregaID)
            en=Entrega.get_by_id(entrega_id)
            en.key.delete()
            return webapp2.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class DeleteComentario(BaseHandler):

    def post(self, comentarioID,entregaID):
        
        
        
        user = users.get_current_user()

        if user:
            comentario_id= int (comentarioID)
            en=Comentario.get_by_id(comentario_id)
            en.key.delete()
            entrega_id= int (entregaID)
            en=Entrega.get_by_id(entrega_id)     
            return webapp2.redirect('/comentarios/'+entregaID)
        else:
            self.redirect(users.create_login_url(self.request.uri))
       
        
    
class EditEntrega(BaseHandler):

    def get(self, entregaID):
        
        user = users.get_current_user()

        if user:
            entrega_id= int (entregaID)
            en=Entrega.get_by_id(entrega_id)
            self.render_template('editarEntrega.html', {'entrega': en})
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
        
        
    def post(self,entregaID):
        entrega_id= int (entregaID)
        en=Entrega.get_by_id(entrega_id)
        nombreNuevo = self.request.get('nombreEntrega')
        en.nombre=nombreNuevo
        en.put()
        
        return webapp2.redirect('/')  
    
class login(webapp.RequestHandler):
    
    
    def get(self):
        user = users.get_current_user()

        if user:
            usuarioAux = Usuario.query(Usuario.id==user.user_id())
            
            if usuarioAux.get():
               
                self.redirect("/comics")
            else:
                    
                usuarioAux = Usuario(id=user.user_id(), nombre= user.nickname() )
                usuarioAux.put()
                self.redirect("/comics")
        else:
            self.redirect(users.create_login_url(self.request.uri)) 
class logout(webapp.RequestHandler):
    
    
    def get(self):
        
        self.redirect(users.create_logout_url("/"))             

class flickr(BaseHandler):
    def get(self):
        
        
        user = users.get_current_user()

        if user:
            tag = self.request.get('nombreApi')
        
            clave = "b56fe120d5d60193cdff938b0af0ed91"
        #secreto = '7941625e2330f77c'
            url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key='+clave+'&tags='+tag
            r = urlfetch.fetch(url)
            
           
            r = r.content[14:]
            r = r[:-1]
            respuesta = json.loads(r)
            lista=  respuesta['photos']['photo']
           
            listaUrl = []
            for i in range(len(lista)):
                
                secret = lista[i]['secret']
                farm = lista[i]['farm']
                server = lista[i]['server']  
                id=lista[i]['id']
                urlfoto = 'http://farm'+str(farm)+'.staticflickr.com/'+str(server)+'/'+str(id)+'_'+str(secret)+'_z.jpg'
                listaUrl.append(urlfoto)
                
            
            self.render_template('flickr.html', {'lista': listaUrl}) 
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
class comicVinesAPI(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            off= random.randint(1,200000)
            apikey="b901f389a03fdda0105174f012fc273e6bd273c9"  
            url= "https://comicvine.gamespot.com/api/issues/?api_key="+apikey+"&format=json&offset="+str(off)
            headers={'User-Agent': 'HumilArt app'}
            result = urlfetch.fetch(
                        url=url,
                        headers=headers)
            r = json.loads(result.content)
            lista = r['results']
            listaCo = []
            for i in range(20):
                nombre = lista[i]['volume']['name'].encode('utf-8')
                link = lista[i]['volume']['site_detail_url'].encode('utf-8')
                capitulo= '#'+lista[i]['issue_number']
                imagen = lista[i]['image']['medium_url']
                co = comicAPI.comicAPI(nombre,link,capitulo,imagen)
                listaCo.append(co)
            self.render_template('comicVinesAPI.html', {'lista' : listaCo}) 
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
 
     
            
        
        
            
    
