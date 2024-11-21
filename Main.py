import pygame
import time
import random

# Inicialização
pygame.init()
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha')
preto, branco, vermelho, verde, azul = (0, 0, 0), (255, 255, 255), (200, 0, 0), (0, 200, 0), (0, 0, 200)
relogio = pygame.time.Clock()

# Configurações do jogo
tamanho_bloco = 10
velocidade = 15
fonte = pygame.font.SysFont(None, 35)

def mensagem(msg, cor, x, y):
    texto = fonte.render(msg, True, cor)
    tela.blit(texto, [x, y])

def jogo():
    fim_jogo = False
    sair = False

    x1, y1 = largura // 2, altura // 2
    x1_mudanca, y1_mudanca = 0, 0
    corpo_cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0

    while not sair:
        while fim_jogo:
            tela.fill(preto)
            mensagem("Fim de Jogo! Pressione Q para sair ou C para jogar novamente", vermelho, largura // 10, altura // 3)
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        sair = True
                        fim_jogo = False
                    if evento.key == pygame.K_c:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_mudanca, y1_mudanca = -tamanho_bloco, 0
                elif evento.key == pygame.K_RIGHT:
                    x1_mudanca, y1_mudanca = tamanho_bloco, 0
                elif evento.key == pygame.K_UP:
                    x1_mudanca, y1_mudanca = 0, -tamanho_bloco
                elif evento.key == pygame.K_DOWN:
                    x1_mudanca, y1_mudanca = 0, tamanho_bloco

        if x1 >= largura or x1 < 0 or y1 >= altura or y1 < 0:
            fim_jogo = True

        x1 += x1_mudanca
        y1 += y1_mudanca
        tela.fill(preto)
        pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        cabeca_cobra = [x1, y1]
        corpo_cobra.append(cabeca_cobra)
        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]
        for bloco in corpo_cobra[:-1]:
            if bloco == cabeca_cobra:
                fim_jogo = True

        for bloco in corpo_cobra:
            pygame.draw.rect(tela, branco, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0
            comprimento_cobra += 1

        relogio.tick(velocidade)

    pygame.quit()
    quit()

jogo()
