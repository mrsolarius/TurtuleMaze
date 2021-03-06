import math
import random

from urllib3.connectionpool import xrange
from Grid.orientation import Orientation
import time
from operator import itemgetter


def printMatrice(array):
    printer = array[:]
    printer.reverse()
    string = ""
    for tb in printer:
        for item in tb:
            string += str(item) + ""
        string += "\n"
    print(string)


class MazeReader:
    """
    @param env Varible d'environement
    @param agent Un seul agent tortue
    @param mode (deux mode LightExploration, DeepExploration)
    @param time temps d'attendte entre deux action en secconde
    """

    def __init__(self, env, agent, mode, time):
        self.env = env
        self.agent = agent
        self.orientation = Orientation.NORTH
        self.prevOrientation = Orientation.NORTH
        self.time = time
        self.position = (0, 0)
        self.salad = 0
        self.oldPositions = []
        self.wallPositions = []
        self.canGoPositions = [(0, 0)]
        self.map = []
        self.origin = (0, 0)
        self.maxX = 0
        self.maxY = 0
        self.mode = mode

    def walk(self):
        time.sleep(self.time)
        result = self.env.step(self.agent, 0)
        if (result != 1):
            self.setNewPosition()
        return result

    def turnRight(self):
        time.sleep(self.time)
        self.changeOrientationRight()
        return self.env.step(self.agent, 3)

    def turnLeft(self):
        time.sleep(self.time)
        self.changeOrientationLeft()
        return self.env.step(self.agent, 2)

    def goEast(self):
        if (self.orientation == Orientation.NORTH):
            self.turnRight()
        elif (self.orientation == Orientation.WEST):
            self.turnRight()
            self.turnRight()
        elif (self.orientation == Orientation.SOUTH):
            self.turnLeft()

    def goWest(self):
        if (self.orientation == Orientation.NORTH):
            self.turnLeft()
        elif (self.orientation == Orientation.EST):
            self.turnLeft()
            self.turnLeft()
        elif (self.orientation == Orientation.SOUTH):
            self.turnRight()

    def goNorth(self):
        if (self.orientation == Orientation.WEST):
            self.turnRight()
        elif (self.orientation == Orientation.EST):
            self.turnLeft()
        elif (self.orientation == Orientation.SOUTH):
            self.turnLeft()
            self.turnLeft()

    def goSouth(self):
        if (self.orientation == Orientation.WEST):
            self.turnLeft()
        elif (self.orientation == Orientation.EST):
            self.turnRight()
        elif (self.orientation == Orientation.NORTH):
            self.turnRight()
            self.turnRight()

    def detect(self):
        return self.env.step(self.agent, 1)

    """
    Le detector mod permet ?? la tortue d'effectuer une rotation ?? 360?? sur elle m??me 
    Cela permet d'inisialiser les diff??rent tableu contenant les coordon??es des objet d??tecter
    """

    def detectorMode(self):
        # Ajout de la position actuel au tableau des case explorer
        self.oldPositions.append(self.position)
        # enregistrement de la position inisital
        primaryOrientation = self.orientation
        # la tortue utilise toujours le m??me shemas de d??tection d'abors nord puis est sud et west
        # pour chaque oriantation on ajoute les ??lement d??tecter au bonne coordon??e et au bon tableau (c'est r??p??titif mais sa marche)
        self.goNorth()
        detect = self.env.step(self.agent, 1)
        if detect == 1:
            self.wallPositions.append((self.position[0], self.position[1] + 1))
            if self.position[1] + 1 > self.maxY:
                self.maxY = self.position[1] + 1
        elif detect == 2:
            if self.canGoPositions.count((self.position[0], self.position[1] + 1)) < 1:
                self.canGoPositions.append((self.position[0], self.position[1] + 1))
            if self.position[1] + 1 > self.maxY:
                self.maxY = self.position[1] + 1
        elif detect == 3:
            self.salad = (self.position[0], self.position[1] + 1)
        self.goEast()
        detect = self.env.step(self.agent, 1)
        if detect == 1:
            self.wallPositions.append((self.position[0] + 1, self.position[1]))
            if self.position[0] + 1 > self.maxX:
                self.maxX = self.position[0] + 1
        elif detect == 2:
            if self.canGoPositions.count((self.position[0] + 1, self.position[1])) < 1:
                self.canGoPositions.append((self.position[0] + 1, self.position[1]))
            if self.position[0] + 1 > self.maxX:
                self.maxX = self.position[0] + 1
        elif detect == 3:
            self.salad = (self.position[0] + 1, self.position[1])
        self.goSouth()
        detect = self.env.step(self.agent, 1)
        if detect == 1:
            self.wallPositions.append((self.position[0], self.position[1] - 1))
            if self.position[1] - 1 < 0:
                self.increaseAllY()
        elif detect == 2:
            if self.canGoPositions.count((self.position[0], self.position[1] - 1)) < 1:
                self.canGoPositions.append((self.position[0], self.position[1] - 1))
            if self.position[1] - 1 < 0:
                self.increaseAllY()
        elif detect == 3:
            self.salad = (self.position[0], self.position[1] - 1)
        self.goWest()
        detect = self.env.step(self.agent, 1)
        if detect == 1:
            self.wallPositions.append((self.position[0] - 1, self.position[1]))
            if self.position[0] - 1 < 0:
                self.increaseAllX()
        elif detect == 2:
            if self.canGoPositions.count((self.position[0] - 1, self.position[1])) < 1:
                self.canGoPositions.append((self.position[0] - 1, self.position[1]))
            if self.position[0] - 1 < 0:
                self.increaseAllX()
        elif detect == 3:
            self.salad = (self.position[0] - 1, self.position[1])
        # remise en place de l'oriantation insitial
        if primaryOrientation == Orientation.NORTH:
            self.goNorth()
        elif primaryOrientation == Orientation.EST:
            self.goEast()
        elif primaryOrientation == Orientation.SOUTH:
            self.goSouth()
        elif primaryOrientation == Orientation.WEST:
            self.goWest()

    def changeOrientationRight(self):
        self.prevOrientation = self.orientation
        if self.orientation == Orientation.NORTH:
            self.orientation = Orientation.EST
        elif self.orientation == Orientation.EST:
            self.orientation = Orientation.SOUTH
        elif self.orientation == Orientation.SOUTH:
            self.orientation = Orientation.WEST
        else:
            self.orientation = Orientation.NORTH

    def changeOrientationLeft(self):
        self.prevOrientation = self.orientation
        if self.orientation == Orientation.NORTH:
            self.orientation = Orientation.WEST
        elif self.orientation == Orientation.WEST:
            self.orientation = Orientation.SOUTH
        elif self.orientation == Orientation.SOUTH:
            self.orientation = Orientation.EST
        else:
            self.orientation = Orientation.NORTH

    # Permet d'inisialiser la nouvelle position lorsque la tortue avance
    # et de pr??munire est exeption de sortie de tableau
    def setNewPosition(self):
        if self.orientation == Orientation.NORTH:
            self.position = (self.position[0], self.position[1] + 1)
            if self.position[1] > self.maxY:
                self.maxY = self.position[1]
        elif self.orientation == Orientation.WEST:
            self.position = (self.position[0] - 1, self.position[1])
            if self.position[0] < 0:
                self.increaseAllX()
        elif self.orientation == Orientation.SOUTH:
            self.position = (self.position[0], self.position[1] - 1)
            if self.position[1] < 0:
                self.increaseAllY()
        else:
            self.position = (self.position[0] + 1, self.position[1])
            if self.position[0] > self.maxX:
                self.maxX = self.position[0]

    # cette fonction permet lorsque les coordon??e de y sont n??gatif de toute augmenter de 1
    # afin d'avoirs toujours un tableau de map avec une origine de 0 0
    # cela implique aussi d'augemnter tous les co??ficient en relation de 1
    def increaseAllY(self):
        for i in range(0, len(self.oldPositions)):
            self.oldPositions[i] = (self.oldPositions[i][0], self.oldPositions[i][1] + 1)
        for i in range(0, len(self.wallPositions)):
            self.wallPositions[i] = (self.wallPositions[i][0], self.wallPositions[i][1] + 1)
        for i in range(0, len(self.canGoPositions)):
            self.canGoPositions[i] = (self.canGoPositions[i][0], self.canGoPositions[i][1] + 1)
        self.position = (self.position[0], self.position[1] + 1)
        self.origin = (self.origin[0], self.origin[1] + 1)
        self.maxY += 1
        if self.salad:
            self.salad = (self.salad[0], self.salad[1] + 1)

    # cette fonction permet lorsque les coordon??e de x sont n??gatif de toute augmenter de 1
    # afin d'avoirs toujours un tableau de map avec une origine de 0 0
    # cela implique aussi d'augemnter tous les co??ficient en relation de 1
    def increaseAllX(self):
        for i in range(0, len(self.oldPositions)):
            self.oldPositions[i] = (self.oldPositions[i][0] + 1, self.oldPositions[i][1])
        for i in range(0, len(self.wallPositions)):
            self.wallPositions[i] = (self.wallPositions[i][0] + 1, self.wallPositions[i][1])
        for i in range(0, len(self.canGoPositions)):
            self.canGoPositions[i] = (self.canGoPositions[i][0] + 1, self.canGoPositions[i][1])
        self.position = (self.position[0] + 1, self.position[1])
        self.origin = (self.origin[0] + 1, self.origin[1])
        self.maxX += 1
        if self.salad:
            self.salad = (self.salad[0] + 1, self.salad[1])

    # Cette fonction transforme tous les tableau de coordon??e en une map avec une valeur dif??rente pour chaque ??lement :
    # - ? : Position inconue
    # - 1 : Mure
    # - 2 : Case vide non visit??
    # - 4 : Case vide d??j?? visit??
    def convertToMap(self):
        # supretion du tableau des possition possible toutes les position se trouvant d??j?? dans le tableau des positions visit??e (oldPositions)
        # Je suis pas certain que cette action soit ici au meilleurs endrois mais vu que sa marche je les laisser
        tempArr = [i for i in self.canGoPositions if i not in self.oldPositions]
        self.canGoPositions = tempArr
        # le sigle [:] veut dire que je copie tous le tableu ?? une nouvelle adresse
        tempPositions = self.oldPositions[:]
        tempWall = self.wallPositions[:]
        tempCanGo = self.canGoPositions[:]
        self.map = []
        for y in range(0, self.maxY + 1):
            xArr = []
            for x in range(0, self.maxX + 1):
                # par default je place des ?
                xArr.append("?")
                lengthPosition = len(tempPositions)
                lengthWall = len(tempWall)
                lengthCanGo = len(tempCanGo)
                i = 0
                # parcour des case vide non visit??e
                while i < lengthCanGo:
                    if tempCanGo[i][0] == x and tempCanGo[i][1] == y:
                        xArr[x] = 2
                        # je retire chaque element ajouter des pr??c??dent tableau
                        tempCanGo.pop(i)
                        lengthCanGo = lengthCanGo - 1
                    i = i + 1
                i = 0
                # parcour des case vide visiter
                while i < lengthPosition:
                    if tempPositions[i][0] == x and tempPositions[i][1] == y:
                        xArr[x] = 4
                        tempPositions.pop(i)
                        lengthPosition = lengthPosition - 1
                    i = i + 1
                i = 0
                # parcour des mure
                while i < lengthWall:
                    if tempWall[i][0] == x and tempWall[i][1] == y:
                        xArr[x] = 1
                        tempWall.pop(i)
                        lengthWall = lengthWall - 1
                    i = i + 1
            self.map.append(xArr)

    # Le cerveau de robot asspirateur tourne toujours ?? droite
    # il ne sert plus mais je les laisser dans mon code parce qu'il est amusant
    def vacuumCleanerBrain(self):
        if self.orientation == Orientation.NORTH:
            self.goEast()
        elif self.orientation == Orientation.WEST:
            self.goSouth()
        elif self.orientation == Orientation.SOUTH:
            self.goWest()
        else:
            self.goNorth()

    # Cette fonction permet d'explorer le labyrinth jusqu'?? trouver la salade (mode LightExploration)
    # ou ?? explorer le labyrinthe en entier (mode deepEpxloration)
    # Quoi qu'il arrive ?? la fin de cette fonction la tortue se trouve sur la salade (sauf si celle ci n'est pas acc??sible)
    def exploreMaze(self):
        # on commance par faire une premier d??t??ction de l'environement
        self.detectorMode()
        self.convertToMap()
        loop = True
        while loop:
            if self.mode == "LightExploration":
                # en mode light exploration on sort de la boucle des que la salade et inisialiser
                # ou si tous le labyrinthe ?? ??tait explorer sans trouver la salade
                if self.salad != 0 or len(self.canGoPositions) < 1:
                    loop = False
            elif self.mode == "DeepExploration":
                # en mode deep exploration on ne sort de la boucle que si il n'y a plus aucun endroit ou allez
                if len(self.canGoPositions) < 1:
                    loop = False
            # detection de l'environement avant traitement
            self.detectorMode()
            self.convertToMap()
            printMatrice(self.map)
            if self.salad != 0:
                if self.mode == "LightExploration":
                    # en mode light exploration si la salade et trouver on fonce dessus et on quite la fonction
                    self.followListCoordinate([self.salad], False)
                    return
                elif self.mode == "DeepExploration":
                    # en mode deep exploration si l'on trouve la salade on fait comme si on ??tait d??j?? allez sur la case
                    # pour ne plus y retourner
                    self.oldPositions.append(self.salad)
                    # puis on mes ?? jour la map
                    self.convertToMap()
            # par default on vas regarder autour de nous si il y a sur la map une position ouverte ?? allez explorer
            if self.map[self.position[1] + 1][self.position[0]] == 2:
                self.goNorth()
            elif self.map[self.position[1] - 1][self.position[0]] == 2:
                self.goSouth()
            elif self.map[self.position[1]][self.position[0] + 1] == 2:
                self.goEast()
            elif self.map[self.position[1]][self.position[0] - 1] == 2:
                self.goWest()
            # si on se retrouve entourer de position d??j?? explorer on utilise a*
            # pour explorer la position la plus proche de nous
            else:
                distance = 10000000000
                bestNode = (0, 0)
                for pos in self.canGoPositions:
                    # pour chaque case vide et non visiter on calcule sa distance par rapport ?? la position actuelle
                    # si la distance et plus pettie que les distance pr??c??dament t??ster
                    # alors on inisialise avec les nouvelle coordon??e le but
                    if abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1]) < distance:
                        distance = abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1])
                        bestNode = pos
                # une fois le node non explorer le plus proche trouver on lance a*
                solveMe = pathSolver(self.position, bestNode, self.map)
                # on r??cup??re le dernier noeu trouver avec solver()
                finalNode = solveMe.solver()
                # si ce noeux ?? bien un parent on l'envoie sur follow back node
                if hasattr(finalNode, 'parent'):
                    self.followBackNode(finalNode, True)
            # en mode deep exploration si on se retrouve face ?? la salade on ne marche pas dessus et on l'??vite
            if self.mode == "DeepExploration":
                if ((self.position[1] + 1, self.position[0]) != self.salad or
                        (self.position[1] - 1, self.position[0]) != self.salad or
                        (self.position[1], self.position[0] + 1) != self.salad or
                        (self.position[1], self.position[0] - 1) != self.salad):
                    self.walk()
            # en mode light exploration on avance quoi qu'il arrive
            elif self.mode == "LightExploration":
                self.walk()
        printMatrice(self.map)
        # si ici on ?? toujours pas de sallade elle et maleureusement inacs??sible et on quite la fonction
        if self.salad == 0:
            print("impossible de trouver la salade")
            return
        # en mode exploration profonde lorsque l'on sort de la boucle on et potentiellement loin de la salade
        if self.mode == "DeepExploration":
            # alors on execute a* pour la retrouver
            solveMe = pathSolver(self.position, self.salad, self.map)
            finalNode = solveMe.solver()
            if hasattr(finalNode, 'parent'):
                self.followBackNode(finalNode, False)

    # la fonction return home permet de revenir ?? l'origine quelle que soit l'??tat de la tortue
    def returnHome(self):
        if self.origin != 0:
            time.sleep(2)
            # on utilise a* pour revenir ?? la position inisial
            solveMe = pathSolver(self.position, self.origin, self.map)
            finalNode = solveMe.solver()
            self.followBackNode(finalNode)
            print("Position initiale trouv??e !")
            print("Trouver en", self.env.getNbActions(), "mouvements")
            time.sleep(2)

    # follow back node prend en entrer le dernier node retrouner par a*
    # puis il remote c'est parent pour en d??duire le chemin que la tortue doit empreinter
    # enfin il appel une fonction permettant de suivre un tableau de coordon??e pour faire bouger la tortue
    # il et possible d'activer le detector mode ce qui aura pour consequance d'appeler les fonction de d??t??ction ?? chque ??tape
    def followBackNode(self, goalNode, detectorMode=False):
        positionsList = []
        node = goalNode
        # parcour des parent
        while node.parent != 0:
            positionsList.append(node.position)
            node = node.parent
            # print(node.position)
        # inversion de la liste pour r??cup??rer suivre les noeux dans le bonne ordre
        positionsList.reverse()
        self.followListCoordinate(positionsList, detectorMode)

    # followListCoordinate permet de faire bouger la tortue de case en case ?? partire d'un tableau de coordon??e
    # il et possible d'activer le detector mode ce qui aura pour consequance d'appeler les fonction de d??t??ction ?? chque ??tape
    def followListCoordinate(self, positionsList, detectorMode=False):
        for position in positionsList:
            if self.position[0] > position[0]:
                self.goWest()
            elif self.position[0] < position[0]:
                self.goEast()
            elif self.position[1] > position[1]:
                self.goSouth()
            elif self.position[1] < position[1]:
                self.goNorth()
            self.walk()
            if detectorMode and position != self.salad:
                self.detectorMode()
                self.convertToMap()


class Node:
    def __init__(self, position: tuple, goal: tuple, parent, cost: int = 0):
        # lsite des enfant
        self.children = []
        # parent direct
        self.parent = parent
        # coordon??e final
        self.goal = goal
        # position du noeux
        self.position = position
        # cout depuis le d??part
        self.costFromStart = cost
        if parent:
            self.path = parent.path[:]
            self.path.append(position)
        else:
            self.path = [position]
        # heuristique du noeu
        self.heuristic = self.getHeuristic()
        # cout total du noeux
        self.fullCost = 0

    # get euristique permet de r??cup??rer la distance qui s??pare le noeux du but
    def getHeuristic(self):
        return abs(self.goal[0] - self.position[0]) + abs(self.goal[1] - self.position[1])

    # create children permet ?? partir de la map de cr??e les neux enfant de se noeu
    def createChildren(self, map):
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if self.position[0] == x and self.position[1] == y:
                    if y + 1 < len(map):
                        # les noeux enfant ne peuve ni ??tre des mure ni des valeur inconue
                        if map[y + 1][x] != 1 and map[y + 1][x] != "?":
                            self.children.append(Node((x, y + 1), self.goal, self, self.costFromStart + 1))
                    if y - 1 >= 0:
                        if map[y - 1][x] != 1 and map[y - 1][x] != "?":
                            self.children.append(Node((x, y - 1), self.goal, self, self.costFromStart + 1))
                    if x + 1 < len(map[0]):
                        if map[y][x + 1] != 1 and map[y][x + 1] != "?":
                            self.children.append(Node((x + 1, y), self.goal, self, self.costFromStart + 1))
                    if x - 1 >= 0:
                        if map[y][x - 1] != 1 and map[y][x - 1] != "?":
                            self.children.append(Node((x - 1, y), self.goal, self, self.costFromStart + 1))


# pathSolver et la classe qui implement a*
class pathSolver:
    def __init__(self, start, goal, theMap):
        # chemin de noeu
        self.path = []
        # liste des noeu d??j?? visiter
        self.closeList = []
        # liste des noeux d??couver et non visit??e
        self.openList = []
        # coordon??e de d??part
        self.start = start
        # coordon??e du but
        self.goal = goal
        # map du labyrinte
        self.map = theMap

    def solver(self):
        # on inisisalise le premier noeu avec les coordon??e de d??part et aucun parent
        startNode = Node(self.start, self.goal, 0)
        # on ajout le noeu que l'on vient de cr??e ?? l'open list
        self.openList.append(startNode)
        # tant que il n'y a aucun chemin ou qu'il y a encore des noeu ouvert
        while not self.path and len(self.openList) > 0:
            # print("open list :", len(self.openList))
            # print("close list :", len(self.closeList))
            lowerCost = -1
            selectedItem = 0
            # on parcour l'open list
            for i in range(len(self.openList)):
                if lowerCost == -1:
                    lowerCost = self.openList[i].fullCost
                if lowerCost > self.openList[i].fullCost:
                    lowerCost = self.openList[i].fullCost
                    selectedItem = i
            # on d??fini le noeu courent comme ??tant le noeux avec le plus pettit fullcost
            # c'est ?? dire la somme de l'euristique et du coup depuis le d??part le moin ??lever
            currentNode = self.openList[selectedItem]
            # vu que on traite ce noeux on le suprime de l'open list courente
            self.openList.pop(selectedItem)
            # et on l'ajoute ?? la liste des neu d??j?? visit??
            self.closeList.append(currentNode)

            # si le noeud courent est ?? la m??me position que le noeud de fin
            if currentNode.position == self.goal:
                # alors c'est ganger on ?? trouver le chemain
                self.path = currentNode.path
                return currentNode

            # sinon on cr??e c'est enfant
            currentNode.createChildren(self.map)
            # et on d??finit la nouvelle plus petite distance depuis le d??part
            shortDistance = len(currentNode.path)
            # on parcour la liste de c'est enfant
            for node in currentNode.children:
                # on cherche dans la close liste si le neux actuel ?? d??j?? ??tait traiter
                isClose = 0
                for closedNode in self.closeList:
                    if closedNode.position == node.position:
                        # si c'est le cas on passe au noeu enfant suivant
                        isClose = 1
                # si le noeu n'est pas clo on vas chercher dans l'open list si il et pr??srent
                if not isClose:
                    isOpen = 0
                    for openNode in self.openList:
                        if openNode.position == node.position:
                            # si il et pr??sent on inisialise un nouveau drapeau isOpen
                            isOpen = 1

                    # si le nouveau chemain passant par se noeud et plus cour que le pr??c??dent
                    # ou si le noeu n'a jammais ??tait explorer
                    if len(node.path) < shortDistance or not isOpen:
                        # on recalcule le full cost
                        node.fullCost = node.heuristic + currentNode.costFromStart + 1
                        # on d??finis le noeu parent comme ??tant le noeu courent
                        node.parent = currentNode
                        # si le noeux na jammais ??tait explorer alors on le place dans l'open list
                        if not isOpen:
                            self.openList.append(node)
