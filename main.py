from views import login,showEntregasComic,AddEntrega, DeleteEntrega,EditEntrega
from views import showComics
from views import AddComic
from views import Image
from views import EditComic
from views import DeleteComic
from views import BuscarFechaMayor

import webapp2
#comentario github



app = webapp2.WSGIApplication([
        ('/',showComics),
        ('/newComic',AddComic),
        ('/img',Image),
        ('/editarComic/([\d]+)', EditComic),
        ('/deleteComic/([\d]+)', DeleteComic),
        ('/buscarFechaMayor', BuscarFechaMayor),
        ('/entregasComic/([\d]+)',showEntregasComic),
        ('/newEntrega/([\d]+)',AddEntrega),
        ('/deleteEntrega/([\d]+)', DeleteEntrega),
        ('/editarEntrega/([\d]+)', EditEntrega)
        
        
        ],
        debug=True)

