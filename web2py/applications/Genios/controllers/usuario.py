# coding: utf8
# tente algo como
def index(): return dict(message="hello from usuario.py")

def criarUsuario():

    #recupera o perfil do usuário
    perfil = request.vars['p']
    id_perfil = False
    #verifica se foi enviado um valor válido
    if perfil is not None :
        if len(perfil)>0:
            #diminui o tamanho da letra do perfil
            perfil = perfil.lower()
            #recuperando o id do perfil
            myquery = (db.tb_perfil.nome == perfil)
            myset = db(myquery)
            rows = myset.select()

            for r in rows:
                id_perfil = r.id_perfil
        else:
            #mensagemSistema = "Perfil inválido"
            redirect(URL('autenticacao', 'login'))
        #recupera o id do perfil
        #id_perfil = db.executesql("SELECT id_perfil from tb_perfil WHERE nome = \""+perfil+"\"")

        #if perfil != 'administrador' and perfil != 'professor' and perfil != 'responsavel':
            #perfil = False
    else:
        #mensagemSistema = "Informe um perfil"
        redirect(URL('autenticacao', 'login'))

    form = getFormularioUsuario(id_perfil)

    form.add_button('Voltar', URL('autenticacao', 'login'))
    #idPerfil = form.elements('input', _name='fk_id_perfil')

#    db.my_table.a_field.readable = False

    #idPerfil['_writable'] = False
    #writable=True, readable=True,

    #submit = form.element('input',_type='submit')
    #idPerfil[0] = 'readonly'
    #return dict(form=form)


    #if form.process().accepted:
        #response.flash = "Usuário salvo com sucesso"
        #enviar email para confirmação
    
    response.flash = request.vars
    return dict(formulario = form)


def getFormularioUsuario(id_perfil):

    if id_perfil != False:
        #escondendo o campo de perfil de usuário
        db.tb_usuario.fk_id_perfil.writable = False
        db.tb_usuario.fk_id_perfil.readable = False
        #gerando o formulário
        form = SQLFORM(db.tb_usuario,hidden=dict(ativo=0,fk_id_perfil=id_perfil), submit_button='Salvar')
    else:
        form = SQLFORM(db.tb_usuario,hidden=dict(ativo=0), submit_button='Salvar');

    return form
