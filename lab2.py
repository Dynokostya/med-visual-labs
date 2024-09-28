import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Визначення розмірів вікна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Перетворення декартових координат у циліндричні
def cartesian_to_cylindrical(x, y, z):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta, z

# Малюємо осі координат
def draw_axes():
    glBegin(GL_LINES)
    
    # Вісь X (Червона)
    glColor3f(1, 0, 0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    
    # Вісь Y (Зелена)
    glColor3f(0, 1, 0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    
    # Вісь Z (Синя)
    glColor3f(0, 0, 1)
    glVertex3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, 0.0, 1.0)
    
    glEnd()

# Малюємо коло (примітив)
def draw_circle(radius):
    glBegin(GL_LINE_LOOP)
    num_segments = 100
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments  # кут
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex3f(x, y, 0)
    glEnd()

# Ініціалізація налаштувань OpenGL
def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Встановлення чорного фону
    glMatrixMode(GL_PROJECTION)       # Переключення на матрицю проекції
    glLoadIdentity()                  # Скидання матриці проекції
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)  # Встановлення перспективи
    glMatrixMode(GL_MODELVIEW)        # Повернення до матриці моделі
    glEnable(GL_DEPTH_TEST)           # Увімкнення тестування глибини

# Головний цикл програми
def main():
    pygame.init()  # Ініціалізація pygame
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)  # Створення вікна
    init_opengl()  # Ініціалізація OpenGL

    # Початкова позиція камери
    glTranslatef(0.0, 0.0, -5)  # Переміщення камери назад

    # Головний цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Вихід з циклу при закритті вікна
                running = False

        # Очищення екрану
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищення буферів кольору і глибини

        # Малювання декартової системи координат
        draw_axes()

        # Малювання кола
        draw_circle(1.0)

        # Оновлення дисплея
        pygame.display.flip()
        pygame.time.wait(10)  # Затримка для контролю частоти кадрів

    pygame.quit()  # Завершення pygame


if __name__ == "__main__":
    main()
