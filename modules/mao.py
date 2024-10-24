# Definir a classe Mao
class Mao:
    def _init_(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.dedos = {
            'polegar': False,   # Cada dedo é False (não pressionado) ou True (pressionado)
            'indicador': False,
            'medio': False,
            'anelar': False,
            'mindinho': False
        }
        self.altura_dedo = 20  # Altura inicial dos dedos

    def desenhar(self, tela):
        # Desenhar a palma da mão
        pygame.draw.rect(tela, self.cor, (self.x, self.y, 100, 50))

        # Desenhar os dedos, verificando se estão pressionados
        self.desenhar_dedo(tela, 'polegar', self.x + 10, self.y + 50)
        self.desenhar_dedo(tela, 'indicador', self.x + 30, self.y + 50)
        self.desenhar_dedo(tela, 'medio', self.x + 50, self.y + 50)
        self.desenhar_dedo(tela, 'anelar', self.x + 70, self.y + 50)
        self.desenhar_dedo(tela, 'mindinho', self.x + 90, self.y + 50)

    def desenhar_dedo(self, tela, dedo, x, y):
        # O dedo se move para baixo quando pressionado
        if self.dedos[dedo]:
            pygame.draw.rect(tela, self.cor, (x, y, 10, self.altura_dedo - 10))  # Dedo abaixado
        else:
            pygame.draw.rect(tela, self.cor, (x, y, 10, self.altura_dedo))  # Dedo normal

    def atualizar_movimento(self, tecla):
        # Mapeia as teclas para os dedos e ajusta o estado pressionado
        if tecla == pygame.K_a:  # Tecla A para o dedo mindinho da mão esquerda
            self.dedos['mindinho'] = True
        elif tecla == pygame.K_s:  # Tecla S para o dedo anelar da mão esquerda
            self.dedos['anelar'] = True
        elif tecla == pygame.K_d:  # Tecla D para o dedo médio da mão esquerda
            self.dedos['medio'] = True
        elif tecla == pygame.K_f:  # Tecla F para o dedo indicador da mão esquerda
            self.dedos['indicador'] = True

    def soltar_dedos(self):
        # Soltar todos os dedos (quando a tecla é liberada)
        for dedo in self.dedos:
            self.dedos[dedo] = False

