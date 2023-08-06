# Outils de gestion du service d'hébergement du KI : générateur de fiches d'hébergement

## Installation (sous Arch, stop kidding with Debian)

### Serveur MongoDB

Lancer
```
sudo pacman -S mongodb
sudo systemctl enable mongodb
```
Alternativement, le serveur peut être lancer sur commande avec
```
mongod
```
Se connecter au serveur sans mot de passe dans le terminal avec
```
mongo
```

Il faudra se connecter au serveur Mongo de hebergement.enpc.org pour rester synchroniser

### Thème XeLaTeX ki019

Lancer
```
cd ..
git clone https://github.com/KIClubinfo/latex-ki.git
cd latex-ki/019/templates/
make install
```

## Architecture
* ki_hosting/
  * templates/ : templates de fiche
  * tex/ : fiches tex
    * clubs/ : version pour les clubs
    * ki/ : version pour le KI
  * pdf/
    * clubs/
    * ki/
  * tmp/ : fichiers de compilation temporaires laissés en mode debug

TODO : version RSI

## Command line tools

Générer toutes les fiches clubs
```
fi:generate all
```

Générer les fiches des clubs *club1*, *club2*
```
fi:generate club1 club2

```

Générer les fiches version réservée au KI
```
fi:generate --ki club1 club2
```

Générer des brouillons de fiche pour approbation : ajoute une watermark "Draft for approval"
```
fi:generate --draft club1 club2
```

Lancer en mode debug : affiche les infos de compilation dans le terminal, n'efface pas *app/tmp/*
```
fi:generate --debug club1 club2
```

Supprime la fiche de club dans la table clubs
```
fi:remove club
```

Traite les données de demande de fiches de la table requests, enregistre la fiche dans clubs et génère le pdf dans *app/pdf/clubs/*
```
req:handle club
```

Traite les données de demande de fiches de la table requests et génère un brouillon de fiche dans *app/pdf/draft/*
```
req:handle club --draft
```

FIXME: option --open pour ouvrir le pdf généré avec xdg-open

## Development

```
sudo pip install -e .
```
Cela créer un lien symbolique dans site-packages vers le répo pour que les modifications des sourcse prennent effet immédiatement.

## Publish to PyPi

Mettre dans ~/.pypirc
```
[distutils]
index-servers =
    pypi

[pypi]
repository: https://pypi.python.org/pypi
username: <username>
password: <password>
```

Modifier le numéro de version dans *ki_hosting/version.py* et lancer
```
python setup.py sdist upload -r pypi
```
