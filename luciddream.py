#!/usr/bin/python

# math stuff
import numpy as np
import scipy.ndimage as nd
from random import randint

# data stuff
from cStringIO import StringIO
import PIL.Image
from google.protobuf import text_format
# system stuff
import os
import argparse
import sys
# a little sauce
import caffe
from deepdream import deepdream, net

import json
import conf

from io import BytesIO
import base64
# app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
#
# @app.route('/', methods=['GET', 'POST'])
# def handle_requests():
#     print 'handling request'
#     if request.method == 'POST':
#         if 'buffer' in request.form:
#             frame = np.float32(PIL.Image.open(BytesIO(base64.b64decode(request.form['buffer'].partition('data:image/jpeg;base64,')[2]))))
#             frame = deepdream(net, frame, iter_n=1, octave_n=5, end=net.blobs.keys()[42])
#             buf = StringIO()
#             pil = PIL.Image.fromarray(np.uint8(frame))
#             pil.save(buf, format='jpeg')
#             buf.seek(0)
#             return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
#         else:
#             return 'no data'
#
#     else:
#         return 'what is this'

# @socketio.on('connect', namespace='/')
# def test_connect():
#     emit('response', {'data': 'Connected'})
# @socketio.on('image', namespace='/')
# def on_image():
#     # print request.form
#     emit('image', request.form)

# from gevent import monkey; monkey.patch_all()
# from flask import Flask, request, render_template
#
# from socketio import socketio_manage
# from socketio.namespace import BaseNamespace
# from socketio.mixins import RoomsMixin, BroadcastMixin
#
# # The socket.io namespace
# class DeepDreamNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
#     def initialize():
#         print 'initializing socket.io'
#         self.emit('connect')
#
#     def on_image(self, info):
#         print 'recieved image'
#         info = json.loads(info)
#         if 'buffer' in info:
#             frame = np.float32(PIL.Image.open(BytesIO(base64.b64decode(info['buffer'].partition('data:image/jpeg;base64,')[2]))))
#             frame = deepdream(net, frame, iter_n=1, octave_n=5, end=net.blobs.keys()[42])
#             buf = StringIO()
#             pil = PIL.Image.fromarray(np.uint8(frame))
#             pil.save(buf, format='jpeg')
#             buf.seek(0)
#             info['buffer'] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
#             self.emit('image', info)
#
# @app.route("/socket.io/<path:path>")
# def run_socketio(path):
#     socketio_manage(request.environ, {'': DeepDreamNamespace})

import zerorpc
from time import time
class LucidRPC(object):
    def dream(self, buffer, calltime):
        print "invoked in", time() - calltime
        # print buffer
        frame = np.float32(PIL.Image.open(BytesIO(base64.b64decode(buffer.partition('data:image/jpeg;base64,')[2]))))
        try:
            t = time()
            frame = deepdream(net, frame, iter_n=10, octave_n=5, end=net.blobs.keys()[111])
            print 'dream took', time() - t, 'sec'
        except:
            print "dream failed"
            return buffer;
        buf = StringIO()
        pil = PIL.Image.fromarray(np.uint8(frame))
        pil.save(buf, format='jpeg')
        buf.seek(0)
        retval = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
        return retval


##########################################################################
# main function
# -------------
# runs light, for webcam use.
##########################################################################
if __name__ == '__main__':
    s = zerorpc.Server(LucidRPC())
    s.bind("tcp://0.0.0.0:8080")
    s.run()
    # print 'Listening on http://localhost:8080';
    # app.debug = True
    # socketio.run(app, host='127.0.0.1', port=8080);
    # import os
    # from werkzeug.wsgi import SharedDataMiddleware
    # app = SharedDataMiddleware(app, {
    #     '/': os.path.join(os.path.dirname(__file__), 'static')
    #     })
    # from socketio.server import SocketIOServer
    # SocketIOServer(('0.0.0.0', 8080), app,
    #     resource="socket.io", policy_server=False).serve_forever()
