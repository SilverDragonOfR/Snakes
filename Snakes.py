import pygame
import random
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

pygame.init()

screen_width,screen_height = 900,600

gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("The Classic Snakes Game")
pygame.display.update()

def is_eaten(snake_x,snake_y,food_x,food_y,snake_size):
    point_a_x = snake_x
    point_a_y = snake_y
    point_b_x = snake_x + snake_size
    point_b_y = snake_y
    point_c_x = snake_x
    point_c_y = snake_y + snake_size
    point_d_x = snake_x + snake_size
    point_d_y = snake_y + snake_size

    cond1 = (food_x<=point_a_x<=food_x+snake_size) and (food_y<=point_a_y<=food_y+snake_size)
    cond2 = (food_x<=point_b_x<=food_x+snake_size) and (food_y<=point_b_y<=food_y+snake_size)
    cond3 = (food_x<=point_c_x<=food_x+snake_size) and (food_y<=point_c_y<=food_y+snake_size)
    cond4 = (food_x<=point_d_x<=food_x+snake_size) and (food_y<=point_d_y<=food_y+snake_size)

    if(cond1 or cond2 or cond3 or cond4):
        return True
    else:
        return False

def display_text(text,color,x,y,font):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def blocked(snake,snake_length,snake_size,margin,color,font_m):
    point_a_x = snake[0][0]
    point_a_y = snake[0][1]
    point_b_x = snake[0][0] + snake_size
    point_b_y = snake[0][1]
    point_c_x = snake[0][0]
    point_c_y = snake[0][1] + snake_size
    point_d_x = snake[0][0] + snake_size
    point_d_y = snake[0][1] + snake_size

    margin_a = margin - 2;
    cond1 = not (margin_a<point_a_x<(screen_width-margin_a) and margin_a<point_a_y<(screen_height-margin_a) and margin_a<point_b_x<(screen_width-margin_a) and margin_a<point_b_y<(screen_height-margin_a) and margin_a<point_c_x<(screen_width-margin_a) and margin_a<point_c_y<(screen_height-margin_a) and margin_a<point_d_x<(screen_width-margin_a) and margin_a<point_d_y<(screen_height-margin_a))
    cond2 = False
    a = -3
    if snake_length>=7:
        for i in range(10,snake_length):
            c1 = (snake[i][0]-a<=point_a_x<=snake[i][0]+snake_size+a) and (snake[i][1]-a<=point_a_y<=snake[i][1]+snake_size+a)
            c2 = (snake[i][0]-a<=point_b_x<=snake[i][0]+snake_size+a) and (snake[i][1]-a<=point_b_y<=snake[i][1]+snake_size+a)
            c3 = (snake[i][0]-a<=point_c_x<=snake[i][0]+snake_size+a) and (snake[i][1]-a<=point_c_y<=snake[i][1]+snake_size+a)
            c4 = (snake[i][0]-a<=point_d_x<=snake[i][0]+snake_size+a) and (snake[i][1]-a<=point_d_y<=snake[i][1]+snake_size+a)
            if(c1 or c2 or c3 or c4):
                cond2 = True
                break
            
    if cond1 or cond2:
        return True
    else:
        return False


def game_start():

    exit_game = False
    game_over = False
    white = (255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    black = (0,0,0)
    yellow = (255,255,0)
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    speed = 7
    snake_size = 30
    margin = 64
    food_x = random.randint(margin,screen_width-snake_size-margin)
    food_y = random.randint(margin,screen_height-snake_size-margin)
    score = 0
    fps = 30
    font_size = 55
    font = pygame.font.SysFont("a Autobus Omnibus",font_size)
    font_size_m = 20
    font_m = pygame.font.SysFont("Lato",font_size_m)
    snake = [[snake_x,snake_y]]
    snake_length = 1
    message_displayed = False

    clock = pygame.time.Clock()
    
    while not exit_game:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                exit_game = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if velocity_x == 0:
                        velocity_x = speed
                        velocity_y = 0
                if event.key == pygame.K_LEFT:
                    if velocity_x == 0:
                        velocity_x = -speed
                        velocity_y = 0
                if event.key == pygame.K_UP:
                    if velocity_y == 0:
                        velocity_x = 0
                        velocity_y = -speed
                if event.key == pygame.K_DOWN:
                    if velocity_y == 0:
                        velocity_x = 0
                        velocity_y = speed

        for i in range(snake_length-1,0,-1):
            snake[i] = snake[i-1]
            
        snake_x += velocity_x
        snake_y += velocity_y
        snake[0] = [snake_x,snake_y]

        if blocked(snake,snake_length,snake_size,margin,green,font_m):
            game_over = True

        if game_over:
            if not message_displayed:
                display_text("Press 'a' to play again and 'x' to quit",green,300,30,font_m)
                pygame.display.update()
                message_displayed = True

        gameWindow.fill(white)
        pygame.draw.rect(gameWindow,green,[margin,margin,screen_width-2*margin,screen_height-2*margin],1)
        pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
        for i in range(snake_length-1,-1,-1):
            if i%2==0:
                pygame.draw.rect(gameWindow,black,[snake[i][0],snake[i][1],snake_size,snake_size])
            else:
                pygame.draw.rect(gameWindow,yellow,[snake[i][0],snake[i][1],snake_size,snake_size])
        display_text(str(score),green,0,0,font)

        if is_eaten(snake_x,snake_y,food_x,food_y,snake_size):
            score += 1
            snake.append([snake[-1][0],snake[-1][1]])
            snake_length +=1
            food_x = random.randint(margin,screen_width-snake_size-margin)
            food_y = random.randint(margin,screen_height-snake_size-margin)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])

        
        if not game_over:
            pygame.display.update()

        clock.tick(fps)

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('a'):
                        return {"score":score,"again":True}
                    elif event.key == ord('x'):
                        return {"score":score,"again":False}


dt = game_start()
while dt["again"] == True:
    dt = game_start()

pygame.quit()


pygame.init()
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Good Game !")

input_board = True
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
yellow = (255,255,0)
font_size_k = 40
font_k = pygame.font.SysFont("Lato",font_size_k)
name = ""

while input_board:
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_board = False
            if event.type == pygame.KEYDOWN:
                if event.key == 32 or ord("a")<=event.key<=ord("z") or ord("A")<=event.key<=ord("Z"):
                    name = name + event.dict["unicode"]
                if event.key == pygame.K_RETURN:
                    input_board = False
            

    gameWindow.fill(black)
    display_text("Your Score is",green,330,110,font_k)
    display_text(str(dt["score"]),green,440,170,font_k)
    display_text("Type your name and press enter",green,170,300,font_k)
    display_text(name,green,440-len(name)*8,360,font_k)
    
    pygame.display.update()
            
pygame.quit()

if len(name) == 0:
    name = "NightFalcon"

pygame.init()
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Leaderboard")

leader_board = True
font_size_k = 40
font_k = pygame.font.SysFont("Lato",font_size_k)

df = pd.read_csv("./Data.csv")
if len(df) == 0:
    my_id = 1
else:
    my_id = df["Id"].max() + 1
df2 = {"Id": my_id, "Score": dt["score"], "Name":name}
df = df.append(df2, ignore_index=True)
df = df.sort_values(by=["Score"], ascending=False)
df.to_csv('./Data.csv', index=False)

while leader_board:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            leader_board = False

    display_text("Leaderboard",green,330,0,font_k)
    display_text("Rank",green,120,100,font_k)
    display_text("Name",green,330,100,font_k)
    display_text("Score",green,680,100,font_k)
    for i in range(len(df)):
        display_text(str(i+1)+".",green,150,150+(i+1)*40,font_k)
        display_text(df.iloc[i,2],green,330,150+(i+1)*40,font_k)
        display_text(str(df.iloc[i,1]),green,710,150+(i+1)*40,font_k)
        if df.iloc[i,0] == my_id:
            display_text(str(i+1)+".",white,150,150+(i+1)*40,font_k)
            display_text(df.iloc[i,2],white,330,150+(i+1)*40,font_k)
            display_text(str(df.iloc[i,1]),white,710,150+(i+1)*40,font_k)

    display_text("Press any key to exit Game...",green,10,555,font_k)
            
    pygame.display.update()
    

pygame.quit()
