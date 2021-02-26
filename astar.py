import numpy as np

x = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def search(matrix, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    goal = Node(None, tuple(end))
    goal.g = goal.h = goal.f = 0
    not_visit_list = []
    visited_list = []
    not_visit_list.append(start_node)
    outer_iterations = 0
    max_iterations = (len(matrix) // 2) ** 10
    while len(not_visit_list) > 0:
        outer_iterations += 1
        current_node = not_visit_list[0]
        current_index = 0
        for index, item in enumerate(not_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return matrix, None
            # return return_path(current_node, matrix)

        
        not_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == goal:
            return return_path(current_node, matrix)

        children = expand(current_node, matrix)
        for child in children:
            if not visited(child, visited_list):
                child.g = current_node.g + cost
                child.h = heuristic(child, goal)
                child.f = child.g + child.h
                if not better_path(child, not_visit_list):
                    not_visit_list.append(child)
    return matrix, None


def expand(parent, matrix):
    rows, columns = np.shape(matrix)
    directions = [[-1, 0],  # go up
                  [0, -1],  # go left
                  [1, 0],  # go down
                  [0, 1]]  # go right
    children = []
    for direction in directions:
        position = (parent.position[0] + direction[0], parent.position[1] + direction[1])
        if not ((position[0] > (rows - 1) or position[0] < 0 or position[1] > (columns - 1) or position[1] < 0) or \
                matrix[position[0]][position[1]] == 1):
            child = Node(parent, position)
            children.append(child)
    return children


def visited(child, visited_list):
    for node in visited_list:
        if node == child:
            return True
    return False


def better_path(child, yet_to_visit_list):
    exist = False
    for node in yet_to_visit_list:
        if node == child:
            exist |= node.g < child.g
    return exist


def heuristic(node, goal):
    return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])


def return_path(current_node, result):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    for i in range(1, len(path) - 1):
        result[path[i][0]][path[i][1]] = 3
    return result, path


def get_color_coded_str(i):
    return "\033[3{}m{}\033[0m".format(i + 1, i)


def get_color_coded_background(i):
    if i == 3:
        return "\033[4{}m {} \033[0m".format(i + 3, i)
    if i == 1:
        return "\033[4{}m {} \033[0m".format(i + 0, i)
    if i == 5:
        return "\033[4{}m {} \033[0m".format(i + -3, i)
    if i == 6:
        return "\033[4{}m {} \033[0m".format(i + 1, i)
    return "\033[4{}m {} \033[0m".format(i + 10, i)


def print_a_ndarray(matrix, row_sep=" "):
    n, m = matrix.shape
    fmt_str = "\n".join([row_sep.join(["{}"] * m)] * n)
    print(fmt_str.format(*matrix.ravel()))


def convert(matrix):
    start = [0, 0]  # starting position
    end = [0, 0]    # ending position
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == 'G':
                x[i][j] = 5
                end = [i, j]
            elif matrix[i][j] == 'P':
                x[i][j] = 6
                start = [i, j]
            else:
                x[i][j] = int(matrix[i][j])
    return start, end, x


if __name__ == '__main__':
    matrix = np.loadtxt("matrix.txt", dtype='str', delimiter=' ')
    start, end, matrix = convert(matrix)
    back_map_modified = np.vectorize(get_color_coded_background)(matrix)
    print_a_ndarray(back_map_modified, row_sep="")
    cost = 1  # cost per movement
    map, path = search(matrix, cost, start, end)
    if path:
        back_map_modified = np.vectorize(get_color_coded_background)(map)
        print("----------------------------------------")
        print("A path has been found : ")
        print(path)
        print()
        print_a_ndarray(back_map_modified, row_sep="")
    else:
        print("----------------------------------------")
        print("Not found any path")
