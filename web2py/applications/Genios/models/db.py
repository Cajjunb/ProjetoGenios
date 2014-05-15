db = DAL('sqlite://storage.db') # Conecta com o banco


db.define_table('pai',Field('nome'),Field('ativo','boolean'),Field('nome','text'),format = '%(nome)s')
db.define_table('filho',Field('fk_pai', 'reference pai'),Field('ativo','boolean'),Field('nome'),format = '%(nome)s')
db.define_table('pai_x_filho',Field('fk_pai','reference pai'),Field('fk_filho','reference filho') )
