def busca_emp_total():
	response.title = "Emprestimos totais"
	mes = request.vars.mes
	cpf = request.vars.cpf
	sup = request.vars.sup
	res_pesquisa=True
	soma=""

	query = cria_busca()
	print query
	#
	paginate 	=	10
	if not request.vars.page:
		redirect(URL(vars={'page':1, 'mes':mes, 'cpf':cpf, 'sup':sup}))
	else:
		page 	=	int(request.vars.page)
	start 	=	(page-1)*paginate
	end 	=	page*paginate
	regis 	=	db(query).count()
	x=1
	if regis%paginate == 0:
		x=0
	#

	con = db(query).select(left=db.estados.on(db.estados.id == db.emprestimo.estado), 
		limitby=(start,end), orderby=db.emprestimo.id)

	if db(query).count() == 0:
		res_pesquisa = False

	return response.render("initial/list_emprestimo_busca.html", 
					con=con, paginacao='on', end=end, regis=regis, 
				paginate=paginate, x=x, res_pesquisa=res_pesquisa)


@auth.requires('login')
def cria_busca():
	print 'cria busca'
	print request.vas
	mes = request.vars.mes
	sup = request.vars.sup	
	ano = session.data_hoje.split('-')[0]
	cpf = request.vars.cpf

	query = (db.emprestimo.id_empresa == db.empresa.id)
	print 'cpf:%s -- mes:%s -- sup:%s' %(cpf, mes, sup)

	if session.auth.user.funcao == "supervisor":
		query=query & (db.emprestimo.vendedora == db.auth_user.username)\
			& (db.auth_user.supervisor == session.auth.user.username)
	if session.auth.user.funcao == "agente":
		query=query & (db.emprestimo.vendedora == session.auth.user.username)
	if mes != '':
		print 'entrou mes'
		query=query & (db.emprestimo.data_emp.year()==ano)\
					& (db.emprestimo.data_emp.month()==mes)
	if cpf != '':
		print ' entrou cpf'
		query=query & (db.emprestimo.cpf == cpf)
	if sup != '':
		print ' entrou sup'
		query=query & (db.emprestimo.vendedora == db.auth_user.username)\
					&(db.auth_user.supervisor == sup)

	return query