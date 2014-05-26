##Agenda
#db.agenda.empresa.requires = IS_NOT_EMPTY(error_message=
#						T("valor não pode ser nulo"))

#db.agenda.telefone.requires = [IS_NOT_EMPTY(error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_NOT_IN_DB(db, 'agenda.telefone', error_message=T("este número está em uso")),
#IS_LENGTH(minsize=9, maxsize=11, error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_MATCH('[0-9]+', error_message=T("somente números"))]

#db.emprestimo.estado.requires = IS_IN_DB(db, 'estados.id', '%(nome)s', zero=T('escolha um'), 
#	error_message=T("valor inválido"))
#db.user_ponto.tipo.requires = IS_IN_DB(query,'tipos.id','%(descricao)s')


##Empréstimo
db.emprestimo.data_emp.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))
db.emprestimo.nome.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))
db.emprestimo.valor_total.requires = requires=IS_DECIMAL_IN_RANGE(0, None, dot=".")
db.emprestimo.valor_parcela.requires = requires=IS_DECIMAL_IN_RANGE(0, None, dot=".")
db.emprestimo.n_parcelas.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))
#db.emprestimo.valor_total.requires = [
#IS_NOT_EMPTY(error_message=T("valor não pode ser nulo")),
#IS_FLOAT_IN_RANGE(0, 999999999, error_message='algo errado, use o ponto ao invés da virgula')
#]
db.emprestimo.nome.requires = IS_LOWER()
db.emprestimo.telefone.requires = IS_LIST_OF(
IS_INT_IN_RANGE(0, 999999999999, error_message=T("somente números"))
)

db.emprestimo.cpf.requires = IS_CPF_OR_CNPJ()
db.emprestimo.estado.requires = IS_EMPTY_OR(IS_IN_DB(db, 'estados.id', 
	'%(sigla)s', error_message=T("valor inválido")))
db.emprestimo.id_empresa.requires = IS_EMPTY_OR(IS_IN_DB(db, 'empresa.id', 
	'%(nome)s', error_message=T("valor inválido")))
db.emprestimo.id_produto.requires = IS_EMPTY_OR(IS_IN_DB(db, 'produto.id', 
	'%(nome)s', error_message=T("valor inválido")))

db.emprestimo.banco.requires = IS_EMPTY_OR(IS_IN_DB(db, db.banco.id, '%(nome)s', 
	error_message=T("valor inválido")))
db.emprestimo.orgao.requires = IS_IN_DB(db, db.orgao.id, '%(nome)s', 
	error_message=T("valor inválido"))
db.emprestimo.envio.requires = IS_IN_DB(db, db.envio.id, '%(nome)s', 
	error_message=T("valor inválido"))



##Auth_user
sup=[]
query=(db.auth_user.funcao == 'supervisor')
var=db(query).select(db.auth_user.username)
for row in var:
	#print row.username
	sup.append(row.username)
#print sup
db.auth_user.supervisor.requires = IS_EMPTY_OR(IS_IN_SET(sup, 
	error_message=T("valor inválido")))
db.auth_user.meta.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

##auth_user
#db.auth_user.last_name = IS_EMPTY()

##Agendamento
db.agendamento.cpf.requires = IS_CPF_OR_CNPJ()