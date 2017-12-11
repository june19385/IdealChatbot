# -*- coding: utf-8 -*-
#---------------------------------

def create_message(message_text):
    dataSend = {
        "message": {
            "text": message_text
        }
    }
    return dataSend

def create_btnmessage(message_text,btn_text):
    dataSend = {
        "message": {
            "text": message_text
        },
        "keyboard": {
            "type": "buttons",
        "buttons": btn_text
        }
    }
    return dataSend

def create_imgbtnmessage(meesage_text,imgurl,btn_text):
    dataSend = {
        "message": {
            "text": meesage_text,
            "photo": {
                "url": imgurl,
                "width": 640,
                "height": 480
            },
        },
        "keyboard": {
            "type": "buttons",
            "buttons": btn_text
        }
    }
    return dataSend
