import time
def index():
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
        aula_velha.update_record(ativo=True)
    
    response.flash = resultado

    return dict(mensagem=aulas_desatualizadas)