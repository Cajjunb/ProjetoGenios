db = DAL('mysql://admin:admin@localhost/mydb',migrate=False,lazy_tables=True) # Conecta com o banco

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()



db.define_table('tb_filho',
                Field('foto','upload', uploadfield='foto_arquivo'),
                Field('foto_arquivo','blob'),Field('ativo','boolean'),
                Field('nome',requires=IS_NOT_EMPTY()),
                Field('colegio',requires=IS_NOT_EMPTY()),
                Field('ano','integer'),
                format='%(nome)s')

db.define_table('tb_pai_x_filho',Field('fk_pai','reference tb_usuario'),Field('fk_filho','reference tb_filho') )

db.define_table('tb_perfil',
                Field('id_perfil','id'),
                Field('nome','string'),
                Field('ativo','integer'),
                redefine=True,
                format = '%(nome)s')


'''db.define_table("tb_usuario",
                Field('id_usuario','id'),
                Field('nome'),
                Field('fk_id_perfil','reference tb_perfil'),
                Field('email'),
                Field('senha','password'),
                Field('numero_filhos','integer'),
                Field('ano_escolar','integer'),
                Field('ativo','boolean'),
                Field('foto_nome','upload',uploadfield='foto'),
                Field('foto','blob'),
                redefine=True,
                format = '%(nome)s')'''

db.define_table('tb_usuario',
	Field('id_usuario','id'),
	Field('fk_id_perfil','reference tb_perfil',required=True,requires=IS_IN_DB(db,db.tb_perfil.id_perfil,'%(nome)s')),
	Field('nome','string',length=80,required=True),
	Field('email','string',required=True,length=200),
	Field('senha','password',required=True,length=128),
    Field('ano_escolar','integer'),
	Field('colegio','string',length=70),
    Field('ativo','boolean'),
    redefine=True,
    format = '%(nome)s')



db.define_table('tb_operacao',
                Field('nome', length=128, default=''),
                redefine=False
                )

db.define_table('tb_erro',
                Field('excessao', 'text')
                )

db.define_table('tb_pais',
                Field('nome', length=128, default=''),
                Field('ativo','boolean')
                )

db.define_table('tb_estado',
                Field('fk_id_pais','reference tb_pais'),
                Field('nome', length=128, default=''),
                Field('ativo','boolean')
                )

db.define_table('tb_cidade',
                Field('id_cidade','id'),
                Field('nome', length=128, default=''),
                Field('ativo','boolean'),
                format= '%(nome)s'
                )

db.define_table('tb_endereco',
                Field('id_endereco','id'),
                Field('fk_id_cidade','reference tb_cidade'),
                Field('fk_id_usuario','reference tb_usuario'),
                Field('endereco', length=200, default=''),
                Field('complemento', length=200, default=''),
                Field('cep'),
                Field('ativo','boolean')
                )

db.define_table('tb_telefone',
                Field('id_telefone','id'),
                Field('numero'),
                Field('fk_id_usuario','reference tb_usuario'),
                Field('ativo','boolean')
                )

db.define_table('tb_curso',
                Field('id_curso','id'),
                Field('nome', length=200, default=''),
                Field('ativo','boolean'),
                format='%(nome)s'
                )

db.define_table('ta_usuario_x_curso',
                Field('id_usuario','reference tb_usuario'),
                Field('id_curso','reference tb_curso'),
                Field('semestre', 'integer'),
                Field('ativo','boolean')
                )

db.define_table('tb_materia',
                Field('id_materia','id'),
                Field('nome', length=200, default=''),
                Field('ativo','boolean'),
                format='%(nome)s'
                )


db.define_table('ta_usuario_x_materia',
                Field('id','id'),
                Field('id_usuario','reference tb_usuario'),
                Field('id_materia','reference tb_materia'),
                Field('ativo','boolean')
                )

# HORARIO
db.define_table('tb_horario_livre',
                Field('id_horario_livre','id'),
                Field('fk_id_usuario','reference tb_usuario'),
                Field('horario_inicial', 'time'),
                Field('horario_final', 'time'),
                Field('data_horario_livre', 'date', requires=IS_DATE('%d/%m')),
                Field('marcado', 'integer'),
                Field('ativo','integer')
                )

# PROFESSOR
db.define_table('tb_professor',
                Field('nome', length=128, default=''),
                Field('email', length=128, default=''),
                Field('senha', 'password', length=512, readable=False),
                Field('instEns', length=128, default=''),
                Field('curso', length=128, default=''),
                Field('semestre', 'integer'),
                Field('ativo','boolean'),
                Field('foto', 'upload'),
                Field('fk_id_perfil','reference tb_perfil'),
                Field('foto_nome','upload',uploadfield='foto'),
                Field('foto','blob'),
                redefine=False,
                format = '%(nome)s')

# AULAS
db.define_table('tb_aula',
                Field('id_aula','id'),
                Field('fk_id_usuario_pai','reference tb_usuario'),
                Field('fk_id_usuario_aluno','reference tb_filho'),
                Field('fk_id_usuario_professor','reference tb_usuario'),
                Field('fk_id_materia','reference tb_materia'),
                Field('horario_inicial', 'time'),
                Field('horario_final', 'time'),
                Field('data_aula','date', requires=IS_DATE('%d/%m')),
                Field('conteudo'))

#PRODUTO
db.define_table('tb_produto',
                Field('id_produto','id'),
                Field('creditos','integer'),
                Field('preco','float')
                )
