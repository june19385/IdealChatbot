# -*- coding: utf-8 -*-
#---------------------------------
import Create_ResponseMsg

def orderMethod(orderNum,responseMessage,instanceVar):
	if orderNum==0:
		return __welcomeMsg()
	elif orderNum==1:
		return __modeselectMsg(responseMessage,instanceVar)
	else:
		instanceVar.setIsCommonOrder(False)
		__modeSave(responseMessage,instanceVar)

def __welcomeMsg():
	return Create_ResponseMsg.create_btnmessage("환영합니다. FCDB 입니다.\n 이상형을 찾아드려요.\n 먼저 자신의 성별을 입력해주세요.",["남","여"])

def __modeselectMsg(responseMessage,instanceVar):
	instanceVar.setUsergender(responseMessage)
	return Create_ResponseMsg.create_btnmessage("시작할 컨텐츠를 선택해주세요.",["정보입력으로 이상형 찾기","이상형 월드컵","이름 궁합 점","이상형 통계"])

def __modeSave(responseMessage,instanceVar):
	if responseMessage == u"정보입력으로 이상형 찾기":
		instanceVar.setMode(1)
	elif responseMessage == u"이상형 월드컵":
		instanceVar.setMode(2)
	elif responseMessage == u"이름 궁합 점":
		instanceVar.setMode(3)
	else:
		instanceVar.setMode(4)


		