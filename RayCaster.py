import pygame
from math import cos, sin, pi

BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)
GREEN = (152,251,152)

textures = {
    '1' : pygame.image.load('./textures/diamond.png'),
    '2' : pygame.image.load('./textures/stone.png'),
    '3' : pygame.image.load('./textures/emerald.png')
    }

class Raycaster(object):
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.blocksize = 25
        self.wallHeight = 25

        self.stepSize = 5

        self.player = {
            "x" : 65,
            "y" : 50,
            "angle" : 90,
            "fov" : 40
            }

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize))
        rect = tex.get_rect()
        rect = rect.move( (x,y) )
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self,color):

        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize

                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY

                tx = maxHit / self.blocksize

                return dist, self.map[j][i], tx

            self.screen.set_at((x,y), WHITE)

            dist += 5

    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, wallType, tx = self.castRay(angle)

            x = halfWidth + i 

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

            start = int( halfHeight - h/2)
            end = int( halfHeight + h/2)

            img = textures[wallType]
            tx = int(tx * img.get_width())

            for y in range(start, end):
                ty = (y - start) / (end - start)
                ty = int(ty * img.get_height())
                texColor = img.get_at((tx, ty))
                self.screen.set_at((x, y), texColor)

        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)

    def pause(self):

        paused = True

        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_c:
                        paused = False
                
                    elif ev.key == pygame.K_q:
                        pygame.quit()
                        quit()
            screen.fill(BLACK)
            pause_text = menu_font.render('Pausa', True, (255,255,255))
            continue_text = menu_font.render('Presione C para continuar o Q para salir.', True, (255,255,255))
            screen.blit(pause_text , (width/2,height/2))
            screen.blit(continue_text , (width/2 - 250,height/2 + 30)) 

            pygame.display.update()
            clock.tick(5)

    def start(self):

        start = True

        while start:
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:
                        break

pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)
menu_font = pygame.font.SysFont('Corbel', 35)

width = screen.get_width()
height = screen.get_height()

title = menu_font.render('MineGame', True, (255, 255, 255))
start_text = menu_font.render('Start', True, (255,255,255))

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

r = Raycaster(screen)
r.load_map('map.txt')

isRunning = True
while isRunning:

    # for ev in pygame.event.get():
    #     if ev.type == pygame.QUIT:
    #         isRunning = False

    #     if ev.type == pygame.MOUSEBUTTONDOWN:
    #         if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:
    #             break

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        newX = r.player['x']
        newY = r.player['y']

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:
                break
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                newY += sin(r.player['angle'] * pi / 180) * r.stepSize
            elif ev.key == pygame.K_s:
                newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
            elif ev.key == pygame.K_a:
                newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
            elif ev.key == pygame.K_d:
                newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
            elif ev.key == pygame.K_q:
                r.player['angle'] -= 5
            elif ev.key == pygame.K_e:
                r.player['angle'] += 5
            elif ev.key == pygame.K_p:
                r.pause()


            i = int(newX / r.blocksize)
            j = int(newY / r.blocksize)

            if r.map[j][i] == ' ':
                r.player['x'] = newX
                r.player['y'] = newY

    # Mouse position
    mouse = pygame.mouse.get_pos()

    screen.fill(pygame.Color("dimgray")) #Fondo
    
    r.render()
    
    # FPS
    screen.fill(pygame.Color("black"), (0,0,30,30))
    screen.blit(updateFPS(), (0,0))
    clock.tick(30)  
    
    if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:  
        pygame.draw.rect(screen,(200,200,200),[width/2-5,height/2-10,80,50])  
        
    else:  
        pygame.draw.rect(screen,(50,50,50),[width/2-5,height/2-10,80,50])  
    
    # superimposing the text onto our button  
    screen.blit(start_text , (width/2,height/2)) 
    
    pygame.display.update()

# pygame.quit()
