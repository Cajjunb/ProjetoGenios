# coding: utf8
# tente algo como
from  applications.Genios.modules.chimpy import *
import sys
import datetime
import time

def index():
    #Faz a autenticacao
    teste_autenticacao()
    
    query =( db.tb_usuario.id_usuario > 0 and db.tb_usuario.ativo == True)
    #try:
    #    cache.ram
    #except:
    #    cache.ram = SQLFORM.grid(query)
    #Pega as aulas marcadas
    query2 = db.tb_aula

    aulas = db(db.tb_aula).select(db.tb_aula.id_aula,db.tb_aula.fk_id_horario_livre,db.tb_aula.data_aula, db.tb_aula.ativo)

    hoje = datetime.datetime.now().date()

    aulas_desatualizadas = filter( lambda a: a.data_aula < hoje  ,aulas)

    '''grid = SQLFORM.grid(query2,
                        sortable=True,
                        deletable=True,
                        editable=True,
                        details=False,
                        _class="info-table",
                        create=False,
                        csv=False,
                        formstyle="table3cols")
'''
    resultado = []
    for aula_velha in aulas_desatualizadas:
        aula_velha.update_record(ativo=False)
    
    response.flash = resultado

    return dict(mensagem=aulas_desatualizadas)


def desmarca_aulas():
    #Faz a autenticacao
    teste_autenticacao()
    
    query =( db.tb_usuario.id_usuario > 0 and db.tb_usuario.ativo == True)
    #try:
    #    cache.ram
    #except:
    #    cache.ram = SQLFORM.grid(query)
    #Pega as aulas marcadas
    query2 = db.tb_aula

    aulas = db(db.tb_aula).select(db.tb_aula.id_aula,db.tb_aula.fk_id_horario_livre,db.tb_aula.data_aula)

    hoje = datetime.datetime.now().date()

    aulas_desatualizadas = filter( lambda a: a.data_aula >= hoje  ,aulas)

    '''grid = SQLFORM.grid(query2,
                        sortable=True,
                        deletable=True,
                        editable=True,
                        details=False,
                        _class="info-table",
                        create=False,
                        csv=False,
                        formstyle="table3cols")
'''
    response.flash = aulas_desatualizadas

    return dict(mensagem=aulas_desatualizadas)



#pagina para cadastrar professor
def cadastrar_professor():
    #Faz a autenticacao
    teste_autenticacao()
    
    response.flash="Cadastro de Professor"
    form = db.teste = SQLFORM.factory(db.tb_usuario,db.ta_usuario_x_curso,
                                      fields=['nome','fk_id_perfil','email','senha','ano_escolar','colegio','fk_id_curso','semestre'])
    #form.vars.fk_id_perfil= 4


    if form.process().accepted:
        id = db.tb_professor.insert(**db.tb_professor._filter_fields(form.vars))
        response.flash=(form.vars)
        form.vars.fk_id_usuario = id
        form.vars.ativo=true
        form.vars.tb_professor=id
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
    #Faz a autenticacao
    teste_autenticacao()

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
    #Faz a autenticacao
    teste_autenticacao()
    
    form = SQLFORM(db.tb_cidade,request.args(0), fields=['nome'],showid=False)
    if form.process().accepted:
        response.flash ="Alterado"

    return dict(form= form)


def cadastrarmateria():
    #Faz a autenticacao
    teste_autenticacao()
    
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
    #Faz a autenticacao
    teste_autenticacao()
    
    form = SQLFORM(db.tb_materia,request.args(0), fields=['nome'],showid=False)
    if form.process().accepted:
        response.flash ="Alterado"

    return dict(form= form)

def cadastro_produto():
    #Faz a autenticacao
    teste_autenticacao()

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


def teste_autenticacao():
    try:
        if filter( lambda a: a.id_perfil == session.perfilUser.id_perfil and  a.nome == "Administrador", session.SetPerfis):
            if not session.id_user:
                response.flash = "Sessão Expirada, Logue-se novamente!"
                redirect(URL("default","index"))
            else:
                return True
        else:
            response.flash = "Voce não tem permissão para acessar essa area!"
            redirect(URL("default","index"))
    except:
        response.flash = "Erro na sua autenticação! Logue-se novamente!"
        redirect(URL("default","index"))
