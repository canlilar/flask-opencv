from flask import Flask, render_template, Response
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    """ Video streaming home page """
    return render_template('index.html')


def gen():
    vs = WebcamVideoStream(src=1).start()
    time.sleep(2.0)
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)