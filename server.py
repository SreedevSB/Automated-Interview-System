from flask import Flask, render_template, Response, jsonify, request,send_from_directory
from camera import VideoCamera
import cv2
import sys
from moviepy.editor import *
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
    return render_template('instructions.html')
    
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

def writetoexcel(em,em1):
    # Writing to an excel  
    # sheet using Python 
    import xlwt 
    from xlwt import Workbook 
    
    # Workbook is created 
    wb = Workbook() 
    e=em.tolist()
    
    e1=em1.tolist()
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 
    
    sheet1.write(1, 0, 'Angry') 
    sheet1.write(2, 0, 'Disgust') 
    sheet1.write(3, 0, 'Fear') 
    sheet1.write(4, 0, 'Happy') 
    sheet1.write(5, 0, 'Sad') 
    sheet1.write(6, 0, 'Surprise') 
    sheet1.write(7, 0, 'Neutral')
    i=0
    sheet1.write(1, 1, str(e[i][0])); i+=1
    sheet1.write(2, 1, str(e[i][0])) ; i+=1
    sheet1.write(3, 1, str(e[i][0])) ; i+=1
    sheet1.write(4, 1, str(e[i][0])) ; i+=1
    sheet1.write(5, 1, str(e[i][0])) ; i+=1
    sheet1.write(6, 1, str(e[i][0])) ; i+=1
    sheet1.write(7, 1, str(e[i][0]))

    i=0
    sheet1.write(1, 2, str(e1[i][0])); i+=1
    sheet1.write(2, 2, str(e1[i][0])) ; i+=1
    sheet1.write(3, 2, str(e1[i][0])) ; i+=1
    sheet1.write(4, 2, str(e1[i][0])) ; i+=1
    sheet1.write(5, 2, str(e1[i][0])) ; i+=1
    sheet1.write(6, 2, str(e1[i][0])) ; i+=1
    sheet1.write(7, 2, str(e1[i][0]))
    
    i=0;
    sheet1.write(1, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)); i+=1
    sheet1.write(2, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)) ; i+=1
    sheet1.write(3, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)) ; i+=1
    sheet1.write(4, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)) ; i+=1
    sheet1.write(5, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)); i+=1
    sheet1.write(6, 3, (e[i][0] *0.9) +(e1[i][0]*0.1)) ; i+=1
    sheet1.write(7, 3, (e[i][0] *0.9) +(e1[i][0]*0.1))
    
    wb.save('xlwt example.xls') 




@app.route('/record_status', methods=['POST','GET'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    candidate=json['candidate']

    if status == "true":
        video_camera.start_record(candidate)
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



@app.route('/cv2')
def basiccv():
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	return tuple(frame,"Content-Type : image/jpeg\r\n\r\n")


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)