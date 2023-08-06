from pymongo import MongoClient
import subprocess

monclub = {
	'_id': "monclub",
	'site': {
		'name': "Site de Mon Club",
		'domain': "monclub.enpc.org",
		'creation_date': "1 janvier 2017",
		'expiry_date': "1 janvier 2018"
	},
	'owner': {
		'entity': "Mon Club",
		'person': "M. Spock",
		'email': "monsieur.spock@eleves.enpc.fr"
	},
	'redirection': {
		'from': [
			"monsitedeclub.enpc.org",
			"monsitedeclub2.enpc.org"
		],
		'to': "https://monclub.enpc.org",
		'type': "visible permanente"
	},
	'ftp': {
		'authorized_people': [
			"M. Spock",
			"Captain Kirk"
		],
		'user': "enpc-monclub",
		'password': "0SecretPassword0"
	},
	'wordpress': {
		'login_page': "https://monclub.enpc.org/wp-admin",
		'user': "enpc-monclub",
		'password': "0SecretPassword0"
	},
	'email': {
		'address': "monclub@enpc.org",
		'password': "0SecretPassword0"
	},
	'database': {
		'name': "monclub",
		'user': "username",
		'password': "0SecretPassword0"
	},
    'dns': {
		'domain': "monclub.enpc.org.",
        'cname': "monclub.domaineperso.fr.",
        'mx': ["20 mail.domaineperso.fr.", "100 mx.sendgrid.net."],
		'txt': "mon entrée TXT"
	},
	'ki': {
		'directory': "my/hosting/path/on/server/"
	}
}

client = MongoClient()
db = client.fiches
clubs = db.clubs
print("Données insérées :")
print(clubs.insert_one(geoponts).inserted_id)
subprocess.call('fi-gen', 'monclub', '--open')
