import pprint
import datetime
import time
import sys

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

    #Faz a autenticacao
    teste_autenticacao()

    query = db.tb_usuario.id_usuario == db.ta_usuario_x_materia.id_usuario and db.tb_materia.id_materia == db.ta_usuario_x_materia.id_materia
    query2= db.tb_aula.fk_id_usuario_pai == session.id_user and db.tb_aula.ativo == True

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

    #REQUEST METHOD SET POST
    request.env.request_method = 'POST'

    links = [lambda row:  A('Editar',_href=URL("responsavel","alterar_aula",args=[row.id_aula]) ),
             lambda row:   A('Excluir', _href=URL("responsavel","desmarcar_aula",args=[row.id_aula]))
             ]

    link = [lambda row: operator.setitem(row.id_aula, ['id_aula'], request.post_vars)]



    grid = SQLFORM.grid(query=query2,headers=headers,fields=Fields,maxtextlength=20, links=links, details=False, csv=False, _class="info-table")


    return dict(grid=grid)


########################## DESMARCAR AULA #############################################
def desmarcar_aula():
    #Faz a autenticacao
    teste_autenticacao()

    #Pegando o registro aula para dar update
    row = db( request.args(0) == db.tb_aula.id_aula).select(db.tb_aula.ALL)

    #Separo a data por ano, mes e dia
    data = str( row.first().data_aula ).split('-')

    #Crio um objeto date
    data_aula = datetime.date(int(data[0]),int(data[1]),int(data[2]))

    #Pego a data do servidor
    hoje = datetime.datetime.now().date()

    #Calculo a diferença
    deltadata =  data_aula - hoje

    #Testo se tem 24h de antecedência
    if deltadata.days > 0  and deltadata.days != 1:
        mensagem = "Tem certeza que quer cancelar?"
    else:
        mensagem = "Não é Possível cancelar a aula com menos de 24h de antecedência Entre em contato conosco para Melhor atendermos!"
    #mensagem = (row.first().data_aula )- (mensagem)


    return dict(mensagem = mensagem)


################### ALTERAÇÃO DE AULAS #########################################################################
def alterar_aula():
    #Retorna o Id do Perfil de um administrador
    id_perfil_professor = next(x for x in session.SetPerfis if x.nome == "Professor" )

    mensagem = ' '

    #try:
    #     professores_disponiveis = session.professores_subst
   # except:
        # JOIN GIGANTESCO QUE RETORNA TODOS OS ID's dos PROFESSORE QUES ESTÂO DISPONIVEIS NAQUELA HORA!
    session.professores_subst = db( ( db.tb_aula.id_aula == request.args(0)
                                       and (db.tb_aula.horario_inicial >=  db.tb_horario_livre.horario_inicial and db.tb_aula.horario_final <= db.tb_horario_livre.horario_final and db.tb_horario_livre.marcado  == False)
                                       and (db.tb_aula.fk_id_cidade == db.tb_endereco.fk_id_cidade)
                                       and (db.tb_usuario.ativo == True)
                                       and(db.tb_usuario.fk_id_perfil == id_perfil_professor )
                                       and (db.tb_usuario.id_usuario == db.tb_endereco.fk_id_usuario))
                                   ).select(db.tb_usuario.id_usuario,db.tb_usuario.nome).as_list()

    professores_disponiveis = session.professores_subst

    horarios_livres = db(  db.tb_aula.id_aula == request.args(0) and
                           (db.tb_aula.horario_inicial >=  db.tb_horario_livre.horario_inicial and
                            db.tb_aula.horario_final <= db.tb_horario_livre.horario_final and
                            db.tb_horario_livre.marcado  == False)).select(db.tb_horario_livre.id_horario_livre).as_list()



#    sys.exit(db( db.tb_aula.id_aula == request.args(0) and                (db.tb_aula.horario_inicial >=  db.tb_horario_livre.horario_inicial                 and db.tb_aula.horario_final <= db.tb_horario_livre.horario_final                 and db.tb_horario_livre.marcado  == False) and (db.tb_aula.fk_id_cidade == db.tb_endereco.fk_id_cidade)            and            (db.tb_usuario.ativo == True) and(db.tb_usuario.fk_id_perfil == id_perfil_professor ) and          (db.tb_usuario.id_usuario == db.tb_endereco.fk_id_usuario)
          # ))

    if professores_disponiveis is None:
        form = "Nao há Professores disponiveis para substituir o professor! Caso queira cancelar a aula utilize o link abaixo"
    else:


        #Inicializa a lista
        listaNomesProfessores = list()

        for professor in professores_disponiveis:
            listaNomesProfessores.append(professor['nome'])

        form = SQLFORM.factory(Field("Escolha Professor", "reference tb_usuario" ,
                                     requires =IS_IN_SET(listaNomesProfessores)))

    return dict(professores = professores_disponiveis, mensagem = form)


############ ALTERAÇÃO PERFIL RESPONSAVEL E FILHOS  #############################################################
def alterar():

    #Faz a autenticacao
    teste_autenticacao()


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
        
        #Manda Email
        send_mail(db(db.tb_usuario.id_usuario == session.id_user).select(db.tb_usuario.email).first().email[0],"Filho Cadastrado!",
                  "O seu filho(a) Foi Cadastado(a)!")

    #fim for
    return dict(pai=session.id_user, form = formfilho, formrel = formrel)


#############MARCAÇÃO DE AULAS  #############################################################
def marcar_aulas():

    #Faz a autenticacao
    teste_autenticacao()

    #Testa se o Endereço esta na session
    #try:
    cidadeUsuario = session.cidadeUsuario
    #except:
        #SELECIONA A CIDADE DO USUARIO


    cidadeUsuario = db((db.tb_cidade.id_cidade == db.tb_endereco.fk_id_cidade )
                           &(db.tb_cidade.ativo == True)
                           &( session.id_user == db.tb_endereco.fk_id_usuario)
                           ).select(db.tb_cidade.id_cidade)

            #cidadeUsuario = db.tb_cidade(db.tb_endereco.fk_id_usuario==session.id_user)
    session.cidadeUsuario = cidadeUsuario

    cidadeUsuario = session.cidadeUsuario

    #SELECIONA PROFESSOR QUE ATUA NA REGIAO

    professorCidadeIgual = db((cidadeUsuario.first().id_cidade == db.tb_endereco.fk_id_cidade) &
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
                                    db.tb_horario_livre.fk_id_dia_semana,
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

##################### MARCAÇÂO DE AULAS  #############################################################
def criar_aula():
    #Faz a autenticacao
    teste_autenticacao()

    #Form
    form = SQLFORM(db.tb_aula,fields=['fk_id_materia','fk_id_usuario_aluno','data_aula','conteudo'], showid=False)

    row = db( request.args[0] == db.tb_horario_livre.id_horario_livre).select(db.tb_horario_livre.ALL)

    #PREPOPULA O FORMULARIO
    form.vars.fk_id_usuario_pai = session.id_user
    form.vars.horario_inicial = row.first().horario_inicial
    form.vars.horario_final = row.first().horario_final
    form.vars.data_aula = row.first().data_horario_livre
    form.vars.fk_id_usuario_professor = row.first().fk_id_usuario
    form.vars.fk_id_cidade = session.cidadeUsuario.first().id_cidade

    if form.process().accepted:
        response.flash = " Marcada a aula"
        #Update no horario!
        row.first().marcado = True
        row.first().update_record()


    return dict(form=form)




def download():
    return response.render()


def download2():
    table = SQLTABLE(rows)

    return dict(table=table)

def teste():
    return dict(paypal_id='leandroferreira@cjr.org.br')

############################# AUTENTICACAO USUARIO ##################################################
def teste_autenticacao():
    try:
        if filter( lambda a: a.id_perfil == session.perfilUser.id_perfil and  a.nome == "Responsavel", session.SetPerfis):
            if not session.id_user:
                response.flash = "Sessão Expirada, Logue-se novamente!"
                #LIMPA A SESSION
                session.clear()
                redirect(URL("default","index"))
            else:
                return True
        else:
            response.flash = "Voce não tem permissão para acessar essa area!"
            session.clear()
            redirect(URL("default","index"))
    except:
        response.flash = "Erro na sua autenticação! Logue-se novamente!"
        #LIMPA A SESSION
        session.clear()
        redirect(URL("default","index"))

        
def send_mail(email, subject ,mensagem):
    mail.send(to=[email],
          subject=subject,
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to='naoResponda@gmail.com',
          message=mensagem)
