import turtle
import random
import os
# import playsound
# import winsound
 
numero_de_macas = 10
numero_de_macas_podres = 5
 
 
#Criação da tela do jogo
jogo = turtle.Screen()
jogo.title("Falling Apples")
jogo.bgcolor("light blue")
jogo.bgpic("apple_trees.gif")
jogo.setup(width=800, height=600)
jogo.tracer(0)
 
jogo.register_shape("apple.gif")
jogo.register_shape("bad_apple.gif")
jogo.register_shape("basket.gif")
 
#Criação da classe de Elementos (Pai)
class Elemento(turtle.Turtle):
  
   def __init__(self, formato, cor, posicao_x, posicao_y, velocidade):
       turtle.Turtle.__init__(self)
       self.speed(velocidade)
       self.penup()
       self.shape(formato)
       self.color(cor)
       self.goto(posicao_x, posicao_y)
       self.direction = "stop"
      
   def colidiu(elemento_0, elemento_1):
       if elemento_1.distance(elemento_0) < 40:
           return True
       else:
           return False
      
#Criação da classe de Cesta (jogador)
class Cesta(Elemento):
  
   def __init__(self, formato, cor, posicao_x, posicao_y, velocidade):
       Elemento.__init__(self, formato, cor, posicao_x, posicao_y, velocidade)
       self.pontuacao = 0
       self.vidas = 3
      
   def movimenta_para_direita(self):
       self.direction = "right"
      
   def movimenta_para_esquerda(self):
       self.direction = "left"
      
      
   def movimenta(self, distancia):
       x = self.xcor() #Localizar a posição x do self
       x += distancia
       if x < 390 and x > -390:
           self.setx(x)
       self.direction = "stop"
      
   def movimenta_cesta(self):
       if self.direction == "right":
           self.movimenta(20)
       if self.direction == "left":
           self.movimenta(-20)
          
#Criacao da classe da Maçã
class Maca(Elemento):
  
   def __init__(self, formato, cor, posicao_x, posicao_y, velocidade, podre, som):
       Elemento.__init__(self, formato, cor, posicao_x, posicao_y, velocidade)
       self.podre = podre
       self.som = som
  
   def reposicionar_maca(self):
       x = random.randint(-380, 380)
       y = random.randint(200, 300)
       self.goto(x, y)
      
   def movimenta(self, cesta):
       y = self.ycor()
       y -= self.speed()/5
       self.sety(y)
       if self.ycor() < -300:
           self.reposicionar_maca()
       if Elemento.colidiu(cesta, self):
           self.reposicionar_maca()
           if self.podre == False:
               cesta.pontuacao += 1
           else:
               cesta.vidas -= 1
           os.system("aplay " + self.som + "&")
           # os.system("afplay " + self.som + "&")
           # playsound.playsound(self.som, block=False)
           # winsound.PlaySound(self.som, winsound.SND_FILENAME)
           # winsound.PlaySound(self.som, winsound.SND_ASYNC)
           placar.escrever("Pontuação: {} - Vidas: {}".format(cesta.pontuacao, cesta.vidas))
                    
#Criação da classe de notificação
class Texto(Elemento):
  
   def __init__(self, formato, cor, posicao_x, posicao_y, velocidade, fonte):
       Elemento.__init__(self, formato, cor, posicao_x, posicao_y, velocidade)
       self.hideturtle()
       self.fonte = fonte
      
   def escrever(self, texto):
       self.clear()
       self.write(texto, align="center", font = self.fonte)
                  
      
#Adicionar o jogador
cesta = Cesta("basket.gif", "blue", 0, -250, 0)
 
#Criar maçãs
macas = []
 
for _ in range(numero_de_macas):
   macas.append(Maca("apple.gif", "red", random.randint(-380, 380), random.randint(200, 300), random.randint(1, 4), False, "apple.wav"))
 
#Criar maçãs podres
macas_podres = []
 
for _ in range(numero_de_macas_podres):
   macas_podres.append(Maca("bad_apple.gif", "black", random.randint(-380, 380), random.randint(200, 300), random.randint(1, 4), True, "smash.wav"))
 
 
#Vincular o teclado
jogo.listen()
jogo.onkeypress(cesta.movimenta_para_direita, "Right")
jogo.onkeypress(cesta.movimenta_para_esquerda, "Left")
 
 
placar = Texto("circle", "white", 0, 260, 0, ("Arial", 24, "normal"))
placar.escrever("Pontuação: {} - Vidas: {}".format(cesta.pontuacao, cesta.vidas))
 
#Loop principal do jogo
while cesta.vidas > 0:
  
   jogo.update()
  
   #Movimentar as maçãs
   for maca in macas:
       maca.movimenta(cesta)
  
   #Movimentar as maçãs podres
   for maca_podre in macas_podres:
       maca_podre.movimenta(cesta)
  
   #Movimentar o jogador
   cesta.movimenta_cesta()
 
 
game_over = Texto("circle", "red", 0, 0, 0, ("Arial", 48, "bold"))
game_over.escrever("GAME OVER!")
 
jogo.mainloop()