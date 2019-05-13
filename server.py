from flask import Flask, render_template, Response, jsonify, request,send_from_directory
from camera import VideoCamera
import cv2
import sys
import time


import math
import logging as log
import datetime as dt


app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/instructions')
def instructions():
    cname = request.args.get('name')
    return render_template('instructions.html',cname=cname)
    
@app.route('/process')
def process():
    return render_template('process.html')


    
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/staticfiles/<path:path>')
def send_static(path):
    return send_from_directory('templates', path)

@app.route('/welcome')
def welcome():
    from mlfiles import faceframes
    from mlfiles import modelloaded
    from mlfiles import voiceloaded
    #faceframes.getFaceFrames()
    emotion=modelloaded.modelPrediction()
    emotion2=voiceloaded.voicemodelPrediction()
    writetoexcel(emotion,emotion2)
    return render_template('index.html',emotion=emotion,emotion2=emotion2)



@app.route('/record_status', methods=['POST','GET'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    candidate=json['candidate']
    qn=json['question']

    if status == "true":
        video_camera.start_record(candidate,qn)
        return jsonify(result="started")
    else:
        video_camera.stop_record(candidate)
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




def fetch_audio(a,b):
	video = VideoFileClip(a)
	audio = video.audio
	audio.write_audiofile(b)



@app.route('/getscore/<candidate>/')
def getscore(candidate):
    from os.path import isfile, join,isdir
    if(isfile("./static/{}/score.txt".format(candidate))):
        f = open("./static/{}/score.txt".format(candidate), "r")
        return jsonify({"score": f.read()})
    else:
        return jsonify({"score": False})

@app.route('/setscore/<candidate>/')
def setscore(candidate):
    from os.path import isfile, join,isdir
    if(isfile("./static/{}/score.txt".format(candidate))):
        k=0
    else:
        if(isdir("./static/{}".format(candidate))):
            import json
            score=json.loads(getcandidatescore('./static/{}/{}-1.avi'.format(candidate,candidate),'./static/{}/{}-1.wav'.format(candidate,candidate)))['score']
            file = open("./static/{}/score.txt".format(candidate), "w") 
            file.write(str(score))
            file.close() 
            return jsonify({"score":score})
        else:
            return jsonify({"score": False})


@app.route('/cv2')
def basiccv():
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	return tuple(frame,"Content-Type : image/jpeg\r\n\r\n")


@app.route('/admin/dashboard')
def admindashboard():
    mypath="./static/"
    from os import listdir
    from os.path import isfile, join,isdir
    onlyfiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    return render_template('admin.html',onlyfiles=onlyfiles)






def getcandidatescore(tfile1,tfile2):
    from mlfiles import audiomodal
    from mlfiles import videomodal
    import json

    em=videomodal.analysevideo(tfile1)
    em1=audiomodal.analyseaudio(tfile2)

    e=em.reshape(1,7)[0].tolist()
    e1=em1.reshape(1,7)[0].tolist()
    #print(e)
    #print(e1)
    del sys.modules['mlfiles']
    score=0
    score=((e[0] *0.7) +(e1[0]*0.3))*(-0.2)
    score=score+((e[1] *0.7) +(e1[1]*0.3))*(-0.2)
    score=score+((e[2] *0.7) +(e1[2]*0.3))*(-0.3)
    score=score+((e[3] *0.7) +(e1[3]*0.3))*(0.8)    
    score=score+((e[4] *0.7) +(e1[4]*0.3))*(-0.1)
    score=score+((e[5] *0.7) +(e1[5]*0.3))*(0.15)
    score=score+((e[6] *0.7) +(e1[6]*0.3))*(0.05)
    return json.dumps({"score" :score})


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)