#!/usr/bin/env python
# coding: utf-8


from flask import Flask, render_template, Response, jsonify, request,send_from_directory
import cv2
import sys
import time


import math
import logging as log
import datetime as dt
from pathlib import Path



from AudioModal import analyseaudio
from VideoModal import analysevideo


def getscore(tfile1,tfile2):
    em=analysevideo(tfile1)
    em1=analyseaudio(tfile2)

    e=em.reshape(1,7)[0].tolist()
    e1=em1.reshape(1,7)[0].tolist()
    #print(e)
    #print(e1)
    return jsonify({"score" :(e[i] *0.7) +(e1[i]*0.3)})
