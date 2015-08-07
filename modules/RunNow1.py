import time
import subprocess
import filecmp
from datetime import datetime
import datetime
import os
import tempfile
import shutil
from gluon.tools import Mail
from gluon import current

########################################### C PROGRAM  ####################################################
def cprogram():
	print "Inside C Program"
	compile_output=subprocess.call(['gcc',submissionpath,'-o','newTest'])						#compiling c program
	run_output=subprocess.call(["newTest", sampleipfile], stdin=None,stdout=resultopfile)	    #Run the c program


######################################### JAVA PROGRAM  #####################################################
def javaprogram():
	print folder
	Javafile = os.path.abspath(os.path.join(rqFolder, folder, submission.originalname)) #creating a .java file
	shutil.copyfile(submissionpath,Javafile)					 #copying into the java file
	subprocess.call(["javac",Javafile])							 #Compiling the Java file
	classfile = submission.originalname[:-5] + ".class"
	classname = submission.originalname[:-5]
	classpath = os.path.dirname(os.path.abspath(os.path.join(rqFolder, folder, classfile)))
	classfile1 = os.path.abspath(os.path.join(rqFolder, folder, classfile))
	x=subprocess.call(["java","-cp",classpath,classname,sampleipfile],stdout=resultopfile)    #Run the .class file

	#removing copied Java file, .class file
	print classfile1
	#x=os.remove(classpath)
	os.remove(Javafile)

#######################################   PYTHON PROGRAM  #######################################################
def pythonprogram():
	subprocess.call(['python',submissionpath,sampleipfile],stdout=resultopfile)

def RunNow(ProblemID, SubmissionID):

	db = current.db
	request = current.request
	mail = current.mail

	global folder
	folder = 'uploads'
	global rqFolder
	rqFolder = request.folder
	global submission= SubmissionID

	print "I have been started"
	problem = db(db.problem.id == ProblemID).select().first()
	submission = db((db.submission.problem_id == ProblemID) & (db.submission.id == SubmissionID)).select().first()

	print "Success point 1"

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

        global submissionpath
        global sampleipfile
        global resultopfile
        submissionpath = os.path.abspath(os.path.join(rqFolder, folder, submission.file))
        sampleipfile = os.path.abspath(os.path.join(rqFolder, folder, problem.inputfile))
        resultopfile = tempfile.NamedTemporaryFile(suffix='.out',
               prefix=newfile)#Since the result opfile is temporary it will be deleted automatically once closed
        sampleopfile = open(os.path.abspath(os.path.join(rqFolder,folder,problem.outputfile)),'r')
        lines = sampleopfile.readlines()
        sampleop_list = [l.strip() for l in lines if l.strip()]

        options = { 'gcc':cprogram,
                                'java':javaprogram,
                                'python':pythonprogram
                                }
        options[compiler]()

        resultopfile.seek(0)
        lines = resultopfile.readlines()
        resultopfile.close()
        resultop_list = [l.strip() for l in lines if l.strip()]
        #print sampleop_list
        #print resultop_list

        if cmp(sampleop_list,resultop_list)== 0:
                #submissionstatus = "correct"
                submitValue = "correct"
                submission.update_record(status="correct")
        else:
                #submissionstatus = "incorrect"
                submitValue = "incorrect"
                submission.update_record(status="incorrect")

        print submitValue

        mailmessage = "Hello "+submission.name+",\n\n\t Your "+problem.title+" submission is "+submission.status+"\n\nThanks,\nDropbox Team"
        if mail.send(to = submission.email,
                                subject = problem.title+" grading",
                                message = mailmessage):
                print 'sent'
        else:
                print 'failed'

	return submitValue
