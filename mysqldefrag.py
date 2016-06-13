# coding: utf-8

import time, re, os, subprocess, smtplib, socket, argparse

from email.mime.text import MIMEText

try:
	import mysql.connector
	db = "mc"
except ImportError:
	try:
		import MySQLdb
		db = "mdb"
	except ImportError:
		print("Please install mysql.connector or mysqldb package")
		exit()

class mysqlDefrag :

	__mysqlActions = ("CHECK","ANALYZE","OPTIMIZE","REPAIR")
	__typeDataBase = ("MyISAM","InnoDB")
	__excludeDatabase = ("information_schema","performance_schema")
	__returnResponse = ("Table is already up to date","OK")

	def __init__(self) :
		mysqlRootPassword = self.__getMysqlRootPassword()
		if db == "mc" :
			self.__mysqlInstance = mysql.connector.connect(host="localhost",user="root",password=mysqlRootPassword)
		else :
			self.__mysqlInstance = MySQLdb.connect(host="localhost",user="root",passwd=mysqlRootPassword)
		self.__logging = False
		self.__logShort = ""
		self.__logLong = ""
		self.__tableError = False
		self.__verbose = 0

	def __del__(self):
		try :
			self.__mysqlInstance.close()
		except :
			pass

	def __getMysqlRootPassword(self) :
		mysqlConfFile = os.path.expanduser('~')+"/.my.cnf"
		file = open(mysqlConfFile, 'r')
		content = file.read()
		file.close()
		try :
			return(re.findall('password=(.*)', content)[0])
		except IndexError :
			print("""Please enter mysql root password in {0} file.
Example :
[client]
password=p4ssw0rD
Protect this file
chmod 600 {0}""".format(mysqlConfFile))
			exit()

	def __actionOnDataBase(self,dataBase) :
		if db == "mc" :
			self.__mysqlInstance.database="`{0}`".format(dataBase)
		else :
			self.__mysqlInstance.select_db(dataBase)

		logHeader  = "\n----------------------------------\n"
		logHeader += "DataBase : `{0}`\n".format(dataBase)
		logShort = ""

		for action in mysqlDefrag.__mysqlActions :
			ok, ko = 0, 0
			logLong, logError = "", ""
			start = time.time()
			if db == "mc" :
				cursor = self.__mysqlInstance.cursor(buffered=True)
			else :
				cursor = self.__mysqlInstance.cursor()
			cursor.execute("SHOW TABLE STATUS FROM `{0}` WHERE ENGINE IN ('{1}')".format(dataBase,"','".join(mysqlDefrag.__typeDataBase)))
			for tables in cursor.fetchall() :
				table, engine = tables[0], tables[1]
				if engine == "InnoDB" and action == "REPAIR" :
					continue
				elif engine == "InnoDB" and action == "OPTIMIZE" :
					cursor.execute("ALTER TABLE `{0}` ENGINE = InnoDB;".format(table))
					if self.__logging :
						logLong += "ALTER TABLE `{0}` {1}\n".format(table,engine)
				else :
					cursor.execute("{0} TABLE `{1}`".format(action,table))
					row = cursor.fetchone()
					returnResponse = "{0} `{1}` {2} {3}\n".format(action,table,engine,row[3])
					if self.__logging :
						logLong += returnResponse
					if (row[3] in mysqlDefrag.__returnResponse) :
						ok+=1
					else :
						ko+=1
						logError += returnResponse

			logTemp = "{0} {1} in {2} seconds\n".format(ok,action,"{0:.3f}".format(time.time()-start))
			if ko > 0 :
				logTemp += "{0} tables with errors\n".format(ko)
				logTemp += logError
				self.__tableError = True

			logShort += logTemp

			if self.__logging :
				self.__logLong += logHeader
				self.__logLong += logTemp+"\n"
				self.__logLong += logLong
				self.__logLong += "----------------------------------\n"

		self.__logShort += logHeader
		self.__logShort += logShort
		self.__logShort += "----------------------------------\n"

		if self.__verbose == 1 :
			print(self.__logShort)
		elif self.__verbose > 1 :
			print(self.__logLong)



	def __notificationMail(self,email,log) :
		error = ""
		if self.__tableError :
			error = "Error"
		msg = MIMEText(log)
		msg['Subject'] = 'MysqlDefrag {0} {1}'.format(socket.gethostname(),error)
		msg['From'] = email
		msg['To'] = email
		s = smtplib.SMTP('localhost')
		s.sendmail(email, [email], msg.as_string())
		s.quit()

	def __mysqlDump(self,dataBase) :
		option = ""
		if dataBase == "mysql" :
			option = " --ignore-table=mysql.event "
		subprocess.call("mysqldump -c -u root {0}{1} > {2}.sql".format(option,dataBase,self.__dumpPath+dataBase))

	def run(self) :
		parser = argparse.ArgumentParser(description='Mysql Defragmentation')
		parser.add_argument('--email', metavar='', type=str, help='Email where to send report')
		parser.add_argument('--dumppath', metavar='', type=str, help='Mysql dump path')
		parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity (add several to increase)')
		args = parser.parse_args()

		if args.dumppath :
			self.__dumpPath = args.dumppath
		if args.verbose > 0 :
			self.__verbose = args.verbose
			if args.verbose > 1 :
				self.__logging = True

		self.__cursor = self.__mysqlInstance.cursor()
		self.__cursor.execute("SHOW DATABASES")
		for dataBases in self.__cursor.fetchall() :
			dataBase = dataBases[0]
			if (dataBase in mysqlDefrag.__excludeDatabase) == False :
				self.__actionOnDataBase(dataBase)
				if args.dumppath :
					self.__mysqlDump(dataBase)
		if args.email :
			self.__notificationMail(args.email,self.__logShort)


if __name__ == "__main__":

	myDefrag = mysqlDefrag()
	myDefrag.run()
