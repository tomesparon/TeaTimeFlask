# camera dependencies
from importlib import import_module
import os

from flask import Flask, render_template, request,Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        #press button via gpio
        from subprocess import call
        call(["python", "piservo.py"])
        return render_template('boiling.html')
        
    else:
        return render_template('main_template.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,threaded=True)
