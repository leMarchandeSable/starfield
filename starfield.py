import pygame
import numpy as np
import os
import time


class Star:
    def __init__(self):
        # les coords vont entre -1 et 1
        self.x = np.random.random() * 2 - 1
        self.y = np.random.random() * 2 - 1
        self.z = np.random.rand() * 2

        self.z_temp = self.z

    def translate(self, x, y):
        tx = int(x + L/2)
        ty = int(y + H/2)
        return tx, ty

    def rayon(self, n):
        # n est la grosseur max des étoiles
        # 1.9 est le delta z (2 - 0.1)
        i = 0
        while True:
            if self.z < 0.1 + i * 1.9 / n:
                r = i
                break
            i += 1
        return r

    def update(self, speed):
        if self.z < 0.1:
            # si l'étoile sort du cadre on en recrée une
            self.x = np.random.random() * 2 - 1
            self.y = np.random.random() * 2 - 1
            self.z = np.random.rand() * 2

            # on actualise z_temp
            self.z_temp = self.z

        else:
            self.z -= 0.004 * speed

    def show(self):

        # on calcul leurs position en fonction du temps (z)
        # z varie entre 0.1 et 2
        sx = self.x / self.z * L/2
        sy = self.y / self.z * H/2

        # les coords sx vont entre 0 et L
        sxt, syt = self.translate(sx, sy)

        # on affiche les étoiles avec une taille qui dépend de z
        # r varie entre 0 et 4
        r = self.rayon(4)
        pygame.draw.circle(surface, blanc, (sxt, syt), r)

        # on calcul les positions précedentes des étoiles
        sx_temp = self.x / self.z_temp * L/2
        sy_temp = self.y / self.z_temp * H/2

        # les coords sx_temp transposé
        sxt_temp, syt_temp = self.translate(sx_temp, sy_temp)

        # on affiche les trainées
        pygame.draw.line(surface, blanc, (sxt, syt), (sxt_temp, syt_temp), 1)

        # on actualise z_temp pas a chaque fois (timer du bled)
        if np.random.rand() > 0.97:
            self.z_temp = self.z


def save(surface, doc_name):

    path = 'C:/Users/simon/Documents/IPSA/A2/python/Pygame/'

    if doc_name not in os.listdir(path):
        os.mkdir(doc_name)
    else:
        os.chdir(path + doc_name)
        pygame.image.save(surface, str(round(time.time(), 1)) + ".jpg")


# ----------------------------------------------------------------------------------------------------------------------
# initialisation constante + environnement
H = 600
L = 800
stars = [Star() for i in range(400)]

blanc = (255, 255, 255)
gris = (150, 150, 150)
noir = (0, 0, 0)
rouge = (255, 0, 0)
bleu = (0, 0, 255)
vert = (0, 255, 0)

# initialisation fenetre
pygame.init()
pygame.display.set_caption("StarField")
surface = pygame.display.set_mode((L, H))

# ----------------------------------------------------------------------------------------------------------------------
# boucle infinie
launched = 1
while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = 0

    surface.fill(noir)

    # on récupère la position verticale de la souris
    speed = (H - pygame.mouse.get_pos()[1]) * 2 / H

    # on actualise toute les étoiles
    for star in stars:
        star.update(speed)
        star.show()

    save(surface, 'starfield')

    pygame.display.flip()
