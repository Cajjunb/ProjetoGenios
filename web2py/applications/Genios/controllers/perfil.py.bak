# coding: utf8
# tente algo como
def index(): return dict(message="hello from perfil.py")

def criarPerfil():
    form = SQLFORM(db.tb_perfil)
    if form.process().accepted:
        response.flash = "Perfil salvo com sucesso"
    return dict(formulario = form)
