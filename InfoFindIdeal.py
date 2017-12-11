# -*- coding: utf-8 -*-
#---------------------------------
import os
import Create_ResponseMsg, DatabaseConnection
from datetime import date, datetime, timedelta
from PIL import Image

class InfoFindIdeal(object):

	def __init__(self):
		self.__height=""
		self.__age=""
		self.__facecolor=u""
		self.__faceshape=u""
		self.__istwineye=u""
		self.__DBinstance = DatabaseConnection.DatabaseConnection()
		self.__containinsertlist=[]
		self.__dirname = str(id(self))
		self.__isfinished = False
		os.mkdir("/home/ec2-user/database_project/static/"+self.__dirname,0777)

	def detailProcess(self,order,responseMessage,instanceVar):
		if self.__isfinished == True:
			return self.__whereGo(responseMessage,instanceVar)

		if order==1:
			return self.__heightMsg()
		elif order==2:
			return self.__ageMsg(responseMessage,instanceVar)
		elif order==3:
			return self.__facecolorMsg(responseMessage,instanceVar)
		elif order==4:
			return self.__faceshapeMsg(responseMessage, instanceVar)
		elif order==5:
			return self.__istwineyeMsg(responseMessage, instanceVar)
		elif order==6:
			return self.__calcIdeal(responseMessage,instanceVar)
		else:
			return self.__loopFindideal(responseMessage,instanceVar)


	def __heightMsg(self):
		return Create_ResponseMsg.create_message("이상형으로 생각하는 키를 입력해주세요.\n ex> 160~165, 160대 초반")

	def __ageMsg(self,responseMessage, instanceVar):
		tmpheight = self.__textparsing(responseMessage)
		if tmpheight == u"":
			instanceVar.setDetailOrder(instanceVar.getDetailOrder()-1)
			return Create_ResponseMsg.create_message("이상형으로 생각하는 키를 올바르게 입력해주세요.\n ex> 160~165, 160대 초반")

		iscorrectrange = self.__rangereturnlist(tmpheight)

		if int(str(iscorrectrange[0]))>int(str(iscorrectrange[1])):
			instanceVar.setDetailOrder(instanceVar.getDetailOrder()-1)
			return Create_ResponseMsg.create_message("이상형으로 생각하는 키를 올바르게 입력해주세요.\n ex> 160~165, 160대 초반")

		self.__height=tmpheight
		return Create_ResponseMsg.create_message("이상형으로 생각하는 나이대를 입력해주세요.\n ex> 20~30, 20대 후반")

	def __facecolorMsg(self,responseMessage, instanceVar):
		tmpage = self.__textparsing(responseMessage)
		if tmpage == u"":
			instanceVar.setDetailOrder(instanceVar.getDetailOrder()-1)
			return Create_ResponseMsg.create_message("이상형으로 생각하는 나이대를 올바르게 입력해주세요.\n ex> 20~30, 20대 후반")

		iscorrectrange = self.__rangereturnlist(tmpage)
		
		if int(str(iscorrectrange[0]))>int(str(iscorrectrange[1])):
			instanceVar.setDetailOrder(instanceVar.getDetailOrder()-1)
			return Create_ResponseMsg.create_message("이상형으로 생각하는 나이대를 올바르게 입력해주세요.\n ex> 20~30, 20대 후반")

		self.__age=tmpage
		btns = []
		btns = self.__DBinstance.getDetaillist(u"피부톤",instanceVar.getUsergender())
		return Create_ResponseMsg.create_btnmessage("이상형으로 생각하는 상대의 피부톤을 입력해주세요.",btns)

	def __faceshapeMsg(self,responseMessage, instanceVar):
		self.__facecolor=responseMessage
		btns = []
		btns = self.__DBinstance.getDetaillist(u"얼굴상",instanceVar.getUsergender())
		return Create_ResponseMsg.create_btnmessage("이상형으로 생각하는 상대의 얼굴상을 입력해주세요.",btns)

	def __istwineyeMsg(self,responseMessage, instanceVar):
		self.__faceshape=responseMessage
		btns = []
		btns = self.__DBinstance.getDetaillist(u"쌍커풀 유무",instanceVar.getUsergender())
		return Create_ResponseMsg.create_btnmessage("이상형으로 생각하는 상대의 쌍커풀 유무를 입력해주세요.",btns)

	def __calcIdeal(self,responseMessage,instanceVar):
		self.__istwineye=responseMessage

		heightlist = self.__rangereturnlist(self.__height)
		agelist = self.__rangereturnlist(self.__age)

		dateobj = date.today()
		currentyear = int(dateobj.year)+1
		tmpage = int(agelist[0])
		agelist[0] = unicode(currentyear-int(agelist[1]))
		agelist[1] = unicode(currentyear-tmpage)
		insertlist=[]
		tmpinsertlist = [u"키",u"(P.height>="+unicode(heightlist[0])+u" AND P.height<="+unicode(heightlist[1])+u")"]
		insertlist.append(tmpinsertlist)
		tmpinsertlist = [u"나이",u"(YEAR(P.age)>="+unicode(agelist[0])+u" AND YEAR(P.age)<="+unicode(agelist[1])+u")"]
		insertlist.append(tmpinsertlist)
		tmpinsertlist = [u"얼굴상",u"(I1.Detail_category_name = '"+self.__facecolor+u"')"]
		insertlist.append(tmpinsertlist)
		tmpinsertlist = [u"피부색",u"(I2.Detail_category_name = '"+self.__faceshape+u"')"]
		insertlist.append(tmpinsertlist)
		tmpinsertlist = [u"쌍커풀 유무",u"(I3.Detail_category_name = '"+self.__istwineye+u"')"]
		insertlist.append(tmpinsertlist)
		self.__containinsertlist = insertlist


		returnlist = self.__DBinstance.getInfoIdeal(insertlist,instanceVar.getUsergender())
		if returnlist==u"":
			return Create_ResponseMsg.create_btnmessage(u"조건에 맞는 이상형이 없습니다.\n 가장 중요하지 않은 조건을 선택해주세요",["키","나이","얼굴상","피부색","쌍커풀 유무"])
		else:
			self.__isfinished = True
			imagesource = self.__createFinalimage(returnlist[2])
			return Create_ResponseMsg.create_imgbtnmessage(u"입력한 조건에 맞는 이상형은 "+returnlist[1]+u" 입니다.\n" ,u"http://13.125.39.205:5000/static/"+imagesource,[u"처음으로 돌아가기"])

	def __loopFindideal(self,responseMessage,instanceVar):
		returnbtn = []
		i = 0
		k = -1
		while i < len(self.__containinsertlist):
			if self.__containinsertlist[i][0]==responseMessage:
				k = i
			else:
				returnbtn.append(self.__containinsertlist[i][0])
			i+=1
		del(self.__containinsertlist[k])
			

		returnlist = self.__DBinstance.getInfoIdeal(self.__containinsertlist,instanceVar.getUsergender())

		if returnlist==u"":
			return Create_ResponseMsg.create_btnmessage(u"조건에 맞는 이상형이 없습니다.\n 가장 중요하지 않은 조건을 선택해주세요",returnbtn)
		else:
			self.__isfinished = True
			imagesource = self.__createFinalimage(returnlist[2])
			return Create_ResponseMsg.create_imgbtnmessage(u"입력한 조건에 맞는 이상형은 "+returnlist[1]+u" 입니다.\n" ,u"http://13.125.39.205:5000/static/"+imagesource,[u"처음으로 돌아가기"])

	def __createFinalimage(self,image):
		new_image = Image.new("RGB",(640,480),(256,256,256))
		new_image.paste(Image.open("/home/ec2-user/database_project/"+str(image)),(160,0,480,480))
		imagesource = self.__dirname+"/"+self.__dirname+".png"
		new_image.save("/home/ec2-user/database_project/static/"+imagesource,"PNG")
		return imagesource.decode("utf-8")

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
		

	def __rangereturnlist(self, rangestring):
		before=u""
		after=u""
		i = 0
		flag = False
		while i<len(rangestring):
			if rangestring[i]!=u"~":
				if flag == False:
					before+=rangestring[i]
				else:
					after+=rangestring[i]
			else:
				flag = True
			i+=1
		return [before,after]



	def __textparsing(self,inputtext):
		text = u""
		for i in range(0,len(inputtext)):
			if inputtext[i]!=u" " and inputtext[i]!=u"대" and inputtext[i]!=u"cm" and inputtext[i]!=u"살" and inputtext[i]!=u"세":
				text+=inputtext[i]

		if text == u"":
			return text

		midlist = [u"~",u"-",u"에서"]
		midparsing = u""

		#범위 파싱
		for i in range(0,len(midlist)):
			j = len(midlist[i])-1
			storetext = u""
			flag = False
			k = 0

			while k<len(text)-j:
				tmptext = u""
				for m in range(0,j+1):
					tmptext+=text[k+m]

				if tmptext!=midlist[i]:
					storetext+=text[k]
				else:
					storetext+=u"~"
					k+=j
					flag = True
				k+=1
			while k<len(text):
				storetext+=text[k]
				k+=1
			if flag == True:
				midparsing = storetext
				break

		if midparsing == u"":
			#범위 없이 초반 중반 후반만 경우 or 숫자만 있을 경우 ex> 160, 160초반
			if self.__is_number(text):
				#숫자만 있을 경우 ex> 160, 160초반
				text+=u"~"+text
				return text
			else:
				#범위 없이 초반 중반 후반만 경우
				savetext = u""
				cjhlist=[u"초반",u"중반",u"후반"]
				for i in range(0,len(cjhlist)):
					j = len(cjhlist[i])-1
					storetext = u""
					flag = False
					flagnum = 0
					k = 0
					while k<len(text)-j:
						tmptext = u""
						for m in range(0,j+1):
							tmptext+=text[k+m]

						if tmptext!=cjhlist[i]:
							storetext+=text[k]
						else:
							flagnum = k
							tmpsavetext = u""
							for m in range(0,k):
								tmpsavetext+=text[m]
							if self.__is_number(tmpsavetext):
								if cjhlist[i]==u"초반":
									start = (int(tmpsavetext)/10)*10
									end = ((int(tmpsavetext)/10)*10)+3
								elif cjhlist[i]==u"중반":
									start = ((int(tmpsavetext)/10)*10)+3
									end = ((int(tmpsavetext)/10)*10)+6
								else:
									start = ((int(tmpsavetext)/10)*10)+6
									end = ((int(tmpsavetext)/10)*10)+9
								savetext+=unicode(start)+"~"+unicode(end)
								return savetext
							return savetext						
						k+=1
				return savetext
			return midparsing


		else:
			tmptext = u""
			for i in range(0,len(midparsing)):
				if midparsing[i]!=u"~":
					tmptext+=midparsing[i]

			if self.__is_number(tmptext):
				#이미 범위값인경우
				return midparsing
			else:
				#초반, 중반, 후반 파싱해야하는 경우
				before=u""
				after=u""
				flag = False
				for i in range(0,len(midparsing)):
					if midparsing[i]!=u"~":
						if flag == False:
							before+=midparsing[i]
						else:
							after+=midparsing[i]
					else:
						flag = True
				finaltext = u""
				if self.__is_number(before):
					finaltext+=before
				else:
					cjhlist=[u"초반",u"중반",u"후반"]
					first_flag = False
					for i in range(0,len(cjhlist)):
						j = len(cjhlist[i])-1
						numarea = u""
						k = 0
						while k<len(before)-j:
							ttmptext = u""
							for m in range(0,j+1):
								ttmptext+=before[k+m]

							if ttmptext!=cjhlist[i]:
								numarea+=before[k]
							else:
								if self.__is_number(numarea):
									if cjhlist[i]==u"초반":
										start = (int(numarea)/10)*10
									elif cjhlist[i]==u"중반":
										start = ((int(numarea)/10)*10)+3
									else:
										start = ((int(numarea)/10)*10)+7
									finaltext+=unicode(start)
									first_flag=True
									break						
							k+=1
					if first_flag==False:
						return finaltext

				finaltext+=u"~"

				if self.__is_number(after):
					finaltext+=after
					return finaltext
				else:
					cjhlist=[u"초반",u"중반",u"후반"]
					second_flag = False
					for i in range(0,len(cjhlist)):
						j = len(cjhlist[i])-1
						numarea = u""
						k = 0
						while k<len(after)-j:
							ttmptext = u""
							for m in range(0,j+1):
								ttmptext+=after[k+m]

							if ttmptext!=cjhlist[i]:
								numarea+=after[k]
							else:
								if self.__is_number(numarea):
									if cjhlist[i]==u"초반":
										end = ((int(numarea)/10)*10)+3
									elif cjhlist[i]==u"중반":
										end = ((int(numarea)/10)*10)+7
									else:
										end = ((int(numarea)/10)*10)+9
									finaltext+=unicode(end)
									return finaltext
							k+=1

					return u""
				return u""
			return u""	
		return u""

	def __is_number(self,s):
	    try:
	        float(s)
	        return True
	    except ValueError:
	        return False