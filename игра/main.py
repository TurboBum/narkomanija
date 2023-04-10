from pygame import *
from random import randint
from time import time

background = transform.scale(image.load("battleground.png"),(1000,1000))
windows = display.set_mode((1000, 1000))
display.set_caption('Танчики')

class gamesprite(sprite.Sprite):

    def __init__(self,image1,speed,x,y,proverka):
        super().__init__()
        self.image = transform.scale(image.load(image1), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.proverka = proverka
        self.q = "bullet.png"
        #self.angle = 2
        
    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

class prepatstvie(gamesprite):
    def update(self):
        hits = sprite.groupcollide(bullets,bads, True, False)
        for hit in hits:
            bullets.remove(Bullet)

class player(gamesprite):
    def set_sprite(self,src):
        self.image = transform.scale(image.load(src), (65, 65))

    def update(self):

        keys = key.get_pressed()
        
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.q = "bullet.png"
            self.proverka = 1
            display.set_caption('Танк передаигается вверх')
            self.set_sprite("tank1.png")
        if keys[K_s] and  self.rect.y < 950:
            self.rect.y += self.speed
            self.q = "bullet2.png"
            self.proverka = 2
            display.set_caption('Танк передаигается вниз')
            self.set_sprite("tank3.png")
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.q = "bullet3.png"
            self.proverka = 3
            display.set_caption('Танк передаигается влево')
            self.set_sprite("tank4.png")
        if keys[K_d] and self.rect.x < 950:
            self.rect.x += self.speed
            self.proverka = 4
            self.q = "bullet1.png"
            display.set_caption('Танк передаигается вправо')
            self.set_sprite("tank2.png")
    ############################################################4
    #ВЫСТРЕЛ (НЕ ТРОГАТЬ. Работает на силе Божьей)
    def __init__(self, image1, speed, x, y, proverka):
        super().__init__(image1, speed, x, y, proverka)
        self.last_shot_time = 0
      
    #задержка
    def shoot(self):
        current_time = time()
        if current_time - self.last_shot_time >= 5:
            fire = mixer.Sound('tankovyiy-vyistrel.ogg')
            fire.play()
            bullet = Bullet(self.q, 3, self.rect.x, self.rect.y, self.proverka)
            bullets.add(bullet)
            self.last_shot_time = current_time
    ##############################################################3

    def stolknovene(self):
        hits = sprite.groupcollide(allsprites, bads, False, False)
        for hit in hits:
            keys = key.get_pressed()
            if keys[K_w] :
                self.rect.y = self.rect.y + self.speed
            if keys[K_s] :
                self.rect.y = self.rect.y - self.speed
            if keys[K_a] :
                self.rect.x = self.rect.x + self.speed
            if keys[K_d] :
                self.rect.x = self.rect.x - self.speed

class Bullet (gamesprite):
    def update(self):
        #print(self.proverka)
        if self.proverka == 1 :
            self.rect.y -= self.speed
        elif self.proverka == 2 :
            self.rect.y += self.speed
        elif self.proverka == 3 :
            self.rect.x -= self.speed
        elif self.proverka == 4 :
            self.rect.x += self.speed
        if self.rect.y < 0:
            self.kill()

class samagon(gamesprite):
    def __init__(self, image1, speed, x, y, proverka, group):
        super().__init__(image1, speed, x, y, proverka)
        self.group = group
    def update(self):
        hits = sprite.groupcollide(allsprites, self.group, False, True)
        for hit in hits:
            hero.speed = hero.speed + 5
            self.kill()

class konjak(gamesprite):
    def update(self):
        hits = sprite.groupcollide(allsprites, bonuce_zamedlenie, False, True)
        for hit in hits:
            hero.speed = 1
            bonuce_zamedlenie.remove(zamedlenie)

            
bullets = sprite.Group() #пули
allsprites = sprite.Group()#игрок (может и враг)
bads = sprite.Group()#препятствия
bonuce_speed = sprite.Group()# бонус(скорость)
bonuce_zamedlenie = sprite.Group() #бонус(замедление)

hero = player('tank1.png', 2, 275, 250,1)
allsprites.add(hero)
kamen = prepatstvie('obstacle.png', 1, 300, 400,0)
bads.add(kamen)
uskorenie = samagon('spedd.png', 1, 850, 700,0, bonuce_speed)
bonuce_speed.add(uskorenie)
zamedlenie = konjak('ulitka.png', 1, 700, 900,0)
bonuce_zamedlenie.add(zamedlenie)

mixer.init()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE :
                hero.shoot()
                   
    windows.blit(background, (0, 0))
    hero.update()
    hero.reset()
    kamen.update()
    kamen.reset()
    uskorenie.update()
    uskorenie.reset()
    zamedlenie.update()
    zamedlenie.reset()
    hero.stolknovene()
    bullets.draw(windows)
    bullets.update()
    display.update()
