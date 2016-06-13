#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random
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

Fontrans=pygame.image.load("imagenes/Bossbackg.jpg")


class Jugador(pygame.sprite.Sprite):
    velx=0
    vely=0

    nivel=None

    def __init__(self, tipo):
        pygame.sprite.Sprite.__init__(self)

        self.ancho=40
        self.alto=60
        self.tipoj=tipo
        if self.tipoj==0:
            self.imager=pygame.image.load("imagenes/rtank.png")
            self.imager=pygame.transform.scale(self.imager,(72,60))
            self.imagel=pygame.image.load("imagenes/ltank.png")
            self.imagel=pygame.transform.scale(self.imagel,(72,60))
            self.imaged=pygame.image.load("imagenes/ftank.png")
            self.imaged=pygame.transform.scale(self.imaged,(69,72))
            self.imageu=pygame.image.load("imagenes/btank.png")
            self.imageu=pygame.transform.scale(self.imageu,(69,72))
            self.image=self.imagel
            self.rect=self.image.get_rect()
            self.vel=12
        elif self.tipoj==1:
            self.imager=pygame.image.load("imagenes/rana.png")
            self.imager=pygame.transform.scale(self.imager,(33,48))
            self.imagel=pygame.image.load("imagenes/lana.png")
            self.imagel=pygame.transform.scale(self.imagel,(33,48))
            self.imaged=pygame.image.load("imagenes/fana.png")
            self.imaged=pygame.transform.scale(self.imaged,(33,48))
            self.imageu=pygame.image.load("imagenes/bana.png")
            self.imageu=pygame.transform.scale(self.imageu,(33,48))
            self.image=self.imagel
            self.rect=self.image.get_rect()
            self.vel=8

        self.dir=0
        self.vidas=100
        self.psi=100
        self.walking   = False

    def mover(self, px, py):
                self.rect.move_ip(px, py)

    def refrescar(self, superficie, px, py):
                if self.dir==0:
                        self.image = self.imagel
                elif self.dir==1:
                        self.image = self.imager
                elif self.dir==2:
                        self.image = self.imageu
                elif self.dir==3:
                        self.image = self.imaged
                self.mover(px, py)
                superficie.blit(self.image, self.rect)
class Vidas():

    def __init__(self,nvidas, pantalla, px):
        self.alto=2
        self.ancho=40
        self.sep=1
        self.vidas=nvidas
        self.Verde=2.55
        self.Rojo=255-(nvidas*self.Verde)
        self.color=[self.Rojo,self.Verde*nvidas,0]
        self.pos_x=px
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

        def __init__(self, posx, posy,tipo, direc, dan):
                pygame.sprite.Sprite.__init__(self)
                self.tipo      = tipo
                self.direccion = direc
                self.danopsi   = dan
                if self.tipo == 0:
                    self.vel   =  5
                    if self.direccion == 1:
                        self.image = pygame.image.load("imagenes/shockwave.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy - 50
                    if self.direccion ==0:
                        self.image = pygame.image.load("imagenes/shockwavel.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy - 50
                    if self.direccion ==2:
                        self.image = pygame.image.load("imagenes/shockwaveu.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx - 50
                        self.rect.y = posy
                    if self.direccion ==3:
                        self.image = pygame.image.load("imagenes/shockwaved.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx - 50
                        self.rect.y = posy
                if self.tipo ==1:
                    self.vel   =  10
                    if self.direccion ==1:
                        self.image = pygame.image.load("imagenes/Longshot.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==0:
                        self.image = pygame.image.load("imagenes/Longshotl.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==2:
                        self.image = pygame.image.load("imagenes/Longshotu.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==3:
                        self.image = pygame.image.load("imagenes/Longshotd.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                if self.tipo ==2:
                    self.vel   =  15
                    if self.direccion ==1:
                        self.image = pygame.image.load("imagenes/rbullet.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==0:
                        self.image = pygame.image.load("imagenes/lbullet.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==2:
                        self.image = pygame.image.load("imagenes/ubullet.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy
                    if self.direccion ==3:
                        self.image = pygame.image.load("imagenes/dbullet.png")
                        self.rect  = self.image.get_rect()
                        self.rect.x = posx
                        self.rect.y = posy

        def derecha(self, superficie):
                self.rect.x = self.rect.x + self.vel
                superficie.blit(self.image, self.rect)
        def izquierda(self, superficie):
                self.rect.x = self.rect.x - self.vel
                superficie.blit(self.image, self.rect)
        def arriba(self, superficie):
                self.rect.y = self.rect.y - self.vel
                superficie.blit(self.image, self.rect)
        def abajo(self, superficie):
                self.rect.y = self.rect.y + self.vel
                superficie.blit(self.image, self.rect)

class Nivel(object):

    plataforma_lista=None

    fondo1=Fontrans
    rect1=fondo1.get_rect()

    def __init__(self,jugador):
        self.plataforma_lista=pygame.sprite.Group()
        self.jugador=jugador

    def update(self):
        self.plataforma_lista.update()

    def draw(self,pantalla):

        pantalla.fill(GRIS)
        pantalla.blit(self.fondo1,(100,100))
        self.plataforma_lista.draw(pantalla)  

class Nivel_01(Nivel):

    def __init__(self,jugador):

        Nivel.__init__(self,jugador)

        nivel=[[10,600,100,90],[650,10,100,100],[10,600,750,100],[650,10,100,590]]


        for plataforma in nivel:
            bloque =Plataforma(plataforma[0],plataforma[1])
            bloque.rect.x=plataforma[2]
            bloque.rect.y=plataforma[3]
            bloque.jugador =self.jugador
            self.plataforma_lista.add(bloque)

def main():
    pygame.init()
    pygame.mixer.init()
    fuente   = pygame.font.Font("fuentes/wisdom.ttf", 30)
    fuentep  = pygame.font.Font("fuentes/wisdom.ttf",12)
    pygame.mixer.Sound("sonidos/Poltergeist.ogg").play(-1)
    Fire     = pygame.mixer.Sound("sonidos/Bomb.wav")
    Pau      = pygame.mixer.Sound("sonidos/Snowman.ogg")
    tamano   = [Ancho,Alto]
    pantalla = pygame.display.set_mode(tamano)
    pygame.display.set_caption("PlatformInvasion")
    w_score  = open("data/puntaje.txt", "a+")
    r_score  = open("data/puntaje.txt", "r")
    puntos   = 0
    tipopsi  = 1
    posix    = 0
    posiy    = 0
    rpress   = lpress = upress = dpress = spress = False
    distmax  = 0
    dist     = 0
    psidano  = 0
    dano     = 0
    psic     = 0
    balac    = 0
    tanquedis= 0
    tiempdis = 0
    maxdis   = 0

    jugador=Jugador(1)
    jefe=Jugador(0)

    nivel_lista=[]
    nivel_lista.append(Nivel_01(jugador))
    nivel_actual=nivel_lista[0]

    activos_sp_lista=pygame.sprite.Group()
    jefe_lista=pygame.sprite.Group()
    psilanzado=pygame.sprite.Group()
    disparostanque=pygame.sprite.Group()
    jugador.nivel=nivel_actual

    jefe.rect.x=(Ancho-jefe.rect.width)/2
    jefe.rect.y=(Alto-jefe.rect.height)/2
    activos_sp_lista.add(jefe)
    jefe_lista.add(jefe)
    jugador.rect.x=440
    jugador.rect.y=Alto-20-jugador.rect.height
    activos_sp_lista.add(jugador)

    fin=False

    while not fin:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                fin=True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    rpress = True
                    jugador.dir=1
                    posix=(jugador.vel)
                if e.key ==pygame.K_LEFT:
                    lpress = True
                    jugador.dir=0
                    posix=-(jugador.vel)
                if e.key ==pygame.K_UP:
                    upress = True
                    jugador.dir=2
                    posiy=-(jugador.vel)
                if e.key ==pygame.K_DOWN:
                    dpress = True
                    jugador.dir=3
                    posiy=jugador.vel
                if e.key ==pygame.K_SPACE:
                    if tipopsi==0:
                        if psic < 1:
                            if jugador.psi>10:
                                psidano=random.randint(10,15)
                                Ps1 = Ondapsi(jugador.rect.x,jugador.rect.y,tipopsi, jugador.dir, psidano)
                                psilanzado.add(Ps1)
                                activos_sp_lista.add(Ps1)
                                jugador.psi-=10
                                psic+=1
                    if tipopsi==1:
                        if psic < 3:
                            if jugador.psi>2:
                                psidano=random.randint(2,4) 
                                Ps1 = Ondapsi(jugador.rect.x,jugador.rect.y,tipopsi, jugador.dir, psidano)
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
                    if e.key == pygame.K_LEFT:
                            lpress=False
                            if lpress: posix = veloci
                            else: posix = 0
                    if e.key == pygame.K_RIGHT:
                            rpress = False
                            if rpress: posix = veloci
                            else: posix = 0
                    if e.key == pygame.K_UP:
                            upress=False
                            if upress: posiy = veloci
                            else: posiy = 0
                    if e.key == pygame.K_DOWN:
                            dpress=False
                            if dpress: posiy = veloci
                            else: posiy = 0

        activos_sp_lista.update()

        txt_puntos = fuentep.render("Puntaje: " + str(puntos),True,(255,255,255))
        pantalla.blit(txt_puntos,[10,10])

        bloque_col_list=pygame.sprite.spritecollide(jugador,jugador.nivel.plataforma_lista,False)
        for bloque in bloque_col_list:
            if jugador.rect.x<110:
                jugador.rect.x+=10
            if jugador.rect.x>720:
                jugador.rect.x-=10
            if jugador.rect.y<110:
                jugador.rect.y+=10
            if jugador.rect.y>550:
                jugador.rect.y-=10

        for en in jefe_lista:
            if en.dir==0:
                tanquedis=random.randint(25,50)
                distmax=random.randint(100,600)
                if dist<=distmax:
                    en.refrescar(pantalla,-5,0)
                    dist+=5
                    tiempdis+=1
            elif en.dir==1:
                tanquedis=random.randint(25,50)
                distmax=random.randint(100,600)
                if dist<=distmax:
                    en.refrescar(pantalla,5,0)
                    dist+=5
                    tiempdis+=1
            elif en.dir==2:
                tanquedis=random.randint(25,50)
                distmax=random.randint(100,600)
                if dist<=distmax:
                    en.refrescar(pantalla,0,-5)
                    dist+=5
                    tiempdis+=1
            elif en.dir==3:
                tanquedis=random.randint(25,50)
                distmax=random.randint(100,600)
                if dist<=distmax:
                    en.refrescar(pantalla,0,5)
                    dist+=5
                    tiempdis+=1
            if dist>distmax:
                dist=0
                en.dir=random.randint(0,3)
            if tiempdis>tanquedis and maxdis<5:
                psidano=random.randint(20,25)
                if en.dir==0 or en.dir==1:
                    Ps1 = Ondapsi(en.rect.x,en.rect.y+20,2, en.dir, psidano)
                else:
                    Ps1 = Ondapsi(en.rect.x+30,en.rect.y,2, en.dir, psidano)
                disparostanque.add(Ps1)
                activos_sp_lista.add(Ps1)
                maxdis+=1
                tiempdis=0
                
            if en.rect.x > 630:
              en.rect.x-=10
              en.dir=random.randint(0,3)
              dist=0
              if jugador.psi<100:
                  jugador.psi+=1
            elif en.rect.x < 100:
              en.rect.x+=10
              en.dir=random.randint(0,3)
              dist=0
              if jugador.psi<100:
                  jugador.psi+=1
            elif en.rect.y < 100:
              en.rect.y+=10
              en.dir=random.randint(0,3)
              dist=0
              if jugador.psi<100:
                  jugador.psi+=1
            elif en.rect.y > 530:
              en.rect.y-=10
              en.dir=random.randint(0,3)
              dist=0
              if jugador.psi<100:
                  jugador.psi+=1

        for psd in psilanzado:
            if psd.direccion==1:
                psd.derecha(pantalla)
            if psd.direccion==0:
                psd.izquierda(pantalla)
            if psd.direccion==2:
                psd.arriba(pantalla)
            if psd.direccion==3:
                psd.abajo(pantalla)
            if psd.rect.x > 800 or psd.rect.x <100 or psd.rect.y <100 or psd.rect.y>650:
                psilanzado.remove(psd)
                activos_sp_lista.remove(psd)
                psic-=1
            psimp = pygame.sprite.spritecollide(psd,jefe_lista,False)
            for en in psimp:
                    psilanzado.remove(psd)
                    activos_sp_lista.remove(psd)
                    jefe.vidas-=psd.danopsi
                    en.vidas-=psd.danopsi
                    if en.vidas<=0:
                        jefe_lista.remove(en)
                        activos_sp_lista.remove(en)
                    psic-=1
                    puntos +=1000
        for dis in disparostanque:
            if dis.direccion==1:
                dis.derecha(pantalla)
            if dis.direccion==0:
                dis.izquierda(pantalla)
            if dis.direccion==2:
                dis.arriba(pantalla)
            if dis.direccion==3:
                dis.abajo(pantalla)
            if dis.rect.x > 800 or dis.rect.x <100 or dis.rect.y <100 or dis.rect.y>650:
                disparostanque.remove(dis)
                activos_sp_lista.remove(dis)
                maxdis-=1
            disimp = pygame.sprite.spritecollide(jugador,disparostanque,False)
            for di in disimp:
                    disparostanque.remove(di)
                    activos_sp_lista.remove(di)
                    jugador.vidas-=di.danopsi
                    psic-=1
                    puntos +=1000
            
        if jefe.vidas<=0:
            fin=True
            w_score.write(str(puntos) + "\n")
            w_score.close()
            Intro=True
            FonInt=0
            Fondo=None
            fuente1 = fuente.render("Enter - Continuar", 1, (255,255,255))
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

        if jugador.vidas<=0:
            fin=True
            activos_sp_lista.remove(jugador)
            w_score.write(str(puntos) + "\n")
            w_score.close()
        
        golpazo=pygame.sprite.spritecollide(jugador,jefe_lista,False)
        for f in golpazo:
            Fire.play()
            jugador.vidas-=100
            
            
        nivel_actual.update()

        nivel_actual.draw(pantalla)
        activos_sp_lista.draw(pantalla)
        for nv in range(jugador.vidas):
            vd=Vidas(nv,pantalla,5)
        for jv in range(jefe.vidas):
            vd=Vidas(jv,pantalla,755)
        for np in range (jugador.psi):
            ps=Psi(np,pantalla)
        txt_puntos=fuentep.render("Puntaje: "+str(puntos),True,BLANCO)
        pantalla.blit(txt_puntos,[10,10])
        if tipopsi==0:
            txt_psiname=fuentep.render("PSI actual: Onda de Choque",True,BLANCO)
            pantalla.blit(txt_psiname,[10,30])
            txt_info=fuentep.render("Elimina los fantasmas a su paso",True,BLANCO)
            pantalla.blit(txt_info,[10,50])
            txt_info=fuentep.render("PSI usado: 10",True,BLANCO)
            pantalla.blit(txt_info,[10,70])
        if tipopsi==1:
            txt_plasma=fuentep.render("PSI actual: Longshot",True,BLANCO)
            pantalla.blit(txt_plasma,[10,30])
            txt_info=fuentep.render("Elimina el primer fantasma que encuentre",True,BLANCO)
            pantalla.blit(txt_info,[10,50])
            txt_info=fuentep.render("PSI usado: 2",True,BLANCO)
            pantalla.blit(txt_info,[10,70])
        jugador.refrescar(pantalla,posix,posiy)
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
