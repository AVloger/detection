import base64
import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector
import cv2
import numpy as np
import core.main
from flask_cors import CORS
from torchvision import transforms

import core.predict

UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
CORS(app, resources=r'/*')
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    # return base64.decodestring(data)
    return base64.b64decode(data)
transform=transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485,0.456,0.406],
                                 std=[0.229,0.224,0.225])
                            ])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    # 这样获取就可以了
    data = json.loads(request.get_data("data"))
    data_64 = str.encode(data['data'])

    imgdata = decode_base64(data_64)
    filename = 'C:\\Users\\ASUS\\Desktop\\Yolov5-Flask-VUE-master\\Yolov5-Flask-VUE-master\\back-end\\test.jpg'
    file = open(filename, 'wb')
    file.write(imgdata)
    file.close()
    image_info,img_y = core.predict.my_predict(filename,current_app.model)
    infos = []
    for info in image_info:
        infos.append({"object":info,"confidence":image_info[info][1]})
    print(infos)
    img_str = cv2.imencode('.jpeg', img_y)[1].tostring()  # 将图片编码成流数据，放到内存缓存中，然后转化成string格式
    b64_code = base64.b64encode(img_str)  # 编码成base64
    return jsonify({'status':200,
                    'image_info': image_info ,
                    'image_dev':str(b64_code, 'utf8')})
    # return jsonify({'status': 0})
    # file = request.files['file']
    # print(datetime.datetime.now(), file.filename)
    # if file and allowed_file(file.filename):
    #     src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #     file.save(src_path)
    #     shutil.copy(src_path, './tmp/ct')
    #     shutil.copy(src_path, './tmp/draw')
    #     image_path = os.path.join('./tmp/ct', file.filename)
    #     pid, image_info = core.main.c_main(
    #         image_path, current_app.model, file.filename.rsplit('.', 1)[1])
    #     return jsonify({'status': 1,
    #                     'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
    #                     'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
    #                     'image_info': image_info})
    #
    # return jsonify({'status': 0})


@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
# @app.route('/video_feed')  # 这个地址返回视频流响应
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    with app.app_context():
        current_app.model = Detector()
    app.run(host='127.0.0.1', port=5003, debug=True)
