# -*- coding: utf-8 -*-
#---------------------------------

import CommonProcess, InfoFindIdeal, IdealWorldCup, NameMatch, RankView

class MainProcess(object):
	"""docstring for MainProcess"""

	def __init__(self):
		self.__usergender = u""
		self.__isCommonOrder = True
		self.__commonOrder = 0
		self.__mode = 0
		self.__modeInstance=None
		self.__detailOrder = 1
		self.__isLoop = False

	def mainOrder(self,responseMessage):
		self.__isLoop = True

		while self.__isLoop == True:
			self.__isLoop = False

			if self.__isCommonOrder == True:

				dataSend = CommonProcess.orderMethod(self.__commonOrder,responseMessage,self)
				self.__commonOrder+=1

				if self.__isCommonOrder == False:

					if self.__mode==1:
						self.__modeInstance = InfoFindIdeal.InfoFindIdeal()
					elif self.__mode==2:
						self.__modeInstance = IdealWorldCup.IdealWorldCup()
					elif self.__mode==3:
						self.__modeInstance = NameMatch.NameMatch()
					else:
						self.__modeInstance = RankView.RankView()
					self.__commonOrder = 0

			if self.__isCommonOrder == False:
				dataSend = self.__modeInstance.detailProcess(self.__detailOrder,responseMessage,self)
				self.__detailOrder+=1

		return dataSend


	def setUsergender(self,gender):
		self.__usergender = gender

	def getUsergender(self):
		return self.__usergender

	def setMode(self,mode):
		self.__mode = mode

	def getMode(self):
		return self.__mode

	def setIsCommonOrder(self,iscommonorder):
		self.__isCommonOrder = iscommonorder

	def getIsCommonOrder(self):
		return self.__isCommonOrder

	def setDetailOrder(self,detailorder):
		self.__detailOrder = detailorder

	def getDetailOrder(self):
		return self.__detailOrder

	def setIsLoop(self,isloop):
		self.__isLoop = isloop

	def getIsLoop(self):
		return self.__isLoop

	def setModeInstance(self,modeinstance):
		self.__modeInstance = modeinstance

	def getModeInstance(self):
		return self.__modeInstance

		
