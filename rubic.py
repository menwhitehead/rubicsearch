import os, sys
import random, math
import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

WHITE = 0
ORANGE = 1
YELLOW = 2
GREEN = 3
BLUE = 4
RED = 5

colors = ["#FFF", "#FA0", "#FF0", "#0F0", "#00F", "#F00"]


TOP_CLOCKWISE = 0
TOP_COUNTER = 1
FRONT_CLOCKWISE = 2
FRONT_COUNTER = 3
RIGHT_CLOCKWISE = 4
RIGHT_COUNTER = 5

NUMBER_ACTIONS = 6

TOP = 0
BOTTOM = 1
FRONT = 2
RIGHT = 3
BACK = 4
LEFT = 5

TOP_ROW = 0
BOTTOM_ROW = 1

LEFT_COL = 0
RIGHT_COL = 1




def isWinningState(state):
    for i in range(len(state)):
        num = state[i][0][0]
        for j in range(len(state[i])):
            for k in range(len(state[i][j])):
                if state[i][j][k] != num:
                    return False
    return True

    #     if not np.all(state[i].all() == state[i][0][0], axis=0):
    #         return False
    # return True

def toString(state):
    # return str(state)
    result = ''
    for i in range(len(state)):
        for j in range(len(state[i])):
            for k in range(len(state[i][j])):
                result += str(state[i][j][k])

    # Make a canonical representation starting with the first 0
    point = result.index('0')
    result = result[point:] + result[:point]

    return result

def solve(state):
    execution_count = 0
    visited = {}
    not_visited_count = 0
    frontier = []
    frontier.append((np.copy(state), []))
    while len(frontier) > 0:
        curr, path = frontier[0]
        execution_count += 1
        if execution_count % 1000 == 0:
            print execution_count, len(visited), len(path), not_visited_count, "%.4f" % (float(not_visited_count) / len(visited))
        # print curr
        frontier = frontier[1:]
        if isWinningState(curr):
            print "WINNER!"
            print curr
            print path
            return True
        for i in range(NUMBER_ACTIONS):
            new_state = changeState(np.copy(curr), i)
            s = toString(new_state)
            # print s
            if s not in visited:
                frontier.append((new_state, path + [i]))
                # print frontier
                visited[s] = True
            else:
                not_visited_count += 1


def changeState(state, action):
    if action == TOP_CLOCKWISE:
        state[TOP] = np.rot90(state[TOP], k=-1)
        tmp1 = state[FRONT][TOP_ROW, LEFT_COL]
        tmp2 = state[FRONT][TOP_ROW, RIGHT_COL]

        state[FRONT][TOP_ROW, LEFT_COL] = state[RIGHT][TOP_ROW, LEFT_COL]
        state[FRONT][TOP_ROW, RIGHT_COL] = state[RIGHT][TOP_ROW, RIGHT_COL]

        state[RIGHT][TOP_ROW, LEFT_COL] = state[BACK][TOP_ROW, LEFT_COL]
        state[RIGHT][TOP_ROW, RIGHT_COL] = state[BACK][TOP_ROW, RIGHT_COL]

        state[BACK][TOP_ROW, LEFT_COL] = state[LEFT][TOP_ROW, LEFT_COL]
        state[BACK][TOP_ROW, RIGHT_COL] = state[LEFT][TOP_ROW, RIGHT_COL]

        state[LEFT][TOP_ROW, LEFT_COL] = tmp1
        state[LEFT][TOP_ROW, RIGHT_COL] = tmp2

    elif action == TOP_COUNTER:
        state[TOP] = np.rot90(state[TOP], k=1)
        tmp1 = state[FRONT][TOP_ROW, LEFT_COL]
        tmp2 = state[FRONT][TOP_ROW, RIGHT_COL]

        state[FRONT][TOP_ROW, LEFT_COL] = state[LEFT][TOP_ROW, LEFT_COL]
        state[FRONT][TOP_ROW, RIGHT_COL] = state[LEFT][TOP_ROW, RIGHT_COL]

        state[LEFT][TOP_ROW, LEFT_COL] = state[BACK][TOP_ROW, LEFT_COL]
        state[LEFT][TOP_ROW, RIGHT_COL] = state[BACK][TOP_ROW, RIGHT_COL]

        state[BACK][TOP_ROW, LEFT_COL] = state[RIGHT][TOP_ROW, LEFT_COL]
        state[BACK][TOP_ROW, RIGHT_COL] = state[RIGHT][TOP_ROW, RIGHT_COL]

        state[RIGHT][TOP_ROW, LEFT_COL] = tmp1
        state[RIGHT][TOP_ROW, RIGHT_COL] = tmp2

    elif action == FRONT_CLOCKWISE:
        tmp = state[FRONT][0, 0]
        state[FRONT][0, 0] = state[FRONT][1, 0]
        state[FRONT][1, 0] = state[FRONT][1, 1]
        state[FRONT][1, 1] = state[FRONT][0, 1]
        state[FRONT][0, 1] = tmp

        tmp1 = state[TOP][BOTTOM_ROW, LEFT_COL]
        tmp2 = state[TOP][BOTTOM_ROW, RIGHT_COL]

        state[TOP][BOTTOM_ROW, LEFT_COL] = state[LEFT][BOTTOM_ROW, RIGHT_COL]
        state[TOP][BOTTOM_ROW, RIGHT_COL] = state[LEFT][TOP_ROW, RIGHT_COL]

        state[LEFT][TOP_ROW, RIGHT_COL] = state[BOTTOM][TOP_ROW, LEFT_COL]
        state[LEFT][BOTTOM_ROW, RIGHT_COL] = state[BOTTOM][TOP_ROW, RIGHT_COL]

        state[BOTTOM][TOP_ROW, LEFT_COL] = state[RIGHT][BOTTOM_ROW, LEFT_COL]
        state[BOTTOM][TOP_ROW, RIGHT_COL] = state[RIGHT][TOP_ROW, LEFT_COL]

        state[RIGHT][TOP_ROW, LEFT_COL] = tmp1
        state[RIGHT][BOTTOM_ROW, LEFT_COL] = tmp2

    elif action == FRONT_COUNTER:
        tmp = state[FRONT][0, 0]
        state[FRONT][0, 0] = state[FRONT][0, 1]
        state[FRONT][0, 1] = state[FRONT][1, 1]
        state[FRONT][1, 1] = state[FRONT][1, 0]
        state[FRONT][1, 0] = tmp

        tmp1 = state[TOP][BOTTOM_ROW, LEFT_COL]
        tmp2 = state[TOP][BOTTOM_ROW, RIGHT_COL]

        state[TOP][BOTTOM_ROW, LEFT_COL] = state[RIGHT][TOP_ROW, LEFT_COL]
        state[TOP][BOTTOM_ROW, RIGHT_COL] = state[RIGHT][BOTTOM_ROW, LEFT_COL]

        state[RIGHT][TOP_ROW, LEFT_COL] = state[BOTTOM][TOP_ROW, RIGHT_COL]
        state[RIGHT][BOTTOM_ROW, LEFT_COL] = state[BOTTOM][TOP_ROW, LEFT_COL]

        state[BOTTOM][TOP_ROW, LEFT_COL] = state[LEFT][TOP_ROW, RIGHT_COL]
        state[BOTTOM][TOP_ROW, RIGHT_COL] = state[LEFT][BOTTOM_ROW, RIGHT_COL]

        state[LEFT][TOP_ROW, RIGHT_COL] = tmp2
        state[LEFT][BOTTOM_ROW, RIGHT_COL] = tmp1


    elif action == RIGHT_CLOCKWISE:
        tmp = state[RIGHT][0, 0]
        state[RIGHT][0, 0] = state[RIGHT][1, 0]
        state[RIGHT][1, 0] = state[RIGHT][1, 1]
        state[RIGHT][1, 1] = state[RIGHT][0, 1]
        state[RIGHT][0, 1] = tmp

        tmp1 = state[TOP][TOP_ROW, RIGHT_COL]
        tmp2 = state[TOP][BOTTOM_ROW, RIGHT_COL]

        state[TOP][TOP_ROW, RIGHT_COL] = state[FRONT][TOP_ROW, RIGHT_COL]
        state[TOP][BOTTOM_ROW, RIGHT_COL] = state[FRONT][BOTTOM_ROW, RIGHT_COL]

        state[FRONT][TOP_ROW, RIGHT_COL] = state[BOTTOM][TOP_ROW, RIGHT_COL]
        state[FRONT][BOTTOM_ROW, RIGHT_COL] = state[BOTTOM][BOTTOM_ROW, RIGHT_COL]

        state[BOTTOM][TOP_ROW, RIGHT_COL] = state[BACK][BOTTOM_ROW, LEFT_COL]
        state[BOTTOM][BOTTOM_ROW, RIGHT_COL] = state[BACK][TOP_ROW, LEFT_COL]

        state[BACK][TOP_ROW, LEFT_COL] = tmp2
        state[BACK][BOTTOM_ROW, LEFT_COL] = tmp1


    elif action == RIGHT_COUNTER:
        tmp = state[RIGHT][0, 0]
        state[RIGHT][0, 0] = state[RIGHT][0, 1]
        state[RIGHT][0, 1] = state[RIGHT][1, 1]
        state[RIGHT][1, 1] = state[RIGHT][1, 0]
        state[RIGHT][1, 0] = tmp

        tmp1 = state[TOP][TOP_ROW, RIGHT_COL]
        tmp2 = state[TOP][BOTTOM_ROW, RIGHT_COL]

        state[TOP][TOP_ROW, RIGHT_COL] = state[BACK][BOTTOM_ROW, LEFT_COL]
        state[TOP][BOTTOM_ROW, RIGHT_COL] = state[BACK][TOP_ROW, LEFT_COL]

        state[BACK][TOP_ROW, LEFT_COL] = state[BOTTOM][BOTTOM_ROW, RIGHT_COL]
        state[BACK][BOTTOM_ROW, LEFT_COL] = state[BOTTOM][TOP_ROW, RIGHT_COL]

        state[BOTTOM][TOP_ROW, RIGHT_COL] = state[FRONT][TOP_ROW, RIGHT_COL]
        state[BOTTOM][BOTTOM_ROW, RIGHT_COL] = state[FRONT][BOTTOM_ROW, RIGHT_COL]

        state[FRONT][TOP_ROW, RIGHT_COL] = tmp1
        state[FRONT][BOTTOM_ROW, RIGHT_COL] = tmp2

    return state


def saveImage(state, filename):
    img = Image.new("RGB", (100, 800))
    img_d = ImageDraw.Draw(img)
    size = 50
    y = 0
    for face in state:
        for row in face:
            x = 0
            for col in row:
                # print x, y
                img_d.rectangle((x, y, x + size, y + size), fill=colors[int(col)])
                x += size
            y += size
        y += 20
    img.save(filename)



s = np.array([
    [[YELLOW, RED], [WHITE, YELLOW]],
    [[BLUE, WHITE], [WHITE, YELLOW]],
    [[GREEN, GREEN], [ORANGE, RED]],
    [[ORANGE, YELLOW], [GREEN, GREEN]],
    [[BLUE, ORANGE], [RED, BLUE]],
    [[BLUE, ORANGE], [RED, WHITE]],
    ])


# r.changeState(TOP_COUNTER)
# r.changeState(TOP_CLOCKWISE)
saveImage(s, "test1.png")
solve(s)
# r.changeState(TOP_CLOCKWISE)
# r.changeState(TOP_CLOCKWISE)
# r.changeState(TOP_COUNTER)
# r.changeState(TOP_COUNTER)
# r.changeState(TOP_COUNTER)

# r.changeState(FRONT_CLOCKWISE)
# r.changeState(FRONT_COUNTER)
#
# r.changeState(RIGHT_CLOCKWISE)
# r.changeState(RIGHT_COUNTER)

saveImage(s, "test2.png")

print isWinningState(s)




