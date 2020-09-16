import pygame
from random import randrange
import time
import sys
import math
import random
import bisect


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        raise NotImplementedError

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self):
        raise NotImplementedError



class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0  # search depth
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):

        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def solve(self):
        return [node.state for node in self.path()[0:]]

    def path(self):
        x, result = self, []
        while x:
            result.append(x)
            x = x.parent
        result.reverse()
        return result


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)



class Queue:

    def __init__(self):
        raise NotImplementedError

    def append(self, item):
        raise NotImplementedError

    def extend(self, items):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError


class FIFOQueue(Queue):

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


def graph_search(problem, fringe):
    closed = set()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        if node.state not in closed:
            closed.add(node.state)
            fringe.extend(node.expand(problem))
    return None


def breadth_first_graph_search(problem):
    return graph_search(problem, FIFOQueue())


def distance(a, b):
    return math.hypot((a[0] - b[0]), (a[1] - b[1]))


class Graph:
    def __init__(self, dictionary=None, directed=True):
        self.dict = dictionary or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
        else:
            nodes_no_edges = list({y for x in self.dict.values()
                                   for y in x if y not in self.dict})
            for node in nodes_no_edges:
                self.dict[node] = {}

    def make_undirected(self):
        for a in list(self.dict.keys()):
            for (b, dist) in self.dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, node_a, node_b, distance_val=1):
        self.connect1(node_a, node_b, distance_val)
        if not self.directed:
            self.connect1(node_b, node_a, distance_val)

    def connect1(self, node_a, node_b, distance_val):
        self.dict.setdefault(node_a, {})[node_b] = distance_val

    def get(self, a, b=None):
        links = self.dict.get(a)
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):

        return list(self.dict.keys())


def ateApple(head,apple):
    return head == apple

def out_of_range(glava):
    snakeX = glava[0]
    snakeY = glava[1]
    if snakeX > 540 or snakeX < 0:
        return False
    elif snakeY > 640 or snakeY < 0:
        return False
    else:
        return True

def coalision(tail,head):
    lista_zmija = list(tail)
    if lista_zmija.__contains__(head):
        return False
    else:
        return True

#ProdolziPravo
def prodolziPravo(state):
    direction = state[0]
    tail = state[1]
    head = state[2]
    apple = state[3]
    new_head = head
    if direction == 3:
        new_head = head[0] + 60, head[1]
    elif direction == 4:
        new_head = head[0] - 60, head[1]
    elif direction == 2:
        new_head = head[0], head[1] - 60
    else:
        new_head = head[0], head[1] + 60

    if out_of_range(new_head) and coalision(tail, new_head):
        if ateApple(new_head, apple):
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            return (direction, tuple(lista_zmija), new_head, apple)
        else:
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            lista_zmija.pop(0)
            return (direction, tuple(lista_zmija), new_head, apple)

    return state

#SvrtiDesno
def svrtiDesno(state):
    direction = state[0]
    tail = state[1]
    head = state[2]
    apple = state[3]
    new_head = head
    new_direction = direction
    if direction == 3:
        new_head = head[0], head[1] + 60
        new_direction = 1
    elif direction == 4:
        new_head = head[0], head[1] - 60
        new_direction = 2
    elif direction == 2:
        new_head = head[0] + 60, head[1]
        new_direction = 3
    else:
        new_head = head[0] - 60, head[1]
        new_direction = 4

    if out_of_range(new_head) and coalision(tail, new_head):
        if ateApple(new_head, apple):
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            return (new_direction, tuple(lista_zmija), new_head, apple)
        else:
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            lista_zmija.pop(0)
            return (new_direction, tuple(lista_zmija), new_head, apple)

    return state

#SvrtiLevo
def svrtiLevo(state):
    direction = state[0]
    tail = state[1]
    head = state[2]
    apple = state[3]
    new_head = head
    new_direction = direction
    if direction == 3:
        new_head = head[0], head[1] - 60
        new_direction = 2
    elif direction == 4:
        new_head = head[0], head[1] + 60
        new_direction = 1
    elif direction == 2:
        new_head = head[0] - 60, head[1]
        new_direction = 4
    else:
        new_head = head[0] + 60, head[1]
        new_direction = 3

    if out_of_range(new_head) and coalision(tail, new_head):
        if ateApple(new_head, apple):
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            return (new_direction, tuple(lista_zmija), new_head,apple)
        else:
            lista_zmija = list(tail)
            lista_zmija.append(new_head)
            lista_zmija.pop(0)
            return (new_direction, tuple(lista_zmija), new_head,apple)

    return state



#da ne se izede samata sebe i da ne izleze nadvor od tablata 10x10(pocnuva od 0 do 9)

class Snake(Problem):

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal


    def goal_test(self, state):
        return state[2] == state[3]

    def successor(self, state):
        successors = dict()
        new_State = prodolziPravo(state)
        if new_State != state:
            successors["S"] = new_State
        new_State = svrtiDesno(state)
        if new_State != state:
            successors["R"] = new_State
        new_State = svrtiLevo(state)
        if new_State != state:
            successors["L"] = new_State

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]



def findPath(direction,tail,head,apple):
    snake = Snake((direction, tail, head, apple), None)
    answer = breadth_first_graph_search(snake)
    return answer.solution()

pygame.init()
screen = pygame.display.set_mode((600,600))
playerImg = pygame.image.load('./snake.png')
tailImg = pygame.image.load('./snake1.png')
appleImg = pygame.image.load('./apple.png')


snakeX = 60
snakeY = 0
tail = [(0,0)]
appleX = 120
appleY = 120
appleEaten = False
direction = 3
first = True
lastKey = pygame.K_RIGHT;
theEnd = False


def drawTail(tail):
    for temp in tail:
        screen.blit(tailImg, temp)


def moveInDirection(direction):
    time.sleep(0.3)
    global snakeX
    global snakeY
    global tail
    oldX = snakeX
    oldY = snakeY
    if direction == 1:
        if snakeY == 540:
            snakeY = 0
        else:
            snakeY += 60
    elif direction == 2:
        if snakeY == 0:
            snakeY = 540
        else:
            snakeY -= 60
    elif direction == 3:
        if snakeX == 540:
            snakeX = 0
        else:
            snakeX += 60
    elif direction == 4:
        if snakeX == 0:
            snakeX = 540
        else:
            snakeX -= 60
    tail.append((oldX, oldY))
    tail.pop(0)

def moveInDirectionTest(direction):
    time.sleep(0.3)
    global snakeX
    global snakeY
    global tail
    oldX = snakeX
    oldY = snakeY
    if direction == 1:
        snakeY += 60
    elif direction == 2:
        snakeY -= 60
    elif direction == 3:
        snakeX += 60
    elif direction == 4:
        snakeX -= 60
    tail.append((oldX, oldY))
    tail.pop(0)


def drawSnake(x,y):
    screen.blit(playerImg,(x,y))

def drawApple(x,y):
    screen.blit(appleImg,(x,y))

def checkEaten():
    global snakeX
    global snakeY
    global appleX
    global appleY
    global appleEaten
    if snakeX == appleX and snakeY == appleY:
        appleEaten = True
    else:
        appleEaten = False

def moveUp():
    global snakeY
    global snakeX
    global tail
    snakeY -= 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def moveDown():
    global snakeY
    global snakeX
    global tail
    snakeY += 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def moveLeft():
    global snakeX
    global snakeY
    global tail
    snakeX -= 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def moveRight():
    global snakeX
    global snakeY
    global tail
    snakeX += 60
    tail.append((snakeX, snakeY))
    tail.pop(0)



def generateRandomApple():
    randomX = randrange(10)
    randomY = randrange(10)
    print(randomX)
    print(randomY)
    global appleX
    global appleY
    global tail
    while True:
        appleX = randomX * 60
        appleY = randomY * 60
        if (appleX, appleY) in tail:
            randomX = randrange(10)
            randomY = randrange(10)
        else:
            break


def checkTheEnd(tail,sX,sY):
    if (sX,sY) in tail:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over!', True, (255,255,255), (150,150,150))
        textRect = text.get_rect()
        textRect.center = (630 // 2, 600 // 2)
        screen.blit(text, textRect)
        global theEnd
        theEnd = True

running = True
find = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    path = findPath(direction, tuple(tail), (snakeX,snakeY), (appleX,appleY))

    for temp in path:
        screen.fill((192, 192, 192))
        drawApple(appleX, appleY)
        drawTail(tail)
        drawSnake(snakeX, snakeY)
        pygame.display.update()
        print(temp)
        if temp == 'S':
            moveInDirectionTest(direction)
        elif temp == 'L':
            if direction == 1:
                moveInDirectionTest(3)
                direction = 3
            elif direction == 2:
                moveInDirectionTest(4)
                direction = 4
            elif direction == 3:
                moveInDirectionTest(2)
                direction = 2
            elif direction == 4:
                moveInDirectionTest(1)
                direction = 1
        else:
            if direction == 1:
                moveInDirectionTest(4)
                direction = 4
            elif direction == 2:
                moveInDirectionTest(3)
                direction = 3
            elif direction == 3:
                moveInDirectionTest(1)
                direction = 1
            elif direction == 4:
                moveInDirectionTest(2)
                direction = 2


    #checkTheEnd(tail, snakeX, snakeY)

    if appleEaten:
        generateRandomApple()

    checkEaten()

    if appleEaten:
        tail.insert(0, tail.__getitem__(0))

    print(snakeX)
    print(snakeY)
    print(tail)






