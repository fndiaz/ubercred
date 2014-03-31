# coding=UTF-8
import  json
from datetime import datetime
from pprint import pprint


@auth.requires_login()
def principal():
	func 	= session.auth.user.funcao
	id_user = session.auth.user.id
	if func == "supervisor":
		auth.add_membership(1, id_user)
		redirect(URL(emprestimo))
	if func == "agente":
		auth.add_membership(2, id_user)
		redirect(URL(form_emprestimo))
	
	return response.render("initial/principal.html", teste=teste)

def cpf_json():
	if request.vars.func == "pend":
		query = (db.emprestimo.id_empresa == db.empresa.id) \
		& (db.emprestimo.estado == None) & (db.emprestimo.telefone == "")

	if request.vars.func == "total":
		query = (db.emprestimo.id_empresa == db.empresa.id)

	cpf = db(query).select(db.emprestimo.cpf)
	lista = []
	for dado in cpf:
		lista.append(dado.cpf)
	lista = list(set(lista))

	return response.json(lista)

def estados_json():
	print request.vars
	with open('/home/fernado/web2py/tronco/applications/ubercred/views/estados.json') as json_data:
		json_data = json.load(json_data)
		#print json_data[0]
		#for dado in json_data:
		#	print dado

	return response.json(json_data)
	#return response.render("estados.json")

def cidades_json():
	print request.vars
	var = URL('/views/cidades.json')
	print var
	with open('/home/fernado/web2py/tronco/applications/ubercred/views/cidades.json') as json_data:
		json_data = json.load(json_data)
		print(json_data)

	return response.json(json_data)	
	#return response.render("cidades.json")

def user():
	print request.args(0)
	if request.args(0) == 'login':
			return response.render("login/user.html", 
										user=auth())

	if request.args(0) == 'register':
		return response.render("login/user.html", 
							user=auth.register())

	if request.args(0) == 'not_authorized':
		print 'nao'

	if request.args(0) == 'profile':
		return response.render("login/user.html", 
							user=auth.profile())

	return response.render("login/user.html", user=auth())

##---------------------------Emepresa
@auth.requires_membership('supervisor')
def form_empresa():
	response.title = 'Empresa'
	id_edit	= request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.empresa)
	else:
		form 	= SQLFORM(db.empresa, id_edit)

	if form.process().accepted:
		redirect(URL("empresa"))

	return response.render("initial/show_form.html", form=form)

@auth.requires_membership('supervisor')
def empresa():
	print session
	response.title = 'empresa'
	empresa =	db(db.empresa).select(orderby=db.empresa.id)

	return response.render("initial/list_empresa.html", 
		empresa=empresa)

##---------------------------Status
@auth.requires_membership('supervisor')
def form_status():
	response.title = "Status"
	id_edit = request.vars['id_edit']

	if id_edit is None:
		form 	= SQLFORM(db.status)
	else:
		form 	= SQLFORM(db.status, id_edit)

	if form.process().accepted:
		redirect(URL("status"))

	return response.render("initial/show_form.html", form=form)	

@auth.requires_membership('supervisor')
def status():
	response.title = 'status'
	status 	=	db(db.status).select(orderby=db.status.id)

	return response.render("initial/list_status.html", 
		status=status)

##---------------------------Emprestimo
@auth.requires_login()
def form_emprestimo():
	id_edit = request.vars['id_edit']
	print id_edit
	print session.auth.user
	funcao = session.auth.user.funcao
	if funcao == "agente":
		redirect(URL(form_emprestimo_agt))
	if funcao == "supervisor":
		if id_edit != None:
			redirect(URL("initial",
		"form_emprestimo_spv?id_edit="+id_edit))
		else:
			redirect(URL(form_emprestimo_spv))

@auth.requires_login()
def form_emprestimo_agt():
	response.title = 'Emprestimo agente'
	id_edit = request.vars['id_edit']
	date = datetime.now()
	date = date.strftime("%Y-%m-%d %I:%M:%S")
	ls_user = get_user()
	print session.auth.user.id
	query = (db.auth_user.id == session.auth.user.id)
	lem = db(query).select(db.auth_user.lembrete)
	lem = lem[0].lembrete

	if id_edit is None:
		form 	= SQLFORM(db.emprestimo)
	else:
		form 	= SQLFORM(db.emprestimo, id_edit)

	if form.process().accepted:
		session.flash="Registro processado"
		redirect(URL("form_emprestimo_agt")) 
	elif form.errors:
		response.flash=("Ops, algo está errado")
	
	return response.render("initial/form_emprestimo_agt.html", 
				date=date, lem=lem, form=form, ls_user=ls_user)

@auth.requires_membership('supervisor')
def form_emprestimo_spv():
	response.title = 'Emprestimo supervisor'
	id_edit = request.vars['id_edit']
	cidade = ""
	ls_user = get_user()
	print ls_user

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
		session.flash=("Registro processado")
		redirect(URL("emprestimo2")) 
	else:
		print request.vars
	
	return response.render("initial/form_emprestimo_spv.html", 
		cidade=cidade, id_edit=id_edit, form=form, ls_user=ls_user)

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
	print ls_user
	return ls_user


@auth.requires_membership('supervisor')
def emprestimo():
	response.title = "Emprestimos pendentes"
	query = (db.emprestimo.id_empresa == db.empresa.id) \
		& (db.emprestimo.estado == None) & (db.emprestimo.telefone == "")
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	con = db(query).select(limitby=(start,end))
	grid 	= SQLFORM.grid(db.emprestimo, user_signature=False)
	
	return response.render("initial/list_emprestimo.html", con=con, grid=grid,
		end=end, paginacao="on", regis=regis, paginate=paginate, x=x)

@auth.requires_membership('supervisor')
def emprestimo2():
	response.title = "Emprestimos totais"
	query = (db.emprestimo.id_empresa == db.empresa.id)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	print regis
	x=1
	if regis%paginate == 0:
		x=0
	#	
	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=db.emprestimo.id)
	
	return response.render("initial/list_emprestimo2.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x)

def emprestimo_agt():
	response.title = "Emprestimos"
	user = session.auth.user.username
	query = (db.emprestimo.id_empresa == db.empresa.id) &\
	(db.emprestimo.vendedora == user)
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	print regis
	x=1
	if regis%paginate == 0:
		x=0
	#

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), limitby=(start,end), orderby=db.emprestimo.id)
	return response.render("initial/list_emprestimo2.html", con=con,
		end=end, paginacao='on', regis=regis, paginate=paginate, x=x)


def detalhes_emprestimo():
	response.title = "Detalhes"
	id_det = request.vars.id_det
	query=((db.emprestimo.id == id_det) & (db.emprestimo.id_empresa == db.empresa.id))
	con=db(query).select()
	print con

	return response.render("initial/detalhes_emprestimo.html", con=con)

def busca_emp_pend():
	response.title = "Emprestimos pendentes"
	query = (db.emprestimo.id_empresa == db.empresa.id) \
		& (db.emprestimo.estado == None) & (db.emprestimo.telefone == "")\
		& (db.emprestimo.cpf == request.vars.cpf)

	con = db(query).select(orderby=db.emprestimo.id)
	
	return response.render("initial/list_emprestimo.html", con=con,
													paginacao='off')

def busca_emp_total():
	response.title = "Emprestimos pendentes"
	query = (db.emprestimo.id_empresa == db.empresa.id)\
		& (db.emprestimo.cpf == request.vars.cpf)

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), orderby=db.emprestimo.id)
	
	return response.render("initial/list_emprestimo2.html", con=con,
													paginacao='off')



##---------------------------Situação
@auth.requires_membership('supervisor')
def form_situacao():
	response.title = 'situação'
	id_emp = request.vars.id_emp
	print id_emp

	if id_emp is None:
		form 	= SQLFORM(db.situacao)
	else:
		query = db.emprestimo.id == id_emp
		emp =db(query).select(db.emprestimo.id, db.emprestimo.nome)
		emp = emp[0]
		form 	= SQLFORM(db.situacao)

	if form.process().accepted:
		session.flash=("Registro processado")
		redirect(URL("situacao?id_emp=%s" %(id_emp))) 
	else:
		print request.vars

	return response.render("initial/form_situacao.html", form=form, 
												emp=emp, id_emp=id_emp)	

@auth.requires_membership('supervisor')
def situacao():
	print request.vars.id_emp
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
	#print regis
	x=1
	if regis%paginate == 0:
		x=0
	
	con = db(query).select(limitby=(start,end), orderby=db.situacao.id)
	#con = db(query).select()
	
	return response.render("initial/list_situacao.html", con=con, id_emp=id_emp, 
		x=x, end=end, paginacao='on', regis=regis, paginate=paginate) 	

@auth.requires_membership('supervisor')
def users():
	print 'users'
	grid 	= SQLFORM.grid(db.auth_user, csv=False, user_signature=False)
	#print usuarios
	
	return response.render("initial/show_grid.html", grid=grid)

def group():
	print 'users'
	grid 	= SQLFORM.grid(db.auth_group, user_signature=False)
	#print usuarios
	
	return response.render("initial/show_grid.html", grid=grid)

def membership():
	print 'users'
	grid 	= SQLFORM.grid(db.auth_membership, user_signature=False)
	#print usuarios
	
	return response.render("initial/show_grid.html", grid=grid)

def delete():
	funcao 	=	request.vars['tabela']
	id_tab	=	request.vars['id_tab']
	print funcao
	print id_tab
	if funcao 	== "empresa":
		tabela 	=	 db.empresa.id
	if funcao 	==	"status":
		tabela 	= 	db.status.id
	if funcao 	==	"emprestimo":
		tabela 	= 	db.emprestimo.id
	if funcao 	==	"situacao":
		tabela 	= 	db.situacao.id

	db(tabela == id_tab).delete()	
	redirect(URL(funcao))

def lembrete(): 
	query = (db.auth_user.id == session.auth.user.id)
	db(query).update(lembrete=request.vars.lembrete)
	redirect(URL(form_emprestimo))
	



	



