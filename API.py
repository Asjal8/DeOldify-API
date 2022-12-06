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

# choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

plt.style.use('dark_background')
torch.backends.cudnn.benchmark = True

warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

app = Flask(__name__)


# Image Colorizer Artistic

@app.route('/uploadImgArtistic', methods=['POST'])
def myServerCall():
    colorizer = get_image_colorizer(artistic=True)

    # these 2 parameters we receive from frontend
    myImg = request.files['img']

    filename = myImg.filename

    print("source img 1 = ", myImg)

    myImg.save("./test_images/" + filename)
    source_image = "./test_images/" + filename
    myImg_path = source_image

    # NOTE:  Max is 45 with 11GB video cards. 35 is a good default
    render_factor = 19
    # NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    source_url = None
    source_path = 'test_images/image.png'
    result_path = 'result_images'

    if source_url is not None:
        result_path = colorizer.plot_transformed_image_from_url(url=source_url, path=source_path,
                                                                render_factor=render_factor, compare=True)
    else:
        result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)

    # show_image_in_notebook(result_path)

    with open("result_images/image.png", "rb") as img_file:
        myStr = base64.b64encode(img_file.read()).decode('utf-8')

    os.remove(myImg_path)
    # os.remove("ConvertedImages/result.mp4")

    return jsonify({
        "responseVideo": myStr,
        "myServerMessage": "Image converted",
    })


# Image Colorizer Stable

@app.route('/uploadImgStable', methods=['POST'])
def myServer2Call():
    # choices:  CPU, GPU0...GPU7
    device.set(device=DeviceId.GPU0)

    colorizer = get_image_colorizer(artistic=False)

    # these 2 parameters we receive from frontend
    myImg = request.files['img']

    filename = myImg.filename

    print("source img 1 = ", myImg)

    myImg.save("./test_images/" + filename)
    source_image = "./test_images/" + filename
    myImg_path = source_image

    # NOTE:  Max is 45 with 11GB video cards. 35 is a good default
    render_factor = 19
    # NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    source_url = None
    source_path = 'test_images/image.png'
    result_path = 'result_images'

    if source_url is not None:
        result_path = colorizer.plot_transformed_image_from_url(url=source_url, path=source_path,
                                                                render_factor=render_factor, compare=True)
    else:
        result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)

    # show_image_in_notebook(result_path)

    with open("result_images/image.png", "rb") as img_file:
        myStr = base64.b64encode(img_file.read()).decode('utf-8')

    os.remove(myImg_path)
    # os.remove("ConvertedImages/result.mp4")

    return jsonify({
        "responseVideo": myStr,
        "myServerMessage": "Image converted",
    })


# Video Colorizer

@app.route('/uploadVideo', methods=['POST'])
def myServer3Call(video_file=None):
    # choices:  CPU, GPU0...GPU7
    device.set(device=DeviceId.GPU0)

    warnings.filterwarnings("ignore", category=UserWarning,
                            message=".*?Your .*? set is empty.*?")

    # these 2 parameters we receive from frontend
    myVideo = request.files['video']

    filename = myVideo.filename

    print("source video 1 = ", myVideo)

    myVideo.save("./video/source/" + filename)
    source_video = "./video/source/" + filename
    myImg_path = source_video

    colorizer: VideoColorizer = get_video_colorizer()

    # NOTE:  Max is 44 with 11GB video cards.  21 is a good default
    render_factor = 19
    # NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    source_url = None
    file_name = 'GIF'
    file_name_ext = file_name + '.mp4'
    result_path = 'result_video'

    if source_url is not None:
        result_path = colorizer.colorize_from_url(source_url, file_name_ext,
                                                  render_factor=render_factor)
    else:
        result_path = colorizer.colorize_from_file_name(file_name_ext,
                                                        render_factor=render_factor)

    show_video_in_notebook(result_path)

    for i in range(10, 45, 2):
        colorizer.vis.plot_transformed_image('video/bwframes/' + file_name + '/00001.jpg',
                                             render_factor=i,
                                             display_render_factor=True, figsize=(8, 8))

    with open("./video/result", "rb") as video_file:
        myStr = base64.b64encode(video_file.read()).decode('utf-8')

    os.remove(myImg_path)
    # os.remove("ConvertedImages/result.mp4")

    return jsonify({
        "responseVideo": myStr,
        "myServerMessage": "Image converted",
    })


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=50100, threads=1)
