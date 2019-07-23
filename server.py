# ai 서버, display 클라이언트
# server.py

import flask
from flask import request, make_response, jsonify
from PIL import Image
import time

import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
from PIL import Image
from IPython.display import display

import requests

num_seats = input("좌석 수 :")
num_seats = int(num_seats)
global empty_num_seats
empty_num_seats = num_seats

app = flask.Flask(__name__)

return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
pb_file         = "./yolov3_coco.pb"
image_path      = "./images/capture.jpg"
num_classes     = 80
input_size      = 128
graph           = tf.Graph()

# IP = "172.29.148.144"
# PORT = 8899


@app.route('/api/calculateEmptySeats', methods=['POST'])
def match():
    image = request.files['file']
    if image:
        with open(image_path, "wb") as fw:
        # with open('images/test{}.jpg'.format(time.time()), 'wb') as fw:
            fw.write(image.read())
            
            start = time.time()
            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            original_image_size = original_image.shape[:2]
            image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
            image_data = image_data[np.newaxis, ...]
            
            pred_sbbox, pred_mbbox, pred_lbbox = sess.run([return_tensors[1], return_tensors[2], return_tensors[3]],feed_dict={ return_tensors[0]: image_data})
            pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),np.reshape(pred_mbbox, (-1, 5 + num_classes)),np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)
            
            bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.5)
            bboxes = utils.nms(bboxes, 0.4, method='nms')
            image = utils.draw_bbox(original_image, bboxes)
            image = Image.fromarray(image)
            print("좌석 수: {}".format(num_seats))
            print("찾은 사람 수: {}".format(len(bboxes)))
            
#             requests.post(url="http://{}:{}/api/displayEmptySeats".format(IP,PORT), data={"num_empty_seats": num_seats})
            
            image.show()
            # display(image)
            end = time.time()
            print("{}seconds".format(end-start))
    else:
        print('Image empty!')
    return 'OK'

@app.route("/api/displayEmptySeats", methods=["POST"])
def display():
    global empty_num_seats
    
    if empty_num_seats < 9:
        empty_num_seats += 1
    else:
        empty_num_seats = 0
    return make_response(jsonify({"num_empty_seats": empty_num_seats}))

return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)
with tf.Session(graph=graph) as sess:
    app.run('0.0.0.0', port=5001, threaded=True)
