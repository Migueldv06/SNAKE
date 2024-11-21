import pygame
import random
from pygame import mixer

# Inicialização do Pygame
pygame.init()
mixer.init()

# Constantes
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 40
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

# Carregando sons
try:
    som_comida = mixer.Sound('comida.wav')
    som_colisao = mixer.Sound('colisao.wav')
except:
    print("Arquivos de som não encontrados")

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
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    cobra.mudar_direcao((0, -1))
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    cobra.mudar_direcao((0, 1))
                elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    cobra.mudar_direcao((-1, 0))
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    cobra.mudar_direcao((1, 0))

        # Movimento e colisão
        if not cobra.mover():
            try:
                som_colisao.play()
            except:
                pass
            pygame.time.wait(1000)
            cobra = Snake()
            comida = Comida()
            continue

        # Verificar se comeu a comida
        if cobra.pegar_cabeca() == comida.posicao:
            cobra.tamanho += 1
            cobra.pontos += 10
            try:
                som_comida.play()
            except:
                pass
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