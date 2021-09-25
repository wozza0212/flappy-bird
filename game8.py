'''
Created on 25 Sep 2021

@author: thomaswasnidge
'''
import cfg 
import sys 
import random 
import pygame 
from modules import *

def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((cfg.SCREENWIDTH, cfg.SCREENHEIGHT))
    pygame.display.set_caption("Flappy Bird")
    return screen 

def showScore(screen, score, number_images):
    digits = list(str(int(score)))
    width = 0
    
    for n in digits:
        width += number_images.get(n).get_width()
    offset = (cfg.SCREENWIDTH - width) / 2
    for n in digits:
        screen.blit(number_images.get(n), (offset, cfg.SCREENHEIGHT * 0.1))
        offset += number_images.get(n).get_width()
        
def main():
    
    screen = initGame() 
    
    sounds = dict() 
    
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
        
    number_images = dict()
    for key, value in cfg.NUMBER_IMAGE_PATHS.items():
        number_images[key] = pygame.image.load(value).convert_alpha()
        
    pipe_images = dict()
    pipe_images['bottom'] = pygame.image.load(random.choice(list(cfg.PIPE_IMAGE_PATHS.values()))).convert_alpha()
    pipe_images['top'] = pygame.transform.rotate(pipe_images['bottom'], 180)
    
    bird_images = dict()
    for key, value in cfg.BIRD_IMAGE_PATHS[random.choice(list(cfg.BIRD_IMAGE_PATHS.keys()))].items():
        bird_images[key] = pygame.image.load(value).convert_alpha()
        
    background_image = pygame.image.load(random.choice(list(cfg.BACKGROUND_IMAGE_PATHS.values()))).convert_alpha()
    
    other_images = dict() 
    for key, value in cfg.OTHER_IMAGE_PATHS.items():
        other_images[key] = pygame.image.load(value).convert_alpha()
        
    game_start_info = startGame(screen, sounds, bird_images, other_images, background_image, cfg)
    
    score = 0
    
    bird_pos, base_pos, bird_idx = list(game_start_info.values())
    base_diff_bg = other_images['base'].get_width() - background_image.get_width()
    clock = pygame.time.Clock()
    
    pipe_sprites = pygame.sprite.Group()
    for i in range(2):
        pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
        pipe_sprites.add(Pipe(image=pipe_images.get('top'), position=(cfg.SCREENWIDTH + 200 + i * cfg.SCREENWIDTH/2, pipe_pos.egt('top')[-1])))
        pipe_sprites.add(Pipe(image=pipe_images.get('bottom'), position=(cfg.SCREENWIDTH+200+i*cfg.SCREENWIDTH/2, pipe_pos.get('bottom')[-1])))
        
    bird = Bird(images=bird_images, idx=bird_idx, position=bird_pos)
    
    is_add_pipe = True 
    
    is_game_running = True 
    
    