# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

import RunNow

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

@auth.requires_login()
def teacher():
	problems = db().select(db.problem.ALL)
	return dict(problems = problems)

def show():
	problem = db.problem(request.args(0,cast=int))
	submissions = db(db.submission.problem_id==problem.id).select()

	if (request.args(1)):
            response.flash = request.args(1)

	return dict(problem=problem,  submissions = submissions)

def new():

	form = SQLFORM(db.problem)
	form.add_button("Back",URL(f='teacher'),_class="btn btn-primary")
	form.element('input[name=Duedate]')['_style']='width:100px'

	if form.validate():
		#form.vars.ori_file = request.vars.file.filename
		id = db.problem.insert(**dict(form.vars))
		response.flash = "Your comment posted"
		redirect (URL('teacher'))
	return dict(form=form)

def student():
	problems = db().select(db.problem.ALL)
	students = db().select(db.problem.ALL)
	return dict(problems= problems, students = students)

def desc():
	problem = db.problem(request.args(0,cast=int))
	session.this_problem = problem
	form = SQLFORM(db.submission)
	form.add_button("Back",URL(f='student'),_class="btn btn-primary")
	form.element('input[name=name]')['_style']='width:350px'
	form.element('input[name=email]')['_style']='width:350px'

	if form.validate():

            # If a prior submission is made for this problem by a student
            # don't allow a second submission. This is checked using his email
            row = db((db.submission.problem_id == problem.id) & (db.submission.email==form.vars.email)).select()
            if not row:
                response.flash = "Your comment posted"
                form.vars.problem_id = session.this_problem.id
                form.vars.status="pending"
                form.vars.originalname = request.vars.file.filename
                #form.vars.student_id = session.this_student.id
                submission_id=db.submission.insert(**dict(form.vars))

                if ( problem.Type == "Immediate" ):
                    RunNow.RunNow(problem.id, submission_id)
                redirect(URL('student'))
            else:
                response.flash = "You have already made a prior submission"

        return dict(problem=problem, form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def edit():
	"""edit an existing wiki page"""
	this_problem = db.problem(request.args(0,cast=int))
	form = SQLFORM(db.problem, this_problem).process(
	next = URL('teacher'))
	form.add_button("Back",URL(f='teacher'),_class="btn btn-primary")
	form.element('input[name=Duedate]')['_style']='width:98px'
	return dict(form=form)

def delete():
	this_problem = db.problem(request.args(0,cast=int))
	problems = db().select(db.problem.ALL)
	if(db(db.problem.id==this_problem.id).delete()):
		response.flash = T("Deleted")
		redirect(URL('teacher'))
	return dict(problems=problems)

def display():
        response.headers['Content-Type']='image/jpeg'
        img = db(db.problem.id == request.args[0]).select()[0]
        import os
        return response.stream(open(os.getcwd() + '/applications/' +request.application + '/uploads/' + img.image, 'rb'))

def mailing():
	ProblemID = request.args(0, cast=int)
	SubmissionID = request.args(1, cast=int)
	submitValue = RunNow.RunNow(ProblemID, SubmissionID)
	response.flash = submitValue
	redirect(URL('show', args=[ProblemID, submitValue]))
	return submitValue



	
