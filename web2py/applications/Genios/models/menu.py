# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

if [elem for elem in session.listPerfis if session.id_perfil == elem['id_perfil'] and elem['nome'] == "Responsavel"] is not None:
    response.menu = [
        (T('Home'), False, URL('responsavel', 'index'), []),
        (T('Perfil'), False, URL('responsavel', 'alterar'), []),
        (T('Cidades'), False, URL('administrador', 'cidades'), []),
        (T('Aulas'), False, URL('responsavel', 'marcar_aulas'), [])
    ]
elif [elem for elem in session.listPerfis if session.id_perfil == elem['id_perfil'] and elem['nome'] == "Administrador"] is not None:
    response.menu = [
        (T('Home'), False, URL('default', 'index'), []),
        (T('Responsavel'),False,URL('responsavel','index'), []),
        (T('Administrador'), False, URL('administrador', 'cadastrar_professor'), []),
        (T('Cidades'), False, URL('administrador', 'cidades'), []),
        (T('Aulas'), False, URL('responsavel', 'marcaraulas'), [])
    ]
elif [elem for elem in session.listPerfis if session.id_perfil == elem['id_perfil'] and elem['nome'] == "Professor"] is not None:
    response.menu = [
        (T('Home'), False, URL('professor', 'index'), []),
        (T('Responsavel'),False,URL('responsavel','index'), []),
        (T('Administrador'), False, URL('administrador', 'cadastrar_professor'), []),
        (T('Cidades'), False, URL('administrador', 'cidades'), []),
        (T('Aulas'), False, URL('responsavel', 'marcaraulas'), [])
    ]
