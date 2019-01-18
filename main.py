from views import login,showEntregasComic,AddEntrega, DeleteEntrega,EditEntrega
from views import showComics
from views import AddComic
from views import Image
from views import EditComic
from views import DeleteComic
from views import BuscarFechaMayor
import views

import webapp2
#comentario github



app = webapp2.WSGIApplication([
        ('/',views.login), 
        ('/comics',showComics),
        ('/logout',views.logout),
        ('/newComic',AddComic),
        ('/newComentario/([\d]+)',views.AddComentario),
        ('/img',Image),
        ('/comicsPorUsuario',views.comicsPorUsuario),
        ('/imgEntrega',views.ImagenEntrega),
        ('/flickr',views.flickr),
        ('/comicVinesAPI',views.comicVinesAPI),   
        ('/editarComic/([\d]+)', EditComic),
        ('/deleteComic/([\d]+)', DeleteComic),
        ('/buscarFechaMayor', BuscarFechaMayor),
        ('/entregasComic/([\d]+)',showEntregasComic),
        ('/newEntrega/([\d]+)',views.AddEntrega),
        ('/deleteEntrega/([\d]+)', views.DeleteEntrega),
        ('/comentarios/([\d]+)', views.Comentarios),
        ('/deleteComentario/([\d]+)/([\d]+)', views.DeleteComentario),
        ('/editarEntrega/([\d]+)', EditEntrega)
        
        
        ],
        debug=True)

