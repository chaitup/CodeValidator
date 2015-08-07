import time
import subprocess
import filecmp
from datetime import datetime
import datetime
import os
import tempfile
t = datetime.date.today()
folder = 'uploads'


problems = db(db.problem.Duedate<= t-datetime.timedelta(days=1)).select()
for problem in problems:
	submissions = db(db.submission.problem_id == problem.id).select()
	for submission in submissions:
		filename = submission.file
		filename1 = filename[:-2]
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
		submissionpath = os.path.abspath(os.path.join(request.folder, folder, submission.file))
		sampleipfile = os.path.abspath(os.path.join(request.folder,folder,problem.inputfile))
		temp = tempfile.NamedTemporaryFile(suffix='.out',
                                   prefix=filename1)
		print 'temp:', temp
		print 'temp.name:', temp.name
		subprocess.call(['gcc',submissionpath,'-o','newTest'])
		subprocess.call(["newTest", sampleipfile], stdin=None,stdout=temp)
		temp.seek(0)
		lines = temp.readlines()
		resultop_list = [l.strip() for l in lines if l.strip()]
		print "resultant list is"
		print resultop_list
		temp.close()