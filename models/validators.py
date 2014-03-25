##Agenda
#db.agenda.empresa.requires = IS_NOT_EMPTY(error_message=
#						T("valor não pode ser nulo"))

#db.agenda.telefone.requires = [IS_NOT_EMPTY(error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_NOT_IN_DB(db, 'agenda.telefone', error_message=T("este número está em uso")),
#IS_LENGTH(minsize=9, maxsize=11, error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_MATCH('[0-9]+', error_message=T("somente números"))]

#db.emprestimo.estado.requires = IS_IN_DB(db, 'estados.id', '%(nome)s', zero=T('escolha um'), 
#	error_message=T("valor inválido"))


##Empréstimo
db.emprestimo.data_emp.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

db.emprestimo.nome.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

db.emprestimo.valor_parcela.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

db.emprestimo.n_parcelas.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

db.emprestimo.valor_total.requires = IS_NOT_EMPTY(error_message=
	T("valor não pode ser nulo"))

db.emprestimo.orgao.requires = IS_IN_SET(["INSS", "Estadual", "Federal"], 
	error_message=T("valor não pode ser nulo"))

db.emprestimo.cpf.requires = IS_CPF_OR_CNPJ()

db.emprestimo.estado.requires = IS_EMPTY_OR(IS_IN_DB(db, 'estados.id', 
	'%(sigla)s', error_message=T("valor inválido")))

db.emprestimo.id_empresa.requires = IS_EMPTY_OR(IS_IN_DB(db, 'empresa.id', 
	'%(nome)s', error_message=T("valor inválido")))

db.emprestimo.banco.requires = IS_EMPTY_OR(IS_IN_SET(["itau", "bmg"], 
	error_message=T("valor inválido")))

db.emprestimo.contrato.requires = IS_EMPTY_OR(IS_IN_SET(["cheque", "fisico", "gravacao"], 
	error_message=T("valor inválido")))




