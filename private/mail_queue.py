## in file /app/private/mail_queue.py
import time
import subprocess
import filecmp
from datetime import datetime
import datetime
import sys,os
t = datetime.date.today()

problems = db(db.problem.Duedate<= t-datetime.timedelta(days=1)).select()
for problem in problems:
	submissions = db(db.submission.problem_id == problem.id).select()
	for submission in submissions:
		
		filename = submission.file
		newfile = filename[:-2]+'.out'
		newfile1 = filename[:-2]
		ofile = open('C:\\web2py\\applications\\dropbox1\\cache\\temp\\'+newfile, 'w')
		
		x=subprocess.call(["gcc","C:\\web2py\\applications\\dropbox1\\uploads\\"+submission.file,"-o","newTest"])
		#print x
		
		#rfile = open("C:\\web2py\\applications\\dropbox1\\uploads\\"+problem.inputfile,'r') --> 
		#print rfile.readlines()		
		rfile = "C:\\web2py\\applications\\dropbox1\\uploads\\"+problem.inputfile
		subprocess.call(["newTest", rfile], stdin=None,stdout=ofile)
		
		sampleoutput = problem.outputfile
		
		ofile.close()
		ofile = open('C:\\web2py\\applications\\dropbox1\\cache\\temp\\'+newfile, 'r')
		print ofile.readlines()
		if(filecmp.cmp('C:\\web2py\\applications\\dropbox1\\uploads\\'+sampleoutput,'C:\\web2py\\applications\\dropbox1\\cache\\temp\\'+newfile)):
			submission.update_record(status='bug free')
			db.commit()
		else:
			submission.update_record(status='your programs has errors')
			db.commit()
			
		#rfile.close()
		ofile.close()
		problem.update_record(status='checked')
		db.commit()

	
	
	
	
	
	##import filecmp
	##filecmp.cmp('file1','file2')