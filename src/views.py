import os
import webapp2
import jinja2
import requests
from models import Comic


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

class premium(BaseHandler):
    def get(self):
        o = Controller().login()  
        Controller().premium()
        cos = Controller().listComics(o) 
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })     

class guardarSesion(BaseHandler):
    def get(self,idUsuario):
        #Controller().login(idUsuario)
        return webapp2.redirect("/showComics");
        
class invitado(BaseHandler):
    def get(self):   
        cos = Controller().listComics(str(2)) 
        self.render_template('invitado.html', {'listaComic': cos})
        
class showComics(BaseHandler):
    def get(self): 
        o = Controller().login()  
        cos = Controller().listComics(o)      
        u = Controller().findUsuario(o)
        
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })     
    #Con google app engine
    #def get(self):
        #Aquí es donde vamos a hacer la query de buscar todos los comics de un usuario
        
        
        
        
        
class AddComic(BaseHandler):
    def get(self):
        self.render_template('newComic.html', {})
    
    def post(self):
        
        #Creamos un objeto comic
        comic=Comic(nombre=self.request.get('nombreComic'),descripcion=self.request.get('descripcionComic'))
        
        return webapp2.redirect('/showComics' )
        
class EditComic(BaseHandler):
    def get(self, comicID):      
        co = Controller().findComicById(int(comicID))
        self.render_template('editarComic.html', {'comic': co})
        
    def post(self,comicID):
        nombre = self.request.get('nombreComic')
        descripcion = self.request.get('descripcionComic')
        Controller().editComic(comicID, nombre, descripcion)
        #o = Controller().login()
        return webapp2.redirect('/showComics')

class DeleteComic(BaseHandler):
    def get(self, comicID):
        Controller().deleteComic(comicID)
        #id = Controller().login()
        return webapp2.redirect('/showComics')
    
class OrdenAlfabetico(BaseHandler):
    def get(self):
        cos=Controller().listaOrden()
        o = Controller().login()  
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })

        
class OrdenFecha(BaseHandler):
    def get(self):
        cos=Controller().listaFecha()
        o = Controller().login()  
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })
        
class BuscarNombre(BaseHandler):
    def get(self):
        nombre = self.request.get('busquedaNombre')
        cos=Controller().listaNombre(nombre)
        o = Controller().login()  
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })
        
class BuscarFechaMayor(BaseHandler):
    def get(self):
        fecha=self.request.get('busquedaFechaMayor')
        cos=Controller().listaFechaMayor(fecha)
        o = Controller().login()  
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })
        
class OrdenEntregas(BaseHandler):
    def get(self):
        cos=Controller().listaNumEntregas();
        o = Controller().login()  
        u = Controller().findUsuario(o)
        self.render_template('comics.html', {'listaComic': cos , "permiso" : u.permiso })


class flickr(BaseHandler):
    def get(self):
        tag = self.request.get('nombreApi')
        lista = Controller().flickr(tag)
        self.render_template('flickr.html', {'lista': lista})        
        
        
        
        
        
        
        
        
        
        
        