# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    if not session.counter:
        session.counter = 1
    else :
        session.counter += 1
    return dict(message="OI galewras",counter=session.counter)
    
    
    
def firstpage():
    form = SQLFORM.factory(Field('nome', requires=IS_NOT_EMPTY()))
    if form.process().accepted :
        nome = form.vars.nome
        redirect(URL('secondpage',vars=dict(nome=nome)))
    return dict(form=form)

def secondpage():
    nome =  request.vars.nome or redirect(URL('firstpage'))
    return dict(nome=nome)

def images():
    images =  db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images);
