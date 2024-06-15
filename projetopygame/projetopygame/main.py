import pygame
from pygame.locals import *
from pygame import mixer
import random
import math
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
relogio = pygame.time.Clock()
largura = 600
altura = 700
pontos = 0
velocidade_jogo = 10
'''def exibe_mensagem(msg,tamanho,cor):
    fonte = pygame.font.SysFont('comicsanssms',tamanho,True,False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem,True,cor)
    return texto_formatado'''

# definir fontes:
fonte15 = pygame.font.SysFont('constantia', 15)
fonte30 = pygame.font.SysFont('constantia', 30)
fonte40 = pygame.font.SysFont('constantia', 40)
fonte_pontuacao = pygame.font.SysFont('Showcard Gothic',20)
base_font = pygame.font.Font(None,32)
user_text = ' '

# sons
son_explosao = pygame.mixer.Sound('sons/explosion.wav')
# aumentar volume
son_explosao.set_volume(1)

son_explosao2 = pygame.mixer.Sound('img/explosion2.wav')
son_explosao2.set_volume(1)

son_laser = pygame.mixer.Sound('img/laser.wav')
son_laser.set_volume(1)

son_destruicao = pygame.mixer.Sound('img/scream_horror1.mp3')
son_destruicao.set_volume(1)


# cores 
vermelho = (255, 0, 0)
verde = (0, 255, 0)
branco = (255, 255, 255)

# variáveis do jogo
alien_cooldown = 1000
ultimo_tiro_alien = pygame.time.get_ticks()
tempo_proximo_alien = pygame.time.get_ticks()
contagem = 3  # 3 segundos para comecar o jogo
ultima_contagem = pygame.time.get_ticks()
game_over = 0  # 0 jogo nao acabou, 1 = ganhou , -1 perdeu
menu = True

# criacao da tela de fundo
# Define a janela do jogo com as dimensões largura e altura
display = pygame.display.set_mode((largura, altura))

tela_inicio = pygame.display.set_mode((largura, altura))


# Função para desenhar texto na tela
def draw_texto(texto, fonte, cor_texto, x, y):
    img = fonte.render(texto, True, cor_texto)  # Renderiza o texto com a fonte e a cor especificadas
    display.blit(img, (x, y))  # Desenha o texto na tela nas coordenadas (x, y)

# Carrega a imagem de fundo da tela e redimensiona de acordo com a largura e altura da tela
bg = pygame.image.load('img/bg (1).png')
bg = pygame.transform.scale(bg, (largura, altura))
bg_altura = bg.get_height()  # Obtém a altura da imagem de fundo
tiles = math.ceil(altura / bg_altura) + 1  # Calcula o número de vezes que a imagem de fundo cabe na tela verticalmente
rolagem = 0  # Inicializa a variável de rolagem do fundo
#botao reset

start_img = pygame.image.load('img/start_btn (1).png')
start_img = pygame.transform.scale(start_img, (100, 50)) #diminuir tamanho do resetar_img
exit_img = pygame.image.load('img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img, (100, 50)) #diminuir tamanho do exit_img
resetar_img = pygame.image.load('img/restart.png')

def resetar_game(): 
    global pontos, contagem
    
    contagem = 3
    pontos = 0
    nave = Nave(int(largura / 2), altura - 100, 3)
    nave_grupo.empty()
    nave_grupo.add(nave)
    navesviloes_grupo.empty()
    planeta = Planeta(5)
    planeta_grupo.empty()
    planeta_grupo.add(planeta)
    alien = Navesviloes(random.randint(50, largura - 50), -50)  # Cria um novo vilão
    navesviloes_grupo.add(alien)
    balas_grupo.empty()
    viloes_balas_grupo.empty()
    
    return pontos, nave, planeta, contagem, alien

class Botao:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect() #cria um retangulo
        self.rect.topleft = (x , y) 
    def draw(self):
        acao = False
        #obter posicao do mouse
        pos = pygame.mouse.get_pos() #retornar coodernada x e y do mouse
        #checar se o mouse esta sobre o botao
        if self.rect.collidepoint(pos): #verifica se o mouse esta sobre o botao
            if pygame.mouse.get_pressed()[0] == 1: #lista que contem o click esquerdo e o direito  para o botao esquerdo o indice e 0 se el for igual a 1 ele foi clicado
                acao = True 
            
        #desenha botao
        display.blit(self.image, (self.rect.x, self.rect.y)) #desenha o botao
        return acao
  
            
        

# classes
class Nave(pygame.sprite.Sprite):  # Define a classe Nave, que herda da classe pygame.sprite.Sprite
    def __init__(self, x, y, saude):  # Método de inicialização da classe, recebe coordenadas x e y e a saúde da nave
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        
        self.image = pygame.image.load('img/principal.png').convert_alpha()  # Carrega a imagem da nave com transparência
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona a imagem da nave
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da nave
        self.rect.centerx = x 
        self.rect.centery = y # Define a posição inicial da nave
        self.mask = pygame.mask.from_surface(self.image)
        self.saude_incial = saude  # Define a saúde inicial da nave
        self.saude_restante = saude  # Define a saúde restante da nave
        self.ultimo_tiro = pygame.time.get_ticks()  # Guarda o tempo do último disparo da nave
        
    def update(self):  # Método para atualizar a nave
        velocidade = 10  # Define a velocidade de movimento da nave
        game_over = 0  # Inicializa a variável de controle do estado do jogo
        cooldown = 500  # Define o tempo de cooldown para os tiros da nave
        key = pygame.key.get_pressed()  # Obtém as teclas pressionadas

        # Movimentação da nave
        if key[pygame.K_a] and self.rect.left > 0:  # Move a nave para a esquerda
            self.rect.x -= velocidade
        if key[pygame.K_d] and self.rect.right <= largura:  # Move a nave para a direita
            self.rect.x += velocidade
        if key[pygame.K_w] and self.rect.top > 0:  # Move a nave para cima
            self.rect.y -= velocidade
        if key[pygame.K_s] and self.rect.bottom < altura - 60:  # Move a nave para baixo
            self.rect.y += velocidade
        
        tempo_atual = pygame.time.get_ticks()  # Obtém o tempo atual do jogo

        # Disparo de tiros
        if key[pygame.K_SPACE] and tempo_atual - self.ultimo_tiro > cooldown:  # Dispara um tiro
            son_laser.play()  # Toca o som de disparo de laser
            balas = Balas(self.rect.centerx, self.rect.top)  # Cria um objeto de bala
            balas_grupo.add(balas)  # Adiciona a bala ao grupo de balas
            self.ultimo_tiro = tempo_atual  # Atualiza o tempo do último disparo

        self.mask = pygame.mask.from_surface(self.image)  # Define a máscara de colisão da nave

        if pygame.sprite.spritecollide(self,planeta_grupo,False,pygame.sprite.collide_mask):
            if key[pygame.K_s]:
                 self.rect.y -= velocidade #nao pode ir para baixo
            



        # Verifica se a nave foi destruída
        if self.saude_restante <= 0:
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)  # Cria uma explosão
            explosao_grupo.add(explosao)  # Adiciona a explosão ao grupo de explosões
            self.kill()  # Remove a nave
            game_over = -1  # Define que o jogo acabou
         


        if pygame.sprite.spritecollide(self,planeta_grupo,False,pygame.sprite.collide_mask):
            self.rect.center = [self.rect.centerx, self.rect.centery]
        
        
        

        # Verifica colisão com inimigos
        if pygame.sprite.spritecollide(self, navesviloes_grupo, False, pygame.sprite.collide_mask):
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)  # Cria uma explosão
            explosao_grupo.add(explosao)  # Adiciona a explosão ao grupo de explosões
            self.kill()  # Remove a nave
            nave.kill()
            game_over = -1  # Define que o jogo acabou

        return game_over  # Retorna o estado do jogo

        
     
    def desenho_barrasaude(self):  # Método para desenhar a barra de saúde da nave na tela
        # Desenha a barra de saúde
        pygame.draw.rect(display, vermelho, (10, altura - 50, 100, 15))  # Desenha o fundo vermelho da barra de saúde
        if self.saude_restante > 0:  # Verifica se a saúde restante é maior que zero
            # Desenha a barra de saúde verde proporcional à saúde restante
            pygame.draw.rect(display, verde, (10, altura - 50, int(100 * (self.saude_restante / self.saude_incial)), 15))
        # Desenha o texto "SAÚDE"
        draw_texto('SAÚDE  NAVE', fonte15, branco, 5, altura - 30)


class Planeta(pygame.sprite.Sprite):  # Define a classe Balas, que herda da classe pygame.sprite.Sprite
    def __init__(self,saude):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.image = pygame.image.load('img/planeta.png')  # Carrega a imagem da bala
        self.image = pygame.transform.scale(self.image, (600, 300 )) 
        #self.image = pygame.transform.scale(self.image, (700, 300))
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da bala
        self.rect.x = largura // 2 - self.rect.width // 2 # Centraliza horizontalmente
        self.rect.y = altura - self.rect.height // 3 # Define a posição inicial da bala
        self.planeta_velocidade = 0.01 
        self.mask = pygame.mask.from_surface(self.image)
        self.saude_planetainicial = saude
        self.saude_planetrestante = saude
        self.inavdiu = False
    def update(self):
        global pontos
        global game_over
        if pygame.sprite.spritecollide(self,navesviloes_grupo,True,pygame.sprite.collide_mask):
            
            self.saude_planetrestante -= 1
        if self.saude_planetrestante<= 0:
          
            game_over = -2  # Define que o jogo acabou
        
         

        
            
        pygame.draw.rect(display, vermelho, (self.rect.x + 20, (self.rect.top - 570 ), (self.rect.width - 100)//4,  15))
        if self.saude_planetrestante > 0:  # Verifica se a saúde
             pygame.draw.rect(display, verde, (self.rect.x + 20, (self.rect.top - 570 ), int((self.rect.width - 100)//4*(self.saude_planetrestante/self.saude_planetainicial)),  15))
        draw_texto('SAÚDE PLANETA', fonte15, branco, 5, altura - 650)
            

        return game_over
            
        

         
        

    

        
        



class Balas(pygame.sprite.Sprite):  # Define a classe Balas, que herda da classe pygame.sprite.Sprite
    def __init__(self,x,y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.image = pygame.image.load('img/bullet.png')  # Carrega a imagem da bala
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da bala
        self.rect.center = [x, y]  # Define a posição inicial da bala

    def update(self):  # Método para atualizar a bala
        self.rect.y -= 5  # Move a bala para cima
        if self.rect.bottom < 0:  # Verifica se a bala saiu da tela
            self.kill()  # Remove a bala do jogo
        if pygame.sprite.spritecollide(self, navesviloes_grupo, True):  # Verifica colisão com inimigos
            self.kill()  # Remove a bala do jogo
            son_explosao.play()  # Toca o som de explosão
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 2)  # Cria uma explosão
            explosao_grupo.add(explosao)  # Adiciona a explosão ao grupo de explosões
            global pontos
            pontos += 1  # Incrementa a pontuação
        
        def resetar_bala(self):
           self.bala = None 



class Navesviloes(pygame.sprite.Sprite):  # Define a classe Navesviloes, que herda da classe pygame.sprite.Sprite
    def __init__(self, x, y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        # Carrega uma imagem aleatória do vilão e atribui à variável image
        self.image = pygame.image.load('img/vilao' + str(random.randint(1, 5)) + '.png')
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem do vilão
        self.rect.center = [x, y]  # Define a posição inicial do vilão
        self.mask = pygame.mask.from_surface(self.image)  # Define a máscara de colisão do vilão
       
        
    
    
    
    def update(self):  # Método para atualizar o vilão
        self.rect.y += 2  # Move o vilão para baixo
        if self.rect.top > altura:  # Verifica se o vilão saiu da tela
            self.kill()  # Remove o vilão do jogo
        
      
  


class Naves_viloes_balas(pygame.sprite.Sprite):  # Define a classe Naves_viloes_balas, que herda da classe pygame.sprite.Sprite
    def __init__(self, x, y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.image = pygame.image.load('img/alien_bullet.png')  # Carrega a imagem do projétil do inimigo
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem do projétil
        self.rect.center = [x, y]  # Define a posição inicial do projétil
       
    def update(self):  # Método para atualizar o projétil do inimigo
        self.rect.y += 5  # Move o projétil para baixo
        if self.rect.top > altura:  # Verifica se o projétil saiu da tela
            self.kill()  # Remove o projétil do jogo
            son_explosao2.play()  # Toca o som de explosão
        if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):  # Verifica colisão com a nave do jogador
            self.kill()  # Remove o projétil do jogo
            nave.saude_restante -= 1  # Reduz a saúde da nave do jogador
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)  # Cria uma explosão
            explosao_grupo.add(explosao)  # Adiciona a explosão ao grupo de explosões
        

class Explosoes(pygame.sprite.Sprite):  # Define a classe Explosoes, que herda da classe pygame.sprite.Sprite
    def __init__(self, x, y, tamanho):  # Método de inicialização da classe, recebe coordenadas x e y, e tamanho da explosão
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.images = []  # Lista para armazenar as imagens da explosão
        for num in range(1, 6):  # Loop para carregar as cinco imagens de explosão
            img = pygame.image.load(f'img/exp{num}.png')  # Carrega a imagem de explosão correspondente
            if tamanho == 1:  # Verifica o tamanho da explosão
                img = pygame.transform.scale(img, (20, 20))  # Redimensiona a imagem para 20x20 pixels
            if tamanho == 2:  # Verifica o tamanho da explosão
                img = pygame.transform.scale(img, (40, 40))  # Redimensiona a imagem para 40x40 pixels
            if tamanho == 3:  # Verifica o tamanho da explosão
                img = pygame.transform.scale(img, (160, 160))  # Redimensiona a imagem para 160x160 pixels
            self.images.append(img)  # Adiciona a imagem à lista de imagens
        self.index = 0  # Índice atual da imagem da explosão
        self.image = self.images[self.index]  # Define a imagem atual da explosão
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da explosão
        self.rect.center = [x, y]  # Define a posição inicial da explosão
        self.contador = 0  # Contador para controlar a troca de imagens da explosão

    def update(self):  # Método para atualizar a explosão
        velocidade_explosao = 3  # Velocidade de troca de imagens da explosão
        self.contador += 1  # Incrementa o contador
        # Verifica se é hora de trocar para a próxima imagem e se ainda há imagens para mostrar
        if self.contador >= velocidade_explosao and self.index < len(self.images) - 1:
            self.contador = 0  # Reinicia o contador
            self.index += 1  # Avança para a próxima imagem da explosão
            self.image = self.images[self.index]  # Define a próxima imagem da explosão

        # Verifica se todas as imagens da explosão foram mostradas e remove a explosão do jogo
        if self.index >= len(self.images) - 1 and self.contador >= velocidade_explosao:
            self.kill()  # Remove a explosão do jogo


# Cria grupos para armazenar diferentes tipos de sprites
nave_grupo = pygame.sprite.Group()  # Grupo para a nave do jogador
balas_grupo = pygame.sprite.Group()  # Grupo para as balas do jogador
navesviloes_grupo = pygame.sprite.Group()  # Grupo para os vilões
viloes_balas_grupo = pygame.sprite.Group()  # Grupo para as balas dos vilões
explosao_grupo = pygame.sprite.Group()  # Grupo para as explosões
planeta = Planeta(5) #5 aliens podem entrar
planeta_grupo = pygame.sprite.Group()
planeta_grupo.add(planeta)
botao_resetar = Botao(largura//2 - 200 , altura//2 + 200  , resetar_img)
botao_start = Botao(largura//2 - 200  , altura//2 + 200 , start_img)
botao_sair = Botao(largura//2 + 100 , altura//2 + 200,exit_img)

# Cria a nave do jogador e a adiciona ao grupo da nave
nave = Nave(int(largura / 2), altura - 100, 3)  # Cria uma instância da classe Nave
nave_grupo.add(nave)  # Adiciona a nave ao grupo de naves do jogador

run = True  # Variável de controle do loop principal do jogo
#retangulo caixa texto
input_rect = pygame.Rect(200,450,170,32) # x e y e dimensoes retangulo
cor_ativa= pygame.Color('lightskyblue')
cor_passadados = pygame.Color('gray15')
cor = cor_passadados
ativa = False

digitando = True
jogadores = []
while run:  # Loop principal do jogo
    
    relogio.tick(60)  # Limita a taxa de atualização do jogo a 60 frames por segundo
    
    


    # Desenha o fundo em loop, deslocando-o verticalmente
    for i in range(0, tiles):
        display.blit(bg, (0, i * bg_altura + rolagem))
    
    



    # Rola o fundo para cima
    rolagem -= 5
    # Reseta a rolagem se ultrapassar a altura do fundo
    if abs(rolagem) > bg_altura:
        rolagem = 0
    if menu == True:
        text_surface = base_font.render(user_text,True,(255,255,255))
        pygame.draw.rect(display,cor,input_rect,2)
        display.blit(text_surface,(input_rect.x + 5,input_rect.y + 5))
        input_rect.w = max(100,text_surface.get_width() + 10)
        if botao_sair.draw():
            run = False
        if botao_start.draw():
            if len(user_text) > 1:
             menu = False
             print(user_text)
             jogadores.append(user_text)
            
             
    else:
    
    
    
        # Verifica se a contagem regaressiva acabou
        if contagem == 0:
            tempo_atual = pygame.time.get_ticks()  # Obtém o tempo atual do jogo
            
            # Adiciona um novo vilão em intervalos regulares
            if tempo_atual - tempo_proximo_alien > 1000:
                alien_image_width = 50  # Largura da imagem do vilão
                x = random.randint(alien_image_width, largura - alien_image_width)  # Posição x aleatória para o vilão
                alien = Navesviloes(x, -50)  # Cria um novo vilão
                navesviloes_grupo.add(alien)  # Adiciona o vilão ao grupo de vilões
                tempo_proximo_alien = tempo_atual  # Atualiza o tempo para o próximo vilão
                
            # Adiciona tiros dos vilões
            if tempo_atual - ultimo_tiro_alien > alien_cooldown and len(viloes_balas_grupo) < 5 and len(navesviloes_grupo) > 0:
                ataque_alien = random.choice(navesviloes_grupo.sprites())  # Seleciona aleatoriamente um vilão para atirar
                alien_bala = Naves_viloes_balas(ataque_alien.rect.centerx, ataque_alien.rect.bottom)  # Cria um tiro do vilão
                viloes_balas_grupo.add(alien_bala)  # Adiciona o tiro ao grupo de tiros dos vilões
                ultimo_tiro_alien = tempo_atual  # Atualiza o tempo do último tiro dos vilões
                
            # Verifica se todos os vilões morreram
            if len(navesviloes_grupo) == 0:
                game_over = 1  # Indica que o jogador ganhou o jogo
            
            # Atualiza o estado do jogo se ainda não acabou
            if game_over == 0:  
                game_over = nave.update()  # Atualiza a nave do jogador
                balas_grupo.update()  # Atualiza as balas do jogador
                navesviloes_grupo.update()  # Atualiza os vilões
                viloes_balas_grupo.update()  # Atualiza os tiros dos vilões
                planeta_grupo.update()
                
                
            if game_over == - 1 :  # Se o jogador perdeu
                print(pontos)
                draw_texto('GAME OVER : NAVE DESTRUIDA!', fonte15, branco, int(largura /2  - 100), int(altura / 2 - 50 ))  # Exibe a mensagem de "GAME OVER!"  
                if botao_resetar.draw():
                    
                    game_over = 0    
                    pontos,nave, planeta ,contagem , alien = resetar_game() 
                  
                if botao_sair.draw():
                    run = False
                
                
            if game_over == - 2 :  # Se o jogador perdeu
                draw_texto('GAME OVER : TERRA INVADIDA!', fonte15, branco, int(largura / 2 - 100), int(altura / 2 - 50))  # Exibe a mensagem de "GAME OVER!"  
                son_destruicao.play()
                if botao_resetar.draw():  
                    game_over = 0    
                    pontos,nave, planeta ,contagem , alien = resetar_game() 
                if botao_sair.draw():
                    run = False
                
                
                
        # Se ainda há contagem regressiva
        if contagem > 0:
            draw_texto('GET READY!', fonte40, branco, int(largura / 2 - 110), int(altura / 2 + 50))  # Exibe a mensagem "GET READY!"
            draw_texto(str(contagem), fonte40, branco, int(largura / 2 - 10), int(altura / 2 + 100))  # Exibe a contagem regressiva

            # Atualiza a contagem regressiva
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultima_contagem >= 1000:
                contagem -= 1  # Decrementa a contagem regressiva
                ultima_contagem = tempo_atual  # Atualiza o tempo da última contagem regressiva

        # Atualiza o grupo de explosões
        explosao_grupo.update()
        
        # Desenha as sprites na tela
        nave_grupo.draw(display)  # Desenha a nave do jogador
        balas_grupo.draw(display)  # Desenha as balas do jogador
        navesviloes_grupo.draw(display)  # Desenha os vilões
        viloes_balas_grupo.draw(display)  # Desenha as balas do vilao
        planeta_grupo.draw(display)
    

        explosao_grupo.draw(display)

        # desenha barra de saúde
        nave.desenho_barrasaude()
        
        pontos_texto = fonte_pontuacao.render(f'Pontos: {pontos}', True, (255, 255, 255))
        text_rect = pontos_texto.get_rect(center=(largura // 2, altura //16 ))  # Centraliza o texto na tela
        display.blit(pontos_texto, text_rect)
    
    

    # eventos do pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                ativa = True
            else:
                ativa = False
        
        if event.type == pygame.KEYDOWN:
            if ativa == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:  
                 user_text += event.unicode
    if ativa:
        cor = cor_ativa
    else:
        cor = cor_passadados
    
    pygame.display.update()
    
#fecha o pygame
pygame.quit()

