# coding: utf8
#
def index():
    #Redireciona para a pagina inicial do usuario
    switch(session.perfilUser)

    return dict(message="hello from autenticacao.py")

############## FUNCIONALIDADE DE LOGIN######################################
def login():

    form=FORM('Login:', INPUT(_name='email'), 'Senha', INPUT(_name="senha",_type="password"), INPUT(_type='submit'))

    email = request.vars['email']
    senha = request.vars['senha']
    #if request.post_vars:
    if request.env.request_method == 'POST':
        myquery = (db.tb_usuario.email == email)&(db.tb_usuario.senha == senha)&(db.tb_usuario.ativo == 1)
        myset = db(myquery)
        rows = myset.select()
        if len(rows) == 1:
            response.flash = "Bem vindo ao sistema"
            #redirect(URL('usuario','criarUsuario'))

            #envio de email

            #isset(session.perfilUser)
            row = rows[0]

            #Seta a Session para ser segura
            #session.secure()
            #Armazena o Nome do Perifl do User
            perfil_current_user = db(db.tb_perfil.id_perfil == row('tb_usuario.fk_id_perfil')).select(db.tb_perfil.ALL)
            session.perfilUser = perfil_current_user.first()
            #Armazena os Perfiis dos Usuarios
            session.SetPerfis = db().select(db.tb_perfil.ALL)
            
            session.id_user = row('tb_usuario.id_usuario')
                       
            
            response.flash =  session.SetPerfis[0](db.tb_perfil.nome)
            session.idpai = session.id_user
            
            index()
            

        else:
            response.flash = "Login inválido"


    return dict(form = form)


#Implentacao  do switch
def switch(x):
    try:
        switch_dict[x]()
    except:
        case_default()


#definicao dos cases
def case_1():
    redirect(URL("responsavel","alterar"))
def case_2():
    redirect(URL("administrador","index"))
def case_3():
    redirect(URL("professor","index"))
def case_default():
    redirect(URL('responsavel','alterar'))


#Dicionario do Switchs
switch_dict = {'Responsavel' : case_1, "Professor" : case_2, 3 : case_3}

############## FUNCIONALIDADE DE LOGOUT######################################
def logout():
    session.clear()
    redirect(URL("default","index"))
