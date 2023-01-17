# NOTE:  This must be the first call in order to work properly!
# from ast import main
import warnings
from urllib3 import request
import urllib3.request

import matplotlib
from flask import Flask, jsonify, request
from waitress import serve

from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
from deoldify.visualize import VideoColorizer


matplotlib.use('Agg')
import os, shutil
import glob


# choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

plt.style.use('dark_background')
torch.backends.cudnn.benchmark = True

warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

app = Flask(__name__)


# Image Colorizer Artistic

@app.route('/uploadImgArtistic', methods=['POST'])
def myServerCall():
    # choices:  CPU, GPU0...GPU7
    device.set(device=DeviceId.GPU0)

    colorizer = get_image_colorizer(artistic=True)

    # these 2 parameters we receive from frontend
    img = request.files['img']

    factor = int(request.form['factor'])

    img_name = img.filename

    print("source img 1 = ", img_name)

    img_path = "./test_images/" + img_name

    img.save(img_path)

    # NOTE:  Max is 45 with 11GB video cards. 35 is a good default
    render_factor = factor
    # NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    result_path = colorizer.plot_transformed_image(path=img_path, render_factor=render_factor, compare=True)

    output_img_path = "./result_images/" + img_name

    with open(output_img_path, "rb") as img_file:
        myStr = base64.b64encode(img_file.read()).decode('utf-8')

    os.remove(img_path)
    # os.remove(output_img_path)S

    return jsonify({
        "responseImage": myStr,
        "myServerMessage": "Image converted",
    })



# Image Colorizer Stable

@app.route('/uploadImgStable', methods=['POST'])
def myServer2Call():
    # choices:  CPU, GPU0...GPU7
    device.set(device=DeviceId.GPU0)

    colorizer = get_image_colorizer(artistic=False)

    # these 2 parameters we receive from frontend
    img = request.files['img']

    factor = int(request.form['factor'])

    img_name = img.filename

    print("source img 1 = ", img_name)

    img_path = "./test_images/" + img_name

    img.save(img_path)

    # NOTE:  Max is 45 with 11GB video cards. 35 is a good default
    render_factor = factor
    # NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    result_path = colorizer.plot_transformed_image(path=img_path, render_factor=render_factor, compare=True)

    output_img_path = "./result_images/" + img_name

    with open(output_img_path, "rb") as img_file:
        myStr = base64.b64encode(img_file.read()).decode('utf-8')

    os.remove(img_path)
    # os.remove(output_img_path)

    return jsonify({
        "responseImage": myStr,
        "myServerMessage": "Image converted",
    })


# Video Colorizer

@app.route('/uploadVideo', methods=['POST'])
def myServer3Call():
    # choices:  CPU, GPU0...GPU7
    device.set(device=DeviceId.GPU0)

    # these 2 parameters we receive from frontend
    video = request.files['video']
    factor = int(request.form['factor'])

    video_name = video.filename

    print("source video 1 = ", video_name)

    video_path = "./video/source/" + video_name
    video.save(video_path)

    colorizer: VideoColorizer = get_video_colorizer()

    # NOTE:  Max is 44 with 11GB video cards.  21 is a good default
    render_factor = factor

    result_path = colorizer.colorize_from_file_name(video_path,
                                                    render_factor=render_factor)

    show_video_in_notebook(result_path)

    # for i in range(10, 45, 2):
    #     colorizer.vis.plot_transformed_image('video/bwframes/' + file_name + '/00001.jpg',
    #                                         render_factor=i,
    #                                        display_render_factor=True, figsize=(8, 8))

    output_video_path = "./video/result/" + video_name

    with open(output_video_path, "rb") as video_file:
        myStr = base64.b64encode(video_file.read()).decode('utf-8')

    os.remove(video_path)
    # os.remove("ConvertedImages/result.mp4")

    return jsonify({
        "responseVideo": myStr,
        "myServerMessage": "Video converted",
    })




if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=50100, threads=1)
