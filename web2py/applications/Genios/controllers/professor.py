# coding: utf8
# try something like
def index():
    
    if not session.id_user:
        redirect(URL("default","index"))
        response.flash = "Sessão Expirada, Logue-se novamente!"

    query = db.tb_usuario.id_usuario == db.ta_usuario_x_materia.id_usuario and db.tb_materia.id_materia == db.ta_usuario_x_materia.id_materia
    query2= db.tb_aula.fk_id_usuario_pai == session.id_user

    #Headers para o GRID
    headers = {'tb_aula.fk_id_usuario_aluno':"Aluno",'tb_aula.fk_id_materia':"Materia",'tb_aula.conteudo':"Conteúdo",'tb_aula.data_aula':"Data"
               ,'tb_aula.horario_inicial':"Inicio",'tb_aula.horario_final':"Final"}
    #Fields do GRID
    Fields = [db.tb_aula.fk_id_usuario_aluno,
              db.tb_aula.fk_id_materia,
              db.tb_aula.conteudo ,
              db.tb_aula.data_aula,
              db.tb_aula.horario_inicial,
              db.tb_aula.horario_final,]
    #Lengths
    lengths={'tb_aula.fk_id_usuario_aluno':20,'tb_aula.fk_id_materia':30,'tb_aula.conteudo':30,'tb_aula.data_aula':20}


    links = [lambda row:  A('Editar',_href=URL("responsavel","alterar_aula",args=[row.id_aula])),
             lambda row:  A('Excluir', _href=URL("responsavel","excluir",args=[row.id_aula]))
             ]

    #REQUEST METHOD SET POST
    request.env.request_method = 'POST'

    grid = SQLFORM.grid(query=query2,headers=headers,fields=Fields,maxtextlength=20, links=links, details=False, csv=False, _class="info-table")


    return dict(grid=grid)
