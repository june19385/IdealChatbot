# -*- coding: utf-8 -*-
#---------------------------------
import os
import Create_ResponseMsg, DatabaseConnection
from PIL import Image

class RankView(object):
	"""docstring for RankView"""
	def __init__(self):
		self.__DBinstance = DatabaseConnection.DatabaseConnection()
		self.__dirname = str(id(self))

	def detailProcess(self,order,responseMessage,instanceVar):
		if order == 1:
			return self.__modeSelectMsg()
		elif order == 2:
			return self.__divideMode(responseMessage,instanceVar)
		else:
			return self.__whereGo(responseMessage, instanceVar)


	def __modeSelectMsg(self):
		return Create_ResponseMsg.create_btnmessage("보고싶은 통계 모드를 선택해주세요.",["이상형 순위","이름 궁합점 순위"])

	def __divideMode(self,responseMessage,instanceVar):
		if responseMessage == u"이상형 순위":
			return self.__showIdealRank(instanceVar.getUsergender())
		else:
			return self.__showNameMatchRank()

	def __showIdealRank(self,gender):
		returnlist = []
		returnlist = self.__DBinstance.getIdealRank(gender)
		returnMsg = u""
		for i in range(len(returnlist)):
			returnMsg+=returnlist[i][0]+u"  |  "+unicode(returnlist[i][2])+u"점\n"

		imagesource = u""
		imagesource = self.__imageMerge(returnlist[0][1],returnlist[1][1])
		return Create_ResponseMsg.create_imgbtnmessage(returnMsg,u"http://13.125.39.205:5000/static/"+imagesource,["처음으로 돌아가기"])


	def __showNameMatchRank(self):
		returnlist = []
		returnlist = self.__DBinstance.getNameMatchRank()
		returnMsg = u""
		for i in range(len(returnlist)):
			returnMsg+=returnlist[i][0]+u" ♥ "+returnlist[i][1]+u" | "+unicode(returnlist[i][2])+u"점\n"

		return Create_ResponseMsg.create_btnmessage(returnMsg,["처음으로 돌아가기"])


	def __whereGo(self,responseMessage,instanceVar):
		if os.path.isfile("/home/ec2-user/database_project/static/"+self.__dirname+"/"+self.__dirname+".png"):
			os.remove("/home/ec2-user/database_project/static/"+self.__dirname+"/"+self.__dirname+".png")
		if os.path.isdir("/home/ec2-user/database_project/static/"+self.__dirname):
			os.rmdir("/home/ec2-user/database_project/static/"+self.__dirname)
		instanceVar.setIsLoop(True)
		instanceVar.setIsCommonOrder(True)
		instanceVar.setDetailOrder(0)
		instanceVar.setModeInstance(None)
		return None	

	def __imageMerge(self,firstimage,secondimage):
		os.mkdir("/home/ec2-user/database_project/static/"+self.__dirname,0777)

		new_image = Image.new("RGB",(640,480),(256,256,256))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(firstimage)),(0,0,320,480))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(secondimage)),(320,0,640,480))
		imagesource = self.__dirname+"/"+self.__dirname+".png"

		new_image.save("/home/ec2-user/database_project/static/"+imagesource,"PNG")
		return imagesource.decode("utf-8")

