import os, sys, inspect

#Pour inclure les fichiers de l'environnement
cmd_subfolder_grid = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"Grid")))
if cmd_subfolder_grid not in sys.path:
    sys.path.insert(0, cmd_subfolder_grid)

from Grid.parser import Parser
from grid import Grid

import random
import math

class Generator:

    def __init__(self, size):
        self.r = random.randint(1000, 9999999)
        self.size = size
        self.map = ""
        self.nb_wall = self.size - 1
        self.agent_start = 1
        self.salad = 1

    '''
    Objectif : Génère une map
    '''
    def generate(self):
        while not self._test():
            self.map = ""
            nb_wall = self.nb_wall
            agent_start = self.agent_start
            salad = self.salad
            for i in range(self.size):
                for j in range(self.size):
                    if i == 0:
                        self.map += "B"
                    elif i == self.size - 1:
                        self.map += "B"
                    elif j == 0:
                        self.map += "B"
                    elif j == self.size - 1:
                        self.map += "B"
                    else:
                        r = random.randint(0, self.size * self.size)
                        # Ajouter un mur
                        if nb_wall > 0 and r < self.size * self.size / (self.size - nb_wall):
                            self.map += "B"
                            nb_wall -= 1
                        # Ajouter un agent
                        elif r > (self.size * self.size) - i + j and agent_start > 0:
                            self.map += "a"
                            agent_start -= 1
                        # Ajouter une salade
                        elif r < j + math.log(i * i * i) and salad > 0:
                            self.map += "A"
                            salad -= 1
                        else:
                            self.map += " "
                self.map += "\n"

    '''
    Objectif : Sauvegarde la map dans un fichier
    '''
    def save(self):
        with open("Data/Environments/" + str(self.r), "w") as text_file:
            text_file.write(self.map)
        pass

    '''
    Objectif : Vérifie que la map soit utilisable (pas d'impasse pour l'agent)
    Retour: True si le labyrinthe est pratiquable, False sinon
    '''
    def _test(self):
        print(self.map)
        res = False
        nb_wall = self.nb_wall
        agent_start = self.agent_start
        salad = self.salad
        for char in self.map:
            if char == "a":
                agent_start -= 1
            if char == "A":
                salad -= 1
        # Bon formattage, on peut tester le terrain
        if salad == 0 and agent_start == 0:
            path = "Data/Environments"
            parser = Parser(path)
            gui, map, agents = parser.parse_string(self.map)
            env = Grid(gui, map, agents, False, "test")
            cnt = 0
            max_cnt = 50000
            result = 0
            while result != 3 and cnt <= max_cnt:
                result = env.step(agents[0], random.randint(0, 3))  # To use if the task is a Maze
            if cnt < max_cnt:
                res = True
        return res