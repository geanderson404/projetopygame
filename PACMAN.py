import pygame
from pygame.locals import *
from sys import exit

    
pygame.init()

YELLOW = (255, 255, 0)

### Controle tamanho janela e titulo que fica no topo da janela
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('PACMAN')
###

### Controlando a tela
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit() 
    pygame.draw.circle(tela, YELLOW, (320, 240), 25)
            
    pygame.display.update()
###