# coding: utf8
# tente algo como
from chimpy import *

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
