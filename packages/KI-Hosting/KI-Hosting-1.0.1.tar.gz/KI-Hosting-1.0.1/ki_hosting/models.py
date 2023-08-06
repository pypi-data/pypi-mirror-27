import jinja2
import os
import sys
import subprocess
from string import digits

latex_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/')
)

tex_match = {
    '&':  '\&',
    '%':  '\%',
    '$':  '\$',
    '#':  '\#',
    '_':  '\_',
    '^':  '\^',
}

def latex_escape(string):
	if not string:
		return ""
	elif string[0] in tex_match:
		return tex_match[string[0]]+latex_escape(string[1:])
	else:
		return string[0]+latex_escape(string[1:])

def ending_nb_strip(string):
	if type(string) is list:
		return list(map(ending_nb_strip, string))

	elif type(string) is str:
		if not string:
			return ""
		elif string[-1] in digits:
			return ending_nb_strip(string[0:-1])
		else:
			return string
	else:
		assert False, "ending_nb_strip must be applied to a string or a list of strings : \n{}".format(string)

def word_break_aux(string, index):
	if not string:
		return ""
	elif string[0] in {" ", "@", "."}:
		return string[0]+word_break_aux(string[1:], 0)
	elif index == 25:
		return "\\newline "+word_break_aux(string, 0)
	else:
		return string[0]+word_break_aux(string[1:], index+1)

def word_break(string):
	return word_break_aux(string, 0)

def rendered(value):
	return latex_escape(word_break(value))

def flatten(json):
	dico = {}
	for table_slug, table_dict in json.items():
		for row_slug, row_value in table_dict.items():
			dico[table_slug+"_"+row_slug] = row_value

	return dico

class Row():
	def __init__(self, slug, field, values=None, footnote=None, optional=False):
		self.slug = slug
		self.field = field
		self.values = values if not values or type(values) is list else [values]
		self.template = latex_env.get_template('row.tex')
		self.footnote = footnote
		self.optional = optional

	def template(self, table_slug):
		return self.template.render(field=latex_escape(self.field), value=(latex_escape(', '.join(self.values)) if self.values else "\VAR{%s}" % (table_slug+"_"+self.slug)))

	def tex(self, value=None, footnote_id=None):
		if not value and not self.values:
			raise ValueError("Mandatory field not filled")
		if value:
			if type(value) is list:
				prerendered_value = ', '.join(value)
			else:
				prerendered_value = value
		else:
			prerendered_value = ', '.join(self.values)
		if footnote_id:
			rendered_field = latex_escape(self.field)+("$^{%s}$" % ("*"*footnote_id))
		else:
			rendered_field = latex_escape(self.field)
		return self.template.render(field=rendered_field, value=rendered(prerendered_value))

	def filled(self):
		return self.value != None

class Table():
	def __init__(self, slug, title, *rows, mandatory=False):
		self.slug = slug
		self.title = title
		self.rows = rows
		self.template = latex_env.get_template('table.tex')
		self.mandatory = mandatory

	def template(self):
		return self.template.render(title=self.title, rows=[row.template(self.slug) for row in self.rows])

	def tex(self, club_data, footnote_ids):
		return self.template.render(title=self.title, rows=[row.tex(club_data[row.slug] if row.slug in club_data else None, footnote_ids[row.slug]) for row in self.rows if not row.optional or row.slug in club_data])

	def placeholders(self):
		return [self.slug+"_"+row.slug for row in rows if row.filled()]

	def row(self, row_slug):
		for row in self.rows:
			if row.slug == ending_nb_strip(row_slug):
				return row

class Fiche():
	def __init__(self, slug, title, *tables):
		self.slug = slug
		self.title = title
		self.tables = tables
		self.template = latex_env.get_template('fiche.tex')

	def template(self):
		return self.template.render(title=self.title, tables=[table.template() for table in self.tables])

	def tex(self, club_data, options=False):
		if not options.ki:
			footnotes = [self.table(table_slug).row(row_slug).footnote for table_slug, table_data in club_data.items() for row_slug, values in table_data.items() if self.table(table_slug).row(row_slug).footnote]
			footnote_ids = { table.slug: {row.slug: footnotes.index(row.footnote)+1 if row.footnote else None for row in table.rows} for table in self.tables if table.slug in ending_nb_strip(list(club_data.keys()))}
			footnote = '\\\\\n'.join(["$^{\phantom{%s}%s}$ %s" % ("*"*(len(footnotes)-id-1), "*"*(id+1), fn) for id, fn in enumerate(footnotes)])
		else:
			footnote = ""
			footnote_ids = { table.slug: {row.slug: None for row in table.rows} for table in self.tables if table.slug in ending_nb_strip(list(club_data.keys()))}


		return self.template.render(title=self.title, draft=options.draft, ki=options.ki, footnote=footnote, tables=[self.table(table_slug).tex(club_data[table_slug], footnote_ids[ending_nb_strip(table_slug)]) for table_slug, table_data in club_data.items() if table_slug != 'ki' or options.ki])

	def save_tex(self, slug_name, club_data, options=False, dir=None):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))

		if dir:
			if dir[-1] not in {"/", "."}:
				dir+="/"
		elif options.draft:
			dir = "tex/draft/"
		elif options.ki:
			dir = "tex/ki/"
		else:
			dir = "tex/clubs/"
		subprocess.call(["mkdir", "-p", dir])

		with open(dir+'{}.tex'.format(slug_name), 'w') as output_file:
			output_file.write(fiche.tex(club_data, options))

	def clean_all(self):
		subprocess.call(["rm", "-R", "app/tmp/", "app/tex/", "app/pdf/"])

	def clean_tmp(self, slug_name="all"):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		if slug_name == "all":
			tmp_folder = "tmp/"
		else:
			tmp_folder = "tmp/"+slug_name

		subprocess.call(["rm", "-R", tmp_folder])
	def clean_pdf(self):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		subprocess.call(["rm", "-R", "pdf/clubs/", "pdf/ki/", "pdf/draft/"])

	def save_pdf(self, slug_name, club_data, options=False):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		tmp_folder = "tmp/"+slug_name
		self.save_tex(slug_name, club_data, options, tmp_folder)
		subdir = "draft/" if options.draft else "ki/" if options.ki else "clubs/"
		if options.debug:
			for i in range(2):
				subprocess.call(["xelatex", "{}.tex".format(slug_name)], cwd=tmp_folder)
		else:
			for i in range(2):
				FNULL = open(os.devnull, 'w')
				subprocess.call(["xelatex", "{}.tex".format(slug_name)], cwd=tmp_folder, stdout=FNULL)

		subprocess.call(["echo", "{0}.tex compiled in {0}.pdf".format(slug_name)])
		subprocess.call(["mkdir", "-p", "tex/"+subdir])
		subprocess.call(["cp", "{}/{}.tex".format(tmp_folder, slug_name), "tex/{}{}.tex".format(subdir, slug_name)])
		subprocess.call(["mkdir", "-p", "pdf/"+subdir])
		subprocess.call(["cp", "{}/{}.pdf".format(tmp_folder, slug_name), "pdf/{}{}.pdf".format(subdir, slug_name)])

		if options.open:
			subprocess.call('xdg-open', "pdf/{}{}.pdf".format(subdir, slug_name))

		if not options.debug:
			self.clean_tmp(slug_name)

	def placeholders(self):
		return sum(table.placeholders() for table in self.tables)

	def table(self, table_slug):
		for table in self.tables:
			if table.slug == ending_nb_strip(table_slug):
				return table

	def check_mandatory_tables(self, club_data):
		for table in self.tables:
			if table.mandatory:
				assert table.slug in ending_nb_strip(list(club_data.keys())), "Mandatory table '{}' is missing".format(table.title)

	def json(self):
		return {
		'_id': self.slug,
		'title': self.title,
		'tables': {
			table.slug: {
				'title': table.title,
				'mandatory': table.mandatory,
				'rows': {
					row.slug: {
						'field': row.field,
						'values': row.values,
						'optional': row.optional,
						'footnote': row.footnote
					} for row in table.rows
				}
			} for table in self.tables
		}
	}

	def json_form(self):
		return {
		'_id': self.slug,
		'title': self.title,
		'tables': {
			table.slug: {
				'title': table.title,
				'mandatory': table.mandatory,
				'rows': {
					row.slug: {
						'field': row.field,
						'optional': row.optional,
						'footnote': row.footnote
					} for row in table.rows if not row.values
				}
			} for table in self.tables if self.slug != 'ki'
		}
	}


fiche = Fiche("fiche", "Fiche d'hébergement KI",
			Table('site', "Site web",
				Row('name', "Nom"),
				Row('domain', "Nom de domaine"),
				Row('creation_date', "Date de création"),
				Row('expiry_date', "Date d'expiration", None,
					"Hébergement renouvelable auprès du responsable hébergement."),
				Row('ssl', "Certificat SSL", "Oui"),
				Row('ipv6', "IPv6", "Oui"),
				Row('seperated_logs', "Logs séparés", "Non"),
				mandatory=True
			),
			Table('owner',"Détenteur",
				Row('entity', "Entité"),
				Row('person', "Responsable", None,
					"Désigne le Responsable des Systèmes d'Information de l'entité. Il s'engage à faire respecter la charte \
d'hébergement disponible à https://enpc.org/charte selon les modalitées décrites dans la présente fiche."),
				Row('email', "Adresse email"),
				Row('role', "Poste", None, optional=True),
				Row('phone', "Téléphone", None, optional=True),
				mandatory=True
			),
			Table('redirection', "Redirections",
				Row('from', "Origine"),
				Row('to', "Destination"),
				Row('type', "Type")
			),
			Table('ftp', "Compte FTP",
				Row('server_domain', "Serveur hôte", "ftp.enpc.org (ftp.cluster007.ovh.net)"),
				Row('ip', "IP", "213.186.33.18"),
				Row('port', "Port", "21"),
				Row('authorized_people', "Personnes autorisées", None,
					"Liste des personnes autorisées à connaître et utiliser les identifiants de l'accès FTP. Toute modification \
doit être portée à la connaissance du responsable hébergement."),
				Row('user', "Utilisateur"),	# without hiphens
				Row('password', "Mot de passe"),
				Row('ssh', "SFTP / SSH", "Oui"),
				Row('max_space', "Espace maximum", "1 Go"),
				Row('apache', "Apache", "v2.4"),
				Row('php', "PHP", "v5.6"),
				Row('git', "Git", "v2.1")
			),
			Table('database', "Base de données",
				Row('server', "Serveur", "mysql.enpc.org (va1757-001.privatesql)"),
				Row('port', "Port", "35287"),
				Row('name', "Base de données"),
				Row('user', "Utilisateur"),
				Row('permissions', "Droits", "Admin (Select, Insert, Update, Delete, Create, Alter, Drop)"),
				Row('password', "Mot de passe"),
				Row('interface', "Interface admin", "https://phpmyadmin.ovh.net"),
				Row('type', "Type", "MySQL 5.6"),
				Row('max_space', "Espace maximum", "1 Go"),
				Row('backup', "Sauvegarde hebdomadaire", "Oui")
			),
			Table('wordpress', "Wordpress",
				Row('login_page', "Page de login"),
				Row('user', "Utilisateur"),
				Row('password', "Mot de passe")
			),
			Table('email', "Compte email",
				Row('login_page', "Page de login", "mail.enpc.org (mail.ovh.net)"),
				Row('address', "Adresse email"),
				Row('password', "Mot de passe"),
				Row('max_space', "Espace maximum", "1 Go")
			),
			Table('ki', "Réservé au KI",
				Row('directory', "Répertoire FTP")
			),
			Table('dns', "DNS",
				Row('domain', "Nom de domaine"),
				Row('cname', "CNAME", optional=True),
				Row('mx', "MX", optional=True),
				Row('txt', "TXT", optional=True),
				Row('anomaly', "Anomalie", optional=True)
			)
		)
