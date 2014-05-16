# coding: utf8
# try something like
# ENUMERATIONS
ESCREVE_FILHO = 0
ALTERA_FILHO  = 1
DELETA_FILHO  = 2
ALTERA_RESPONSAVEL = 3
NULLOP = 4


#Controller da pagina inicial do Responsavel
def index():
    db.pai_x_filho.fk_filho.writable= False
    form2 = SQLFORM(db.pai_x_filho,fields=["fk_pai"],showid=False)
    if(form2.validate()):
        session.idpai=form2.vars.fk_pai
        session.op = NULLOP
        redirect(URL('responsavel','alterar'))
    else:
        session.idpai= 0
    return dict(form=form2, session=session.idpai)


#Controller da pagina de perfil do responsavel
def alterar():
    # Session com a info do pai foi setada?
    if not session.idpai : # Falta uma condicao aqui! if not session.op
         redirect(URL('responsavel','index'))

    #Pegando form do pai
    formpai = SQLFORM(db.pai,session.idpai,showid=False,fields=['nome'],formstyle="divs")

    #Processa as alteracoes
    if session.op == ALTERA_FILHO and formpai.process().accepted:
        response.flash = "Alteracao Concluida!"


    #SQL query INNER JOIN
    filhosSet = db((session.idpai==db.pai_x_filho.fk_pai)& (db.filho.id==db.pai_x_filho.fk_filho))

    #Get numero de registros
    numFilhos = filhosSet.count()
    
    #Iniciam as Listas
    forms = list()
    fotos = list()

    # i = 0
    i = 0

    #loop criando os formulários referentes aos filhos
    for filhoObj in filhosSet.select():
        #Seta o formulario de acordo com a necessidade
        fotos.append(filhoObj.filho.foto)
        forms.append(SQLFORM(db.filho, filhoObj.filho, fields = ['foto','nome'], showid=False,formstyle="divs"))
        #Incrementa o i
        i += 1
    #fimfor
    
    #Get numFilhos e inicilaiza o i
    numFilhos = i
    i = 0
    
    #for de processamento dos forms
    for i in range(0,numFilhos):
        if forms[i].process().accepted:
            response.flash = "Cadastro Filho Alterado!"
    #fim for
    
    return dict(formpai=formpai,forms=forms,fotos=fotos)

def incluifilho():
    # Testa se a session foi setada
    if not session.idpai:
        redirect(URL("responsavel"))
    
    #Prepara para inserir no banco e seta a FK
    formfilho = SQLFORM(db.filho,fields=['nome','foto'], showid=False, formstyle="divs")
    formfilho.vars.fk_pai = session.idpai
    
    #Prepara para inserir o registro de relacionamento
    formrel = SQLFORM(db.pai_x_filho)
    formrel.vars.fk_pai = session.idpai
    formrel.vars.fk_filho = formfilho.vars.id
    
    #processa o for
    if formfilho.process().accepted:
        response.flash = "Filho Vinculado"
        formrel.process().accepted
    #fim for
    return dict(pai=session.idpai, form = formfilho)
