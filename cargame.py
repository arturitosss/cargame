import random
import pygame
import time


pygame.init()


WIDTH = 800
HEIGTH = 600


screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Car Racing Game")


background = pygame.image.load("road.png")
background = pygame.transform.scale(background, (WIDTH, HEIGTH))
car_image = pygame.image.load("C:\\Users\\artur\\OneDrive\\Desktop\\CARGAME\\R-removebg-preview.png")
car_image = pygame.transform.scale(car_image, (50, 100))
obstacle_image = pygame.image.load("C:\\Users\\artur\\OneDrive\\Desktop\\CARGAME\\obstacle-removebg-preview.png")
obstacle_image = pygame.transform.scale(obstacle_image, (100, 50))


angel_image = pygame.image.load("C:\\Users\\artur\\OneDrive\\Desktop\\CARGAME\\angel-removebg-preview.png")
angel_image = pygame.transform.scale(angel_image, (200,200))
car_crash = pygame.mixer.Sound("falling-143024.mp3")


lives = 3
first_crash = True




red = (255,0,0)
black = (0,0,0)






car_width = 50
car_heigth = 100
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGTH - car_heigth - 20
car_speed = 5


obstacle_width = 100
obstacle_height = 50
obstacle_speed = 15


obstacle = []


def spawn_obstacle():
    x = random.randint(118, 630)
    obstacle.append([x, -car_heigth])




def check_collision(car_x, car_y, obs_x, obs_y):
    car_rect = pygame.Rect(car_x, car_y, car_width, car_heigth)
    obs_rect = pygame.Rect(obs_x, obs_y, obstacle_width, obstacle_height)
    return car_rect.colliderect(obs_rect)


running = True
score = 0
clock = pygame.time.Clock()
spawn_obstacle()


top_score = []
try:
    file = open("score.txt", "r")
    all_score = []
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(",") #parts = [yuka,9]
            if len(parts) == 2:
                nickname = parts[0]
                try:
                    score_value = int(parts[1])
                    all_score.append([nickname, score_value])
                except ValueError:
                    continue
    file.close()


    sorted_scores = []
    while all_score:
        maxScore = -1
        maxIndex = 0
        for i in range(len(all_score)):
            if all_score[i][1] > maxScore:
                maxScore = all_score[i][1]
                maxIndex = i
        sorted_scores.append(all_score[maxIndex])
        all_score.pop(maxIndex)
   
    if len(sorted_scores) > 0:
        top_score.append(sorted_scores[0])
    if len(sorted_scores) > 1:
        top_score.append(sorted_scores[1])
    if len(sorted_scores) > 2:
        top_score.append(sorted_scores[2])
except:
    top_score = [["No scores yet", 0]]












while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 118:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < 630:
        car_x += car_speed
   
    obstacles_to_remove = []
    for o in obstacle[:]:
        o[1] += obstacle_speed
        if o[1] > HEIGTH:
            obstacles_to_remove.append(o)
            score += 1
   
    for o in obstacles_to_remove:
        obstacle.remove(o)


    if random.randint(1, 60)  == 1:
        spawn_obstacle()
   
    for o in obstacle:
        if check_collision(car_x, car_y, o[0], o[1]):
            car_crash.play()
            lives -= 1
            if first_crash:
                for size in range(50, 500, 25):
                    scaled_angel = pygame.transform.scale(angel_image, (size, size))
                    screen.blit(background, (0,0))
                    screen.blit(scaled_angel, (162, 40))
                    pygame.display.update()
                    time.sleep(0.2)
                #screen.blit(angel_image, (car_x, car_y))
                pygame.display.update()
                time.sleep(2)
                first_crash = False
            if lives <= 0:
                running = False
            else:
                obstacle.remove(o)
                car_x = WIDTH // 2 - car_width // 2


    screen.blit(background, (0,0))
    screen.blit(car_image, (car_x, car_y))
    #pygame.draw.rect(screen , red , [car_x, car_y, car_width, car_heigth])
    for o in obstacle:
        screen.blit(obstacle_image, (o[0], o[1]))
        #pygame.draw.rect(screen, black, [o[0], o[1], obstacle_width, obstacle_height])
   


    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10,10))


    lives_text = font.render(f"Lives: {lives}", True, black)
    screen.blit(lives_text, (10, 50))


    y_position = 10
    number = 1
    for scoreEntry in top_score:
        nickname = scoreEntry[0]
        scoreValue = scoreEntry[1]
        text = f"{number}. {nickname}:{scoreValue}"
        leaderboardText = font.render(text, True, black)
        screen.blit(leaderboardText, (WIDTH - 150, y_position))
        y_position += 30
        number += 1




    pygame.display.update()


    clock.tick(60)




font = pygame.font.SysFont(None, 74)
gameOver_text = font.render(f"Game Over! Score: {score}", True, black)
screen.blit(gameOver_text, (WIDTH // 2 - 150, HEIGTH // 2 - 20))
pygame.display.update()
time.sleep(2)


nickname = input("Your nickname:")
file = open("score.txt", "a")
file.write(f"{nickname},{score}\n")
file.close()
