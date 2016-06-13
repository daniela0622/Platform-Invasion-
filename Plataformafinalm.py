#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random, Jefem
from pygame.locals import *

NEGRO= [0,0,0]
ROJO=[255,0,0]
BLANCO=[255,255,255]
AZUL=[0,0,255]
CAFE=[102,51,0]
ROSA=[255,0,255]
AMARILLO=[255,255,0]
CELESTE=[0,255,255]
GRIS=[128,128,128]
GRISOSC=[64,64,64]
MORADO=[128,0,128]
NARANJA=[255,128,0]
Alto=600
Ancho=800
reloj = pygame.time.Clock()

Fontrans=pygame.image.load("imagenes/Background.jpg")


class Jugador(pygame.sprite.Sprite):
    velx=0
    vely=0

    nivel=None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.ancho=40
        self.alto=60
        self.imager=pygame.image.load("imagenes/rteddy.png")
        self.imager=pygame.transform.scale(self.imager,(45,45))
        self.imagel=pygame.image.load("imagenes/lteddy.png")
        self.imagel=pygame.transform.scale(self.imagel,(45,45))
        self.image=self.imagel
        self.rect=self.image.get_rect()
        self.dir=0
        self.vidas=100
        self.psi=100

    def update(self):

        self.calc_grav()

        self.rect.x+=self.velx

        bloque_col_list=pygame.sprite.spritecollide(self,self.nivel.plataforma_lista,False)
        for bloque in bloque_col_list:
            if self.velx>0:
                self.rect.right=bloque.rect.left
            elif self.velx<0:
                self.rect.left=bloque.rect.right

        self.rect.y+=self.vely

        bloque_col_list=pygame.sprite.spritecollide(self,self.nivel.plataforma_lista,False)
        for bloque in bloque_col_list:
            if self.vely>0:
                self.rect.bottom=bloque.rect.top
            elif self.vely<0:
                self.rect.top=bloque.rect.bottom

            self.vely=0

    def calc_grav(self):

        if self.vely==0:
            self.vely=1
        else:
            self.vely+=.3

        if self.rect.y >= Alto - self.rect.height and self.vely >= 0:
            self.vely = 0
            self.rect.y = Alto - self.rect.height

    def salto(self):
        self.rect.y += 2
        plataforma_col_lista=pygame.sprite.spritecollide(self,self.nivel.plataforma_lista,False)
        self.rect.y -= 2

        if len(plataforma_col_lista) > 0 or self.rect.bottom >= Alto:
            self.vely= -12

    def ir_izq(self):
        self.velx=-6
        self.dir=1
        self.image=self.imagel

    def ir_der(self):
        self.velx=6
        self.dir=2
        self.image=self.imager

    def no_mover(self):
        self.velx=0
        self.dir=0

class Vidas():

    def __init__(self,nvidas, pantalla):
        self.alto=2
        self.ancho=40
        self.sep=1
        self.vidas=nvidas
        self.Verde=2.55
        self.Rojo=255-(nvidas*self.Verde)
        self.color=[self.Rojo,self.Verde*nvidas,0]
        self.pos_x=5
        self.pos_yini=400
        self.pos_y=self.pos_yini-(nvidas*(self.alto+self.sep))
        pygame.draw.rect(pantalla,self.color,[self.pos_x,self.pos_y, self.ancho,self.alto])

class Psi():

    def __init__(self,npsi, pantalla):
        self.alto=2
        self.ancho=40
        self.sep=1
        self.vidas=npsi
        self.Azul=2.55
        self.Rojo=255-(npsi*self.Azul)
        self.color=[self.Rojo,0,self.Azul*npsi]
        self.pos_x=50
        self.pos_yini=400
        self.pos_y=self.pos_yini-(npsi*(self.alto+self.sep))
        pygame.draw.rect(pantalla,self.color,[self.pos_x,self.pos_y, self.ancho,self.alto])


class Plataforma(pygame.sprite.Sprite):

    def __init__(self,ancho,alto):
        self.Anc=ancho
        self.Alt=alto
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface([self.Anc,self.Alt])
        self.rect=self.image.get_rect()
        self.color1=CAFE
        if ancho==10:
            self.color1=GRIS
        else:
            self.color1=CAFE
        self.image.fill(self.color1)

class Ondapsi (pygame.sprite.Sprite):

        def __init__(self, posx, posy, tipo):
                pygame.sprite.Sprite.__init__(self)
                self.tipo  = tipo
                if self.tipo == 0:
                    self.image = pygame.image.load("imagenes/fshockwave.png")
                    self.vel   =  5
                    self.rect  = self.image.get_rect()
                    self.rect.x = posx
                    self.rect.y = posy -50
                if self.tipo == 1:
                    self.image = pygame.image.load("imagenes/fLongshot.png")
                    self.vel   =  12
                    self.rect  = self.image.get_rect()
                    self.rect.x = posx
                    self.rect.y = posy

        def derecha(self, superficie):
                self.rect.x = self.rect.x + self.vel
                superficie.blit(self.image, self.rect)

class Fantasma (pygame.sprite.Sprite):

        def __init__(self, posx, posy):
                pygame.sprite.Sprite.__init__(self)
                self.tipo   = random.randint(1,3)
                if self.tipo == 1:
                    self.image  = pygame.image.load("imagenes/Fanta1.png")
                elif self.tipo == 2:
                    self.image  = pygame.image.load("imagenes/Fanta2.png")
                elif self.tipo == 3:
                    self.image  = pygame.image.load("imagenes/Fanta3.png")
                self.image  = pygame.transform.scale(self.image,(42,51))
                self.vel    =  4
                self.rect   = self.image.get_rect()
                self.rect.x = posx
                self.rect.y = posy

        def izquierda(self, superficie):
                self.rect.x = self.rect.x - self.vel
                superficie.blit(self.image, self.rect)

class Nivel(object):

    plataforma_lista=None
    enemigos_lista=None

    fondo1=Fontrans
    fondo2=Fontrans
    fondo3=Fontrans
    fondo4=Fontrans
    rect1=fondo1.get_rect()
    mov_fondo=0

    def __init__(self,jugador):
        self.plataforma_lista=pygame.sprite.Group()
        self.enemigos_lista=pygame.sprite.Group()
        self.jugador=jugador

    def update(self):
        self.plataforma_lista.update()
        self.enemigos_lista.update()

    def draw(self,pantalla):

        pantalla.fill(AZUL)
        pantalla.blit(self.fondo2,(self.rect1.x-1067,self.rect1.y))
        pantalla.blit(self.fondo1,(self.rect1))
        pantalla.blit(self.fondo2,(self.rect1.x+1067,self.rect1.y))
        pantalla.blit(self.fondo2,(self.rect1.x+2134,self.rect1.y))
        self.plataforma_lista.draw(pantalla)
        self.enemigos_lista.draw(pantalla)

    def Mover_fondo(self,mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.plataforma_lista:
            plataforma.rect.x += mov_x
        for enemigos in self.enemigos_lista:
            enemigos.rect.x += mov_x
        self.rect1.x+=mov_x
        

class Nivel_01(Nivel):

    def __init__(self,jugador):

        Nivel.__init__(self,jugador)
        
        self.limiteder=-1500

        nivel=[[10,600,0,0],[210,10,1400,200],[210,10,500,400], [210,10,900,300],
               [210,10,1100,400],[210,10,1000,500],[10,300,1000,300],
               [210,10,1760,330],[10,260,1950,340]]


        for plataforma in nivel:
            bloque =Plataforma(plataforma[0],plataforma[1])
            bloque.rect.x=plataforma[2]
            bloque.rect.y=plataforma[3]
            bloque.jugador =self.jugador
            self.plataforma_lista.add(bloque)

class Nivel_02(Nivel):

    def __init__(self,jugador):

        Nivel.__init__(self,jugador)
        self.limiteizq=500
        self.limiteder=-1500

        nivel=[[210,10,-200,330],[10,260,0,340],[210,10,200,200],
               [210,10,500,400], [210,10,900,300],
               [210,10,1100,550],[210,10,1200,90],
               [210,10,1760,330],[10,260,1950,340]]


        for plataforma in nivel:
            bloque =Plataforma(plataforma[0],plataforma[1])
            bloque.rect.x=plataforma[2]
            bloque.rect.y=plataforma[3]
            bloque.jugador =self.jugador
            self.plataforma_lista.add(bloque)

def main():
    pygame.init()
    pygame.mixer.init()
    fuente= pygame.font.Font("fuentes/wisdom.ttf", 30)
    fuentep=pygame.font.Font("fuentes/wisdom.ttf",12)
    pygame.mixer.Sound("sonidos/Mt_Itoi.ogg").play(-1)
    Fire=pygame.mixer.Sound("sonidos/Bomb.wav")
    Pau=pygame.mixer.Sound("sonidos/Snowman.ogg")
    tamano=[Ancho,Alto]
    pantalla= pygame.display.set_mode(tamano)
    pygame.display.set_caption("PlatformInvasion")
    w_score  = open("puntaje.txt", "a+")
    r_score  = open("puntaje.txt", "r")
    w_temp   = open("data/temp.txt", "w")
    puntos=0
    tipopsi=1
    dano=0
    psic=0

    for li in r_score:
        p = fuentep.render("Puntaje Máximo: " +li, True, (255, 255, 255))

    jugador=Jugador()

    nivel_lista=[]
    nivel_lista.append(Nivel_01(jugador))
    nivel_lista.append(Nivel_02(jugador))
    nivel_tot=len(nivel_lista)

    nivel_actual_no=0
    nivel_actual=nivel_lista[nivel_actual_no]

    activos_sp_lista=pygame.sprite.Group()
    enemigos_lista=pygame.sprite.Group()
    psilanzado=pygame.sprite.Group()
    jugador.nivel=nivel_actual

    jugador.rect.x=340
    jugador.rect.y=Alto-jugador.rect.height
    activos_sp_lista.add(jugador)

    for i in range (7):
            posx=random.randint(1200,1400)
            posy=random.randint(50,500)
            enem=Fantasma(posx,posy)
            enemigos_lista.add(enem)
            activos_sp_lista.add(enem)

    fin=False

    while not fin:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                fin=True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    jugador.ir_der()
                if e.key ==pygame.K_LEFT:
                    jugador.ir_izq()
                if e.key ==pygame.K_UP:
                    jugador.salto()
                if e.key ==pygame.K_SPACE:
                    if tipopsi==0:
                        if psic < 1:
                            if jugador.psi>10:
                                Ps1 = Ondapsi(jugador.rect.x,jugador.rect.y,tipopsi)
                                psilanzado.add(Ps1)
                                activos_sp_lista.add(Ps1)
                                jugador.psi-=10
                                psic+=1
                    if tipopsi==1:
                        if psic < 3:
                            if jugador.psi>2:
                                Ps1 = Ondapsi(jugador.rect.x,jugador.rect.y,tipopsi)
                                psilanzado.add(Ps1)
                                activos_sp_lista.add(Ps1)
                                jugador.psi-=2
                                psic+=1
                if e.key ==pygame.K_1:
                    tipopsi=1
                if e.key ==pygame.K_0:
                    tipopsi=0
                elif e.key == pygame.K_RETURN:
                    pygame.mixer.pause()
                    Pau.play(-1)
                    fuente= pygame.font.Font("fuentes/wisdom.ttf", 30)
                    texto= fuente.render("Pausa",True, AMARILLO)
                    texto_rect=texto.get_rect()
                    texto_x=(Ancho-texto_rect.width)/2
                    texto_y=(Alto-texto_rect.height)/2
                    pantalla.blit(texto,[texto_x,texto_y])
                    texto= fuente.render("Presione b para continuar",True, AMARILLO)
                    texto_rect=texto.get_rect()
                    texto_x=(Ancho-texto_rect.width)/2
                    texto_y=Alto-texto_rect.height-50
                    pantalla.blit(texto,[texto_x,texto_y])
                    texto= fuente.render("Presione s para salir",True, AMARILLO)
                    texto_rect=texto.get_rect()
                    texto_x=(Ancho-texto_rect.width)/2
                    texto_y=Alto-texto_rect.height-100
                    pantalla.blit(texto,[texto_x,texto_y])
                    pygame.display.flip()
                    Pausa=True
                    while Pausa:
                        for k in pygame.event.get():
                          if k.type == pygame.QUIT:
                              Pausa=False
                              fin=True
                              w_score.write(str(puntos) + "\n")
                              w_score.close()
                          if k.type == pygame.KEYDOWN:
                              if k.key == pygame.K_b:
                                  Pau.stop()
                                  Pausa=False
                                  pygame.mixer.unpause()
                              if k.key == pygame.K_s:
                                  Pausa=False
                                  fin=True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT and jugador.velx < 0:
                    jugador.no_mover()
                if e.key ==pygame.K_RIGHT and jugador.velx > 0:
                    jugador.no_mover()

        activos_sp_lista.update()

        txt_puntos = fuentep.render("Puntaje: " + str(puntos),True,(255,255,255))
        pantalla.blit(txt_puntos,[10,10])

        for en in enemigos_lista:
            if jugador.dir==0:
                en.vel=8
            elif jugador.dir==1:
                en.vel=4
            elif jugador.dir==2:
                en.vel=12
            en.izquierda(pantalla)
            if en.rect.x < 0:
              enemigos_lista.remove(en)
              activos_sp_lista.remove(en)
              posx=random.randint(800,1200)
              posy=random.randint(50,500)
              ene=Fantasma(posx,posy)
              enemigos_lista.add(ene)
              activos_sp_lista.add(ene)
              if jugador.psi<100:
                  jugador.psi+=1

        if jugador.vidas<=0:
            fin=True
            activos_sp_lista.remove(jugador)
            w_score.write(str(puntos) + "\n")
            w_score.close()

        for psd in psilanzado:
            psd.derecha(pantalla)
            if psd.rect.x > 850:
                psilanzado.remove(psd)
                activos_sp_lista.remove(psd)
                psic-=1
            psimp = pygame.sprite.spritecollide(psd,enemigos_lista,False)
            for en in psimp:
                    enemigos_lista.remove(en)
                    activos_sp_lista.remove(en)
                    if psd.tipo == 1:
                        psilanzado.remove(psd)
                        activos_sp_lista.remove(psd)
                        psic-=1
                    posx=random.randint(800,1200)
                    posy=random.randint(50,500)
                    ene=Fantasma(posx,posy)
                    enemigos_lista.add(ene)
                    activos_sp_lista.add(ene)
                    puntos +=1000
        
        golpazo=pygame.sprite.spritecollide(jugador,enemigos_lista,True)
        for f in golpazo:
            if f.tipo==1:
                dano=random.randint(5,8)
            elif f.tipo==2:
                dano=random.randint(3,6)
            elif f.tipo==3:
                dano=random.randint(4,12)
            enemigos_lista.remove(f)
            activos_sp_lista.remove(f)
            Fire.play()
            posx=random.randint(800,1200)
            posy=random.randint(50,500)
            ene=Fantasma(posx,posy)
            enemigos_lista.add(ene)
            activos_sp_lista.add(ene)
            jugador.vidas-=dano
            
        nivel_actual.update()
            
        if jugador.rect.right >= 450:
            dif=jugador.rect.x - 450
            jugador.rect.x = 450
            nivel_actual.Mover_fondo(-dif)

        if jugador.rect.left <=120:
            dif=120-jugador.rect.x
            jugador.rect.x=120
            nivel_actual.Mover_fondo(dif)

        pos_actual=jugador.rect.x + nivel_actual.mov_fondo
        nivel_actual.draw(pantalla)
        if pos_actual < nivel_actual.limiteder:
            jugador.rect.x=120
            if nivel_actual_no <nivel_tot-1:
                nivel_actual_no += 1
                nivel_actual=nivel_lista[nivel_actual_no]
                jugador.nivel=nivel_actual
                Nivel.rect1.x = 0
            else:
                pygame.mixer.pause()
                Intro=True
                FonInt=0
                Fondo=None
                fuente1 = fuente.render("Enter - continuar", 1, (255,255,255))
                while Intro:
                    for k in pygame.event.get():
                        if k.type == pygame.QUIT:
                            Bcg.stop()
                            Intro=False
                            fin=True
                        if k.type == pygame.KEYDOWN:
                            if k.key == pygame.K_RETURN:
                                if FonInt==0:
                                    FonInt=1
                        if FonInt==0:
                            Fondo="imagenes/Intermedio.jpg"
                        elif FonInt==1:
                            Intro=False
                        Hist=pygame.image.load(Fondo)
                        pantalla.blit(Hist, [0, 0])
                        pantalla.blit(fuente1, (10,500))
                        pygame.display.flip()
                w_temp.write(str(puntos) + "\n")
                w_temp.close()
                Jefem.main()
                pygame.quit()
        
        for nv in range(jugador.vidas):
            vd=Vidas(nv,pantalla)
        for np in range (jugador.psi):
            ps=Psi(np,pantalla)
        txt_puntos=fuentep.render("Puntaje: "+str(puntos),True,ROJO)
        pantalla.blit(txt_puntos,[10,10])
        if tipopsi==0:
            txt_plasma=fuentep.render("PSI actual: Onda de Choque",True,ROJO)
            pantalla.blit(txt_plasma,[10,30])
            txt_info=fuentep.render("Elimina los fantasmas a su paso",True,ROJO)
            pantalla.blit(txt_info,[10,50])
            txt_info=fuentep.render("PSI usado: 10",True,ROJO)
            pantalla.blit(txt_info,[10,70])
        if tipopsi==1:
            txt_plasma=fuentep.render("PSI actual: Longshot",True,ROJO)
            pantalla.blit(txt_plasma,[10,30])
            txt_info=fuentep.render("Elimina el primer fantasma que encuentre",True,ROJO)
            pantalla.blit(txt_info,[10,50])
            txt_info=fuentep.render("PSI usado: 2",True,ROJO)
            pantalla.blit(txt_info,[10,70])
        activos_sp_lista.draw(pantalla)
        reloj.tick(60)
        pygame.display.flip()
    nivel_actual.draw(pantalla)
    activos_sp_lista.draw(pantalla)
    finjuego=False
    while not finjuego:
        texto= fuente.render("Juego Terminado",True, ROJO)
        texto_rect=texto.get_rect()
        texto_x=(Ancho-texto_rect.width)/2
        texto_y=(Alto-texto_rect.height)/2
        pantalla.blit(texto,[texto_x,texto_y])
        texto= fuente.render("Enter - Terminar juego",True, ROJO)
        texto_rect=texto.get_rect()
        texto_x=(Ancho-texto_rect.width)/2
        texto_y=Alto-texto_rect.height
        pantalla.blit(texto,[texto_x,texto_y])
        pygame.display.flip()
        for e in pygame.event.get():
              if e.type == pygame.QUIT:
                  finjuego=True
              if e.type == pygame.KEYDOWN:
                  if e.key == pygame.K_RETURN:
                      finjuego=True

if __name__=="__main__":
    main()
        
pygame.quit()
