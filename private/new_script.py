import time
import subprocess
import filecmp
from datetime import datetime
import datetime
import os
import tempfile
import shutil
t = datetime.date.today()
folder = 'uploads'
problems = db(db.problem.Duedate<= t-datetime.timedelta(days=1)).select()
for problem in problems:
	submissions = db(db.submission.problem_id == problem.id and proble).select()
	for submission in submissions:
		if sumbission.status == 'pending'
			filename = submission.file
			if filename[-2:] == ".c":
				compiler = 'gcc'
				newfile = filename[:-2]
			elif filename[-3:] == ".py":
				compiler = 'python'
				newfile = filename[:-3]
			else:
				compiler = 'java'
				newfile = filename[:-5]	
			print compiler
			submissionpath = os.path.abspath(os.path.join(request.folder, folder, submission.file))
			sampleipfile = os.path.abspath(os.path.join(request.folder,folder,problem.inputfile))
			resultopfile = tempfile.NamedTemporaryFile(suffix='.out',
                               prefix=newfile)#Since the result opfile is temporary it will be deleted automatically once closed
			sampleopfile = open(os.path.abspath(os.path.join(request.folder,folder,problem.outputfile)),'r')
			lines = sampleopfile.readlines()
			sampleop_list = [l.strip() for l in lines if l.strip()]
		
			########################################### C PROGRAM  ####################################################
			def cprogram():
				compile_output=subprocess.call(['gcc',submissionpath,'-o','newTest'])						#compiling c program
				run_output=subprocess.call(["newTest", sampleipfile], stdin=None,stdout=resultopfile)	    #Run the c program
			
			
			
		######################################### JAVA PROGRAM  #####################################################
			def javaprogram():
				Javafile = os.path.abspath(os.path.join(request.folder, folder, submission.originalname)) #creating a .java file 
				shutil.copyfile(submissionpath,Javafile)					 #copying into the java file									
				subprocess.call(["javac",Javafile])							 #Compiling the Java file	
				classfile = submission.originalname[:-5] + ".class"
				classname = submission.originalname[:-5]
				classpath = os.path.dirname(os.path.abspath(os.path.join(request.folder, folder, classfile)))
				classfile1 = os.path.abspath(os.path.join(request.folder, folder, classfile))
				x=subprocess.call(["java","-cp",classpath,classname,sampleipfile],stdout=resultopfile)    #Run the .class file
			
				#removing copied Java file, .class file
				print classfile1
				#x=os.remove(classpath)
			
				os.remove(Javafile)
			
		
			#######################################   PYTHON PROGRAM  #######################################################
			def pythonprogram():
				subprocess.call(['python',submissionpath,sampleipfile],stdout=resultopfile)
			
		
			options = { 'gcc':cprogram,
					'java':javaprogram,
					'python':pythonprogram
					}
			options[compiler]()
		
			os.remove(submissionpath) 							   						#removing submission file	
			resultopfile.seek(0)
			lines = resultopfile.readlines()
			resultopfile.close()
			resultop_list = [l.strip() for l in lines if l.strip()]
			#print sampleop_list
			#print resultop_list
		
	if cmp(sampleop_list,resultop_list)== 0:
			#submissionstatus = "correct"
		print "correct"
		submission.update_record(status="correct")
	else:
			#submissionstatus = "incorrect"
		print "incorrect"
		submission.update_record(status="incorrect")
	
	mailmessage = "Hello "+submission.name+",\n\n your "+problem.title+" submission is "+submission.status+"\n\nThanks,\n\n DROPBOX TEAM"
	if mail.send(to = submission.email,
				subject = problem.title+" grading",
				message = mailmessage):
		print 'sent'
	else:
		print 'failed'
	problem.update_record(status='checked')
			

		







	


			
			
			
					
					
					
				
				
				
				
		
			