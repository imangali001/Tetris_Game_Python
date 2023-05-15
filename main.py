from settings import *
pygame.init()  # это команда, которая запускает pygame

def random_figure():
    n = random.randint(1, 7)
    if n == 1:
        return Figure_1()
    if n == 2:
        return Figure_2()
    if n == 3:
        return Figure_3()
    if n == 4:
        return Figure_4()
    if n == 5:
        return Figure_5()
    if n == 6:
        return Figure_6()
    if n == 7:
        return Figure_7()

def display():
    text = pygame.font.SysFont('serif', 18)
    text_x = text.render('Record: ' + str(n_recort), True, (0, 255, 0))
    text_Max = text.render('Record: ' + str(n_recort), True, (0, 255, 0))
    window.display(text_x)
    window.display(text_Max)
    figure.display()


window = Window()
figure = Figure()
figure_list = [random_figure()]

n_recort = 0

n = 0
n_max = 20
K_blocking_UP = 3
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверить закрытие окна
            pygame.quit()





    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and K_blocking_UP % 3 == 0:  # стрелка вверх
        K_blocking_UP += 1
        figure_list[-1].changes()
    else:
        K_blocking_UP += 1

    if keys[pygame.K_LEFT] and figure_list[-1].side_edge_left():  # стрелка влево
        figure_list[-1].left()

    elif keys[pygame.K_RIGHT] and figure_list[-1].side_edge_right():  # стрелка вправо
        figure_list[-1].right()


    n += 1
    if (keys[pygame.K_DOWN] or n % n_max == 0) and figure_list[-1].bottom_edge():  # стрелка вниз
        figure_list[-1].down()
    elif not figure_list[-1].bottom_edge():
        n_recort = figure.won()
        figure_list += [random_figure()]



    display()
