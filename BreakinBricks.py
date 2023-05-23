import pygame
from pygame.locals import * # dont forget this to be able to use keybaord presses!

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakin' Bricks")
font = pygame.font.SysFont('arial', 50)
game_over_text = font.render('GAME OVER, YOU WIN!', True, (255, 0, 0))
text_rect = game_over_text.get_rect()
text_rect[0] = screen.get_width()/2 - text_rect.width/2
text_rect[1] = screen.get_height()/2 - text_rect.height/2

# align the image pixel format with the screen pixel format 
# which makes rendering a lot more quicker
# bricks
brick = pygame.image.load('./images/brick.png')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()
# put all bricks in a list using a loop
bricks = []
brick_rows = 5
brick_gap = 10
brick_cols = screen.get_width() // (brick_rect[2] + brick_gap)  
side_gap = (screen.get_width() - (brick_rect[2] + brick_gap) * brick_cols + brick_gap) // 2   # screen width - width all bricks occupy divided by two sides + gap of last brick
# set coordinates of bricks relative to their height and width 
# then append them to the list
for y in range(brick_rows):
    brickY = y * (brick_rect[3] + brick_gap)  # height
    for x in range(brick_cols): 
        brickX = x * (brick_rect[2] + brick_gap) + side_gap # width
        bricks.append((brickX, brickY))

# paddle
paddle = pygame.image.load('./images/paddle.png')
paddle = paddle.convert_alpha()
paddle_rect = paddle.get_rect()
paddle_rect[0] = screen.get_width()/2 - paddle.get_width()/2    # set default x position of paddle
paddle_rect[1] = screen.get_height() - 100    # set y position of the paddle
# football
football = pygame.image.load('./images/football.png')
football = football.convert_alpha()  
football_rect = football.get_rect()
football_rect[0] = screen.get_width()/2 - football.get_width()/2    # default x pos
football_rect[1] = brick_rows * (brick.get_height() + brick_gap)    # default y pos
football_start = (football_rect[0], football_rect[1])   # default coordinates
# football_rect.topleft = football_start
football_speed = (2.0, 3.0) # moving ratio
sx, sy = football_speed
football_served = False

clock = pygame.time.Clock()
game_over = False
x = paddle_rect[0]

while not game_over:
    dt = clock.tick(50)
    screen.fill((0, 0, 0))
    
    # draw bricks and paddle
    for b in bricks:
        screen.blit(brick, b)
    screen.blit(paddle, paddle_rect)
    screen.blit(football, football_rect)
    # events section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    
    # key pressing section
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        x -= 0.5 * dt
    if pressed[K_RIGHT]:
        x += 0.5 * dt
    if pressed[K_SPACE]:
        football_served = True
    # if the ball hit a brick
    delete_brick = None
    for b in bricks:
        bx, by = b
        if bx <= football_rect[0] + football_rect.width/2 <= bx + brick_rect.width and \
            by <= football_rect[1] + football_rect.height/2 <= by + brick_rect.height:
            delete_brick = b
            if football_rect[0] <= bx + 2:  
                sx *= -1
                break
            elif football_rect[0] + football_rect.width/2 >= bx + brick_rect.width -2:
                sx *= -1
                break
            if football_rect[1] <= by + 2:
                sy *= -1
                break
            elif football_rect[1] + football_rect.height/2 >= by + brick_rect.height -2:
                sy *= -1
                break
            break
    if delete_brick is not None:
        bricks.remove(delete_brick)
        
    # if the ball hit the paddle, invert the ball in the opposite y direction
    # and increase its movement speed (to increase game difficulty)
    if paddle_rect[0] <= football_rect[0] + football_rect.width/2 <= paddle_rect[0] + paddle_rect.width and \
        paddle_rect[1] <= football_rect[1] + football_rect.height and \
        sy > 0:
        if football_rect[0] + football_rect.width/2 - paddle_rect[0] < paddle_rect.width/2:    # if ball hits left side of paddle
            if sx < 0:  # if ball is coming from right to left then send back with same angle
                sx *= 1 
            if sx > 0:  # if ball is coming from left to right then invert angle
                sx *= -1
        if football_rect[0] + football_rect.width/2 - paddle_rect[0] >= paddle_rect.width/2:    # if ball hits right side of paddle
            if sx < 0:  # if ball is coming from right to left then invert angle
                sx *= -1
            if sx > 0:  # if ball is coming from left to right then send back with same angle
                sx *= 1
        sy *= -1
        sx *= 1.05
        sy *= 1.05
        continue
    # if the ball hit the top of the screen
    if football_rect[1] <= 0:
        football_rect[1] = 0
        sy *= -1
    # if the ball hit the bottom of the screen then reset position to default value
    if football_rect[1] >= screen.get_height() - football_rect.height:
        football_served = False
        football_rect[0] = screen.get_width()/2 - football.get_width()/2    # default x pos
        football_rect[1] = brick_rows * (brick.get_height() + brick_gap)
    # if the ball hit the left of the screen
    if football_rect[0] <=0:
        football_rect[0] = 0
        sx *= -1
    # if the ball hit the right of the screen
    if football_rect[0] >= screen.get_width() - football_rect.width:
        football_rect[0] = screen.get_width() - football_rect.width
        sx *= -1
    # if football is served using the space key then start moving the ball
    if football_served:
        football_rect[0] += sx
        football_rect[1] += sy
    # update x position of the paddle after key was pressed
    paddle_rect[0] = x
    if not bricks:
        football_served = False
        screen.blit(game_over_text, text_rect)
    pygame.display.update()

pygame.quit()

