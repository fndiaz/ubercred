# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('',SPAN('Backup'),''),XML('&trade;&nbsp;'),
#                  _class="brand", _href="#")
response.title = ' '.join(
    word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'ForIP'
response.meta.description = 'Ubercred'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
#print session.auth
if session.auth == None:
    response.menu =[]
else:
    if session.auth.user.funcao == "admin":
        response.menu = [
        #(T('Empréstimos'), False, URL("initial", "emprestimo2"), []),
        (T('Movimentações'), False, URL(""), [
            (T('Todos'), False, URL("initial", "emprestimo_admin_total")),
            (T('Pendentes'), False, URL("initial", "emprestimo_admin_pen"))
        ]),
        (T('Agendamentos'), False, URL("initial", "agendamento_admin"), []),
        (T('Cadastros'), False, URL(""), [
            (T('Empresas'), False, URL("initial", "empresa")),
            (T('Status'), False, URL("initial", "status")),
            (T('Bancos'), False, URL("initial", "banco")),
            (T('Orgãos'), False, URL("initial", "orgao")),
            (T('Contrato'), False, URL("initial", "funcao"))
        ])
        ]    
    if session.auth.user.funcao == "supervisor":
        response.menu = [
        #(T('Empréstimos'), False, URL("initial", "emprestimo2"), []),
        (T('Movimentações'), False, URL(""), [
            (T('Todos'), False, URL("initial", "emprestimo2")),
            (T('Pendentes'), False, URL("initial", "emprestimo"))
        ]),
        (T('Agendamentos'), False, URL("initial", "agendamento_spv"), [])
        ]
    if session.auth.user.funcao == "agente":
        response.menu = [
            (T('Movimentação'), False, URL("initial", "form_emprestimo"), []),
            (T('Contratos'), False, URL("initial", "emprestimo_agt"), [])
        ]


DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu2 = [
        #(SPAN('Admin', _class='dropdown-toggle'), False, '#', [
        #    (T('Usuários'), False, URL('projeto', 'manager', 'users')),
        #    (T('Grupos'), False, URL('projeto', 'manager', 'groups')),
        #    (T('Membros'), False, URL('projeto', 'manager', 'membership'))
        #]),
        (SPAN('Login', _class='dropdown-toggle'), False, '#', [
        (   T('Usuários'), False, URL('initial', 'users')),
        (   T('Logout'), False, URL('user', 'logout')),
            ])
    ]
if DEVELOPMENT_MENU: _()


