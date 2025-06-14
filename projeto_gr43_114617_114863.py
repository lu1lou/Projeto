"""
Licenciatura em Engenharia Mecânica
ist1114617 - Diogo Chen - diogomchen@tecnico.ulisboa.pt
ist114863 - Luis Tenreiro - luis.tenreiro@tecnico.ulisboa.pt
Grupo - 43
3/6/2025
"""

from graphics import *
import time
import math

class Battery:
    #Classe para gerir a bateria do waiter
    def __init__(self, max_level=100):
        self.max_level = max_level
        self.bateria_atual = max_level
        self.limite_recarga = 20
        
    def consumo(self, energia):
        #Consome bateria
        self.bateria_atual = max(0, self.bateria_atual - energia)
        
    def bateria_baixa(self):
        #Verifica se a bateria está baixa
        return self.bateria_atual <= self.limite_recarga
        
    def bateria_vazia(self):
        #Verifica se a bateria está vazia
        return self.bateria_atual <= 0
        
    def recarga(self):
        #Recarrega a bateria ao máximo
        self.bateria_atual = self.max_level
        
    def nível(self):
        #Retorna o nível atual da bateria
        return self.bateria_atual
    
class Obstaculo:
    #classe para representar obstaculos
    def __init__(self, win, center, size=3):
        self.win = win
        self.center = center
        self.size = size
        self.rect = Rectangle(
            Point(center.getX() - size, center.getY() - size),
            Point(center.getX() + size, center.getY() + size)
        )
        self.rect.setFill("brown")
        self.rect.draw(win)
        self.created_time = time.time()

    def expirado(self, current_time=None):
        #verifica quando um obstaculo existe a mais 3 segundos
        if current_time is None:
            current_time = time.time()
        return current_time - self.created_time >= 3

    def undraw(self):
        self.rect.undraw()
    
    def colisão(self, waiter):
        #Verifica se se sobrepoem ao waiter
        waiter_x, waiter_y = waiter.getCenter().getX(), waiter.getCenter().getY()
        waiter_r = waiter.getRaio()
        obs_x1, obs_y1 = self.rect.getP1().getX(), self.rect.getP1().getY()
        obs_x2, obs_y2 = self.rect.getP2().getX(), self.rect.getP2().getY()
        return obs_x1 - waiter_r <= waiter_x <= obs_x2 + waiter_r and obs_y1 - waiter_r <= waiter_y <= obs_y2 + waiter_r  # o water r está presente para o waiter não se realmente sobrepor ao obstaculo
        
    
class Table:
    #Classe para representar uma mesa do restaurante
    
    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        
    def draw(self, window):
        #Desenha a mesa na janela
        # Criar retângulo da mesa
        mesa_rect = Rectangle(
            Point(self.rectangle.p1.x, self.rectangle.p1.y),
            Point(self.rectangle.p2.x, self.rectangle.p2.y)
        )
        mesa_rect.setFill("blue")
        mesa_rect.setOutline("black")
        mesa_rect.setWidth(2)
        mesa_rect.draw(window)

    def ponto_dentro(self, point):  
        #verifique se o ponto coletado está dentro duma mesa
        return (self.rectangle.p1.x <= point.x <= self.rectangle.p2.x and 
                self.rectangle.p1.y <= point.y <= self.rectangle.p2.y)
       

class Waiter:
    def __init__(self, centro, raio):
       self.position = centro  # Store position
       self.radius = raio
       self.battery = Battery()

    def draw(self, window):
        # Desenhar círculo do robô
        self.circle = Circle(self.position, self.radius)
        self.circle.setFill("light blue")
        self.circle.setOutline("black")
        self.circle.setWidth(2)
        self.circle.draw(window)
        
    def mudança_cor(self):
        #Atualiza a cor baseada no nível da bateria
        if self.battery.bateria_vazia():
            self.circle.setFill("red")
        elif self.battery.bateria_baixa():
            self.circle.setFill("orange")
        else:
            self.circle.setFill("light blue") 
            
    def getCenter(self):
        #Buscar o centro do waiter
        return self.position
        
    def getRaio(self):
        #buscar o raio do waite
        return self.radius
    
    def move_waiter(self, points, window) :
        #função que faz rôbo andar
        for i in range(len(points) - 1):    #vai sobre cada ponto 
            start = points[i] #ponto inicial
            end = points[i + 1] #Ponto final
            dx = end.getX() - start.getX() #distancia em x
            dy = end.getY() - start.getY() #distancia em y
            steps = int(max(abs(dx), abs(dy)))  
            for _ in range(steps):
                # Consumir bateria baseado na distância
                distance = math.sqrt((dx/steps)**2 + (dy/steps)**2)
                self.battery.consumo(distance * 0.1)  # Factor de consumo
                self.mudança_cor()
                # Move o waiter passo a passo
                self.circle.move(dx / steps, dy / steps)        
                self.position = self.circle.getCenter()
                yield


class Botoes :
    #Classe para gerir as botoes
    
    def __init__(self, window):
        self.window = window
        self.info_box_drawn = False
        self.info_box = None
        self.info_text = None
        self.battery_text = None
    
    def criar_botoes(self,window):
        #Botão de saída
        but_saida = Rectangle(Point(66, 0), Point(88, 10))
        but_saida.setFill('red')
        but_saida_txt = Text(Point(77, 5), "Sair")  
        but_saida_txt.setSize(8)
        
        #Desenha o botão de sáida
        but_saida.draw(self.window)
        but_saida_txt.draw(self.window)
        
        #Botão para caixa de informação
        but_info = Rectangle(Point(120, 0), Point(140, 10))
        but_info.setFill("purple")
        but_info.draw(self.window)
        but_info_txt = Text(but_info.getCenter(), "Informação")
        but_info_txt.setSize(8)
        but_info_txt.setTextColor("white")
        but_info_txt.draw(self.window)
        
        # Indicador de bateria
        self.battery_text = Text(Point(30, 5), "Bateria: 100%")
        self.battery_text.setSize(8)
        self.battery_text.draw(self.window)
        
    def caixa_info(self, window):
        #Cria a caixa de informação na janela
       if not self.info_box_drawn:
           self.info_box = Rectangle(Point(50, 90), Point(100, 60))
           self.info_text = Text(self.info_box.getCenter(),
                               "LeMec 2024/2025\n"
                               "ist1114617 - Diogo Chen\n"
                               "ist1114863 - Luis Tenreiro\n"
                               "Grupo - 43\n")
           self.info_box.setFill("orange")
           self.info_box.setOutline("black")
           self.info_text.setSize(10)
           
           self.info_box.draw(self.window)
           self.info_text.draw(self.window)
           self.info_box_drawn = True
       else:
           if self.info_box:
               self.info_box.undraw()
               self.info_text.undraw()
           self.info_box_drawn = False
            
   
    def but_saida_clicked(self, click):
       #Verifica se o botão de saída foi clicado
       return 66 <= click.getX() <= 88 and 0 <= click.getY() <= 10
       
    def but_info_clicked(self, click):
        #Verifica se o botão de informação foi clicado
        return 120 <= click.getX() <= 140 and 0 <= click.getY() <= 10 
    
    def bateria_window(self, battery_level):
        #Atualiza o display da bateria
        if self.battery_text:
            self.battery_text.setText(f"Bateria: {int(battery_level)}%")
            if battery_level <= 20:
                self.battery_text.setTextColor("red")
            elif battery_level <= 50:
                self.battery_text.setTextColor("orange") 
            else:
                self.battery_text.setTextColor("green")
        



def caminhos (ponto_table,posição_atual):
    #Classe para gerir os caminhos do waite
    
    #caminho até zona de saida de pratos
    caminho_mesa = [posição_atual,          # Onde o robot está agora
                       Point(140, 135), ]    # sair de doock
    caminho_pt_entrega = [] # Continuar de onde parou
    caminho_volta = [] #caminho de volta
    
    #Condição que diefine o percurso do robot
    if ponto_table == 'Mesa1':
        caminho_mesa += [Point(11,135), Point(11, 47),Point(18,47),] 
        caminho_pt_entrega = [Point(18,47), Point(11, 47), Point(11,135), Point(75,135)] 
        caminho_volta = [Point(18,47), Point(11, 47),Point(11,135), Point(140,135), Point(140, 147)]
    elif ponto_table == 'Mesa2':
        caminho_mesa += [Point(11,135), Point(11, 75), Point(18,75)]
        caminho_pt_entrega = [Point(18,75), Point(11, 75), Point(11,135), Point(75,135)]
        caminho_volta = [Point(18,75), Point(11, 75),Point(11,135), Point(140,135), Point(140, 147)]
    elif ponto_table == 'Mesa3':
        caminho_mesa += [Point(11,135), Point(11, 103), Point(18,103)]
        caminho_pt_entrega = [Point(18,103), Point(11, 103), Point(11,135), Point(75,135)]
        caminho_volta = [Point(18,103), Point(11, 103),Point(11,135), Point(140,135), Point(140, 147)]

    #caminho para mesas 4,5,6
    elif ponto_table == 'Mesa4':
        caminho_mesa += [Point(75,135),Point(75,47), Point(68, 47),]
        caminho_pt_entrega = [Point(68, 47), Point(75,47), Point(75,135),]
        caminho_volta = [Point(68,47), Point(75,47), Point(75, 135), Point(140,135),Point(140, 147)]
    elif ponto_table == 'Mesa5':    
        caminho_mesa += [Point(75,135), Point(75,75), Point(68, 75)]
        caminho_pt_entrega = [Point(68, 75), Point(75,75), Point(75,135)]
        caminho_volta = [Point(68,75), Point(75,75), Point(75, 135), Point(140,135),Point(140, 147)]
    elif ponto_table == 'Mesa6':
        caminho_mesa += [ Point(75,135), Point(75,103), Point(68, 103),]
        caminho_pt_entrega = [Point(68, 103),Point(75,103), Point(75,135),]
        caminho_volta = [Point(68,103), Point(75,103), Point(75, 135), Point(140,135),Point(140, 147)]
    
    #caminho para mesas 7,8,9
    elif ponto_table == 'Mesa7':
        caminho_mesa += [Point(75,135),Point(75,47), Point(82, 47),]
        caminho_pt_entrega = [Point(82, 47), Point(75,47), Point(75,135),]
        caminho_volta = [Point(82,47), Point(75,47), Point(75, 135), Point(140,135),Point(140, 147)]
    elif ponto_table == 'Mesa8':
        caminho_mesa += [Point(75,135), Point(75,75), Point(82, 75),]
        caminho_pt_entrega = [Point(82, 75), Point(75,75), Point(75,135)]
        caminho_volta = [Point(82,75), Point(75,75), Point(75, 135), Point(140,135),Point(140, 147)]
    elif ponto_table == 'Mesa9':
        caminho_mesa += [Point(75,135), Point(75,103), Point(82, 103),]
        caminho_pt_entrega = [Point(82, 103), Point(75,103), Point(75,135),]
        caminho_volta = [Point(82,103), Point(75,103), Point(75, 135), Point(140,135),Point(140, 147)]
       
    #caminho para mesas 10,11,12
    elif ponto_table == 'Mesa10':
        caminho_mesa += [Point(140,135), Point(140, 47),Point(133, 47),]
        caminho_pt_entrega = [Point(133,47), Point(140, 47),Point(140, 135),Point(75,135)]
        caminho_volta = [Point(133, 47), Point(140, 47), Point(140, 147)]
    elif ponto_table == 'Mesa11':
        caminho_mesa += [Point(140,135), Point(140, 75),Point(133, 75),]
        caminho_pt_entrega = [Point(133, 75), Point(140, 75), Point(140,135), Point(75,135)]
        caminho_volta = [Point(133, 75), Point(140, 75),Point(140, 147)]
    elif ponto_table == 'Mesa12':
        caminho_mesa += [Point(140,135), Point(140, 103),Point(133, 103),]
        caminho_pt_entrega = [Point(133, 103), Point(140, 103), Point(140,135), Point(75,135)]
        caminho_volta = [Point(133, 103), Point(140, 103), Point(140, 147)]

    else:
        return None, None, None
        
    return caminho_mesa, caminho_pt_entrega, caminho_volta, 

def abrir_ficheiro(filename):
    #Carrega o layout da sala a partir do ficheiro de texto
    tables = []
    divisores = []
    dock = []
    coletor = []
    saida = []
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    components = ler_ficheiro(line)
                    if components:
                        name, rectangle = components
                        if name.startswith('Mesa'):
                            tables.append(Table(name, rectangle))
                        elif name.startswith('Divisor'):
                            divisores.append((name, rectangle))
                        elif name.startswith('Dock'):
                            dock.append((name, rectangle))
                        elif name.startswith('Coletor'):
                            coletor.append((name, rectangle))
                        elif name.startswith('Saida'):
                            saida.append((name, rectangle))
                            
    except FileNotFoundError:
        print(f"Erro: Ficheiro {filename} não encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao ler ficheiro: {e}")
        return None
        
    return {
        'tables': tables,
        'divisores': divisores,
        'dock': dock,
        'coletor': coletor,
        'saida': saida
    }

def ler_ficheiro(line):
    #Analisa uma linha do ficheiro e extrai nome e retângulo
    try:
        parts = line.split(' Rectangle(Point(')
        if len(parts) != 2:
            return None
            
        name = parts[0].strip()
        coords_part = parts[1]
        
        coords_part = coords_part.replace('), Point(', ',').replace('))', '')
        coords = [float(x.strip()) for x in coords_part.split(',')]
        
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            rectangle = Rectangle(Point(x1+0.5, y1+0.5), Point(x2-0.5, y2-0.5))
            return name, rectangle
            
    except (ValueError, IndexError) as e:
        print(f"Erro ao processar linha: {line} - {e}")
        
    return None
     
def draw_layout(window, layout_data):
   #Desenha todo os objetos do restaurante

    # Desenhar divisórias primeiro
    for name, rect in layout_data["divisores"]:
        divisor = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
        divisor.setFill("darkgray")
        divisor.setOutline("black")
        divisor.setWidth(1)
        divisor.draw(window)
        
    #Desenhar dock
    for name, rect in layout_data["dock"]:
        dock = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
        dock.setFill("black")
        dock.setOutline("black")
        dock.setWidth(1)
        dock.draw(window)
        
    #Desenhar coletor
    for name, rect in layout_data["coletor"]:
        coletor = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
        coletor.setFill("purple")
        coletor.setOutline("black")
        coletor.setWidth(1)
        coletor.draw(window)
        
    #Desenhar Saida de Pratos
    for name,rect in layout_data["saida"]:
        saida = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
        saida.setFill("yellow")
        saida.setOutline("black")
        saida.setWidth(1)
        saida.draw(window)
        
    # Desenhar mesas
    for table in layout_data["tables"]:
        table.draw(window)

class Restaurante:
    #Classe principal para gerir o restaurante
    
    def __init__(self, filename="salaxx.txt"):
        self.filename = filename
        self.layout_data = None
        self.window = None
        self.botoes = None
        self.waiter = None
        self.obstaculos = []
        self.movimento = []
        self.delay_counter = 0

    def create_window(self):
        #Cria a janela principal
        self.window = GraphWin("Layout do Restaurante", 500, 500)
        self.window.setBackground("lightgray")
        self.window.setCoords(0, 0, 150, 150)
        return self.window
    
    def inicializar(self):
        #Inicializa todos os componentes
        # Carregar layout
        self.layout_data = abrir_ficheiro(self.filename)
        if not self.layout_data:
            return False
            
        # Criar janela
        self.create_window()
        
        # Criar UI manager
        self.botoes = Botoes(self.window)
        self.botoes.criar_botoes(self.window)
        
        # Desenhar layout
        draw_layout(self.window, self.layout_data)
        
        # Criar waiter
        self.waiter = Waiter(Point(140, 147), 3)
        self.waiter.draw(self.window)
        
        return True
        
    def table_click(self, ponto_table):
        #Lida com cliques em mesas
        if self.movimento:  # Já em movimento
            return
        # Verificar se precisa recarregar
        if self.waiter.battery.bateria_baixa():
            self.voltar_para_recarregar()
            return
        
        posição_atual = self.waiter.getCenter()
        paths =caminhos(ponto_table, posição_atual)
        
        if paths[0] is None:  # Mesa não encontrada
            return
        
        caminho_mesa, caminho_pt_entrega, caminho_volta,  = paths
        
        # Adicionar movimentos à fila
        self.movimento.append(self.waiter.move_waiter(caminho_mesa, self.window))
        self.movimento.append("pausa")
        self.movimento.append(self.waiter.move_waiter(caminho_pt_entrega, self.window))
        self.movimento.append("pausa")
        self.movimento.append(self.waiter.move_waiter(list(reversed(caminho_pt_entrega)), self.window))
        self.movimento.append("pausa")
        self.movimento.append(self.waiter.move_waiter(caminho_volta, self.window))
        
    def voltar_para_recarregar(self):
        #Força o waiter a voltar ao dock para recarregar
        posição_atual = self.waiter.getCenter()
        caminho_recarga = [posição_atual, Point(140, 135), Point(140, 147)]  # Define the path to the dock
        self.movimento = []  # Limpar movimentos existentes
        self.movimento.append(self.waiter.move_waiter(caminho_recarga, self.window))
        self.movimento.append("recarga")
        
    def atualização_obs(self):
        #Remove obstáculos expirados
        for obs in self.obstaculos[:]:
            if obs.expirado():
                obs.undraw()
                self.obstaculos.remove(obs)
                
    def atualização_mov(self):
        #Atualiza o movimento do waiter
        if not self.movimento:
            return
            
        current = self.movimento[0]
        
        if current == "pausa":
            if self.delay_counter == 0:
                self.delay_counter = int(2 / 0.02)  # 2 segundos
            if self.delay_counter > 0:
                self.delay_counter -= 1
            if self.delay_counter == 0:
                self.movimento.pop(0)
        
        elif current == "recarga":
            if self.delay_counter == 0:
                self.delay_counter = int(3 / 0.02)  # 3 segundos para recarregar"
            if self.delay_counter > 0:
                self.delay_counter -= 1
            if self.delay_counter == 0:
                self.waiter.battery.recarga()
                self.waiter.mudança_cor()
                self.movimento.pop(0)
                
        else:
            try:
                colisão = any(obs.colisão(self.waiter) for obs in self.obstaculos)
                if colisão:
                    if self.delay_counter == 0:
                        self.delay_counter = int(2 / 0.02)  # 2 segundos
                    elif self.delay_counter > 0:
                        self.delay_counter -= 1
                else:
                    if self.delay_counter > 0:
                        self.delay_counter -= 1
                    else:
                        result = next(current)
                        if result == "battery_empty":
                            # Limpar movimentos atuais
                            self.movimento = []
                            self.voltar_para_recarregar()
                        elif result == "completed":
                            self.movimento.pop(0)
            except StopIteration:
                self.movimento.pop(0)
                
    def run(self):
        #Executa o programa principal
        if not self.inicializar():
            return
            
        # Loop principal
        while True:
            # Atualizar obstáculos
            self.atualização_obs()
            
            # Atualizar movimento
            self.atualização_mov()
            
            # # Atualizar display da bateria
            self.botoes.bateria_window(self.waiter.battery.nível())
            
            # Verificar cliques
            click = self.window.checkMouse()
            if click:
                if self.botoes.but_saida_clicked(click):
                    self.window.close()
                    break
                elif self.botoes.but_info_clicked(click):
                    self.botoes.caixa_info(self.window)
                    continue
                    
                # Verificar clique em mesa
                clicked_table = None
                for table in self.layout_data['tables']:
                    if table.ponto_dentro(click):
                        clicked_table = table.name
                        break
                        
                if clicked_table:
                    self.table_click(clicked_table)
                else:
                    # Criar obstáculo
                    new_obs = Obstaculo(self.window, click)
                    self.obstaculos.append(new_obs)
                    
            time.sleep(0.02)

def main():
    #Executar o programa
    restaurant = Restaurante("salaxx.txt")
    restaurant.run()


if __name__ == "__main__":
    main()
    