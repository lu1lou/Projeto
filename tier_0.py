from graphics import *

class Table:
    """Classe para representar uma mesa do restaurante"""
    
    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        
    def draw(self, window):
        """Desenha a mesa na janela"""
        # Criar retângulo da mesa
        mesa_rect = Rectangle(
            Point(self.rectangle.p1.x, self.rectangle.p1.y),
            Point(self.rectangle.p2.x, self.rectangle.p2.y)
        )
        mesa_rect.setFill("blue")
        mesa_rect.setOutline("black")
        mesa_rect.setWidth(2)
        mesa_rect.draw(window)
        
class Waiter:
    def _init_ (self,centro,raio,dx,dy):
        self.circle = Circle(centro,raio)
        self.circle.setFill("yellow")
        self.circle.move(dx,dy)

    def draw(self,win):
        self.circle.draw(win)

class RestaurantLayout:
    """Classe principal para gerir o layout do restaurante"""
    
    #inserir os objetos para o layout
    def __init__(self, filename="salaxx.txt"):
        self.filename = filename
        self.tables = []
        self.dividers = []
        self.dock = []
        self.coletor = []
        self.saida = []
        self.window = None
        
    #ler o ficheiro
    def load_layout(self):
        """Carrega o layout da sala a partir do ficheiro de texto"""
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                # Processar cada linha que define uma mesa ou divisor
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        self.parse_line(line)
        #verificar se consegue ler o ficheiro                
        except FileNotFoundError:
            print(f"Erro: Ficheiro {self.filename} não encontrado!")
            return False
        except Exception as e:
            print(f"Erro ao ler ficheiro: {e}")
            return False
        return True
    
    def parse_line(self, line):
        """Analisa uma linha do ficheiro e cria o objeto correspondente"""
        # Formato: NomeX Rectangle(Point(x1, y1), Point(x2, y2))
        try:
            # Separar nome do retângulo
            parts = line.split(' Rectangle(Point(')
            if len(parts) != 2:
                return
            name = parts[0].strip()
            coords_part = parts[1]
            
            # Extrair coordenadas: remover parênteses finais e separar
            coords_part = coords_part.replace('), Point(', ',').replace('))', '')
            coords = [float(x.strip()) for x in coords_part.split(',')]
            
            if len(coords) == 4:
                x1, y1, x2, y2 = coords
                rectangle = Rectangle(Point(x1+.5, y1+0.5), Point(x2-0.5, y2-0.5))  
                #para as mesas e divisores nao tocarem
                
                if name.startswith('Mesa'):
                    table = Table(name, rectangle)
                    self.tables.append(table)
                elif name.startswith('Divisor'):
                    self.dividers.append((name, rectangle))
                elif name.startswith('Dock'):
                    self.dock.append((name,rectangle))
                elif name.startswith('Coletor'):
                    self.coletor.append((name,rectangle))
                elif name.startswith('Saida'):
                    self.saida.append((name,rectangle))
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar linha: {line} - {e}")
    
    def create_window(self):
        """Cria a janela principal"""
        # Definir tamanho da janela baseado nas coordenadas
        self.window = GraphWin("Layout do Restaurante", 600, 600)
        self.window.setBackground("lightgray")
        
        # Definir coordenadas da janela`
        self.window.setCoords(0, 0, 150, 150)
         
        #Botão de saída
        but = Rectangle(Point(66, 0), Point(88, 10))
        but.setFill('red')
        but_text = Text(Point(75, 5), "Sair")  # Centered in button
        
        # Draw elements
        but.draw(self.window)
        but_text.draw(self.window)
        
        return self.window
    
    def draw_layout(self):
        """Desenha todo o layout do restaurante"""
        if not self.window:
            return
        
        # Desenhar divisórias primeiro
        for name, rect in self.dividers:
            divisor = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
            divisor.setFill("darkgray")
            divisor.setOutline("black")
            divisor.setWidth(1)
            divisor.draw(self.window)
            
        #Desenhar dock
        for name, rect in self.dock:
            dock = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
            dock.setFill("black")
            dock.setOutline("black")
            dock.setWidth(1)
            dock.draw(self.window)
            
        #Desenhar coletor
        for name, rect in self.coletor:
            coletor = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
            coletor.setFill("purple")
            coletor.setOutline("black")
            coletor.setWidth(1)
            coletor.draw(self.window)
            
        #Desenhar Saida de Pratos
        for name,rect in self.saida:
            saida = Rectangle(Point(rect.p1.x, rect.p1.y), Point(rect.p2.x, rect.p2.y))
            saida.setFill("yellow")
            saida.setOutline("black")
            saida.setWidth(1)
            saida.draw(self.window)
            
        # Desenhar mesas
        for table in self.tables:
            table.draw(self.window)
    
    def run(self):
        """Executa o programa principal"""
        # Carregar layout
        if not self.load_layout():
            return
        
        # Criar janela
        self.create_window()
        
        # Desenhar layout
        self.draw_layout()
        
    # Loop principal para verificar cliques no botão de saída
        while True:
            click = self.window.getMouse()
            click_x, click_y = click.getX(), click.getY()
            
            # Verificar se clique foi dentro do botão de saída
            if 66 <= click_x <= 88 and 0 <= click_y <= 10:
                self.window.close()
                break


def main():
    "exacutar o programa"
    restaurant = RestaurantLayout("salaxx.txt")
    restaurant.run()

if __name__ == "__main__":
    main()