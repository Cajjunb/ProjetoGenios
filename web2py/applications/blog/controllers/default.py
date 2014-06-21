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
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

@auth.requires_membership('manager')
def manage():
    grid = SQLFORM.smartgrid(db.image,linked_tables=['post'],editable=False)
    return dict(grid=grid)


def user():
    return dict(form=auth())
