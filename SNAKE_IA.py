import pygame
import random
from pygame import mixer

# Inicialização do Pygame
pygame.init()
mixer.init()

# Constantes
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20
VELOCIDADE = 15

# Cores
PRETO = (0, 0, 0)
CINZA = (40, 40, 40)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Snake Game')
relogio = pygame.time.Clock()

def desenhar_grid():
    for x in range(0, LARGURA, TAMANHO_BLOCO):
        for y in range(0, ALTURA, TAMANHO_BLOCO):
            # Desenhar o preenchimento do quadrado
            pygame.draw.rect(tela, CINZA, 
                           (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            # Desenhar a borda do quadrado
            pygame.draw.rect(tela, PRETO, 
                           (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

class Snake:
    def __init__(self):
        self.tamanho = 1
        self.posicoes = [(LARGURA//2, ALTURA//2)]
        self.direcao = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.cor = VERDE
        self.pontos = 0
        self.velocidade = VELOCIDADE

    @property
    def x(self):
        return self.posicoes[0][0]
        
    @property
    def y(self):
        return self.posicoes[0][1]

    def pegar_cabeca(self):
        return self.posicoes[0]

    def mover(self):
        x, y = self.pegar_cabeca()
        dx, dy = self.direcao
        novo_x = (x + (dx * TAMANHO_BLOCO)) % LARGURA
        novo_y = (y + (dy * TAMANHO_BLOCO)) % ALTURA
        
        if (novo_x, novo_y) in self.posicoes[2:]:
            return False
        
        self.posicoes.insert(0, (novo_x, novo_y))
        if len(self.posicoes) > self.tamanho:
            self.posicoes.pop()
        return True

    def mudar_direcao(self, nova_direcao):
        dx, dy = self.direcao
        new_dx, new_dy = nova_direcao
        if (dx, dy) != (-new_dx, -new_dy):
            self.direcao = nova_direcao

class Comida:
    def __init__(self):
        self.posicao = None
        self.cor = VERMELHO
        self.gerar_nova_posicao()

    @property
    def x(self):
        return self.posicao[0]
        
    @property
    def y(self):
        return self.posicao[1]

    def gerar_nova_posicao(self):
        x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
        y = random.randrange(0, ALTURA, TAMANHO_BLOCO)
        self.posicao = (x, y)

def desenhar_pontuacao(superficie, pontos):
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f'Pontuação: {pontos}', True, BRANCO)
    superficie.blit(texto, (10, 10))

def main():
    cobra = Snake()
    comida = Comida()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
        #Colocar comandos IA aqui
        if cobra.y == comida.y and cobra.x < comida.x and cobra.direcao == (-1, 0):
            cobra.mudar_direcao((0, random.choice([-1, 1])))

        if cobra.y == comida.y and cobra.x > comida.x and cobra.direcao == (1, 0):
            cobra.mudar_direcao((0, random.choice([-1, 1])))

        if cobra.x == comida.x and cobra.y < comida.y and cobra.direcao == (0, -1):
            cobra.mudar_direcao((random.choice([-1, 1]), 0))

        if cobra.x == comida.x and cobra.y > comida.y and cobra.direcao == (0, 1):
            cobra.mudar_direcao((random.choice([-1, 1]), 0))

        if cobra.y < comida.y:
            cobra.mudar_direcao((0, 1))
        if cobra.y > comida.y:
            cobra.mudar_direcao((0, -1))
        if cobra.x < comida.x:
            cobra.mudar_direcao((1, 0))
        if cobra.x > comida.x:
            cobra.mudar_direcao((-1, 0))

        # Movimento e colisão
        if not cobra.mover():
            pygame.time.wait(1)
            cobra = Snake()
            comida = Comida()
            continue

        # Verificar se comeu a comida
        if cobra.pegar_cabeca() == comida.posicao:
            cobra.tamanho += 1
            cobra.pontos += 10

            comida.gerar_nova_posicao()
            while comida.posicao in cobra.posicoes:
                comida.gerar_nova_posicao()

        # Desenhar
        tela.fill(PRETO)
        desenhar_grid()
        
        # Desenhar cobra
        for posicao in cobra.posicoes:
            pygame.draw.rect(tela, cobra.cor, (posicao[0], posicao[1], 
                                             TAMANHO_BLOCO-2, TAMANHO_BLOCO-2))
        
        # Desenhar comida
        pygame.draw.rect(tela, comida.cor, (comida.posicao[0], comida.posicao[1], 
                                          TAMANHO_BLOCO-2, TAMANHO_BLOCO-2))
        
        desenhar_pontuacao(tela, cobra.pontos)
        pygame.display.flip()
        relogio.tick(cobra.velocidade)

if __name__ == '__main__':
    main()