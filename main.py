import pygame
import neat
import time
import os
import random
pygame.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class FlappyBird:
  IMAGES = BIRD_IMAGES
  ROTATION_VELOCITY = 20
  MAX_ROTATION = 25
  ANIMATE_TIME = 2 # lower the value, faster the bird's flap 

  DISPLACEMENT_PIXEL = 16

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tilt = 0
    self.tick_counter = 0 # how many moves bird made since the last move up or down
    self.velocity = 0
    self.height = self.y # origin from bird jumped from
    self.image_counter = 0
    self.image = self.IMAGES[0]

  def jump(self):
    self.velocity = -10.5 # go upwards - could be changed
    self.tick_counter = 0 # last jumped
    self.height = self.y 

  def move(self):
    self.tick_counter += 1

    # how many pixels bird moving up or down - while chaning y-position of the bird
    displacement = self.velocity * self.tick_counter + 1.5 * self.tick_counter**2
    
    if displacement >= 16:
      displacement = 16

    if displacement < 0:
      displacement -= 2
    
    self.y = self.y + displacement
  
    if displacement < 0 or self.y < self.height + 50:
      if self.tilt <  self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION
    else:
      if self.tilt > -90: #
        self.tilt -= self.ROTATION_VELOCITY # rotating the bird downward completely 90d
           
  def draw(self, window):
    self.image_counter += 1 

    # change bird images acc. to animation time
    if self.image_counter < self.ANIMATE_TIME:
      self.image = self.IMAGES[0]
    elif self.image_counter < self.ANIMATE_TIME*2:
      self.image = self.IMAGES[1]
    elif self.image_counter < self.ANIMATE_TIME*3:
      self.image = self.IMAGES[2]
    elif self.image_counter < self.ANIMATE_TIME*4:
      self.image = self.IMAGES[1]
    elif self.image_counter < self.ANIMATE_TIME*4 + 1:
      self.image = self.IMAGES[0]
      self.image_counter = 0

    if self.tilt <= -80:
      self.image = self.IMAGES[1] # select bird image where its wings are leveled
      self.image_counter = self.ANIMATE_TIME*2

    rotated_image = pygame.transform.rotate(self.image, self.tilt) #image, angle
    new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
    window.blit(rotated_image, new_rectangle.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.image)

class Pipe:
  GAP = 200 # space between pipes
  VELOCITY = 3 # how fast pipes are going to move

  def __init__(self, x):
    self.x = x
    self.height = 0
    self.top = 0
    self.bottom = 0
    self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True) # flip the original pip upsidedown
    self.PIPE_BOTTOM = PIPE_IMAGE
    self.passed = False # bird passed the pipe without collison
    self.set_height()

  def set_height(self):
    self.height = random.randrange(50, 450)
    self.top = self.height - self.PIPE_TOP.get_height()
    self.bottom = self.height + self.GAP

  def move(self):
    self.x -= self.VELOCITY

  def draw(self, window):
    window.blit(self.PIPE_TOP, (self.x, self.top))
    window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

  def collide(self, bird):
    # get image pixels of bird, top and bottom pipes
    bird_mask = bird.get_mask() 
    top_pipe_mask = pygame.mask.from_surface(self.PIPE_TOP)
    bottom_pipe_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

    # offset from the bird to the top pipe mask and bottom
    top_offset = (self.x - bird.x, self.top - round(bird.y))
    bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
    
    # get confirmation if bird image pixel collides with top or bottom pipe image pixle
    top_point_of_collison = bird_mask.overlap(bottom_pipe_mask, bottom_offset)
    bottom_point_of_collison = bird_mask.overlap(bottom_pipe_mask, bottom_offset)
    t_point = top_point_of_collison
    b_point = bottom_point_of_collison

    if b_point or t_point:
      return True

    return False 

class Base:
  VELOCITY = 3
  WIDTH = BASE_IMAGE.get_width()
  IMAGE = BASE_IMAGE

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.WIDTH

  def move(self):
    self.x1 -= self.VELOCITY
    self.x2 -= self.VELOCITY

    if self.x1 + self.WIDTH < 0:
      self.x1 = self.x2 + self.WIDTH

    if self.x2 + self.WIDTH < 0:
      self.x2 = self.x1 + self.WIDTH
  
  def draw(self, window):
    window.blit(self.IMAGE, (self.x1, self.y))
    window.blit(self.IMAGE, (self.x2, self.y))


def draw_window(window, bird, pipes, base, score):
  window.blit(BG_IMAGE, (0,0))
  for pipe in pipes:
    pipe.draw(window)

  text = STAT_FONT.render("Score: " + str(score), True, (255,255,255))
  window.blit(text, (2, 2))

  base.draw(window)
  bird.draw(window)
  pygame.display.update()

def main():
  bird = FlappyBird(230, 350)
  pipes = [Pipe(600)]
  base = Base(730)
  window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  timer = pygame.time.Clock()
  score = 0;

  run = True
  while run:
    timer.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    add_new_pipe = False
    removePipe = []
    for pipe in pipes:
      if pipe.collide(bird):
        pass

      # if the pipe is off the screen
      if pipe.x + pipe.PIPE_TOP.get_width() < 0:
         removePipe.append(pipe)

      if not pipe.passed and pipe.x < bird.x:
        pipe.passed = True
        add_new_pipe = True
      
      pipe.move()
    
    if add_new_pipe:
      score += 1
      pipes.append(Pipe(600))

    for r in removePipe:
      pipes.remove(r)

    
    # check if bird touches the base or ground
    if bird.y + bird.image.get_height() >= 730:
      pass

    # bird.move()
    
    base.move()
    draw_window(window, bird, pipes, base, score)

  pygame.quit()
  quit()

main()





 


