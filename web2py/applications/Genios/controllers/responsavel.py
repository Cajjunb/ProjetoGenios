# coding: utf8
# try something like

#Controller da pagina inicial do Responsavel
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


#Controller da pagina de perfil do responsavel
def alterar():
    # Session com a info do pai foi setada?
    if not session.idpai:
         redirect(URL('responsavel','index'))
    
    #SQL query INNER JOIN 
    filhosSet = db((session.idpai==db.pai_x_filho.fk_pai)& (db.filho.id==db.pai_x_filho.fk_filho))
    #Inicia a Lista
    forms = list()
    fotos = list()
    #loop criando os formulários referentes aos filhos 
    for filhoObj in filhosSet.select():
        #Seta o formulario de acordo com a necessidade
        fotos.append(filhoObj.filho.foto)
        forms.append(SQLFORM(db.filho, filhoObj.filho , fields = ['foto','nome'], showid=False,formstyle="divs"))
        
    return dict(filhos=filhosSet,forms=forms,fotos=fotos)
