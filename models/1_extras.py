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