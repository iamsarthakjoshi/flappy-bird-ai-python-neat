import pygame
import neat
import time
import os
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bg.png")))

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

def draw_window(window, bird):
  window.blit(BG_IMAGE, (0,0))
  bird.draw(window)
  pygame.display.update()

def main():
  bird = FlappyBird(200, 200)
  window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  timer = pygame.time.Clock()

  run = True
  while run:
    timer.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    bird.move()
    draw_window(window, bird)

  pygame.quit()
  quit()

main()





 


