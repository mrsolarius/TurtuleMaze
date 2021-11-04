from datetime import time

from map import *
from gui import *
from turn import *

class Grid:
    def __init__(self, g, m, a, d, name):
        self.display = d
        self._name = name
        self.action_space = 2
        self.gui = g
        self.map = m
        self.debug = False
        self.agents = a
        # Tracer ce que fait l'agent
        self.found_lettuce = False
        self.found_initial = False
        self.nb_action = 0


    '''
    Objectif : Fait executer a l'agent une action
    Param : agent - l'agent qui execute une, action - action que l'agent doit executer
    Retour : résultat du mouvement de l'agent (1 si mur, 2 sinon)
    '''
    def step(self, agent, action):
        square = None
        square_touched = None
        #Mise a jour de la pile de cases parcourues
        squareTmp = self.map.agentNumSquare(agent)
        agent.savePosition(squareTmp)
        if action < 1:
            square = self.map.moveAgent(agent)
        elif action < 2:
            square_touched = self.map.touch(agent)
        else:
            self.map.turnAgent(agent, Turn(action))
        #Mise a jour de la position courante
        agent.setCurrentPosition(square)

        if self.display:
            self.gui.update(self.map)
            self.gui.display()

        result = self.result_generic_env(square, squareTmp, square_touched, agent)
        # Compte le nombre d'actions effectuées pour retourner à la position intiale
        # une fois la salade trouvée
        if self.found_lettuce and not self.found_initial:
            self.nb_action += 1
        return result
    
    def disableDisplay(self):
        self.display = False

    def enableDisplay(self):
        self.display = True

    def getNbActions(self):
        return self.nb_action

    '''
    Objectif : @debug
    '''
    def printQvalues(self, qtable):
        self.map.printQvalues(qtable)

    '''
    Objectif : @debug
    '''
    def countAgents(self):
        return self.map.countAgents()

    '''
    Objectif : @debug
    '''
    def squarePosition(self, numSquare):
        return self.map.squarePosition(numSquare)


    '''
    Objectif : indique le bon retour de l'environnement
    Retour : résultat du mouvement de l'agent ( 0 si position initiale, 
                                                1 si mur, 
                                                2 si case vide, 
                                                3 si case de salade)
    '''
    def result_generic_env(self, square, old_square, square_touched, agent):
        # Si l'agent avance
        if not square is None:
            #Si l'agent n'a pas bougé alors il a rencontré un mur
            if square.equal(old_square):
                return 1
            if square.isEnd():
                self.found_lettuce = True
                return 3
            if square.isBegin():
                if self.found_lettuce:
                    self.found_initial = True
                return 0
            return 2
        # Si l'agent touche
        elif not square_touched is None:
            if square_touched.isWall():
                return 1
            if square_touched.isEnd():
                return 3
            if square_touched.isBegin():
                return 0
            return 2
        return 2


    '''
    Objectif : indique le bon retour de l'environnement spécifiquement par rapport à l'env1
    qui a des règles un peu particulières sur l'alternance e1 / e2
    '''
    def result_for_env1(self, square, old_square, square_touched, agent):
        #Regle de l'environnement : alternance e1 / e2 pour retour r2
        #La case objectif bouge pour de manière à faire apprendre à l'agent cette alternance
        if not square is None:
            if not square.equal(old_square) and self.map.isOnObjective(agent):
                self.map.moveObjOnEmptySquare()
            elif square.equal(old_square) and self.map.isOnObjective(agent):
                pass
            elif square.equal(old_square):
                self.map.moveObjOnEmptySquare()

            #Si l'agent n'a pas bougé alors il a rencontré un mur
            if square.equal(old_square):
                return 1
            return 2
        elif not square_touched is None:
            if square_touched.isWall():
                return 1
            return 2
        return 2