from settings import *
pygame.init()  # это команда, которая запускает pygame

def random_figure():
    n = random.randint(1, 8)
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
    if n == 8:
        return Bomba()

def display(record_max, n_recort, FPS):
    text = pygame.font.SysFont('serif', 18)
    text_x = text.render('Score: ' + str(n_recort), True, (0, 255, 0))
    text_Max = text.render('Record: ' + str(record_max), True, (0, 255, 0))
    window.display(text_x, text_Max, FPS)
    figure.display()


pygame.mixer.music.load('Music/zvuk-tetrisa-na-konsoli.mp3')
pygame.mixer.music.play(-1)

FPS = 0
while True:
    window = Window()
    figure = Figure()
    figure_list = [random_figure()]

    n_record = 0
    record_max_with = open('Record.txt', 'r')
    record_max = record_max_with.read()
    record_max_with.close()

    n = 0
    n_max = 5
    K_blocking_UP = 3
    # FPS = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверить закрытие окна
                pygame.quit()

        FPS += 0.1
        n += 1



        if n % 5 == 0:
            keys = pygame.key.get_pressed()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and K_blocking_UP % 3 == 0 and len(figure_list[-1].cube) != 1:  # стрелка вверх
            K_blocking_UP += 1
            figure_list[-1].changes()
        else:
            K_blocking_UP += 1

        if keys[pygame.K_LEFT] and figure_list[-1].side_edge_left() and len(figure_list[-1].cube) != 1:  # стрелка влево
            figure_list[-1].left()

        elif keys[pygame.K_RIGHT] and figure_list[-1].side_edge_right() and len(figure_list[-1].cube) != 1:  # стрелка вправо
            figure_list[-1].right()

        if (keys[pygame.K_DOWN] or n % n_max == 0) and figure_list[-1].bottom_edge():  # стрелка вниз
            figure_list[-1].down()



        if not figure_list[-1].bottom_edge():
            n_record += figure.won()
            figure_list += [random_figure()]
            if int(record_max) < n_record:
                record_max_with = open('Record.txt', 'w')
                record_max_with.write(str(n_record))
                record_max_with.close()
            if figure.lose():
                n_record = 0
                break

        display(record_max, n_record, FPS)


