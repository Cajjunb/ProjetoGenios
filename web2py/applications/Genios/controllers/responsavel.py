import pprint



# coding: utf8
# try something like
# ENUMERATIONS
ESCREVE_FILHO = 0
ALTERA_FILHO  = 1
DELETA_FILHO  = 2
ALTERA_RESPONSAVEL = 3
NULLOP = 4


############ Controller da pagina inicial do Responsavel ################

def index():

    if not session.id_user:
        redirect(URL("default","index"))
        response.flash = "Sessão Expirada, Logue-se novamente!"

    query = db.tb_usuario.id_usuario == db.ta_usuario_x_materia.id_usuario and db.tb_materia.id_materia == db.ta_usuario_x_materia.id_materia
    query2= db.tb_aula.fk_id_usuario_pai == session.id_user

    #Headers para o GRID
    headers = {'tb_aula.fk_id_usuario_aluno':"Aluno",'tb_aula.fk_id_materia':"Materia",'tb_aula.conteudo':"Conteúdo",'tb_aula.data_aula':"Data"
               ,'tb_aula.horario_inicial':"Inicio",'tb_aula.horario_final':"Final"}
    #Fields do GRID
    Fields = [db.tb_aula.fk_id_usuario_aluno,
              db.tb_aula.fk_id_materia,
              db.tb_aula.conteudo ,
              db.tb_aula.data_aula,
              db.tb_aula.horario_inicial,
              db.tb_aula.horario_final,]
    #Lengths
    lengths={'tb_aula.fk_id_usuario_aluno':20,'tb_aula.fk_id_materia':30,'tb_aula.conteudo':30,'tb_aula.data_aula':20}


    links = [lambda row:  A('Editar',_href=URL("responsavel","alterar_aula",args=[row.id_aula])),
             lambda row:  A('Excluir', _href=URL("responsavel","excluir",args=[row.id_aula]))
             ]

    #REQUEST METHOD SET POST
    request.env.request_method = 'POST'

    grid = SQLFORM.grid(query=query2,headers=headers,fields=Fields,maxtextlength=20, links=links, details=False, csv=False, _class="info-table")


    return dict(grid=grid)

##################### MARCAÇÂO DE AULAS  #############################################################
def criar_aula():
   # try:
       # if(session.perfilUser == session.SetPerfis.select(db.tb_perfil.nome =="Responsavel").nome):
            #response.flash = "Sessão Expirada"
            #redirect(URL("default","index"))
    #except:
       # redirect(URL("default","index"))
    #Form
    
    form = SQLFORM(db.tb_aula,fields=['fk_id_materia','fk_id_usuario_aluno','data_aula','conteudo'], showid=False)

    row = db( request.args[0] == db.tb_horario_livre.id_horario_livre).select(db.tb_horario_livre.ALL)
    
    #PREPOPULA O FORMULARIO
    form.vars.fk_id_usuario_pai = session.id_user
    form.vars.horario_inicial = row.first().horario_inicial
    form.vars.horario_final = row.first().horario_final
    form.vars.data_aula = row.first().data_horario_livre
    form.vars.fk_id_usuario_professor = row.first().fk_id_usuario
    
    
    if form.process().accepted:
        response.flash = " Marcada a aula"
        #Update no horario!
        row.first().marcado = True
        row.first().update_record()
    

    return dict(form=form)




############ ALTERAÇÃO PERFIL RESPONSAVEL E FILHOS  #############################################################
def alterar():
    # Session com a info do pai foi setada?
    if not session.id_user : # Falta uma condicao aqui! if not session.op
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
        formpai = SQLFORM(db.tb_usuario,session.id_user,showid=False,
                          fields=['nome','email','senha'],
                          submit_button="Alterar",
                          formstyle="divs")

        #Pegando Registro do Endereco do pai
        endereco = db.tb_endereco(db.tb_endereco.fk_id_usuario == session.id_user)

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
        filhosSet = db((session.id_user==db.tb_pai_x_filho.fk_pai)& (db.tb_filho.id==db.tb_pai_x_filho.fk_filho)&(db.tb_filho.ativo == True))

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

    if formEndereco.process().accepted:
        response.flash = "Endereço Alterado "

    #Get numFilhos e inicilaiza o i
    numFilhos = i
    i = 0

    #for de processamento dos forms
    for i in range(0,numFilhos):
        if forms[i].process().accepted:
            response.flash = "Cadastro Filho Alterado!"
    #fim for

    response.flash = session.id_user

    return dict(formpai=formpai,formEndereco = formEndereco,fotopai=fotopai,forms=forms,fotos=fotos)


##################### INCLUIR FILHOS  #############################################################
def incluifilho():
    # Testa se a session foi setada
    if not session.id_user:
        redirect(URL("default","index"))
        response.flash = "Sessão Expirada, Logue-se novamente!"


    #Prepara para inserir no banco e seta a FK
    formfilho = SQLFORM.factory(db.tb_filho,db.tb_pai_x_filho,
                                fields=['nome','colegio','foto'],
                                showid=False,
                                formstyle="divs")

    #Prepopula o form filho
    formfilho.vars.fk_pai = session.idpai
    formfilho.vars.ativo = True

    #Cria o form de relação
    formrel = SQLFORM(db.tb_pai_x_filho)

    #processa o form
    if formfilho.process().accepted:
        #Prepara para inserir o registro de relacionamento
        id_filho = db.tb_filho.insert(**db.tb_filho._filter_fields(formfilho.vars))
        response.flash = "Filho Vinculado"

        #Prepopula o formulario
        formfilho.vars.fk_pai = session.id_user
        formfilho.vars.fk_filho = id_filho


        #Insere no Banco
        db.tb_pai_x_filho.insert(**db.tb_pai_x_filho._filter_fields(formfilho.vars))

    #fim for
    return dict(pai=session.id_user, form = formfilho, formrel = formrel)


#############MARCAÇÃO DE AULAS  #############################################################
def marcar_aulas():

    if not session.id_user:
        redirect(URL("default","index"))
        response.flash = "Sessão Expirada, Logue-se novamente!"

    #Testa se o Endereço esta na session
    try:
        cidadeUsuario = db((session.id_user==db.tb_endereco.fk_id_usuario)
                           & (db.tb_cidade.id_cidade == db.tb_endereco.fk_id_cidade)
                           &(db.tb_cidade.ativo == True)).select(db.tb_cidade.id_cidade)
    except:
        #SELECIONA A CIDADE DO USUARIO
        cidadeUsuario = db(( session.id_user== db.tb_endereco.fk_id_usuario)
                           & (db.tb_endereco.fk_id_cidade == db.tb_cidade.id_cidade)
                           &(db.tb_cidade.ativo == True)).select(db.tb_cidade.id_cidade)
        #cidadeUsuario = db.tb_cidade(db.tb_endereco.fk_id_usuario==session.id_user)
        session.cidadeUsuario = cidadeUsuario


    #SELECIONA PROFESSOR QUE ATUA NA REGIAO
    professorCidadeIgual = db((cidadeUsuario.first().id == db.tb_endereco.fk_id_cidade) &
                              (db.tb_usuario.id_usuario == db.tb_endereco.fk_id_usuario ) &
                              (db.tb_usuario.ativo == True) &
                              (db.tb_usuario.fk_id_perfil == 3 )
                              ).select(db.tb_usuario.id_usuario).as_list()


    horariosLivres = []

    #for professorID in professorCidadeIgual:
    #    horariosLivres.append( db( professorID.id_usuario == db.tb_horario_livre.fk_id_usuario))


    # CRIA A PRIMEIRA PARTE da QUERY
    query = ( professorCidadeIgual[0]['id_usuario']== db.tb_horario_livre.fk_id_usuario and db.tb_horario_livre.marcado  == False )

    # CONCATENA INSTRUÇÕES PARA UMA QUERY DINAMICA
    for professorID in professorCidadeIgual:
        query = query | ( professorID['id_usuario'] == db.tb_horario_livre.fk_id_usuario and db.tb_horario_livre.marcado  == False)


    links = [lambda row: A('Editar',_href=URL("responsavel","criar_aula",args=[row.id_horario_livre]))]

    headers = {'tb_horario_livre.fk_id_usuario':   'Professor ','tb_materia.nome':   'Materia'}

    #Creating SQLFORM.GRID
    grid = SQLFORM.grid(query,searchable=True,
                            fields=[db.tb_horario_livre.fk_id_usuario,
                                    db.tb_horario_livre.horario_inicial,
                                    db.tb_horario_livre.horario_final,
                                    db.tb_horario_livre.data_horario_livre],
                             sortable=True,
                             deletable=True,
                             editable=True,
                             details=False,
                             _class="info-table",
                             create=False,
                             links=links,
                             csv=False,
                             formstyle="table3cols")

    #Headers para o GRID
    headers = {'tb_aula.fk_id_usuario_aluno':"Aluno",'tb_aula.fk_id_materia':"Materia",'tb_aula.conteudo':"Conteúdo",'tb_aula.data_aula':"Data"}
    #Fields do GRID
    #Fields = [db.tb_aula.fk_id_usuario_aluno,db.tb_aula.fk_id_materia, db.tb_aula.conteudo ,db.tb_aula.data_aula]
    #Lengths
    #lengths={'tb_aula.fk_id_usuario_aluno':20,'tb_aula.fk_id_materia':30,'tb_aula.conteudo':30,'tb_aula.data_aula':20}


    links = [lambda row:  A('Editar',_href=URL("responsavel","alterar_aula",args=[row.id_aula])),
             lambda row:  A('Excluir', _href=URL("responsavel","excluir",args=[row.id_aula]))
             ]

    #REQUEST METHOD SET POST
    request.env.request_method = 'POST'

   # grid2 = SQLFORM.grid(setCidades,maxtextlength=20, details=False, csv=False, _class="info-table")

    return dict(grid=grid)


def download():
    return response.render()
