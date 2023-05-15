import pygame
import random


class Window:
    # Цвета (R, G, B)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # окно
    __size = 400, 700
    __FPS = 60

    screen = pygame.display.set_mode(__size)  # Дисплей
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    def set_size(self):
        return self.__size

    def display(self, text, text_Max):
        pygame.display.update()
        self.screen.fill((0, 0, 0))

        self.screen.blit(text, (10, 10))
        self.screen.blit(text_Max, (10, 30))

        pygame.time.delay(self.__FPS)





class Cube(Window):
    __size_cube = 20, 20

    def __init__(self, coordinates_x, coordinates_y, difference_x=0, difference_y=0):  # coordinates:(x, y), difference
        self.difference_x = difference_x
        self.difference_y = difference_y
        self.__coordinates_x_y = [coordinates_x, coordinates_y]
        self.__coordinates = (coordinates_x + difference_x * self.__size_cube[0],
                              coordinates_y + difference_y * self.__size_cube[1],
                              self.__size_cube[0], self.__size_cube[1])

    def set_cube(self):
        return self.__coordinates

    def right_cube(self):
        self.__coordinates_x_y[0] += self.__size_cube[0]
        self.changes_coordinates(self.difference_x, self.difference_y)

    def left_cube(self):
        self.__coordinates_x_y[0] -= self.__size_cube[0]
        self.changes_coordinates(self.difference_x, self.difference_y)

    def down_cube(self):
        self.__coordinates_x_y[1] += self.__size_cube[1]
        self.changes_coordinates(self.difference_x, self.difference_y)

    def changes_coordinates(self, difference_x, difference_y):
        self.difference_x = difference_x
        self.difference_y = difference_y
        self.__coordinates = (self.__coordinates_x_y[0] + difference_x * self.__size_cube[0],
                              self.__coordinates_x_y[1] + difference_y * self.__size_cube[1],
                              self.__size_cube[0], self.__size_cube[1])

    def display(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.__coordinates)





class Figure(Window):
    bloc = 1
    n = 1
    coordinates_x = 200
    coordinates_y = 100
    y_min = 130
    list_cube = []

    def changes_figure(self, cube_difference, cube):
        self.n += 1
        if self.n == len(cube_difference) + 1:
            self.n = 1
        for n_i, cube_i in enumerate(cube):
            cube_i.changes_coordinates(cube_difference[self.n][n_i]['x'],
                                       cube_difference[self.n][n_i]['y'])

    def edge_bottom(self, coordinates):
        for i_cube in self.list_cube[:-4]:
            cube_set = i_cube.set_cube()
            if coordinates[1] + cube_set[3] == cube_set[1] and coordinates[0] == cube_set[0]:
                return True

    def edge_side_left(self, coordinates):
        for i_cube in self.list_cube[:-4]:
            cube_set = i_cube.set_cube()
            if coordinates[0] == cube_set[0] + cube_set[2] and coordinates[1] == cube_set[1]:
                return True

    def edge_side_right(self, coordinates):
        for i_cube in self.list_cube[:-4]:
            cube_set = i_cube.set_cube()
            if coordinates[0] + cube_set[2] == cube_set[0] and coordinates[1] == cube_set[1]:
                return True

    def edge_changes(self, cube_x_y):
        seze_x = self.set_size()[0]
        if cube_x_y[0] == 0 or cube_x_y[0] + cube_x_y[2] == seze_x:
            return False
        for cube in self.list_cube[:-4]:
            n_cor = cube.set_cube()
            if (cube_x_y[0] + cube_x_y[2] == n_cor[0] and cube_x_y[1] == n_cor[1]) or (cube_x_y[0] == n_cor[0] + cube_x_y[2] and cube_x_y[1] == n_cor[1]) or (cube_x_y[1] + cube_x_y[3] == n_cor[1] and cube_x_y[0] == n_cor[0]):
                return False
        return True

    def won(self):
        n = dict()
        for cube in self.list_cube:
            size_cube = cube.set_cube()[2]
            n_cube = cube.set_cube()
            if n.get(n_cube[1], {}) == {}:
                n[n_cube[1]] = 1
            else:
                n[n_cube[1]] += 1

        n_list = []
        for n_i, i in n.items():
            if i == self.set_size()[0] // size_cube:
                n_list += [n_i]

        n_pop = []
        for cube in self.list_cube:
            cube_y = cube.set_cube()[1]
            for i in n_list:
                if cube_y == i:
                    n_pop += [cube]
                if cube_y < i:
                    cube.down_cube()

        for cube in n_pop:
            self.list_cube.remove(cube)

        if n_list != []:
            return 1
        return 0

    def lose(self):
        if self.list_cube != [] and self.y_min > self.list_cube[:-4][-1].set_cube()[1]:
            print(';oj;odjiosjid', self.list_cube)
            Figure.list_cube = []
            return True



    def display(self):
        for cube in self.list_cube:
            cube.display()









class Figure_1(Figure):
    def __init__(self):
        super().__init__()
        self.cube = [Cube(self.coordinates_x, self.coordinates_y),
                     Cube(self.coordinates_x, self.coordinates_y, difference_y=1),
                     Cube(self.coordinates_x, self.coordinates_y, difference_x=1),
                     Cube(self.coordinates_x, self.coordinates_y, difference_x=1, difference_y=1)]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        pass





class Figure_2(Figure):
    bloc = 2
    cube_difference = {1: [{'x': 0, 'y': -1},
                           {'x': 0, 'y': 0},
                           {'x': 0, 'y': 1},
                           {'x': 0, 'y': 2}],

                       2: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': 2, 'y': 0}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)





class Figure_3(Figure):
    cube_difference = {1: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': -1, 'y': 1}],

                       2: [{'x': 0, 'y': -1},
                           {'x': 0, 'y': 0},
                           {'x': 0, 'y': 1},
                           {'x': 1, 'y': 1}],

                       3: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': 1, 'y': -1}],

                       4: [{'x': -1, 'y': -1},
                           {'x': 0, 'y': -1},
                           {'x': 0, 'y': 0},
                           {'x': 0, 'y': 1}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)





class Figure_4(Figure):
    cube_difference = {1: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': 1, 'y': 1}],

                       2: [{'x': 0, 'y': -1},
                           {'x': 0, 'y': 0},
                           {'x': 0, 'y': 1},
                           {'x': -1, 'y': 1}],

                       3: [{'x': -1, 'y': -1},
                           {'x': -1, 'y': 0},
                           {'x': 0, 'y': 0},
                           {'x': 1, 'y': 0}],

                       4: [{'x': 0, 'y': -1},
                           {'x': 1, 'y': -1},
                           {'x': 0, 'y': 0},
                           {'x': 0, 'y': 1}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)





class Figure_5(Figure):
    cube_difference = {1: [{'x': 0, 'y': -1},
                           {'x': -1, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': 0, 'y': 0}],

                       2: [{'x': 1, 'y': 0},
                           {'x': 0, 'y': -1},
                           {'x': 0, 'y': 1},
                           {'x': 0, 'y': 0}],

                       3: [{'x': 0, 'y': 1},
                           {'x': -1, 'y': 0},
                           {'x': 1, 'y': 0},
                           {'x': 0, 'y': 0}],

                       4: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': -1},
                           {'x': 0, 'y': 1},
                           {'x': 0, 'y': 0}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)





class Figure_6(Figure):
    cube_difference = {1: [{'x': 1, 'y': 0},
                           {'x': 0, 'y': 1},
                           {'x': -1, 'y': 1},
                           {'x': 0, 'y': 0}],

                       2: [{'x': 0, 'y': -1},
                           {'x': 1, 'y': 0},
                           {'x': 1, 'y': 1},
                           {'x': 0, 'y': 0}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)





class Figure_7(Figure):
    cube_difference = {1: [{'x': 0, 'y': -1},
                           {'x': -1, 'y': 0},
                           {'x': -1, 'y': 1},
                           {'x': 0, 'y': 0}],

                       2: [{'x': -1, 'y': 0},
                           {'x': 0, 'y': 1},
                           {'x': 1, 'y': 1},
                           {'x': 0, 'y': 0}]}

    def __init__(self):
        super().__init__()
        difference = self.cube_difference[self.n]
        self.cube = [Cube(self.coordinates_x, self.coordinates_y, difference[0]['x'], difference[0]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[1]['x'], difference[1]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[2]['x'], difference[2]['y']),
                     Cube(self.coordinates_x, self.coordinates_y, difference[3]['x'], difference[3]['y'])]
        self.list_cube += self.cube

    def right(self):
        for cube in self.cube:
            cube.right_cube()

    def left(self):
        for cube in self.cube:
            cube.left_cube()

    def down(self):
        for cube in self.cube:
            cube.down_cube()

    def bottom_edge(self):
        seze_y = self.set_size()[1]
        for cube in self.cube:
            cube_set = cube.set_cube()
            if cube_set[1] + cube_set[3] >= seze_y or self.edge_bottom(cube_set):
                return False
        return True

    def side_edge_left(self):
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] == 0 or self.edge_side_left(set_cube):
                return False
        return True

    def side_edge_right(self):
        seze_x = self.set_size()[0]
        for cube in self.cube:
            set_cube = cube.set_cube()
            if set_cube[0] + set_cube[2] == seze_x or self.edge_side_right(set_cube):
                return False
        return True

    def changes(self):
        n_cor = self.cube[2].set_cube()

        if self.edge_changes(n_cor):
            self.changes_figure(self.cube_difference, self.cube)
