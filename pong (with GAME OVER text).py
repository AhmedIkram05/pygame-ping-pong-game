# Importing the necessary libraries
import pygame, random, sys, mysql.connector

# This function checks whether the player wants to start a game or not
# It returns a boolean value that represents whether the game should run or not
def input_validation(run):

    # user is prompted to input 'y'
    start = str(input("Type 'y' to play Pong: "))

    # loop while user input is not 'y'
    while not start == "y":

        # print error message
        print("ERROR, please read the prompt!")

        # user is prompted to re-enter 'y' 
        start = str(input("Type 'y' to play Pong: "))

    # when while not loop is broken run is set to true and game loop runs
    run = True

    return run, start


# This function updates the position of the ball
# It takes as arguments the x and y speed of the ball, and the time elapsed since the last score
# It returns the updated x and y speed of the ball, and the score time
def ball_animation(ball_speed_x, ball_speed_y, score_time):
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Checking collisions with the top and bottom of the screen
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Checking collisions with the player's paddle
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    # Checking collisions with the opponent's paddle
    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    return ball_speed_x, ball_speed_y, score_time


# This function updates the position of the player's paddle
# It does not take any arguments and it updates the global variable player_speed
def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height


# This function updates the position of the opponent's paddle
# It does not take any arguments and it updates the global variable opponent_speed
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed

    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0

    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


# This function starts the ball after a score
# It takes as arguments the x and y speed of the ball, and the time elapsed since the last score
# It returns the updated x and y speed of the ball, and the score time
def ball_start(ball_speed_x, ball_speed_y, score_time):
    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()
    
    # Set the ball's center to the center of the screen
    ball.center = (screen_width/2, screen_height/2)

    # If less than one second has passed since a point was scored
    if current_time - score_time < 1000:
        # Set the ball speed to 0, effectively pausing the game
        ball_speed_x, ball_speed_y = 0, 0
    else:
        # Set the ball speed to a random value in the horizontal and vertical directions
        ball_speed_x = 7 * random.choice((1,-1))
        ball_speed_y = 7 * random.choice((1,-1))
        
        # Reset the score time
        score_time = None
    
    # Return the new ball speed and score time
    return ball_speed_x, ball_speed_y, score_time


# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AH Pong Project")

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10,screen_height/2 - 70, 10, 140)

# Colours
bg_color = pygame.Color("grey12")
white = pygame.Color("white")

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
winning_score = 1
max_rounds = 3
rounds = 1

# Score Timer
score_time = True

# Text Variables
scores = [[1,0,0], 
          [2,0,0],
          [3,0,0],
          [0,0,0]]
game_font = pygame.font.SysFont("comicsans", 45)

# Run Variable
run = True

# Run the input validation function to ensure the user inputs a valid choice
run, start = input_validation(run)

# The main game loop
while run:
    # Handling Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            elif event.key == pygame.K_UP:
                player_speed -= 7
       
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            elif event.key == pygame.K_UP:
                player_speed += 7


    # Game Logic 
    # Update the ball's position and check for collisions with walls and paddles
    ball_speed_x, ball_speed_y, score_time = ball_animation(ball_speed_x, ball_speed_y, score_time)
    # Move the player paddle based on the player's input
    player_animation()
    # Move the opponent paddle based on an AI algorithm
    opponent_ai()

    
    #Visuals
    # fill the screen with the background color
    screen.fill(bg_color)

    # draw the player, opponent, ball, and center line
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, opponent)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.line(screen, white, (screen_width/2,0), (screen_width/2,screen_height), 3) 

    # check if the score time is not zero
    if score_time:
        # start the ball movement and reset the score time to zero
        ball_speed_x, ball_speed_y, score_time = ball_start(ball_speed_x, ball_speed_y, score_time)


    # check if the ball is on the left side of the screen (player scores)
    if ball.left <= 0:
        # increment the player score for the current round
        scores[rounds-1][2] += 1
        # start the score time
        score_time = pygame.time.get_ticks()


    # check if the ball is on the right side of the screen (opponent scores)
    if ball.right >= screen_width:
        # increment the opponent score for the current round
        scores[rounds-1][1] += 1
        # start the score time
        score_time = pygame.time.get_ticks()


    # check if either the player or opponent has reached the winning score
    if scores[rounds-1][1] == winning_score or scores[rounds-1][2] == winning_score:
        # move on to the next round
        rounds += 1


    # check if the maximum number of rounds has been reached
    elif rounds > max_rounds:
        # sort the scores 2D array in descending order by the player score
        for i in range(1, len(scores)-1):
            current_Value_1 = scores[i][2]
            current_Value_2 = scores[i][0]
            current_Value_3 = scores[i][1]
            position = i 

            while position > 0 and scores[position-1][2] < current_Value_1:
                scores[position][2] = scores[position-1][2]
                scores[position][0] = scores[position-1][0]
                scores[position][1] = scores[position-1][1]
                position = position - 1

            scores[position][2] = current_Value_1
            scores[position][0] = current_Value_2
            scores[position][1] = current_Value_3     
           

        # end the game loop
        run = False

    # render the player score text and display it on the screen
    player_text = game_font.render(f"{scores[rounds-1][2]}", False, white)
    screen.blit(player_text, (660, 30))
                                   
    # render the opponent score text and display it on the screen
    opponent_text = game_font.render(f"{scores[rounds-1][1]}", False, white)
    screen.blit(opponent_text, (600, 30)) 

    if rounds <= 3:
        # render the round text and display it on the screen
        round_text = game_font.render(f"Round: {rounds}/3", False, white)
        screen.blit(round_text, (500,660))

    else:
        # render the game over text and display it on the screen in the middle of the screen
        game_over_text = game_font.render(f"GAME OVER", False, white)
        screen.blit(game_over_text, (screen_width/2 - 150, screen_height/2 - 50))

    #Updating the window
    pygame.display.flip()
    clock.tick(60)