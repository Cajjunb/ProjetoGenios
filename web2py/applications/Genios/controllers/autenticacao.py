# coding: utf8
# tente algo como
def index(): return dict(message="hello from autenticacao.py")

def login():

    form=FORM('Login:', INPUT(_name='email'), 'Senha', INPUT(_name="senha",_type="password"), INPUT(_type='submit'))

    email = request.vars['email']
    senha = request.vars['senha']
    mensagemSistema = ''
    #if request.post_vars:
    if request.env.request_method == 'POST':
        myquery = (db.tb_usuario.email == email)&(db.tb_usuario.senha == senha)&(db.tb_usuario.ativo == 1)
        myset = db(myquery)
        rows = myset.select()
        if len(rows) > 0:
            mensagemSistema = "Bem vindo ao sistema"
            #redirect(URL('usuario','criarUsuario'))
            #envio de email
        else:
            mensagemSistema = "Login inválido"


    return dict(form = form,mensagemSistema = mensagemSistema)
