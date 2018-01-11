# camera dependencies

from camera import VideoCamera
from flask import Flask, render_template, request,Response


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
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,threaded=True)
