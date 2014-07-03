# coding: utf8
# tente algo como
from applications.Genios.modules.chimpy import *

def index(): return dict(message="hello from administrador.py")

    #pagina para cadastrar professor


def cadastrar_professor():
    response.flash="Cadastro de Professor"
    form = db.teste = SQLFORM.factory(db.tb_usuario,db.ta_usuario_x_curso,fields=['nome','email','senha','ano_escolar','colegio','id_curso','semestre'])
    form.vars.fk_id_perfil= 4
    
    
    if form.process().accepted:
        id = db.tb_usuario.insert(**db.tb_usuario._filter_fields(form.vars))
        db.ta_usuario_x_curso.insert(id_usuario=id, id_curso = form.vars.id_curso, semestre = form.vars.semestre)

        response.flash=(form.vars)
        form.vars.fk_id_usuario = id
        form.vars.ativo=True
        #form.vars.tb_professor=id
        #id = db.tb_telefone.insert(numero = form.vars.numero ,fk_id_usuario= form.vars.tb_professor ,ativo= form.vars.ativo)
        response.flash='Professor Cadastrado'
        try:
            mailChimp(form.vars.email,form.vars.nome)
        except:
            response.flash=("Usuário já cadastrado!")
    
    return dict(form =form)


def mailChimp(email,nome):
    api = Connection('43ddf97a6b8a2c07de2aefce3ff161d0-us8')
    api.list_subscribe('bb403fd503',email,{'FIRST': nome, 'LAST': ''},double_optin=False)

    return
def cidades():


    setCidades =db().select(db.tb_cidade.ALL)

    #Esconde os campos das regiões
    db.tb_cidade.id_cidade.readable = False
    db.tb_cidade.ativo.readable = False

    formCidade = SQLFORM(db.tb_cidade, fields=['nome'],showid = False)

    links = [lambda row: A('Editar',_href=URL("administrador","alterar_cidade",args=[row.id_cidade]))]

    lista = SQLFORM.grid(db.tb_cidade,fields=[db.tb_cidade.nome],headers = {'tb_cidade.nome':   'Região'},
                             searchable=True,
                             sortable=True,
                             deletable=True,
                             editable=True,
                             details=False,
                             create=False,
                             links=links,
                             csv=False,
                             formstyle="table3cols")

    #for forms in setCidades:
        #lista.append( SQLFORM.grid(db.tb_cidade,searchable=True,sortable=False,deletable=False,editable=False,details=False,create=False,csv=False))


    if formCidade.process().accepted:
        response.flash = "Regiao criada"

    return dict(form = formCidade, lista =  lista)



def alterar_cidade():
    form = SQLFORM(db.tb_cidade,request.args(0), fields=['nome'],showid=False)
    if form.process().accepted:
        response.flash ="Alterado"

    return dict(form= form)


def cadastrarmateria():

    #Esconde os campos das regiões
    db.tb_materia.id_materia.readable = False
    db.tb_materia.ativo.readable = False

    formMateria = SQLFORM(db.tb_materia, fields=['nome'],showid = False)
    links = [lambda row: A('Editar',_href=URL("administrador","alterar_materia",args=[row.id_materia]))]

    lista = SQLFORM.grid(db.tb_materia,fields=[db.tb_materia.nome],headers = {'tb_materia.nome':   'Materia'},
                             searchable=False,
                             sortable=True,
                             deletable=True,
                             editable=True,
                             details=False,
                             create=False,
                             links=links,
                             csv=False,
                             formstyle="table3cols")

    if formMateria.process().accepted:
        response.flash = "Matéria criada"

    teste = T('teste')

    return dict(formMateria=formMateria, lista=lista)

def alterar_materia():
    form = SQLFORM(db.tb_materia,request.args(0), fields=['nome'],showid=False)
    if form.process().accepted:
        response.flash ="Alterado"

    return dict(form= form)

def cadastro_produto():
    form = SQLFORM(db.tb_produto,request.args(0),showid=False)
    if form.process().accepted:
        response.flash = "Produto cadastrado com sucesso!"

    grid = SQLFORM.grid(db.tb_produto,fields=[db.tb_produto.creditos,db.tb_produto.preco],headers = {'tb_produto.creditos':   'Creditos'},
                             searchable=False,
                             sortable=True,
                             deletable=True,
                             editable=True,
                             details=False,
                             create=False,
                             csv=False,
                             formstyle="table3cols")
    return dict(form=form, grid=grid)

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

def criar_aulas():
    
    if not session.id_user:
        redirect(URL("default","index"))
        response.flash = "Sessão Expirada, Logue-se novamente!"
    
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

def busca_usuario():
    
    query = db.tb_usuario.fk_id_perfil == 1
    grid=SQLFORM.grid(query,csv=False,details=False,fields=[db.tb_usuario.nome,db.tb_usuario.email])
    
    return dict(grid=grid)
