####Banco de Dados

db.define_table("status",
	Field("status", "string"),
	format="%(status)s")

db.define_table("estados",
	Field("sigla"),
	Field("nome"),
	format="%(sigla)s")

db.define_table("emprestimo",
	Field("data_emp", "datetime"),
	Field("nome", "string", length=60),
	Field("cpf", "string", length=60),
	Field("telefone", "string", length=30),
	Field("estado", db.estados),
	Field("cidade"),
	Field("valor_parcela", "double"),
	Field("valor_total", "double"),
	Field("orgao", requires=IS_IN_SET(["INSS", "Estadual", "Federal"])),
	Field("operacao", "string"),
	Field("vendedora", "string"),
	Field("n_parcelas", "integer"),
	Field("id_empresa", db.empresa),
	Field("banco", requires=IS_IN_SET(["", "itau", "bmg"])),
	Field("contrato", requires=IS_IN_SET(["", "cheque", "fisico", "gravacao"])),
	Field("adesao"),
	format="%(nome)s")

db.define_table("situacao",
	Field("data_sit", "date"),
	Field("obs", "text"),
	Field("id_emprestimo", db.emprestimo),
	Field("id_status", db.status)
	)


if not db(db.estados).count():
	print '>>>>>>'
	import  json
	from pprint import pprint
	print json.dumps("/home/fernado/web2py/tronco/applications/ubercred/views/estados.json")
	with open('/home/fernado/web2py/tronco/applications/ubercred/views/estados.json') as json_data:
		json_data = json.load(json_data)
		print 'ow'
		#print json_data['Nome']
		for row in json_data:
			print "%s -- %s"  %(row['Nome'], row['ID'])
			db.estados.insert(nome=row['Nome'], sigla=row['Sigla'])

if not db(db.empresa).count():
	db.empresa.insert(nome="forip")

if not db(db.auth_group).count():
	auth.add_group('supervisor')
	auth.add_group('atendente')

if not db(db.auth_user).count():
		db.auth_user.insert(first_name="admin",last_name="admin",username="admin"\
		,funcao="supervisor",id_empresa="1",email="admin@admin.com",\
		password=db.auth_user.password.validate("admin123")[0])






