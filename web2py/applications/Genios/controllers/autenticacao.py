# coding: utf8

def index():
    #Redireciona para a pagina inicial do usuario
    
    response.flash = session.perfilUser

    if session.perfilUser == "Professor":
        case_1()
    elif session.perfiUser == "Responsavel":
        case_2()
    elif session.perfiUser == "Administrador":
        case_3()    


    return dict(message="hello from autenticacao.py")

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
            perfil_current_user = db(db.tb_perfil.id_perfil == row('tb_usuario.fk_id_perfil')).select()
            session.perfilUser = perfil_current_user[0].nome
            #Armazena os Perfiis dos Usuarios
            session.setPerfis = db().select(db.tb_perfil.ALL).as_list()
            session.listPerfis = db().select(db.tb_perfil.ALL).as_list()
            
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
    redirect(URL('responsavel','index'))


#Dicionario do Switchs
switch_dict = {'Responsavel' : case_1, "Administrador" : case_2, 'Professor' : case_3}
