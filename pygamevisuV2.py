# -*- coding: utf-8 -*-
import pygame
import os
import creatureV2 as cr

#Größen definieren
WIDTH = 1280
HEIGHT = 720
cr.goal["coord"] = (800,0)
FPS = 60

#Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (0, 0, 255)
ROSE = (204, 165, 171)
RED = (255, 0, 0)
GREEN = (0, 255, 1)
MAGENTA = (200, 0, 200)
YELLOW = (255, 198, 0)
ORANGE = (255, 165, 0)
DAPHNA = (200, 65, 0)
LENA = (185, 125, 0)
LORENZ = (175, 215, 230)

#Gameeinstellungen
moveCap = 500
selection = 2
maxEntities = 100
amountSp = 4

#Counter
gencnt = 1
finpergencnt = 0
ratingcnt = 0
speccnt = [maxEntities/amountSp for i in range(amountSp)]

#Anzahl der Kreaturen 
amountEnt = (maxEntities/selection)*selection

#initialisieren
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.NOFRAME)
pygame.display.set_caption("genAIRation")
clock = pygame.time.Clock()
font_name= pygame.font.match_font('brush script')

#Bilderordner
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#Hintergrundbild
background = pygame.image.load(os.path.join(img_folder, "background.jpg")).convert()
background = pygame.transform.scale(background, (1280 ,720))

#Kreaturbilder
all_images =  []
for spec in range(amountSp):
	if spec == 0:
		image = pygame.image.load(os.path.join(img_folder, "unicorn.png")).convert()
		image = pygame.transform.scale(image, (25,27))	
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 1:
		image = pygame.image.load(os.path.join(img_folder, "penguin.png")).convert()
		image = pygame.transform.scale(image, (23,36))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 2:
		image = pygame.image.load(os.path.join(img_folder, "butterfly.png")).convert()
		image = pygame.transform.scale(image, (25,16))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 3:
		image = pygame.image.load(os.path.join(img_folder, "ladybug.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 4:
		image = pygame.image.load(os.path.join(img_folder, "cat.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 5:
		image = pygame.image.load(os.path.join(img_folder, "libelle.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 6:
		image = pygame.image.load(os.path.join(img_folder, "daphna.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 7:
		image = pygame.image.load(os.path.join(img_folder, "lena.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 8:
		image = pygame.image.load(os.path.join(img_folder, "lorenz.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	elif spec == 9:
		image = pygame.image.load(os.path.join(img_folder, "dodo.png")).convert()
		image = pygame.transform.scale(image, (23,26))
		image.set_colorkey(BLACK)
		all_images.append(image)
	else:
		image = pygame.image.load(os.path.join(img_folder, "spaceship.png")).convert()
		image = pygame.transform.scale(image, (25,26))
		image.set_colorkey(BLACK)
		all_images.append(image)


"""	Karte	"""		
class CREA(pygame.sprite.Sprite):
	
	"""erstellt die kreaturen"""
	
	def __init__(self,spec):
		pygame.sprite.Sprite.__init__(self)
		self.c1 = cr.Creature(species=spec)
		self.c1.appendWay()
		self.image = all_images[spec]
			
		self.spec = spec
		self.rect = self.image.get_rect()
		self.rect.center = (0,0)
		
		self.block_index = 0
		
	def update(self):
		if self.block_index < len(self.c1.briefing):
			block = self.c1.briefing[self.block_index]
			
			self.c1.nextStep(block)
			self.rect.center = (self.c1.stats["pos"][0]+100 , self.c1.stats["pos"][1]+360)
			
			self.block_index += 1
		
			if self.c1.stats["step_counter"] < moveCap and not self.c1.stats["dead"]:
				self.c1.appendWay()
		
		else:
			self.c1.stats["dead"] = True
			
		if (self.c1.stats["pos"][0]+100) < 0 or (self.c1.stats["pos"][0]+100) > 1000:
			self.c1.stats["dead"] = True
			
		
		if (self.c1.stats["pos"][1]+360) < 0 or (self.c1.stats["pos"][1]+360) > 720:
			self.c1.stats["dead"] = True

class CLOUD(pygame.sprite.Sprite):
	
	"""Wolke"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(os.path.join(img_folder, "cloud.png")).convert()
		self.image.set_colorkey(BLACK)
		self.image = pygame.transform.scale(self.image, (324,245))
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = (500,20)

class DROP(pygame.sprite.Sprite):
	"""Regentropfen"""

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		self.x = x
		self.y = y
		
		self.image = pygame.image.load(os.path.join(img_folder, "drop.png")).convert()
		self.image.set_colorkey(BLACK)
		self.image = pygame.transform.scale(self.image, (30,50))
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)

class STAFI(pygame.sprite.Sprite):
	"""Start und Ziel Plattform"""
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		self.x = x
		self.y = y
		
		self.image = pygame.image.load(os.path.join(img_folder, "plattform.png")).convert()
		self.image.set_colorkey(BLACK)
		self.image = pygame.transform.scale(self.image, (80,60))
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)


"""	sprites gruppieren	"""	
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
colliC = pygame.sprite.Group()
creatures = []

#Zeichen-Objekte erstellen
for i in range(amountEnt):
	for n in range(amountSp)[::-1]:
		if i >= (amountEnt/amountSp)*n:
			creature = CREA(n)
			all_sprites.add(creature)
			colliC.add(creature)
			creatures.append(creature)
			break

def defSprites():
	#Start- und Zielplattformen
	plat1 = STAFI(100,360)
	all_sprites.add(plat1)
	
	plat2 = STAFI(900,360)
	all_sprites.add(plat2)
	
	#Hindernisse
	cloudd = CLOUD()
	all_sprites.add(cloudd)
	obstacles.add(cloudd)
	
	dropp1 = DROP(500,200)
	all_sprites.add(dropp1)
	obstacles.add(dropp1) 
	
	dropp2 = DROP(450,300)
	all_sprites.add(dropp2)
	obstacles.add(dropp2)
	
	dropp3 = DROP(550, 375)
	all_sprites.add(dropp3)
	obstacles.add(dropp3)
	
	dropp4 = DROP(500, 500)
	all_sprites.add(dropp4)
	obstacles.add(dropp4)
	
	dropp5 = DROP(450, 600)
	all_sprites.add(dropp5)
	obstacles.add(dropp5)
	
	dropp6 = DROP(500,700)
	all_sprites.add(dropp6)
	obstacles.add(dropp6)

#weitere Funktionen
def bubbly():
	"""Kollision"""
	for c in colliC:
		hits = pygame.sprite.spritecollide(c, obstacles, False, pygame.sprite.collide_mask)
		if hits:
			c.c1.stats["dead"] = True #hier

def newGen(n):
	"""neue Generation"""
	global gencnt
	global ratingcnt
	gencnt+=1
	ratingcnt = 0
	
	for c in creatures:
		c.block_index = 0
		ratingcnt += c.c1.career["score"]	#hier
		
	creatures.sort(key=lambda w: w.c1.rating(), reverse=True)
	
	for i,c in enumerate(creatures[0:len(creatures)/n]):
		spec = c.spec
		for j in range(n)[::-1]:
			creatures[(len(creatures)/n)*j+i].c1 = cr.procreation(c.c1)	#hier
			creatures[(len(creatures)/n)*j+i].c1.appendWay()
			creatures[(len(creatures)/n)*j+i].spec = spec
			creatures[(len(creatures)/n)*j+i].image = all_images[spec]

def stats():
	"""	Anzahl der Spezien	"""
	global speccnt
	speccnt = [0 for i in range(amountSp)]
	
	for c in creatures:
		for n in range(amountSp):
			if c.spec == n:
				speccnt[n]+=1
		
def draw_text(surf,text,size,x,y):
	"""	ermöglicht das Schreiben in den screen	"""
	font= pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.topleft=(x,y)
	surf.blit(text_surface,text_rect)	
	
def draw_bar(surf, x, y, pct, clr):
	"""	zeicnet Balken für die Skala	"""
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	fill = (pct/100.*BAR_LENGTH)
	outline_rect = pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
	pygame.draw.rect(surf,clr,fill_rect)
	pygame.draw.rect(surf, BLACK, outline_rect,2) 
	
def draw():
	#->screen
	screen.fill(BLACK)
	screen.blit(background, (0,0)) 
	pygame.draw.rect(screen, ROSE, [1000, 0, 280, 720])
	pygame.draw.rect(screen, BLACK, [1000, 0, 280, 720], 2)
	pygame.draw.rect(screen, BLACK, [0, 0, 1000, 720], 2)

	#->sprites
	all_sprites.draw(screen)
	
	#->Text
	draw_text(screen,("Start"), 25, 65,320)
	draw_text(screen,("Ziel"), 25, 870,320)
	draw_text(screen,("Generation: " + str(gencnt)), 30, 1050,10)
	draw_text(screen,("Sieger: " + str(finpergencnt)), 30, 1050,50)
	draw_text(screen,("Rating: " + str(int(ratingcnt/amountEnt))), 30, 1050, 90)
	
	x = 0
	while x < amountSp:
		if x == 0:
			draw_text(screen,("Einhorn:"), 18, 1050,150+50*x)
		elif x == 1:
			draw_text(screen,("Pinguin:" ), 18, 1050,150+50*x)
		elif x == 2:
			draw_text(screen,("Schmetterling:"), 18, 1050,150+50*x)
		elif x == 3:
			draw_text(screen,("Marienkäfer:"), 18, 1050,150+50*x)
		elif x == 4:
			draw_text(screen,("Katze:"), 18, 1050,150+50*x)
		elif x == 5:
			draw_text(screen,("Libelle:"), 18, 1050,150+50*x)
		elif x == 6:
			draw_text(screen,("Daphna:"), 18, 1050,150+50*x)
		elif x == 7:
			draw_text(screen,("Lena:"), 18, 1050,150+50*x)
		elif x == 8:
			draw_text(screen,("Lorenz:"), 18, 1050,150+50*x)
		elif x == 9:
			draw_text(screen,("Dodo:"), 18, 1050,150+50*x)
		else:
			draw_text(screen,("Spaceship:"), 18, 1050,150+50*x)
		
		#->Balken
		if x == 0:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, WHITE)
		elif x == 1:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, BLACK)
		elif x == 2:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, YELLOW)
		elif x == 3:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, RED)
		elif x == 4:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, ORANGE)
		elif x == 5:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, MAGENTA)
		elif x == 6:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, DAPHNA)
		elif x == 7:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, LENA)
		elif x == 8:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, LORENZ)
		elif x == 9:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, DARKBLUE)
		else:
			draw_bar(screen, 1050,170+50*x, 100*(speccnt[x])/amountEnt, GREEN)
		
		x+=1


"""	Game loop	"""
running = True
defSprites()
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
	bubbly()
	
	
	for c in creatures:
		if not c.c1.stats["dead"]:	#hier
			allDead  = False
			break
		allDead = True
	
	if allDead:
		newGen(selection)
		stats()
	
	#Update
	all_sprites.update()
	
	finpergencnt = 0
	
	for c in creatures:
		if c.c1.stats["success"]:
			finpergencnt+=1

	#zeichnen
	draw()
	
	pygame.display.flip()

pygame.quit()
