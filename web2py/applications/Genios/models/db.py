db = DAL('mysql://root:Ca_784595@localhost/mydb',migrate=False,lazy_tables=True) # Conecta com o banco


db.define_table('pai',Field('nome'),Field('ativo','boolean'),Field('nome','text'),format = '%(nome)s')
db.define_table('filho',
                Field('fk_pai', 'reference pai'),
                Field('foto','upload', uploadfield='foto_arquivo'),
                Field('foto_arquivo','blob'),Field('ativo','boolean'),
                Field('nome'),
                Field('colegio'),
                Field('ano','integer')
                ,format = '%(nome)s')
db.define_table('pai_x_filho',Field('fk_pai','reference tb_usuario'),Field('fk_filho','reference filho') )

db.define_table('tb_perfil',
                Field('id_perfil','id'),
                Field('nome'),
                Field('ativo','boolean'),
                redefine=True,
                format = '%(nome)s')


db.define_table("tb_usuario",
                Field('id_usuario','id'),
                Field('nome'),
                Field('fk_id_perfil','reference tb_perfil'),
                Field('email'),
                Field('senha','password'),
                Field('numero_filhos','integer'),
                Field('ano_escolar','integer'),
                Field('ativo','boolean'),
                redefine=True,
                format = '%(nome)s')
