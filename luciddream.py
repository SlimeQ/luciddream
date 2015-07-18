#!/usr/bin/python

import socket
import sys

# math stuff
import numpy as np
import scipy.ndimage as nd
from random import randint

# data stuff
from cStringIO import StringIO
import cStringIO
import PIL.Image
from google.protobuf import text_format
# system stuff
import os
import sys
import argparse
import json
# a little sauce
import caffe
from deepdream import deepdream, net
import requests
import time
import sys
import time

from flask import Flask, request
from io import BytesIO
import base64
app = Flask(__name__)
lastFrames = dict()
@app.route('/deepdream', methods=['GET', 'POST'])
def handle_requests():
    global lastFrames
    print 'handling request'
    if request.method == 'POST':
        if 'buffer' in request.form:
            # print request.form
            # img = np.float32(PIL.Image.open(BytesIO(base64.b64decode(request.form['buffer'].partition('base64, ')[2]))))
            # img = np.float32(PIL.Image.open(StringIO(request.form['buffer'])))
            # print request.form['buffer']
            frame = np.float32(PIL.Image.open(BytesIO(base64.b64decode(request.form['buffer'].partition('data:image/jpeg;base64,')[2]))))
            h, w = frame.shape[:2]
            if not request.form['guid'] in lastFrames:
                lastFrames[request.form['guid']] = np.zeros(frame.shape)

            frame = np.add(frame * 0.9, lastFrames[request.form['guid']] * 0.3)
            # frame -= lastFrames[request.environ['REMOTE_ADDR']]
            # only in dreams
            frame = deepdream(net, frame, iter_n=1, octave_n=5, end=net.blobs.keys()[42])
            lastFrames[request.form['guid']] = frame
            # if lastFrames != None:
            #     frame = np.add(frame, lastFrames[request.environ['REMOTE_ADDR']])
            # import code
            # code.interact(local=locals())

            # PIL.Image.fromarray(np.uint8(frame)).save(filename)
            buf = StringIO()
            pil = PIL.Image.fromarray(np.uint8(frame))
            pil.save(buf, format='jpeg')
            buf.seek(0)
            return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
        else:
            return 'no data'

    else:
        return 'what is this'

##########################################################################
# main function
# -------------
# runs light, for webcam use.
##########################################################################
if __name__ == '__main__':
    app.debug = True
    port = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] != '':
        app.run(host="0.0.0.0", port=port)
    else:
        r = requests.post("http://localhost:8080/deepdream", data={'ready': True});
        print r.status_code, r.reason
        if (r.status_code == 200):
            print 'listening on', port
            app.run(host="0.0.0.0", port=port)

    # # get  args if we can.
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-f', '--filename', type=str)
    # parser.add_argument('-b', '--blob_i', default=10, type=int)
    # parser.add_argument('-p', '--port', default=8081, type=int)
    # args = parser.parse_args()
    #
    #
    #
    # # HOST = ''   # Symbolic name meaning all available interfaces
    # # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # # bound = False
    # # while not bound:
    # # 	try:
    # # 		s.bind((HOST, args.port))
    # # 		bound = True
    # # 	except socket.error , msg:
    # # 		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    # # 		args.port += 1
    # # 		print args.port
    # # s = SocketIO()
    # # sent = s.send('port', str(args.port))
    # # print 'connected to localhost', sent
    # # while True:
    # # 	# try:
    # # 		print 'listening on', args.port
    # # 		s.listen(10)
    # # 		conn, addr = s.accept()
    # # 		print conn, addr
    # # 		data = conn.recv(1024)
    # # 		print data
    # # 		filename = data
    # # 		# PIL is stupid, go away PIL
    # # 		img = np.float32(PIL.Image.open(filename))
    # #
    # # 		# see ya on the other side
    # # 		frame = img
    # # 		h, w = frame.shape[:2]
    # #
    # # 		# only in dreams
    # # 		frame = deepdream(net, frame, end=net.blobs.keys(data.blob_i))
    # # 		PIL.Image.fromarray(np.uint8(frame)).save(filename)
    # # 	# except:
    # # 		# print 'failed'
    # # 	# conn.sendall(data)
