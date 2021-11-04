# A* Turtule Maze
Utilisation de l'algorithms A* pour explorer et découvrire le labyrinth de la tortue

# Comment utiliser ?

Installer pygame :

> python3 -m pip install -U pygame --user

Si sa ne fonctionne pas precise la versions :

> python3 -m pip install pygame==2.0.0.dev6

Enfin lancé l'applications :

> python main.py

As noté que il est possible de lancer l'application avec 2 mode diférents :
- LightExploration : Des que la tortue trouve la salade elle arête d'explorer le labyrinte (peut dans certain avoirs un chemin plus long)
- DeepExploration : La tortue explore le labyrinte en entier (peut dans certain cas trouver un chemin de retour plus rapide)
Il faut pour sa modifier la ligne 69 de `main.py`

On peut aussi choisir parmis toutes les map disponible dans `./Environement` à la ligne 17 de `main.py`