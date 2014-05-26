######Banco de Dados

db.define_table("status",
	Field("status", "string"),
	format="%(status)s")

db.define_table("estados",
	Field("sigla"),
	Field("nome"),
	format="%(sigla)s")

db.define_table("orgao",
	Field("nome"),
	format="%(nome)s")

db.define_table("banco",
	Field("nome"),
	format="%(nome)s")

db.define_table("envio",
	Field("nome"),
	format="%(nome)s")

db.define_table("produto",
	Field("nome"),
	format="%(nome)s")

db.define_table("emprestimo",
	Field("data_emp", "datetime"),
	Field("nome", "string", length=60),
	Field("cpf", "string", length=60),
	Field("telefone", "list:string"),
	Field("estado", db.estados),
	Field("cidade"),
	Field("valor_parcela", "double"),
	Field("valor_total", "double"),
	Field("orgao", db.orgao),
	Field("operacao", "string"),
	Field("vendedora", "string"),
	Field("n_parcelas", "integer"),
	Field("id_empresa", db.empresa),
	Field("banco", db.banco),
	Field("adesao", "string"),
	Field("envio", db.envio),
	Field("id_produto", db.produto),
	format="%(nome)s")

db.define_table("situacao",
	Field("data_sit", "datetime"),
	Field("obs", "text"),
	Field("id_emprestimo", db.emprestimo),
	Field("id_status", db.status)
	)

db.define_table("agendamento",
	Field("data_emp"),
	Field("cpf"),
	Field("nome"),
	Field("data_agen", "date"),
	Field("telefone"),
	Field("obs", "text"),
	Field("vendedora"),
	format="%(nome)s")

#db.define_table("funcao",
#	Field("nome"),
#	)

if not db(db.estados).count():
	print '>>>>>>'
	import  json
	from pprint import pprint
	print json.dumps("%s/applications/ubercred/views/estados.json" %(session.raiz))
	with open('%s/applications/ubercred/views/estados.json' %(session.raiz)) as json_data:
		json_data = json.load(json_data)
		#print json_data['Nome']
		for row in json_data:
			print "%s -- %s"  %(row['Nome'], row['ID'])
			db.estados.insert(nome=row['Nome'], sigla=row['Sigla'])
	logger.debug("INICIANDO - criando estados")

if not db(db.status).count():
	db.executesql('alter sequence status_id_seq restart 1;')
	db.status.insert(status="Iniciado")

if not db(db.empresa).count():
	db.empresa.insert(nome="forip")
	logger.debug("INICIANDO - criando empresa forip")

if not db(db.auth_group).count():
	auth.add_group('supervisor')
	auth.add_group('atendente')
	auth.add_group('admin')
	logger.debug("INICIANDO - criando empresa auth_group's")

if not db(db.auth_user).count():
		db.auth_user.insert(first_name="admin",last_name="admin",username="admin"\
		,funcao="admin",id_empresa="1",email="admin@admin.com",\
		password=db.auth_user.password.validate("admin123")[0])
		logger.debug("INICIANDO - adicionado usuario admin")






