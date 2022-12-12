#!/usr/bin/python3
# coding=utf-8
import base64
import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector
import cv2
from pathlib import Path
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
# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Allow-Methods'] = 'POST'
#     response.headers['Access-Control-Allow-Headers'] = '*'
#     return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

VID_FORMATS = ('.mov', '.avi', '.mp4', '.mpg',  '.mpeg', '.m4v', '.wmv', '.mkv', '.mp3')
PHOTO_FORMATS = ('.jpg')


def videos2images(video_dir_path, root_save_dir):
    # 1.检测读取文件路径是否正确
    path_video = Path(video_dir_path)
    if path_video.is_dir():
        print(video_dir_path + '\t ok')
        videos = os.listdir(video_dir_path)
    else:
        print('\033[31mLine36 error: \033[31m' + video_dir_path + 'is not exist!')
        return

    # 2. 生成存储文件夹
    save_name_dir = Path(path_video.name)
    save_name_dir = os.path.join(root_save_dir, save_name_dir)
    if not os.path.exists(save_name_dir):
        os.makedirs(save_name_dir)

    file_count = 0
    for video in videos:
        # 判断是否为视频文件,如果不是视频文件则跳过并进行说明
        if Path(video).suffix in VID_FORMATS:
            file_count += 1  # 视频文件数+1
            save_jpg_dir = os.path.join(save_name_dir, Path(video).stem)
            each_video_path = os.path.join(path_video, video)
            save_dir = save_jpg_dir
        else:
            print('\033[33mLine56 warning: \033[33m' + os.path.basename(video) + ' is not a video file, so skip.')
            continue

        # 3. 开始转换。打印正在处理文件的序号和他的文件名，并开始转换
        print('\033[38m' + str(file_count) + ':' + Path(video).stem + '\033[38m')
        cap = cv2.VideoCapture(each_video_path)

        flag = cap.isOpened()
        if not flag:
            print("\033[31mLine 65 error\033[31m: open" + each_video_path + "error!")

        frame_count = 0  # 给每一帧标号
        while True:
            frame_count += 1
            flag, frame = cap.read()
            if not flag:  # 如果已经读取到最后一帧则退出
                break
            if os.path.exists(
                    save_dir + str(frame_count) + '.jpg'):  # 在源视频不变的情况下，如果已经创建，则跳过
                break
            cv2.imwrite(save_dir + '\\' + str(frame_count) + '.jpg', frame)

        cap.release()
        print('\033[38m' + Path(video).stem + ' save to ' + save_dir + 'finished. \033[38m')  # 表示一个视频片段已经转换完成



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

from werkzeug.utils import secure_filename
@app.route('/uploadVideo', methods=['GET', 'POST'])
def upload_video():
    # if request.method == 'POST':
    # 这样获取就可以了
    store_file_path = 'C:\\Users\\ASUS\\Desktop\\detection\\Flask\\tmp\\'
    file_buffer = request.files['file']
    f_name = secure_filename(file_buffer.filename)
    data = {"code": 500, "msg": "上传失败！"}
    video_path_list = store_file_path

    # 预期存储在的主文件夹，即'result'文件夹下
    image_save_dir = store_file_path+'photo\\'
    path_save = Path(image_save_dir)
    if not path_save.exists():
        path_save.mkdir()
    # 进行转换
    videos2images(video_path_list, image_save_dir)

    file_dir = image_save_dir + 'uploads\\'
    list = []
    for root ,dirs, files in os.walk(file_dir):
        for file in files:
            list.append(file)      # 获取目录下文件名列表

    video = cv2.VideoWriter(store_file_path + 'test.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),5,(1981,991))

    for i in range(1,len(list)):
        img = file_dir + f_name+'\\'+str(i)+'.jpg'
        image_info,img_y = core.predict.my_predict(img,current_app.model)
        infos = []
        for info in image_info:
            infos.append({"object":info,"confidence":image_info[info][1]})
        print(infos)
        img_y = cv2.resize(img_y,(1981,991)) #将图片转换为1280*720像素大小
        video.write(img_y) # 写入视频
    # 释放资源
    video.release()
    try:
        file_buffer.save(store_file_path + 'test.mp4')
        data.update({"code": 200, "msg": "上传成功！", "Data": 'http://127.0.0.1:5003/tmp/' + 'test.mp4'})
    except FileNotFoundError as e:
        print(e)
    return jsonify(data)



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
