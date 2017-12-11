# -*- coding: utf-8 -*-
#---------------------------------
import os
from PIL import Image
import Create_ResponseMsg, DatabaseConnection
from datetime import date, datetime, timedelta

class IdealWorldCup(object):
	"""docstring for IdealWorldCup"""
	def __init__(self):
		self.__mode=u""
		self.__limitnum=0
		self.__indexnum=0
		self.__ideallist = []
		self.__DBinstance = DatabaseConnection.DatabaseConnection()
		self.__dirname = str(id(self))
		self.__imgname = id(self)
		os.mkdir("/home/ec2-user/database_project/static/"+self.__dirname,0777)
		

	def detailProcess(self,order,responseMessage,instanceVar):
		if responseMessage == u"처음으로 돌아가기":
			return self.__whereGo(responseMessage,instanceVar)

		if order==1:
			return self.__howmanyMsg()
		elif order==2:
			return self.__initIdeal(responseMessage,instanceVar)
		else:
			return self.__IdealMsg(responseMessage)

	def __howmanyMsg(self):
		return Create_ResponseMsg.create_btnmessage(u"모드를 선택해주세요.",[u"16강",u"32강"])

	def __initIdeal(self,responseMessage, instanceVar):
		if responseMessage == u"16강":
			self.__limitnum = 16
		else:
			self.__limitnum = 32

		self.__ideallist = self.__DBinstance.getIdeallist(self.__limitnum,instanceVar.getUsergender())

		return self.__IdealMsg(responseMessage)


	def __IdealMsg(self,responseMessage):

		if not responseMessage == u"16강" and not responseMessage == u"32강":
			person_id = -1
			if responseMessage == self.__ideallist[self.__indexnum-1][1]:
				person_id = self.__ideallist[self.__indexnum-1][0]
				del(self.__ideallist[self.__indexnum])
			else:
				person_id = self.__ideallist[self.__indexnum][0]
				del(self.__ideallist[self.__indexnum-1])

			self.__DBinstance.updateCount(person_id)
			
			if self.__indexnum == self.__limitnum/2:
				self.__limitnum = self.__indexnum
				self.__indexnum = 0

		
		if len(self.__ideallist)!=1:
			imagesource = u""
			imagesource = self.__imageMerge(self.__ideallist[self.__indexnum][2],self.__ideallist[self.__indexnum+1][2])
			btn_text=[]
			btn_text.append(self.__ideallist[self.__indexnum][1])
			btn_text.append(self.__ideallist[self.__indexnum+1][1])
			self.__indexnum+=1
			return Create_ResponseMsg.create_imgbtnmessage(self.__ideallist[self.__indexnum-1][1]+u" VS "+self.__ideallist[self.__indexnum][1],u"http://13.125.39.205:5000/static/"+imagesource,btn_text)
		else:
			person_id = self.__ideallist[0][0]
			name = self.__ideallist[0][1]
			age = self.__ideallist[0][3]
			height = self.__ideallist[0][4]

			dateobj = date.today()
			currentyear = int(dateobj.year)+1
			year = int(age.year)
			realage = currentyear-year
			agetext = unicode(str((realage/10)*10))
			if realage%10<4:
				agetext += u"대 초반"
			elif realage%10<7:
				agetext += u"대 중반"
			else:
				agetext += u"대 후반"

			heighttext=unicode(str((height/10)*10))
			if height%10<4:
				heighttext += u"cm 초반"
			elif height%10<7:
				heighttext += u"cm 중반"
			else:
				heighttext += u"cm 후반"

			returntext = u""
			returntext+=u"당신의 이상형은 "+name+u" 입니다!!\n"
			returntext+=u"당신의 취향은\n"
			returntext+=u"나이 : "+agetext+u"\n"
			returntext+=u"키 : "+heighttext+u"\n"

			infolist=[]
			infolist = self.__DBinstance.selectinfo(person_id)
			for i in range(len(infolist)):
				returntext+=infolist[i][0]+u" : "+infolist[i][1]+u"\n"
			returntext+=u"위의 조건을 만족하는 사람입니다.\n"
			returnbtn=[u"처음으로 돌아가기"]
			imagesource = self.__createFinalimage(self.__ideallist[0][2])

			return Create_ResponseMsg.create_imgbtnmessage(returntext,u"http://13.125.39.205:5000/static/"+imagesource,returnbtn)



	def __imageMerge(self,firstimage,secondimage):
		if os.path.isfile("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png"):
			os.remove("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png")
		new_image = Image.new("RGB",(640,480),(256,256,256))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(firstimage)),(0,0,320,480))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(secondimage)),(320,0,640,480))
		imagesource = self.__dirname+"/"+str(self.__imgname)+".png"

		new_image.save("/home/ec2-user/database_project/static/"+imagesource,"PNG")
		self.__imgname+=1
		return imagesource.decode("utf-8")

	def __createFinalimage(self,image):
		if os.path.isfile("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png"):
				os.remove("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png")
		new_image = Image.new("RGB",(640,480),(256,256,256))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(image)),(160,0,480,480))
		imagesource = self.__dirname+"/"+str(self.__imgname)+".png"
		new_image.save("/home/ec2-user/database_project/static/"+imagesource,"PNG")
		self.__imgname+=1
		return imagesource.decode("utf-8")

	def __whereGo(self,responseMessage,instanceVar):
		if os.path.isfile("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png"):
			os.remove("/home/ec2-user/database_project/static/"+self.__dirname+"/"+str(self.__imgname-1)+".png")
		if os.path.isdir("/home/ec2-user/database_project/static/"+self.__dirname):
			os.rmdir("/home/ec2-user/database_project/static/"+self.__dirname)
		instanceVar.setIsLoop(True)
		instanceVar.setIsCommonOrder(True)
		instanceVar.setDetailOrder(0)
		instanceVar.setModeInstance(None)
		return None







