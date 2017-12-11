# -*- coding: utf-8 -*-
#---------------------------------

import Create_ResponseMsg, DatabaseConnection
import Hangulpy

class NameMatch(object):

	def __init__(self):
		self.__username = u""
		self.__idealname = u""
		self.__namelist = []
		self.__countlist = []
		self.__DBinstance = DatabaseConnection.DatabaseConnection()
		self.__chosung_list= [
		u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ',
		u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ',
		u'ㅃ', u'ㅅ', u'ㅆ', u'ㅇ',
		u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ',
		u'ㅌ', u'ㅍ', u'ㅎ']
		self.__jungsung_list = [
		u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ',
		u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ',
		u'ㅗ', u'ㅘ', u'ㅙ', u'ㅚ',
		u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ',
		u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ',
		u'ㅣ']
		self.__jongsung_list = [
		u'', u'ㄱ', u'ㄲ', u'ㄳ',
		u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ',
		u'ㄹ', u'ㄺ', u'ㄻ', u'ㄼ',
		u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ',
		u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ',
		u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ',
		u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ']
		self.__chosung_count= [2,4,2,3,6,5,4,4,8,2,4,1,3,6,4,3,4,4,3]
		self.__jungsung_count = [2,3,3,4,2,3,3,4,2,4,5,3,3,2,4,5,3,3,1,2,1]
		self.__jongsung_count = [0,2,4,4,2,5,3,3,5,7,9,9,7,9,9,8,4,4,6,2,4,1,3,4,3,4,4,3]

	def detailProcess(self,order,responseMessage,instanceVar):
		if order==1:
			return self.__usernameMsg()
		elif order==2:
			return self.__idealnameMsg(responseMessage)
		elif order==3:
			return self.__resultMsg(responseMessage)
		else:
			return self.__whereGo(responseMessage,instanceVar)


	def __usernameMsg(self):
		return Create_ResponseMsg.create_message("본인의 이름을 입력해주세요.")

	def __idealnameMsg(self,responseMessage):
		self.__username=responseMessage
		return Create_ResponseMsg.create_message("이상형의 이름을 입력해주세요.")

	def __resultMsg(self,responseMessage):

		self.__idealname=responseMessage
		if self.__ismatchPossible()==False:
			return Create_ResponseMsg.create_btnmessage("궁합을 볼수 없는 조합입니다.",["처음으로 돌아가기","다른 조합 작성하기"])
		else:
			return self.__calcPercents() 

	def __whereGo(self,responseMessage,instanceVar):
		if responseMessage == u"처음으로 돌아가기":
			instanceVar.setIsLoop(True)
			instanceVar.setIsCommonOrder(True)
			instanceVar.setDetailOrder(0)
			instanceVar.setModeInstance(None)
		else:
			instanceVar.setDetailOrder(0)
			instanceVar.setModeInstance(NameMatch())
			instanceVar.setIsLoop(True)

		return None

	def __ismatchPossible(self):
		if abs(len(self.__username)-len(self.__idealname))>1:
			return False
		else:
			return True

	def __calcPercents(self):
		string = ""
		if len(self.__username)>=len(self.__idealname):
			for i in range(0,len(self.__username)):
				self.__namelist.append(self.__username[i])
			j=0
			for i in range(0,len(self.__idealname)):
				self.__namelist.insert(2*j+1,self.__idealname[j])
				j+=1
		else:
			for i in range(0,len(self.__idealname)):
				self.__namelist.append(self.__idealname[i])
			j=0
			for i in range(0,len(self.__username)):
				self.__namelist.insert(2*j+1,self.__username[j])
				j+=1

		for i in range(0,len(self.__namelist)):
			tmplist = Hangulpy.decompose(self.__namelist[i])
			a = self.__chosung_count[self.__chosung_list.index(tmplist[0])]
			b = self.__jungsung_count[self.__jungsung_list.index(tmplist[1])]
			c = self.__jongsung_count[self.__jongsung_list.index(tmplist[2])]
			self.__countlist.append(a+b+c)
			string+=self.__namelist[i]+" "

		string+="\n"

		i=0
		loopcount = len(self.__countlist)-1
		while i<loopcount:
			ttmplist = []

			for j in range(0,i):
				string+="  "

			for j in range(0,len(self.__countlist)):
				string+=str(self.__countlist[j])+"  "

			for j in range(0,len(self.__countlist)-1):
				if len(self.__countlist)!=3:
					k = (self.__countlist[j]+self.__countlist[j+1])%10
				else:
					if j==0:
						k = self.__countlist[j]+self.__countlist[j+1]
						if k!=10:
							k%=10
					else:
						k = (self.__countlist[j]+self.__countlist[j+1])%10
				ttmplist.append(k)

			string+="\n"
			if i!=loopcount-1:
				self.__countlist=ttmplist
			i+=1

		string+=self.__username+u" 님과 "+self.__idealname+u" 님의 궁합은\n"
		string+=str(self.__countlist[0])+str(self.__countlist[1])+u"% 입니다!!!!"

		self.__DBinstance.insertNameMatchRank(self.__username,self.__idealname,str(self.__countlist[0])+str(self.__countlist[1]))

		return Create_ResponseMsg.create_btnmessage(string,["처음으로 돌아가기","다른 조합 작성하기"])