# OK:50フレームごとに画像データを受信してimgタグに表示する
from flask import Flask, jsonify, render_template, Response;
from flask_socketio import SocketIO, send, emit
import base64

from camera import VideoCamera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):

    prefix = 'data:image/png;base64,'

    count = 0
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        count += 1
        if frame is not None:
            if count % 20 == 0:
                emit('capture-send', { 'dataURL': prefix+base64.b64encode(frame).decode('utf-8')})
        else:
            break

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketIo.run(app)
