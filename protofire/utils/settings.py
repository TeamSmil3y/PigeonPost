class Settings:
	def __init__(self, address:str, port:int, urls:dict, errors:dict, cors:tuple=([''],False), https:tuple=(False, '', '', '')):
		# address and port
		self.address = (address, port)
	
		# cors
		self.cors_allowed_origins = cors[0]
		self.cors_allow_creds = cors[1]

		# views
		self.views = urls
		self.error_views = errors
		
		# https
		self.use_https = https[0]
		self.https_cert_path = https[1]
		self.https_privkey_path = https[2]
		self.https_privkey_passwd = https[3]