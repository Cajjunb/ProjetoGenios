# coding: utf8
# tente algo como
def index(): return dict(message="hello from administrador.py")

#pagina para cadastrar professor


def cadastrar_professor():
    response.flash="Cadastro de Professor"
    form = db.teste = SQLFORM.factory(db.tb_professor, fields=['nome','email','senha', 'instEns', 'curso', 'semestre', 'ativo'] )
    if form.process().accepted:
        id = db.tb_professor.insert(**db.tb_professor._filter_fields(form.vars))
        form.vars.tb_professor=id
        #id = db.tb_telefone.insert(numero = form.vars.numero ,fk_id_usuario= form.vars.tb_professor ,ativo= form.vars.ativo)
        response.flash='Professor Cadastrado'
    return dict(form =form)




def cidades():

    setCidades =db().select(db.tb_cidade.ALL)

    formCidade = SQLFORM(db.tb_cidade, fields=['nome'],show_id = False)

    lista = list()

    for forms in setCidades:
        listaForms.append( SQLFORM.grid(db.tb_cidade,forms,fields=["nome"]))

        
    if formCidade.process().accepted:
        response.flash = "Regiao criada"
        
    return dict(form = formCidade, lista =  lista)
