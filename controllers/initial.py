# coding=UTF-8
import  json
from datetime import datetime
from pprint import pprint

@auth.requires_login()
def principal():
	func 	= session.auth.user.funcao
	id_user = session.auth.user.id
	logger.debug("usr:%s - LOGIN - ip:%s - br:%s - funcao:%s"\
		%(session.auth.user.username, request.env.remote_addr,\
		  session._user_agent['browser'], func))
	if func == "supervisor":
		auth.add_membership(1, id_user)
		redirect(URL(emprestimo2))
	if func == "agente":
		auth.add_membership(2, id_user)
		redirect(URL(form_emprestimo))
	if func == "admin":
		auth.add_membership(3, id_user)
		redirect(URL(emprestimo_admin_total))
	
	return response.render("initial/principal.html", teste=teste)

def cpf_json():
	#print request.vars
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	if session.auth.user.funcao == 'supervisor':
		if request.vars.func == "pend":
			query = (db.emprestimo.id_empresa == db.empresa.id) \
			& (db.emprestimo.estado == None)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
	if request.vars.func == "total":
			query = (db.emprestimo.id_empresa == db.empresa.id)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
	if session.auth.user.funcao == 'agente':
		query = (db.emprestimo.id_empresa == db.empresa.id) &\
				(db.emprestimo.vendedora == session.auth.user.username)\
				& (db.emprestimo.data_emp.year()==ano)\
				& (db.emprestimo.data_emp.month()==mes)
	if session.auth.user.funcao == "admin":
		if request.vars.func == "total":
			query = (db.emprestimo.data_emp.year()==ano)\
					& (db.emprestimo.data_emp.month()==mes)
		if request.vars.func == "pend":
			query = (db.emprestimo.estado == None)\
					& (db.emprestimo.data_emp.year()==ano)\
					& (db.emprestimo.data_emp.month()==mes)

	cpf = db(query).select(db.emprestimo.cpf)
	lista = []
	for dado in cpf:
		lista.append(dado.cpf)
	lista = list(set(lista))

	return response.json(lista)

def cpf_agendamento_json():
	#print ">>>"
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	if session.auth.user.funcao == 'supervisor':
		query = (db.agendamento.vendedora == db.auth_user.username)&\
				(db.auth_user.supervisor == session.auth.user.username)\
				& (db.agendamento.data_agen.year()==ano)\
				& (db.agendamento.data_agen.month()==mes)
	if session.auth.user.funcao == 'admin':
		query = (db.agendamento.data_agen.year()==ano)\
				& (db.agendamento.data_agen.month()==mes)

	cpf = db(query).select(db.agendamento.cpf)
	lista = []
	for dado in cpf:
		lista.append(dado.cpf)
	lista = list(set(lista))

	return response.json(lista)

def estados_json():
	#print request.vars
	with open('%s/applications/ubercred/views/estados.json' %(session.raiz)) as json_data:
		json_data = json.load(json_data)
		#print json_data[0]
		#for dado in json_data:
		##	print dado

	return response.json(json_data)
	#return response.render("estados.json")

def cidades_json():
	#print request.vars
	with open('%s/applications/ubercred/views/cidades.json' %(session.raiz)) as json_data:
		json_data = json.load(json_data)
		#print(json_data)

	return response.json(json_data)	
	#return response.render("cidades.json")

def user():
	#print request.args(0)
	if request.args(0) == 'login': 
		logger.debug("ip:%s - ACCESS_LOGIN_PAGE"\
		%(request.env.remote_addr))
		return response.render("login/user.html", 
										user=auth())

	if request.args(0) == 'register':
		return response.render("login/user.html", 
							user=auth.register())

	if request.args(0) == 'not_authorized':
		logger.warning("usr:%s - ACCESS_DENIED - ip:%s"\
		%(session.auth.user.username, request.env.remote_addr))

	if request.args(0) == 'profile':
		return response.render("login/user.html", 
							user=auth.profile())

	if request.args(0) == 'logout':
		logger.debug("usr:%s - LOGOUT "\
			%(session.auth.user.username))

	return response.render("login/user.html", user=auth())

##---------------------------Emepresa
@auth.requires_membership('admin')
def form_empresa():
	response.title = 'Empresa'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.empresa)
	else:
		form 	= SQLFORM(db.empresa, id_edit)

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:empresa - nome:%s"\
		%(session.auth.user.username, request.vars.nome))
		redirect(URL("empresa"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('admin')
def empresa():
	#print session
	response.title = 'empresa'
	empresa =	db(db.empresa).select(orderby=db.empresa.id)

	return response.render("initial/list_empresa.html", 
		empresa=empresa)

##---------------------------Status
@auth.requires_membership('admin')
def form_status():
	response.title = "Status"
	id_edit = request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.status)
	else:
		form 	= SQLFORM(db.status, id_edit)

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:status - nome:%s"\
		%(session.auth.user.username, request.vars.status))
		redirect(URL("status"))

	return response.render("initial/show_form.html", form=form)	

@auth.requires_membership('admin')
def status():
	response.title = 'status'
	status 	=	db(db.status).select(orderby=db.status.id)

	return response.render("initial/list_status.html", 
		status=status)

##---------------------------Funcao
@auth.requires_membership('admin')
def form_funcao():
	response.title = 'contrato'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.funcao)
	else:
		form 	= SQLFORM(db.funcao, id_edit)

	if form.process().accepted:
		redirect(URL("funcao"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('admin')
def funcao():
	#print session
	response.title = 'contrato'
	funcao =	db(db.funcao).select(orderby=db.funcao.id)

	return response.render("initial/list_funcao.html", 
		funcao=funcao)

##---------------------------Envio
@auth.requires_membership('admin')
def form_envio():
	response.title = 'Forma de Envio'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.envio)
	else:
		form 	= SQLFORM(db.envio, id_edit)

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:envio - nome:%s"\
		%(session.auth.user.username, request.vars.nome))
		redirect(URL("envio"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('admin')
def envio():
	#print session
	response.title = 'Forma de envio'
	envio =	db(db.envio).select(orderby=db.envio.id)

	return response.render("initial/list_envio.html", 
		envio=envio)

##---------------------------Banco
@auth.requires_membership('admin')
def form_banco():
	response.title = 'banco'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.banco)
	else:
		form 	= SQLFORM(db.banco, id_edit)

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:banco - nome:%s"\
		%(session.auth.user.username, request.vars.nome))
		redirect(URL("banco"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('admin')
def banco():
	#print session
	response.title = 'banco'
	banco =	db(db.banco).select(orderby=db.banco.id)

	return response.render("initial/list_banco.html", 
		banco=banco)

##---------------------------Orgao
@auth.requires_membership('admin')
def form_orgao():
	response.title = 'orgão'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.orgao)
	else:
		form 	= SQLFORM(db.orgao, id_edit)

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:orgao - nome:%s"\
		%(session.auth.user.username, request.vars.nome))
		redirect(URL("orgao"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('admin')
def orgao():
	#print session
	response.title = 'orgão'
	orgao =	db(db.orgao).select(orderby=db.orgao.id)

	return response.render("initial/list_orgao.html", 
		orgao=orgao)

##---------------------------Agendamentos
#@auth.requires_membership('admin')
def agendamento_agt():
	#print session
	response.title = 'agendamento'
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	dia = session.data_hoje.split('-')[2]
	response.alert_badge=get_count_agen()
	query = (db.agendamento.vendedora == session.auth.user.username)\
			& (db.agendamento.data_agen.year()==ano)\
			& (db.agendamento.data_agen.month()==mes)\
			& (db.agendamento.data_agen.day()==dia)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	agen =	db(query).select(limitby=(start,end))

	return response.render("initial/list_agendamento.html", agen=agen,
		end=end, paginacao="on", regis=regis, paginate=paginate, x=x)

@auth.requires(auth.has_membership('supervisor'))
def agendamento_spv():
	#print session
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	response.title = 'agendamento'
	query = (db.agendamento.vendedora == db.auth_user.username)&\
		(db.auth_user.supervisor == session.auth.user.username)\
		& (db.agendamento.data_agen.year()==ano)\
		& (db.agendamento.data_agen.month()==mes)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	agen =	db(query).select(limitby=(start,end))

	return response.render("initial/list_agendamento.html", agen=agen, 
		end=end, paginacao="on", regis=regis, paginate=paginate, x=x)

def agendamento_admin():
	#print session
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	response.title = 'agendamentos'
	query = (db.agendamento.vendedora == db.auth_user.username)\
			& (db.agendamento.data_agen.year()==ano)\
			& (db.agendamento.data_agen.month()==mes)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	agen =	db(query).select(limitby=(start,end))

	return response.render("initial/list_agendamento.html", agen=agen, 
		end=end, paginacao="on", regis=regis, paginate=paginate, x=x)

##---------------------------Emprestimo
@auth.requires_login()
def form_emprestimo():
	id_edit = request.vars['id_edit']
	#print id_edit
	#print session.auth.user
	funcao = session.auth.user.funcao
	if funcao == "agente":
		redirect(URL(form_emprestimo_agt))
	if funcao == "supervisor":
		if id_edit != None:
			redirect(URL("initial",
		"form_emprestimo_spv", vars={'id_edit':id_edit}))
		else:
			redirect(URL(form_emprestimo_spv))
	if funcao == "admin":
		if id_edit != None:
			redirect(URL("initial",
		"form_emprestimo_spv", vars={'id_edit':id_edit}))
		else:
			redirect(URL(form_emprestimo_spv))

@auth.requires_login()
def form_emprestimo_agt():
	response.title = 'formulário de cadastro'
	id_edit = request.vars['id_edit']
	date = datetime.now()
	date = date.strftime("%Y-%m-%d %I:%M:%S")
	ls_user = get_user()
	response.alert_badge=get_count_agen()
	query = (db.auth_user.id == session.auth.user.id)
	lem = db(query).select(db.auth_user.lembrete)
	lem = lem[0].lembrete

	if id_edit is None:
		form 	= SQLFORM(db.emprestimo)
	else:
		form 	= SQLFORM(db.emprestimo, id_edit)

	form_agen 	= SQLFORM(db.agendamento)

	if form.process().accepted:
		session.flash="Registro processado"
		logger.debug("usr:%s - INSERT - tabela:emprestimo - cpf:%s - nome:%s"\
		%(session.auth.user.username, request.vars.cpf, request.vars.nome))
		redirect(URL("form_emprestimo_agt")) 
	elif form.errors:
		logger.error("usr:%s - FORM_ERROR - tabela:emprestimo - req:%s"\
		%(session.auth.user.username, request.vars))
		response.flash=("Ops, algo está errado")

	if form_agen.process().accepted:
		logger.debug("usr:%s - INSERT - tabela:agendamento - cpf:%s - nome:%s"\
		%(session.auth.user.username, request.vars.cpf, request.vars.nome))
		session.flash="Registro processado"
		redirect(URL("form_emprestimo_agt")) 
	elif form_agen.errors:
		logger.error("usr:%s - FORM_ERROR - tabela:agendamento - req:%s"\
		%(session.auth.user.username, request.vars))
		response.flash=("Ops, algo está errado")
	
		
	return response.render("initial/form_emprestimo_agt.html", 
	 form_agen=form_agen, date=date, lem=lem, form=form, ls_user=ls_user)

#@auth.requires_membership('supervisor', 'admin')
def form_emprestimo_spv():
	response.title = 'Emprestimo supervisor'
	id_edit = request.vars['id_edit']
	cidade = ""
	ls_user = get_user()
	#print ls_user

	if id_edit is None:
		form 	= SQLFORM(db.emprestimo)
	else:
		form 	= SQLFORM(db.emprestimo, id_edit)
		form.element(_name='vendedora')['_readonly'] = 'readonly'
		form.element(_name='id_empresa')['_readonly'] = 'readonly'
		query = db.emprestimo.id == id_edit
		cidade = db(query).select(db.emprestimo.cidade)
		cidade = cidade[0].cidade

	if form.process().accepted:
		if (request.vars['estado'] != '') & (request.vars['banco'] != ''):
			check_situacao(request.vars['id'])
		logger.debug("usr:%s - EDIT - tabela:emprestimo - cpf:%s - id:%s"\
		%(session.auth.user.username, request.vars.cpf, id_edit))
		session.flash=("Registro processado")

		if session.auth.user.funcao == 'supervisor':
			redirect(URL("emprestimo2"))
		if session.auth.user.funcao == 'admin':
			redirect(URL("emprestimo_admin_total"))
	else:
		print request.vars
	
	return response.render("initial/form_emprestimo_spv.html", 
		cidade=cidade, id_edit=id_edit, form=form, ls_user=ls_user)

def check_situacao(id_emp):
	if db(db.situacao.id_emprestimo == id_emp).count() < 1:
		logger.debug("usr:%s - INSERT_AUTOMATICA - tabela:situacao - status:Iniciado - id_emp:%s"\
		%(session.auth.user.username, id_emp))
		date = datetime.now()
		date = date.strftime("%Y-%m-%d %I:%M:%S")
		db.situacao.insert(data_sit=date, id_emprestimo=id_emp, id_status=1)

def get_count_agen():
	# get total agendamentos
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	dia = session.data_hoje.split('-')[2]
	query = (db.agendamento.vendedora == session.auth.user.username)\
			& (db.agendamento.data_agen.year()==ano)\
			& (db.agendamento.data_agen.month()==mes)\
			& (db.agendamento.data_agen.day()==dia)
	reg=db(query).count()
	#print query
	#print reg
	return reg

def get_user():
	# get user empresa
	user = session.auth.user.username
	user_emp_id = session.auth.user.id_empresa
	query = (db.empresa.id == session.auth.user.id_empresa)
	user_emp = db(query).select(db.empresa.nome)
	ls_user=[]
	ls_user.append(user)
	ls_user.append(user_emp[0].nome)
	ls_user.append(user_emp_id)
	#print ls_user
	return ls_user

###Supervisor pendente
@auth.requires(auth.has_membership('supervisor'))
def emprestimo():
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	response.title = "contratos pendentes"
	query = (db.emprestimo.id_empresa == db.empresa.id) \
		& ((db.emprestimo.estado == None) | (db.emprestimo.banco == None))\
		& (db.emprestimo.vendedora == db.auth_user.username)\
		& (db.auth_user.supervisor == session.auth.user.username)\
		& (db.emprestimo.data_emp.year()==ano)\
		& (db.emprestimo.data_emp.month()==mes)
	
	#query =(db.emprestimo.vendedora == db.auth_user.username)
	#print db(db.auth_user.id == session.auth.user.username).select(db.auth_user.funcao)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	con = db(query).select(limitby=(start,end))
	
	return response.render("initial/list_emprestimo.html", con=con,
		end=end, paginacao="on", regis=regis, paginate=paginate, x=x)

##Supervisor total
@auth.requires(auth.has_membership('supervisor'))
def emprestimo2():
	response.title = "contratos totais"
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	query = (db.emprestimo.id_empresa == db.empresa.id)\
		& (db.emprestimo.vendedora == db.auth_user.username)\
		& (db.auth_user.supervisor == session.auth.user.username)\
		& (db.emprestimo.data_emp.year()==ano)\
		& (db.emprestimo.data_emp.month()==mes)
	soma = db(query).select(db.emprestimo.valor_total.sum())
	soma = soma[0]._extra['SUM(emprestimo.valor_total)']
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#
	if session.auth.user.meta <= 0:
		query2 = db.auth_user.supervisor == session.auth.user.username
		meta = db(query2).select(db.auth_user.meta.sum())
		meta = meta[0]._extra['SUM(auth_user.meta)']
	else:
		meta = 	session.auth.user.meta
	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=~db.emprestimo.id)
	
	return response.render("initial/list_emprestimo2.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x, soma=soma, meta=meta)

##Agente Total
def emprestimo_agt():
	response.title = "Contratos em adamento"
	response.alert_badge=get_count_agen()
	user = session.auth.user.username
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	query = (db.emprestimo.id_empresa == db.empresa.id) &\
	(db.emprestimo.vendedora == user) &\
	(db.emprestimo.data_emp.year()==ano) &\
	(db.emprestimo.data_emp.month()==mes)
	soma = db(query).select(db.emprestimo.valor_total.sum())
	soma = soma[0]._extra['SUM(emprestimo.valor_total)']
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#
	meta = session.auth.user.meta
	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=~db.emprestimo.id)
	
	return response.render("initial/list_emprestimo2.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x, soma=soma, meta=meta)

##Admin total
@auth.requires(auth.has_membership('admin'))
def emprestimo_admin_total():
	response.title = "contratos totais"
	user = session.auth.user.username
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	query = (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
	#soma = db(query).select(db.emprestimo.valor_total.sum())
	#soma = soma[0]._extra['SUM(emprestimo.valor_total)']
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=~db.emprestimo.id)
	return response.render("initial/list_emprestimo2.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x)

def emprestimo_admin_pen():
	response.title = "contratos pendentes"
	user = session.auth.user.username
	ano = session.data_hoje.split('-')[0]
	mes = session.data_hoje.split('-')[1]
	query = (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)\
			& ((db.emprestimo.estado == None) | (db.emprestimo.banco == None))
	#soma = db(query).select(db.emprestimo.valor_total.sum())
	#soma = soma[0]._extra['SUM(emprestimo.valor_total)']
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	#

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=db.emprestimo.id)
	return response.render("initial/list_emprestimo.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x)

def detalhes_emprestimo():
	response.title = "Detalhes"
	id_det = request.vars.id_det
	query=(db.emprestimo.id == id_det) & (db.emprestimo.id_empresa == db.empresa.id)\
		  & (db.orgao.id == db.emprestimo.orgao)\
		  & (db.envio.id == db.emprestimo.envio)	
	con=db(query).select()

	return response.render("initial/detalhes_emprestimo.html", con=con)

def busca_emp_pend():
	response.title = "Emprestimos pendentes"
	if session.auth.user.funcao == 'supervisor':
		query = (db.emprestimo.id_empresa == db.empresa.id) \
			& (db.emprestimo.estado == None)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.cpf == request.vars.cpf)
	if session.auth.user.funcao == 'admin':
		query = (db.emprestimo.id_empresa == db.empresa.id) \
			& (db.emprestimo.estado == None)\
			& (db.emprestimo.cpf == request.vars.cpf)

	con = db(query).select(orderby=db.emprestimo.id)
	
	return response.render("initial/list_emprestimo.html", con=con,
													paginacao='off')

def busca_emp_total():
	response.title = "Emprestimos totais"
	mes = request.vars.mes
	cpf = request.vars.cpf
	soma=""
	res_pesquisa=True
	ano = session.data_hoje.split('-')[0]
	if session.auth.user.funcao == "supervisor":
		query = (db.emprestimo.id_empresa == db.empresa.id)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.cpf == request.vars.cpf)\
			& (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
		if request.vars.mes == "":
			query = (db.emprestimo.id_empresa == db.empresa.id)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.cpf == request.vars.cpf)
		if request.vars.cpf == "":
			query = (db.emprestimo.id_empresa == db.empresa.id)\
			& (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)\
			& (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
	if session.auth.user.funcao == "agente":
		query = (db.emprestimo.id_empresa == db.empresa.id) &\
				(db.emprestimo.vendedora == session.auth.user.username)&\
				(db.emprestimo.cpf == request.vars.cpf)
		soma = db(query).select(db.emprestimo.valor_total.sum())
		soma = soma[0]._extra['SUM(emprestimo.valor_total)']
	if session.auth.user.funcao == "admin":
		query = (db.emprestimo.cpf == request.vars.cpf)\
			& (db.emprestimo.data_emp.year()==ano)\
			& (db.emprestimo.data_emp.month()==mes)
		if request.vars.mes == "":
			query = (db.emprestimo.cpf == request.vars.cpf)
		if request.vars.cpf == "":
			query = (db.emprestimo.data_emp.year()==ano)\
					& (db.emprestimo.data_emp.month()==mes)

	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1, 'mes':mes, 'cpf':cpf}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	x=1
	if regis%paginate == 0:
		x=0
	#

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=~db.emprestimo.id)
	if db(query).count() == 0:
		res_pesquisa = False
	
	return response.render("initial/list_emprestimo_busca.html", con=con, soma=soma,
		paginacao='on', end=end, regis=regis, paginate=paginate, x=x, res_pesquisa=res_pesquisa)

def busca_agendamento():
	mes = request.vars.mes
	cpf = request.vars.cpf
	ano = session.data_hoje.split('-')[0]
	res_pesquisa = True
	if session.auth.user.funcao == "supervisor":
		query = (db.agendamento.vendedora == db.auth_user.username)&\
				(db.auth_user.supervisor == session.auth.user.username)\
				& (db.agendamento.cpf == request.vars.cpf)\
				& (db.agendamento.data_agen.year()==ano)\
				& (db.agendamento.data_agen.month()==mes)
		if request.vars.mes == "":
			query = (db.agendamento.vendedora == db.auth_user.username)&\
					(db.auth_user.supervisor == session.auth.user.username)&\
					(db.agendamento.cpf == request.vars.cpf)
		if request.vars.cpf == "":
			query = (db.agendamento.vendedora == db.auth_user.username)&\
					(db.auth_user.supervisor == session.auth.user.username)\
					& (db.agendamento.data_agen.year()==ano)\
					& (db.agendamento.data_agen.month()==mes)
	if session.auth.user.funcao == "admin":
		query = (db.agendamento.vendedora == db.auth_user.username)&\
				(db.agendamento.cpf == request.vars.cpf)\
				& (db.agendamento.data_agen.year()==ano)\
				& (db.agendamento.data_agen.month()==mes)
		if request.vars.mes == "":
			query = (db.agendamento.vendedora == db.auth_user.username)&\
					(db.agendamento.cpf == request.vars.cpf)
		if request.vars.cpf == "":
			query = (db.agendamento.vendedora == db.auth_user.username)\
					& (db.agendamento.data_agen.year()==ano)\
					& (db.agendamento.data_agen.month()==mes)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1, 'mes':mes, 'cpf':cpf}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	x=1
	if regis%paginate == 0:
		x=0
	#

	agen =	db(query).select(limitby=(start,end))
	if db(query).count() == 0:
		res_pesquisa = False

	return response.render("initial/list_agendamento_busca.html", agen=agen,
		paginacao='on', end=end, regis=regis, paginate=paginate, x=x, res_pesquisa=res_pesquisa)

##---------------------------Situação
@auth.requires(auth.has_membership('supervisor') or auth.has_membership('admin'))
def form_situacao():
	response.title = 'situação'
	id_emp = request.vars.id_emp

	if id_emp is None:
		form 	= SQLFORM(db.situacao)
	else:
		query = db.emprestimo.id == id_emp
		emp =db(query).select(db.emprestimo.id, db.emprestimo.nome)
		emp = emp[0]
		form 	= SQLFORM(db.situacao)

	if form.process().accepted:
		logger.debug("usr:%s - INSERT - tabela:situacao - id_emp:%s - id_status:%s"\
		%(session.auth.user.username, id_emp, request.vars.id_status))
		session.flash=("Registro processado")
		redirect(URL("situacao?id_emp=%s" %(id_emp))) 
	else:
		print request.vars

	return response.render("initial/form_situacao.html", form=form, 
												emp=emp, id_emp=id_emp)	

@auth.requires(auth.has_membership('supervisor') or auth.has_membership('admin'))
def situacao():
	#print request.vars.id_emp
	id_emp = request.vars.id_emp
	response.title = "Situação"
	query = (db.situacao.id_emprestimo == db.emprestimo.id) &\
	(db.situacao.id_status == db.status.id) & (db.situacao.id_emprestimo == id_emp)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1, 'id_emp':id_emp}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	x=1
	if regis%paginate == 0:
		x=0
	
	con = db(query).select(limitby=(start,end), orderby=db.situacao.id)
	
	return response.render("initial/list_situacao.html", con=con, id_emp=id_emp, 
		x=x, end=end, paginacao='on', regis=regis, paginate=paginate) 	

@auth.requires_membership('admin')
def users():
	print 'users'
	query = (db.auth_user.id_empresa == db.empresa.id)
	usuarios = db(query).select(orderby=db.auth_user.funcao)
	
	return response.render("initial/list_usuario.html", usuarios=usuarios)

@auth.requires_membership('admin')
def form_users():
	response.title = 'Usuários'
	id_usuario = request.vars['id_edit']
	
	if id_usuario is None:
		form 	=	SQLFORM(db.auth_user)
	else:
		form 	=	SQLFORM(db.auth_user, id_usuario)

	form.element(_name='first_name')['_class'] = "form-control"
	form.element(_name='last_name')['_class'] = "form-control"
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='username')['_class'] = "form-control"
	form.element(_name='password')['_class'] = "form-control"
	form.element(_name='funcao')['_class'] = "form-control"
	form.element(_name='id_empresa')['_class'] = "form-control"
	form.element(_name='supervisor')['_class'] = "form-control"

	if form.process().accepted:
		logger.debug("usr:%s - ADD/INSERT - tabela:auth_user - nome:%s"\
		%(session.auth.user.username, request.vars.username))
		redirect(URL("users"))
	return response.render("initial/form_users.html", form=form)

@auth.requires_membership('admin')
def group():
	print 'groups'
	grid 	= SQLFORM.grid(db.auth_group, user_signature=False)
	
	return response.render("initial/show_grid.html", grid=grid)

@auth.requires_membership('admin')
def membership():
	print 'membership'
	grid 	= SQLFORM.grid(db.auth_membership, user_signature=False)
	
	return response.render("initial/show_grid.html", grid=grid)

@auth.requires_login()
def delete():
	funcao 	=	request.vars['tabela']
	id_tab	=	request.vars['id_tab']
	logger.debug("usr:%s - DELETE - tabelea:%s - id:%s - ip:%s"\
		%(session.auth.user.username, funcao, id_tab, request.env.remote_addr))
	if funcao 	== "empresa":
		tabela 	=	 db.empresa.id
	if funcao 	==	"status":
		tabela 	= 	db.status.id
	if funcao 	==	"emprestimo":
		if session.auth.user.funcao == 'supervisor':
			funcao 	= 	"emprestimo2"
		if session.auth.user.funcao == 'admin':
			funcao 	= 	"emprestimo_admin_total"
		tabela 	= 	db.emprestimo.id
	if funcao 	==	"situacao":
		tabela 	= 	db.situacao.id
	if funcao 	==	"envio":
		tabela 	= 	db.envio.id
	if funcao 	==	"banco":
		tabela 	= 	db.banco.id
	if funcao 	==	"orgao":
		tabela 	= 	db.orgao.id
	if funcao 	==	"auth_user":
		tabela 	= 	db.auth_user.id
		funcao 	= 	"users"

	db(tabela == id_tab).delete()	
	redirect(URL(funcao))

def lembrete(): 
	query = (db.auth_user.id == session.auth.user.id)
	db(query).update(lembrete=request.vars.lembrete)
	redirect(URL(form_emprestimo))
	