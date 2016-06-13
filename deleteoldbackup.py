# coding: utf-8

import os, re, subprocess, shutil, argparse, smtplib, socket

from email.mime.text import MIMEText

class DeleteOldBackup :

	__saveDir = "/home/sauvegarde/"
	__minimumDiskSpace = 40

	def __getSize(self,start_path = '.'):
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(start_path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
		return float(total_size)/(1024*1024*1024)

	def __freeSpace(self) :
		df = subprocess.Popen(["df","/"], stdout=subprocess.PIPE)
		output = df.communicate()[0]
		device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
		return float(available)/(1024*1024)


	def __sendAlert(self,subject,mailContent,email,emailBcc) :
		msg = MIMEText(mailContent)
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
		parser = argparse.ArgumentParser(description='Delete old backup')
		parser.add_argument('--email', metavar='', type=str, help='Email where to send alert')
		parser.add_argument('--emailBcc', metavar='', type=str, help='Email where to send alert')
		parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity')
		args = parser.parse_args()

		delete = False
		somme = 0
		freeSpaceBefore = self.__freeSpace()
		mailBody = ""
		tmp = os.listdir(DeleteOldBackup.__saveDir)
		tmp.sort()
		for dirToDelete in tmp :
			available = self.__freeSpace()
			if available < DeleteOldBackup.__minimumDiskSpace :
				if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', dirToDelete):
					mailBody += "delete {} : {:.2f}Go\n".format(dirToDelete,self.__getSize(DeleteOldBackup.__saveDir+dirToDelete))
					shutil.rmtree(DeleteOldBackup.__saveDir+dirToDelete)
					delete = True
			else :
				break
		if(delete) :
			freeSpaceAfter = self.__freeSpace()
			mailContent = "Free space before : {:.2f}Go\n".format(freeSpaceBefore)
			mailContent += "Free space after : {:.2f}Go\n".format(freeSpaceAfter)
			mailContent += "Freed space : {:.2f}Go\n".format(freeSpaceAfter-freeSpaceBefore)
			mailContent += "---------------------\n"
			mailContent += mailBody
			if args.email :
				self.__sendAlert("Delete old backup",mailContent,args.email,args.emailBcc)
			if args.verbose > 0 :
				print(mailContent)


if __name__ == "__main__":

	newHost = DeleteOldBackup()
	newHost.run()