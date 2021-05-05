from thegame import *
import heapq

SNAKE_CHAR = '+'
EMPTY_CHAR = ' '
WALL_CHAR = '#'
FOOD_CHAR = '@'

def main():
    class Node:
        def __init__(self, position, parent):
            self.position = position
            self.parent = parent

            self.g = 0
            self.h = 0
            self.f = self.g + self.h

    class IAExample:
        def __init__(self):
            self.moves = [RIGHT, DOWN, LEFT, UP]
            self.i = 0
            self.best_path = None

        def choose_next_move(self, state):
            grid, score, alive, head = state
            print("Choosing next move")

            if not self.best_path:
                self.best_path = astar(state)

            next_node = self.best_path.pop()
            next_pos = next_node.position

            next_mov_bool = []

            for i in range(len(next_pos)):
                next_mov_bool.append(next_pos[i]-head[i])
            print(next_mov_bool)

            print(next_mov_bool)

            if next_mov_bool[0] == 0:
                if next_mov_bool[1] == 1:
                    next_move = self.moves[0]
                elif next_mov_bool[1] == -1:
                    next_move = self.moves[2]
                else:
                    print("Problem in moves")
            elif next_mov_bool[0] == 1:
                next_move = self.moves[1]
            elif next_mov_bool[0] == 1:
                next_move = self.moves[3]
            else:
                print("Problem in moves")

            return next_move

    def astar(state):
        print("Starting A* search")
        grid, score, alive, head = state
        closed_list = []
        open_list = []
        head_node = Node(head, None)
        food_node = Node(game.food, None)
        open_list.append(head_node)

        while open_list:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node.position == food_node.position:
                path = []
                while current_node.parent is not None:
                    path.append(current_node)
                    current_node = current_node.parent
                return path

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if grid[node_position[0]][node_position[1]] == SNAKE_CHAR or \
                        grid[node_position[0]][node_position[1]] == WALL_CHAR:
                    continue

                # Create new node
                new_node = Node(node_position, current_node)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child.position == closed_child.position:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = (child.position[0] - food_node.position[0]) + (
                        child.position[1] - food_node.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child.position == open_node.position and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


    agent = IAExample()  # None for interactive GUI
    game = GUISnakeGame()
    game.init_pygame()

    while game.is_running():
        game.next_tick(agent)

    game.cleanup_pygame()

    #game = TrainingSnakeGame(agent)
    #game.start_run()

    #while game.is_alive():
    #    game.next_tick()


if __name__ == '__main__':
    main()
