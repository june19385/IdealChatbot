#-*-coding:utf-8-*-
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

class DatabaseConnection(object):
	"""docstring for DatabaseConnection"""
	def __init__(self):
		self.__conn = mysql.connector.connect(user='fcdbadmin',password='fcdb',host='13.125.39.205',port=3306)
		self.__cursor = self.__conn.cursor()
  		self.__DB_NAME = 'FCDB'
  		self.__cursor.execute('USE {}'.format(self.__DB_NAME))

  	def __del__(self):
  		self.__cursor.close()
		self.__conn.close()

	def getDetaillist(self,main_cat_name,gender):
		returnval = []
		query=u""
		query = (u"SELECT Detail_category_name from `PersonInfo`,`Info` where PersonInfo.Person_id = Info.Person_id AND Main_category_name = '"+main_cat_name+u"' AND Gender!='"+gender+u"' GROUP BY Detail_category_name")
		self.__cursor.execute(query)
		for Detail_category_name, in self.__cursor:
		    returnval.append(Detail_category_name)
		return returnval

	def getIdeallist(self,limitnum,gender):
		returnval = []
		query=u""
		query = (u"SELECT Person_id, Name, Picture_url, Age, Height from `PersonInfo` where Gender!='"+gender+u"' order by rand() limit "+unicode(limitnum))
		self.__cursor.execute(query)
		for Person_id, Name, Picture_url, Age, Height in self.__cursor:
			tmplist=[]
			tmplist.append(Person_id)
			tmplist.append(Name)
			tmplist.append(Picture_url)
			tmplist.append(Age)
			tmplist.append(Height)
			returnval.append(tmplist)
		return returnval

	def updateCount(self,person_id):
		query=u""
		query = (u"UPDATE PersonInfo SET Count = Count + 1 where Person_id = "+unicode(person_id))
		self.__cursor.execute(query)
		self.__conn.commit()

	def selectinfo(self, person_id):
		returnval = []
		query=u""
		query = (u"SELECT Main_category_name, Detail_category_name from `Info` where Person_id ="+unicode(person_id))
		self.__cursor.execute(query)
		for Main_category_name, Detail_category_name in self.__cursor:
			tmplist=[]
			tmplist.append(Main_category_name)
			tmplist.append(Detail_category_name)
			returnval.append(tmplist)
		return returnval

	def getInfoIdeal(self, nodelist, gender):
		querytext=u"SELECT P.Person_id AS Person_id, P.Name AS Name, P.Picture_url AS Picture_url, P.Count AS Count from `PersonInfo` AS P, `Info` AS I1, `Info` AS I2, `Info` AS I3 where "
		for i in range(len(nodelist)):
			querytext+=nodelist[i][1]+u" AND "

		querytext+=u"P.Gender != '남' AND (P.Person_id = I1.Person_id AND P.Person_id = I2.Person_id AND P.Person_id = I3.Person_id) order by P.Count DESC limit 1"
		query = (querytext)
		self.__cursor.execute(query)
		returnval=[]
		returndata = self.__cursor.fetchone()
		if returndata:
			returnval.append(returndata[0])
			returnval.append(returndata[1])
			returnval.append(returndata[2])
			returnval.append(returndata[3])

			return returnval
		else:
			return u""

	def getIdealRank(self, gender):
		returnval = []
		query=u""
		query = (u"SELECT Name, Picture_url, Count from `PersonInfo` where Gender!='"+gender+u"' order by Count DESC limit 10")
		self.__cursor.execute(query)
		for Name, Picture_url, Count in self.__cursor:
			tmplist=[]
			tmplist.append(Name)
			tmplist.append(Picture_url)
			tmplist.append(Count)
			returnval.append(tmplist)
		return returnval

	def insertNameMatchRank(self, username, idealname, score):
		query=u""
		query = (u"insert into `NameMatchScore` (Username, Idealname, Score) values ('"+username+u"','"+idealname+u"',"+unicode(score)+")")
		try:
		    self.__cursor.execute(query)
		except mysql.connector.Error as err:
		    return False
		else:
		    self.__conn.commit()

	def getNameMatchRank(self):
		returnval = []
		query=u""
		query = (u"SELECT Username, Idealname, Score from `NameMatchScore` order by Score DESC limit 10")
		self.__cursor.execute(query)
		for Username, Idealname, Score in self.__cursor:
			tmplist=[]
			tmplist.append(Username)
			tmplist.append(Idealname)
			tmplist.append(Score)
			returnval.append(tmplist)
		return returnval