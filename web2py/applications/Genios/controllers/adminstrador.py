# coding: utf8
# tente algo como
def index(): return dict(message="hello from adminstrador.py")

#pagina para cadastrar professor

def cadastrar_professor():
    response.flash="Cadastro de Professor"
    form = db.teste = SQLFORM.factory(db.tb_professor,
                                      db.tb_telefone,
                                      fields=['nome','email','senha', 'telefone', 'instEns', 'curso', 'semestre', 'ativo'] )
    
    #Esconde os campos das regiões
    form.vars.id_cidade.readable = False
    form.vars.ativo.readable = False
    
    if form.process().accepted:
        id = db.tb_professor.insert(**db.tb_professor._filter_fields(form.vars))
        form.vars.tb_professor=id
        id = db.tb_telefone.insert(telefone = form.vars.telefone ,fk_id_professor= form.vars.tb_professor ,ativo= form.vars.ativo)
        response.flash='Professor Cadastrado'
    return dict(form =form)
