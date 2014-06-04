'''
db = DAL('mysql://root:Ca_784595@localhost/mydb',migrate=False,lazy_tables=True) # Conecta com o banco

db.define_table('tb_perfil',
                Field('nome', length=128, default=''),
                Field('ativo','boolean'),
                redefine=False
                )

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


db.define_table('tb_usuario',

                Field('nome', length=128, default=''),
                Field('email', length=128, default=''),
                Field('senha', 'password', length=512, readable=False),
                Field('numero_filhos', 'integer'),
                Field('ano_escolar', 'integer'),
                Field('colegio', length=128, default=''),
                Field('ativo','boolean'),
                Field('fk_id_perfil','reference tb_perfil'),
                redefine=False,
                format = '%(nome)s'
                )

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
                Field('fk_id_estado','reference tb_estado'),
                Field('nome', length=128, default=''),
                Field('ativo','boolean')
                )

db.define_table('tb_endereco',
                Field('fk_id_cidade','reference tb_cidade'),
                Field('fk_id_usuario','reference tb_usuario'),
                Field('endereco', length=200, default=''),
                Field('complemento', length=200, default=''),
                Field('cep'),
                Field('ativo','boolean')
                )

db.define_table('tb_telefone',
                Field('telefone', 'integer'),
                Field('fk_id_professor','reference tb_professor'),
                Field('ativo','boolean')
                )

db.define_table('tb_curso',
                Field('nome', length=200, default=''),
                Field('ativo','boolean')
                )

db.define_table('ta_usuario_x_curso',
                Field('fk_id_usuario','reference tb_usuario'),
                Field('fk_id_curso','reference tb_curso'),
                Field('semestre', 'integer'),
                Field('ativo','boolean')
                )

db.define_table('tb_materia',
                Field('nome', length=200, default=''),
                Field('ativo','boolean')
                )
db.define_table('ta_usuario_x_materia',
                Field('fk_id_usuario','reference tb_usuario'),
                Field('fk_id_materia','reference tb_materia'),
                Field('ativo','boolean')
                )

db.define_table('tb_horario_livre',
                Field('fk_id_usuario','reference tb_usuario'),
                Field('horario_inicial', 'time'),
                Field('horario_final', 'time'),
                Field('data_horario_livre', 'date', requires=IS_DATE('%m/%d/%Y')),
                Field('ativo','boolean')
                )
'''
