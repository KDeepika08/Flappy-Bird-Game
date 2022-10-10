#importing pygame,system and random modules
import pygame,sys,random

def create_pipe():
    random_pipe_pos = random.choice(pipe_height) 
    bottom_pipe = pipe_surface.get_rect(midtop=(600,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(600,random_pipe_pos-250))
    return bottom_pipe,top_pipe

def move_pipes(pipes_list):
    for pipe in pipes_list:
        pipe.centerx -= 5 # moving the pipes one by one to left of the screen
    return pipes_list

def display_pipes(pipes_list):
    for pipe in pipes_list:
        if pipe.bottom >= 900:
            display_screen.blit(pipe_surface,pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface,False,True)
            display_screen.blit(flipped_pipe,pipe)

#Checking for collisions
def check_collision(pipes_list):
    for pipe in pipes_list:
        if bird_rect.colliderect(pipe): #Checking if the bird collides with a pipe
            bird_hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 900: # If the bird touches the top of the screen or it touches the ground then end the game 
        bird_hit_sound.play()
        return False
    return True

def score_display():
    score_text = game_font.render(f'Score:{int(score)}',True,(0,0,0))
    score_rect = score_text.get_rect(center =(220,90))
    display_screen.blit(score_text,score_rect)


    high_score_text = game_font.render(f'High score:{int(high_score)}',True,(0,0,0))
    high_score_rect = high_score_text.get_rect(center =(220,270))
    display_screen.blit(high_score_text,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

 
pygame.init() #Initialize all imported pygame modules
pygame.font.init()
display_screen = pygame.display.set_mode((450,900))
clock = pygame.time.Clock() # creates an object to track the time
game_font = pygame.font.Font('C:/Users/lucky/Desktop/Latex/font.ttf' ,30)

no_of_FPS=120
downward_fall=0.16
bird_movement=0 
game_active= True # By default
score = 0 
high_score = 0

background_surface = pygame.image.load('C:/Users/lucky/Desktop/Flappy bird/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)


floor_surface = pygame.image.load('C:/Users/lucky/Desktop/Flappy bird/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface) 
floor_x_position = 0

bird_surface = pygame.image.load('C:/Users/lucky/Desktop/Flappy bird/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,300))


pipe_surface = pygame.image.load('C:/Users/lucky/Desktop/Flappy bird/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] 
GENERATE_PIPE = pygame.USEREVENT
pygame.time.set_timer(GENERATE_PIPE,800)#Here we have an event that is going to trigger every 800 milliseconds
pipe_height=[400,450,500,600]

game_over_surface = pygame.image.load('C:/Users/lucky/Desktop/Flappy bird/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (220,400))

bird_flap_sound = pygame.mixer.Sound('C:/Users/lucky/Desktop/Flappy bird/wing.mp3')
bird_hit_sound =  pygame.mixer.Sound('C:/Users/lucky/Desktop/Flappy bird/hit.mp3')

while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT: 
              pygame.quit() #unintiliaze all imported pygame modules
              sys.exit() 
          if event.type == pygame.KEYDOWN: #checks if any of the keys in keyboard is pressed
              if event.key == pygame.K_UP and game_active:
                  bird_movement = 0
                  bird_movement -= 6 
                  bird_flap_sound.play() 
              if event.key == pygame.K_UP and game_active == False:
                  game_active = True
                  pipe_list.clear() 
                  bird_rect.center = (100,400)
                  bird_movement=0
                  score=0
                  

          if event.type == GENERATE_PIPE:
              pipe_list.extend(create_pipe()) 
 
      display_screen.blit(background_surface,(0,0))

      if game_active:

          #Bird
          bird_movement += downward_fall 
          bird_rect.centery += bird_movement
          display_screen.blit(bird_surface,bird_rect)
          game_active = check_collision(pipe_list)

          #Pipes
          pipe_list = move_pipes(pipe_list)    
          display_pipes(pipe_list)

          score += 0.01 
    
      else:
          display_screen.blit(game_over_surface,game_over_rect)
          high_score = update_score(score,high_score)
          score_display()

      #Floor
      floor_x_position -= 1
      display_screen.blit(floor_surface,(floor_x_position,700)) 
      display_screen.blit(floor_surface,(floor_x_position + 200,700))
      if floor_x_position <= -250:
          floor_x_position = 0
      
      pygame.display.update()
      clock.tick(no_of_FPS)

