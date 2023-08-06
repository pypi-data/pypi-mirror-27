from datetime import datetime, timedelta
from pytz import timezone
from pymongo import MongoClient
from bson.codec_options import CodecOptions
from ki_hosting import models
from io import BytesIO

class Options():
    def __init__(self, draft=False, debug=False, ki=False, open=False):
        self.draft = draft
        self.debug = debug
        self.ki = ki
        self.open = open

def format_data(club_data):
    if club_data['site']['creation_date'] == None:
        club_data['site']['creation_date'] = club_data['site']['creation_date'].strftime('%d/%m/%y')
    else:
        club_data['site']['creation_date'] = "Antérieur à 2017"
    club_data['site']['expiry_date'] = club_data['site']['expiry_date'].strftime('%d/%m/%y')
    for key in club_data:
        if club_data[key] is list:
            for idx, item in enumerate(data[key]):
                club_data[key+i] = items
            club_data.pop(key, None)
    return club_data

def generate_fiche(club_data, options):
    slug = club_data.pop('_id', None)
    club_data = format_data(club_data)
    models.fiche.save_pdf(slug, club_data, options)

def handle_request(slug, draft):
    client = MongoClient()
    db = client.fiches
    requests = db.requests.with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=timezone('Europe/Paris')))
    request = requests.find_one({ 'site.subdomain': slug })
    expiry_date = request['date']+timedelta(days=30*int(request['site']['validity']))    # un mois pas toujours 30 jours
    club_data = {
    	'_id': slug,
    	'site': {
    		'name': request['site']['name'],
    		'domain': "{}@enpc.org".format(slug),
    		'creation_date': request['date'],
    		'expiry_date': expiry_date
    	},
    	'owner': {
    		'entity': request['owner']['entity'],
    		'person': request['owner']['person'],
    		'email': "{}@eleves.enpc.fr".format(request['owner']['email'])
    	},
    	'ftp': {
    		'authorized_people': request['ftp']['authorized_people'],
    		'user': "enpc-{}".format(slug),   # tronquer la longueur
    		'password': request['ftp']['password']
    	},
    	'wordpress': {
    		'login_page': "https://{}.enpc.org/wp-admin".format(slug),
    		'user': request['wordpress']['user'],
    		'password': request['wordpress']['password']
    	},
    	'email': {
    		'address': "{}@enpc.org".format(request['email']['username']),
    		'password': request['wordpress']['password']
    	}
    }

    if not draft:
        db.clubs.insert_one(club_data)

    options = Options(draft)
    generate_fiche(club_data, options)
    with open("pdf/{}/{}.pdf".format("draft" if draft else "clubs", slug), "rb") as pdf_file:
        return BytesIO(pdf_file.read())
