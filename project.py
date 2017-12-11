# -*- coding: utf-8 -*-
#---------------------------------
import os
from flask import Flask, request, jsonify
import Hangulpy
import MainProcess

app = Flask(__name__)

mainProcess = None

@app.route('/keyboard')
def Keyboard():
    global mainProcess
    mainProcess = MainProcess.MainProcess()
    dataSend = {
        "type" : "buttons",
        "buttons" : ["챗봇 시작하기"]
    }
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():

    global mainProcess

    dataReceive = request.get_json()
    content = dataReceive['content']

    dataSend = mainProcess.mainOrder(content)

    return jsonify(dataSend)

if __name__ == "__main__":

    app.run(host='0.0.0.0', port = 5000, threaded=True)