from gluon.storage import Storage

config = Storage(
        db=Storage(),
        auth=Storage(),
        mail=Storage()
        )

#config.db.uri = "mysql://root:yma2578k@localhost/adm"
config.db.uri = "postgres:pg8000://postgres:123456@127.0.0.1/ubercred"
#config.db.uri = "sqlite://hosts.sqlite"
config.db.pool_size = 10
config.db.check_reserved = ['all']
#config.migrate_enable=True
#config.migrate=True

db = DAL(**config.db)

# logging
import logging
logger = logging.getLogger("web2py.app.blog")
logger.setLevel(logging.DEBUG)

#auth Rbac
from gluon.tools import Auth

auth = Auth(db, controller="initial", function="user")

#settings
auth.settings.remember_me_form = False
auth.settings.formstyle = "divs"
auth.settings.login_next = URL(a='ubercred', c='initial', f='principal')
auth.settings.logout_next = URL('user?_next=')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
#auth.settings.formstyle = "divs"
auth.settings.actions_disabled = ['register']

auth.messages.logged_in = 'Bem Vindo' 
auth.messages.logged_out = 'Até logo'
auth.messages.access_denied = 'Acesso negado! Contate o administrador'
auth.messages.invalid_email = 'email Inválido'
auth.messages.invalid_login = 'Login Inválido'

#mail
mail = auth.settings.mailer
mail.settings.server = "zmail.ad2.com.br:587"
mail.settings.sender = "smtp_avisos@ad2.com.br"
mail.settings.login = "smtp_avisos@ad2.com.br:ad2root"


#signals
def notifica(form):
	logger.info("notifica")
	mail.send(
		to="fndiaz02@gmail.com",
		subject="Usuario %(first_name)s pendente" % form.vars,
		message="<html>Voce tem um novo usuario para aprovacao %(first_name)s %(last_name)s </html>" % form.vars
	)

#auth.settings.register_onaccept = notifica
#auth.settings.register_onaccept = funcao

#messages
#auth.messages.login_button = "Entrar"

db.define_table("empresa",
	Field("nome", "string"),
	format="%(nome)s")

#authfields
auth.settings.extra_fields['auth_user'] = [
	Field("funcao", requires=IS_IN_SET(["agente", "supervisor"])),
	Field("id_empresa", db.empresa),
	Field("lembrete", 'text'),
#	Field("photo", "upload"),
#	Field("gender", requires=IS_IN_SET(["masculino","feminino"]))
]


#janrain
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth, filename="private/janrain.key")

auth.define_tables(username=True)

#genericas views
if request.is_local:
	response.generic_patterns = ['*']

#import datetime
#response
response.title= "titulo response"
response.meta.keywords= "chave, outra, e outra"

#if not 'pastas' in session:
#    session.pastas = []

#if not 'ano' in session:
#    session.ano = '0'

#if not 'mes' in session:
#    session.mes = '0'

#if not 'form_ano' in session:
#    now = datetime.datetime.now()
#    ano = now.year
#    lista=[]
#    for i in range(12):
#        lista.append(ano)
#        ano = ano - 1
#    session.form_ano = lista

class IS_CPF_OR_CNPJ(object):
 
	def __init__(self, format=False, error_message=T('Número incorreto!')):
		self.error_message = error_message
		self.format = format
 
	def __call__(self, value):
		try:
			cl = str(''.join(c for c in value if c.isdigit()))
 
			if len(cl) == 11:
				cpf = cl
				cnpj = None
			elif len(cl) == 14:
				cpf = None
				cnpj = cl
			else:
				return value, self.error_message

			if cpf:
				def calcdv(numb):
					result = int()
					seq = reversed(
						((range(9, -1, -1)*2)[:len(numb)])
					)
					for digit, base in zip(numb, seq):
						result += int(digit)*int(base)
					dv = result % 11
					return (dv-10) and dv or 0

				numb, xdv = cpf[:-2], cpf[-2:]
 				dv1 = calcdv(numb)
				dv2 = calcdv(numb + str(dv1))
				if '%d%d' % (dv1, dv2) == xdv:
					return self.doformat(cpf) if self.format else cpf, None
				else:
					return cpf, T('CPF inválido')
			
			elif cnpj:
				intmap = map(int, cnpj)
				validate = intmap[:12]
				prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
				while len(validate) < 14:
					r = sum([x*y for (x, y) in zip(validate, prod)]) % 11
					f = 11 - r if r > 1 else 0
					validate.append(f)
					prod.insert(0, 6)
				if validate == intmap:
					return self.doformat(cnpj) if self.format else cnpj, None
				else:
					return cnpj, T('CNPJ inválido')
 
		except:
			return value, self.error_message
 
	def doformat(self, value):
		if len(value) == 11:
			result = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + \
					'-' + value[9:11]

		elif len(value) == 14:
			result = value[0:2] + '.' + value[2:5] + '.' + value[5:8] + \
				'/' + value[8:12] + '-' + value[12:14]
            
		else:
			result = value
			return result
