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
    db.tb_pai_x_filho.fk_filho.writable= False
    form2 = SQLFORM(db.tb_pai_x_filho,fields=["fk_pai"],showid=False)

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


    #Dando um Join tb_usuario e Tb_endereco
    #enderecopai = db(session.idpai == db.tb_endereco.fk_id_usuario).select()

    #IS FORMPAI SET?
    try:
        formpai
        formEndereco
    except NameError:
        formpai = None
        forEndereco = None

    if formpai is None or formEndereco is None:

        #Pegando form do pai
        formpai = SQLFORM(db.tb_usuario,session.idpai,showid=False,
                          fields=['nome','email','senha'],
                          submit_button="Alterar",
                          formstyle="divs")

        #Pegando Registro do Endereco do pai
        endereco = db.tb_endereco(db.tb_endereco.fk_id_usuario == session.idpai)

        #Criando SQLFORM para alterar o Endereco
        formEndereco = SQLFORM(db.tb_endereco,endereco,
                               fields=['fk_id_cidade','endereco','complemento','cep'],
                               submit_button="Alterar",
                               formstyle="divs",
                               showid=False)

        fotopai = SQLFORM.factory(Field('foto','upload',default=formpai.vars.foto))

        #Processa as alteracoes
        if session.op == ALTERA_FILHO and formpai.process().accepted:
            response.flash = "Alteracao Concluida!"


        #SQL query INNER JOIN
        filhosSet = db((session.idpai==db.tb_pai_x_filho.fk_pai)& (db.tb_filho.id==db.tb_pai_x_filho.fk_filho)&(db.tb_filho.ativo == True))

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
            fotos.append(filhoObj.tb_filho.foto)
            forms.append(SQLFORM(db.tb_filho, filhoObj.tb_filho,
                                 fields = ['foto','nome','colegio','ano','ativo'],
                                 submit_button="Alterar",
                                 showid=False,
                                 formstyle="divs"))
            #Incrementa o i
            i += 1
        #fimfor

    if formpai.process().accepted:
        response.flash = "Cadastro Pai Alterado" ;

    #Get numFilhos e inicilaiza o i
    numFilhos = i
    i = 0

    #for de processamento dos forms
    for i in range(0,numFilhos):
        if forms[i].process().accepted:
            response.flash = "Cadastro Filho Alterado!"
    #fim for


    return dict(formpai=formpai,formEndereco = formEndereco,fotopai=fotopai,forms=forms,fotos=fotos)

def incluifilho():
    # Testa se a session foi setada
    if not session.idpai:
        redirect(URL("responsavel"))

    #Prepara para inserir no banco e seta a FK
    formfilho = SQLFORM.factory(db.tb_filho,db.tb_pai_x_filho,
                                fields=['nome','colegio','foto'],
                                showid=False,
                                formstyle="divs")

    formfilho.vars.fk_pai = session.idpai
    formfilho.vars.ativo = True

    formrel = SQLFORM(db.tb_pai_x_filho)

    #processa o for
    if formfilho.process().accepted:
        #Prepara para inserir o registro de relacionamento
        id_filho = db.tb_filho.insert(**db.tb_filho._filter_fields(formfilho.vars))
        response.flash = "Filho Vinculado"

        #Prepopula o formulario
        formfilho.vars.fk_pai = session.idpai
        formfilho.vars.fk_filho = id_filho

        #Insere no Banco
        db.tb_pai_x_filho.insert(**db.tb_pai_x_filho._filter_fields(formfilho.vars))

    #fim for


    return dict(pai=session.idpai, form = formfilho, formrel = formrel)


def download():
    return response.render()

def marcaraulas():
    rows = db().select(db.tb_usuario.id_usuario == db.ta_usuario_x_materia.id_usuario and db.tb_materia.id_materia == db.ta_usuario_x_materia.id_materia)
    
    table = SQLTABLE(rows)
    return dict(table=table)
