import time
import subprocess
import filecmp
from datetime import datetime
import datetime
import os,signal
t = datetime.date.today()
folder = 'uploads'
problems = db(db.problem.Duedate<= t-datetime.timedelta(days=1)).select()
for problem in problems:
	submissions = db(db.submission.problem_id == problem.id).select()
	for submission in submissions:
		
		filename = submission.file
		filename1 = filename[-2:]
		newfile = ""
		if filename[-2:]=='.c':
			compiler = 'gcc'
			newfile = filename[:-2]+'.out'
		elif filename[-3:]=='.py':
			compiler = 'python'
			newfile = filename[:-3]+'.out'
		else:
			compiler = 'java'
			newfile = filename[:-5]+'.out'
		pathnew = os.path.abspath(os.path.join(request.folder, folder, submission.file))
		sampleipfile = open(os.path.abspath(os.path.join(request.folder,folder,problem.inputfile)),'r')
		sampleopfile = open(os.path.abspath(os.path.join(request.folder,folder,problem.outputfile)),'r')
		resultopfile = open(os.path.abspath(os.path.join(request.folder, folder, newfile)),'w') #creating an outputfile#
		submissionstatus = "empty"
			
		############################################ C PROGRAM  ####################################################
		def cprogram():
			subprocess.call(['gcc',pathnew,'-o',"x"])
			lines = list(sampleipfile)
			
			for line in lines:
				p = subprocess.Popen(["./x"],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
				p.stdin.write('%s\n' % line)
				x = p.stdout.readline()
				print x
				resultopfile.write(x)
				resultopfile.write("\n")
				
			sampleop_list = []   ### to add lines of sample output file
			resultop_list = []   ### to add lines of result output file
			resultopfile.close()
			with open(os.path.abspath(os.path.join(request.folder,folder,problem.outputfile)),'r') as f1:
				lines = f1.readlines()
				sampleop_list = [l.strip() for l in lines if l.strip()]
			with open(os.path.abspath(os.path.join(request.folder, folder, newfile)),'r') as f2:
				lines = f2.readlines()
				resultop_list = [l.strip() for l in lines if l.strip()]
			print sampleop_list
			print resultop_list
			if cmp(sampleop_list,resultop_list)== 0:
				submissionstatus = "correct"
				submission.update_record(status=submissionstatus)
			else:
				submissionstatus = "incorrect"
				submission.update_record(status=submissionstatus)
			########################################## JAVA PROGRAM  #####################################################
		#def javaprogram():
	
			
			
		
		#######################################   PYTHON PROGRAM  #######################################################
		# def pythonprogram():
			
			
			
			
		options = { 'gcc':cprogram
				
					}
		options[compiler]()
		mailmessage = "Hello "+submission.name+",\n\n your "+problem.title+" submission is"+submission.status+"\n\nThanks,\n\n DROPBOX TEAM"
		if mail.send(to = submission.email,
					subject = problem.title+" grading",
					message = "Hello "+submission.name+",\n\n your "+problem.title+" submission is " +submission.status+"\n\nThanks,\n\n DROPBOX TEAM"):
			print 'sent'
		else:
			print 'failed'
	problem.update_record(status='checked')
	sampleipfile.close()
	sampleopfile.close()
		

			
			
			
					
					
					
				
				
				
				
		
			