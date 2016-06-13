# coding: utf-8

import os, re, mysql.connector, argparse, smtplib, socket, subprocess

from email.mime.text import MIMEText

class MysqlUp :

	__mysql_down = "mysql_down"

	def __init__(self) :
		self.__myPath = os.path.expanduser('~')

	def __getMysqlRootPassword(self) :
		mysqlConfFile = self.__myPath+"/.my.cnf"
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

	def __mysqlConnect(self) :
		mysqlRootPassword = self.__getMysqlRootPassword()
		try :
			mysql.connector.connect(host="localhost",user="root",password=mysqlRootPassword)
			return True
		except mysql.connector.errors.InterfaceError :
			return False

	def __sendAlert(self,subject,email,emailBcc) :
		msg = MIMEText("")
		msg['Subject'] = '{0} {1}'.format(subject,socket.gethostname())
		msg['From'] = email
		msg['To'] = email
		try :
			s = smtplib.SMTP('localhost')
			s.sendmail(email, [email] + [emailBcc], msg.as_string())
			s.quit()
		except socket.error :
			print("SMTP Down")


	def run(self) :
		parser = argparse.ArgumentParser(description='Mysql Up')
		parser.add_argument('--email', metavar='', type=str, help='Email where to send alert')
		parser.add_argument('--emailBcc', metavar='', type=str, help='Email where to send alert')
		parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity')
		args = parser.parse_args()

		if self.__mysqlConnect() :
			if os.path.isfile(MysqlUp.__mysql_down) :
				os.remove(MysqlUp.__mysql_down)
				if args.email :
					self.__sendAlert("Mysql Up",args.email,args.emailBcc)
			if args.verbose > 0 :
				print("Mysql Up")
		else :
			if not os.path.isfile(MysqlUp.__mysql_down) :
				file = open(MysqlUp.__mysql_down, 'w+')
				file.close()
				if args.email :
					self.__sendAlert("Mysql Down",args.email,args.emailBcc)
			if args.verbose > 0 :
				print("Mysql Down\nRestarting")
			subprocess.call("service mysql stop")
			subprocess.call("service mysql start")


if __name__ == "__main__":

	newHost = MysqlUp()
	newHost.run()