# coding: utf8
# try something like
def index():
    db.pai_x_filho.fk_filho.writable= False
    form2 = SQLFORM(db.pai_x_filho,fields=["fk_pai"])
    form = FORM(INPUT(_name="idpai",_type="text"),INPUT(_type='submit'), _action='', _method='post')
    if(form2.validate()):
        session.idpai=form2.vars.fk_pai
        redirect(URL('responsavel','alterar'))
    else:
        session.idpai= 0
    return dict(form=form2, session=session.idpai)

def alterar():
    if not session.idpai:
         redirect(URL('responsavel','index'))
    #formpai = SQLFORM(db.pai,session.idpai)
    #formfilho = SQLFORM(db.filho)
    filhosSet = db((session.idpai==db.pai_x_filho.fk_pai)& (db.filho.id==db.pai_x_filho.fk_filho))
    forms = list()
    for filhoObj in filhosSet.select():
        forms.append(SQLFORM(db.filho, filhoObj.filho ,fields=['nome']))
    if( not filhosSet):
        filhos = {"ERRO","OPPS"}
    return dict(filhos=filhosSet,forms=forms)
