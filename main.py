import os, sys, inspect

# Pour inclure les fichiers de l'environnement, plot et stat
cmd_subfolder_grid = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "Grid")))
if cmd_subfolder_grid not in sys.path:
    sys.path.insert(0, cmd_subfolder_grid)

from envBuilder import *
from grid import Grid
from mazeReader import *
from generator import Generator


def init_maze_task():
    # Choisire la carte à charger
    __ENVIRONMENT__ = "ultra_mega_maze"

    # Print the GUI
    __GUI__ = True

    # Instanciation des builders
    envbuilder = EnvBuilder(__ENVIRONMENT__)
    gui, map, agents = envbuilder.build()

    # Creation de la grille
    env = Grid(gui, map, agents, __GUI__, __ENVIRONMENT__)

    return agents, env


'''
Actions
-------
0 - avancer
1 - toucher
2 - rotation gauche
3 - rotation droite
'''
'''
mouvement agent :
0 l'agent tortue avance
1 l'agent tortue detecte l'objet devant elle
2 l'agent tortue tourne a gauche
3 l'agent tortue tourne a droite

resultat :
0 si position initiale, 
1 si mur, 
2 si case vide, 
3 si case de salade
'''


def main():
    '''
    g = Generator(9)
    g.generate()
    g.save()
    '''
    agents, env = init_maze_task()

    '''
    Deux mode dispnible :
        -LightExploration : Des que la tortue trouve la salade elle arête d'explorer le labyrinte (peut dans certain avoirs un chemin plus long)
        -DeepExploration : La tortue explore le labyrinte en entier (peut dans certain cas trouver un chemin de retour plus rapide)
    '''
    #Création de mon objet maze reader
    mazeReader = MazeReader(env, agents[0], "DeepExploration", 0.01) # vous pouvez changer le mode ainci que le temps ici
    #exploration du labyrinth
    mazeReader.exploreMaze()
    #retours à la maison une fois explorer
    mazeReader.returnHome()


if __name__ == '__main__':
    main()

'''
Correction :
- Stratégie d'exploration : Mappage du terrain jusqu'à trouver la salade ou jusqu'à avoir exploré toute la map. 
    C'est très bien !
- Algo de retour : A*, le plus court chemin parmi ce qui a été exploré.
- Convention ratée : le _ devant les attributs privés de tes classes
- Organisation du code : ça aurait été bien de répartir toutes les classes dans leur propre fichier, là ça fait 
un fichier infiniment long et dur à lire.
- Lisibilité du code : le code est très propre, bien commenté, les variables bien nommées. L'organisation du 
code en différente classe est bien faite.

C'est super d'avoir mis différents modes de mappage du terrain (lite / deep) et de les avoir passé dans le 
constructeur. Le code est agréable à lire et je me suis bien amusé à tester ton code :)
Génial aussi d'avoir pris en compte la possibilité que la salade ne soit pas accessible. Le code est bien 
robuste comme ça.

Très bon travail !
'''