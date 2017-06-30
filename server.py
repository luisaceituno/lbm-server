"""Server module for LBM"""
import os
import sys
import time
import cherrypy
from app import create_app
from paste.translogger import TransLogger

def run_server(app):
    app_logged = TransLogger(app)
    cherrypy.tree.graft(app_logged, '/')

    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    cherrypy.engine.start()
    cherrypy.engine.block()


app = create_app()
run_server(app)
