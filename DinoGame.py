# -*- coding: utf-8 -*

import pygame
import random
import time

pygame.init()  # initialization of pygame to make him usable at code

display_width = 800  # width of the display
display_height = 600  # height of the display

# making the game's display
display = pygame.display.set_mode((display_width, display_height))
# we put the name that will be indicated above the game display
pygame.display.set_caption("Running Dino")

# MainTestSuite.addTest(unittest.unittest.TestLoader.loadTestsFromTestCase(FunctionsTests))

# creating icon of the game with file loading
icon = pygame.image.load('resources/dino/dino.jpg')
# putting icon into display on the left upper corner
pygame.display.set_icon(icon)

# an array with cactus drawings for ease of use in the main code
cactus_img = [
    pygame.image.load("resources/cactus/Cactus0.png"),
    pygame.image.load("resources/cactus/Cactus1.png"),
    pygame.image.load("resources/cactus/Cactus2.png")]

# consider parameters of every file: the same width;
# height=display_height - 100 - cactus' height
# height = display_height - 100 - cactus' height because -
# we need the max value of cactus "y"
cactus_options = [64, 449, 37, 410, 40, 420]
#  we need these parameters cause our class Objects need width and height

# making array with pictures of different positions of the dinosaur's body
dino_img = [
    pygame.image.load("resources/dino/Dino0.png"),
    pygame.image.load("resources/dino/Dino1.png"),
    pygame.image.load("resources/dino/Dino2.png"),
    pygame.image.load("resources/dino/Dino3.png"),
    pygame.image.load("resources/dino/Dino4.png")]

# counter of count of pictures of dino with already shown body positions
img_counter = 0

# for working with lives counter
health_img = pygame.image.load("resources/mics/heart.png")
# the code is borrowed from the source
# https://pyga.me/docs/ref/transform.html#pygame.transform.scale
health_img = pygame.transform.scale(health_img, (30, 30))
# the code is borrowed from the source
# https://pyga.me/docs/ref/transform.html#pygame.transform.scale
health = 1

# parameters of dino + his location on the display
usr_width = 70
usr_height = 100
# the point of x on the cartesian line is approximately 266px (800px/3)
usr_x = display_width // 3
# because the coordinates are at the left upper corner
usr_y = display_height - usr_height - 100

#                               parameters of realistic (stones, clouds)
stone_img = [pygame.image.load('resources/stones/Stone0.png'),
             pygame.image.load('resources/stones/Stone1.png')]
cloud_img = [pygame.image.load('resources/clouds/Cloud0.png'),
             pygame.image.load('resources/clouds/Cloud1.png')]

clock = pygame.time.Clock()  # responsible for updating game frames

make_jump = False  # should we do jump or not
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

speeed = 4
speed_up = False


# function for clouds, stones, cacti
class Object:
    """The Object's class

    Class creating and drawing and moving the game objects

    Attributes:
        x(int) - x coordinate of object
        y(int) - y coordinate of object
        width(int) - width of object
        image(str) - image of object
        speed(int) - speed of object

    """

    def __init__(self, x, y, width, image, speed):  # args
        """Initialization

        Args:
            x(int) - x coordinate of object
            y(int) - y coordinate of object
            width(int) - width of object
            image(str) - image of object
            speed(int) - speed of object
        """
        self.x = x
        self.y = y  # class's attributes
        self.width = width
        self.image = image
        self.speed = speed

    def move(self, speed=5):  # move - method
        """Updates x-position of an Object

        Args:
            speed(int) - speed of object
            default number = 5

        Returns:
            True - if object x is in display_width=800px
            False - if object x is not in display_width=800px
        """
        self.speed = speed
        if self.x >= -self.width:  # to put object to the right
            # where we will put the object + ability to watch it
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False  # when we can not see the object -> False

    def return_self(self, radius, y, width, image):
        """Updates/re-writes Object attributes

        args:
            radius(int) - distance for reborn object
            y(int) - y coordinate of object
            width(int) - width of object
            image(str) - image of object
        """
        self.x = radius
        self.y = y
        self.width = width
        self.image = image


class Button:
    """ The Button's class

    Class creating and drawing the buttons

    Attributes:
        width (int): width of bottom
        height (int): height of bottom
        inactive_color (tuple): the button color at the inactive condition
        active_color (tuple): the button color at the active condition
    """

    def __init__(self, width, height):
        """Initialization

        Args:
            width (int): button's width setting
            height (int): button's height setting
        """
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=30):
        """Draws button on a game screen and detects mouse key pressing

        - function is making rectangles with parameters that we want to
        - validate if mouse is at the button to choose active-inactive color
        - running some actions if we click it by left part of mouse

        Args:
            x (int): Coordinate "х"
            y (int): Coordinate "у"
            message (str): text at the button
            action (function, optional): A function to call when pressed.
            The default value = None.
            font_size (int, optional): font size. Default value = 30
        """
        # the code is borrowed from the source
        # https://younglinux.info/pygame/mouse?ysclid=lqn35m0v14335914713
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # the code is borrowed from the source
        # https://younglinux.info/pygame/mouse?ysclid=lqn35m0v14335914713

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color,
                             (x, y, self.width, self.height))

            if click[0] == 1:
                # time program wait till respond to a click
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_color,
                             (x, y, self.width, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def show_menu():
    """Create main game menu

     - create menu
     - draw buttons "Start game" and "Quit"
     - stars main game cycle if "Start game" button is pressed

    Args: None

    Returns: None
    """
    menu_background = pygame.image.load('resources/mics/menu.png')

    start_button = Button(288, 60)
    quit_button = Button(120, 60)
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        display.blit(menu_background, (0, 0))
        start_button.draw(250, 235, "Start game", start_game, 50)
        quit_button.draw(342, 350, "Quit", quit, 50)

        pygame.display.update()


def start_game():
    """Main function runs game cycle and resets global
    game variables before each new game

    Args: None

    global variables:
    scores(int) - actual score
    make_jump(bool) - should we jump or not
    jump_counter(int) - counter for making jumps
    usr_y(int) - user y coordinate
    health(int) - count of user's lives
    speeed(int) - actual speed of the cacti

    Returns: None
    """
    global scores, make_jump, jump_counter, usr_y, health, speeed

    while game_cycle():  # while user do not quiting the game
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        health = 1
        speeed = 4


def game_cycle():  # function which starting dino game
    """Runs main game cycle

    Function which starts dino game

    Args: None

    Returns:
        None - the main function of the game, which starts the game
        where all functions are calling

    """
    global make_jump, speeed, speed_up
    game = True
    cactus_arr = []  # empty massive of cactus
    create_cactus_arr(cactus_arr)

    stone, cloud = open_random_objects()
    heart = Object(random.randrange(10000, 12000),
                   random.randrange(300, 500),
                   30, health_img, 4)

    now = time.time()

    # the game cycle ( ultimate, until game become False )
    while game:
        # a passing of all the player's actions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user tap to the red cross
                quit()
                pygame.display.update()

        #                     Working with the keyboard
        # getting all the keys which are pressed:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # if user click SPACE
            make_jump = True

        if make_jump:
            jump()

        world = pygame.image.load("resources/mics/world.jpg")

        count_scores(cactus_arr)

        display.blit(world, (0, 0))  # putting our world picture on display

        print_text("Scores: " + str(scores), 600, 10)

        draw_array(cactus_arr)  # drawing cacti
        move_objects(stone, cloud)

        draw_dino()

        # making a pause when pressing the button Escape
        if keys[pygame.K_ESCAPE]:
            pause()

        # putting it beyond pause() to not show hearts' count and other hearts
        # at the display while pause
        # to make lives reborn:
        heart.move()
        hearts_plus(heart)  # to create new lives

        # checking after all the images are drawn:
        if check_collision(cactus_arr):
            game = False

        # important to do after drawing the main image on the display
        # which is "display.blit(world, (0, 0))" + after check_collision
        # to have 0 count of hearts at the display
        show_health()  # to see the count of lives

        pygame.display.update()  # updating every game moment ( fps )
        clock.tick(80)  # about the game speed in parentheses - fps

        if time.time() - now > 30:
            speed_up = True
        if speed_up:
            speeed += 0.15
            speed_up = False
            now = time.time()
    return game_over()


def jump():
    """The function handles the player's jump over an obstacle.

    The function divides the obstacle into two phases of 30 steps each.
    At the first phase (30->0) dino is going up
    At the second phase (0->-30) dino is going down

    Args: None

    Returns:
        None
        - changes the values of usr_y, allowing you to create the
        feeling of a dinosaur jumping
        - determines when the dino comes out of the
        jump position ( make_jump = False )
    """
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        # changing the value of the usr_y to change dino y-position:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    """Create a list of these cactus; array(list of Objects)

    Args:
        array(list): List of cacti. The first time you run it, the list
         is empty, where we are appending info about 3 cacti by Object class

    Returns:
        None: Adds objects to the passed array(list)
    """
    global speeed
    # 3 is not accessible => 0, 1, 2; equal cacti count
    choice = random.randrange(0, 3)
    img = cactus_img[choice]  # choosing image of random cacti
    # the zero one width is on 0, first one - on second ...
    width = cactus_options[choice * 2]
    # zero one height - second, first one - third ...
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width - random.randint(100, 200), height,
                        width, img, speeed))

    # 3 is not accessible => 0, 1, 2; equal cacti count
    choice = random.randrange(0, 3)
    img = cactus_img[choice]  # choosing image of random cacti
    # the zero one width is on 0, first one - on second ...
    width = cactus_options[choice * 2]
    # zero one height - second, first one - third ...
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + random.randint(100, 300), height,
                        width, img, speeed))
    # 3 is not accessible => 0, 1, 2; equal cacti count
    choice = random.randrange(0, 3)
    img = cactus_img[choice]  # choosing image of random cacti
    # the zero one width is on 0, first one - on second ...
    width = cactus_options[choice * 2]
    # zero one height - second, first one - third ...
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + random.randint(400, 600), height,
                        width, img, speeed))


def draw_array(array):
    """Moves cacti on a screen (updates x-position)

    if we have True in calling move() than
    we are calling to the function object_return(array, cactus) with these args:
        objects(list of Objects)
        cactus(Object)

    Args:
        array(list) of objects

    Returns:
        None
        object_return(array, cactus) -> function with args:
            array -> list of objects
            cactus -> object which we check
    """
    global speeed
    for cactus in array:
        check = cactus.move(speeed)
        if not check:  # if we cannot see the cactus
            object_return(array, cactus)


def find_radius(array):
    """Looking for a suitable distance to regrow the cactus

    Args:
        array(list) of Objects

    Returns:
        radius(int): the distance through which a new cactus will be born,
        when viewed from the rightmost
    """
    # x positions of every cactus
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_width:
        # to reborn cacti out of display_width to hide him
        radius = display_width
        # the distance between the value of distant cactus and new radius
        if radius - maximum < 50:
            radius += 250
    else:
        radius = maximum
    # so that there are more cacti, between which there is a
    # large distance, not a small one
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 30)
    else:
        radius += random.randrange(250, 350)
    return radius


def object_return(objects, obj):
    """Reborn cactus which has collision with dino

    Args:
        objects(list) - of Objects
        obj(Object) - cacti which we gonna reborn because of collision

    Returns:
        None
        but it is calling function return_self for cacti which had collision
    """
    radius = find_radius(objects)
    choice = random.randrange(0, 3)
    img = cactus_img[choice]  # choosing image of random cactus
    # zero has width at zero, first one at the second ...:
    width = cactus_options[choice * 2]
    # zero has height at second, first one - at third ...:
    height = cactus_options[choice * 2 + 1]
    # Object is returning to his new_position:
    obj.return_self(radius, height, width, img)


def open_random_objects():
    """Randomly creates non-active objects in a game (stones, clouds)

    Args: None

    Returns:
        stone(Object)
        cloud(Object)
    """
    choice = random.randrange(0, 2)  # 0 or 1
    img_of_stone = stone_img[choice]
    stone = Object(display_width, display_height - 80, 10, img_of_stone, 5)

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]
    cloud = Object(display_width, 80, 700, img_of_cloud, 5)

    return stone, cloud


def move_objects(stone, cloud):
    """Moves non-active objects (stones, clouds)

    Args:
        stone(Object)
        cloud(Object)

    Returns:
        None
        passes the values of objects stone and cloud to the return_self,
        which outputs new objects according to the assigned info
    """
    global speeed
    check = stone.move(speeed)
    if not check:  # if out of display
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        # where are we reborn and how :
        stone.return_self(display_width, 500 + random.randrange(10, 80),
                          stone.width, img_of_stone)

    check = cloud.move(speeed)
    if not check:  # if out of display
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        # where are we reborn and how :
        cloud.return_self(display_width, random.randrange(10, 200),
                          cloud.width, img_of_cloud)


def draw_dino():
    """Draws dino

    The function that is responsible for the positions of the dinosaur pictures
    It is 5 pictures that are changing with the speed which we choose
    at these function

    Args:   None
        global variable img_counter(int), which is counter
        of dino's pictures right now


    Returns:
        None
        displays different body position frames on the screen Dino, creating
        the feeling that the dinosaur is moving towards the cacti
    """
    global img_counter
    if img_counter == 25:
        # to not go beyond the number of positions of the
        # dinosaur that is equal 5
        img_counter = 0
        # drawing a picture of a dinosaur
    display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1


# working with the game's fonts, PingPong.tts - our game's main font
def print_text(message, x, y, font_color=(0, 0, 0),
               font_type="resources/fonts/PingPong.ttf", font_size=30):
    """Output some text on the display

    Args:
        message(str)
        x(int)
        y(int)
        font_color(tuple) = (0, 0, 0) (black)
        font_type(str) = "resources/fonts/PingPong.ttf"
        font_size(int) = 30

    Returns:
        None
        displays messages at our game's display
    """
    # the code is borrowed from the source
    # https://younglinux.info/pygame/font?ysclid=lqm3h16n9x423393137
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))  # output on the screen = blit
    # the code is borrowed from the source
    # https://younglinux.info/pygame/font?ysclid=lqm3h16n9x423393137


def pause():
    """Pause game

    The function of the pause of our game
    output some text and suggest to continue

    Args:   None

    Returns:
        None
        displays messages about the pause of the game
        stopping the game
    """
    paused = True
    while paused:
        for event in pygame.event.get():  # passing of all the player's actions
            if event.type == pygame.QUIT:  # click red roast
                quit()

        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()  # all kinds of keyboard press
        # setting the right to continue the game on the button ENTER
        if keys[pygame.K_RETURN]:
            paused = False
        # to output "Paused. Press enter to continue" when press esc
        pygame.display.update()


def check_collision(barriers):
    """Check collusion of dino with cacti

    Args:
        barriers(list) - list of cactus(Object)

    Returns:
        True - if that was collision of dino with cactus
        False - if that was not collision od dino with cactus
    """
    for barrier in barriers:  # if we go down - positive count
        if barrier.y == 449:  # for little cactus
            if not make_jump:
                if barrier.x <= usr_x \
                        + usr_width - 30 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:  # if going up
                # if lower edge dino is in barrier (cactus):
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x \
                            + usr_width - 45 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:  # if going down => jump_counter in (-30, 0)
                if usr_y + usr_height - 7 >= barrier.y:
                    if barrier.x <= usr_x + 10 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
                    elif barrier.x <= usr_x + usr_width - 35 <= barrier.x \
                            + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
        else:  # for big cacti
            if not make_jump:  # if right part of dino is in barrier - collision
                if barrier.x <= usr_x + usr_width - 10 <= barrier.x \
                        + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:  # in part of jumping up
                if usr_y + usr_height - 15 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - \
                            40 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter < 0:  # in part of jumping down
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - \
                            43 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
                    if barrier.x <= usr_x <= barrier.x + barrier.width - 10:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True


def count_scores(barriers):
    """Count scores

    Args:
        barriers(list) - list of Objects(cacti)

    Returns:
        None
        updates count of total score at the game right now
    """
    global scores, max_above
    above_cactus = 0
    for barrier in barriers:
        if usr_y + usr_height <= barrier.y:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                above_cactus += 1
            elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                above_cactus += 1
    max_above = max(max_above, above_cactus)
    if jump_counter == -30:
        scores += max_above
        max_above = 0


def game_over():
    """Graceful shutdown of a game and records update

    The function that is checking what user choose when it's collision:
    to continue the playing or quit it.
    Also, it's updating maximum score at the actual game session

    Args: None

    Returns:
        True - if user select to continue the game (pressed ENTER)
        False - if user select to go out of game (pressed ESC)
        - printing info about game over
        - printing info about max_scores
    """
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():  # passing of all the player's actions
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press Enter to play again, Esc to exit', 40, 300)
        print_text('Max scores: ' + str(max_scores), 300, 350)

        keys = pygame.key.get_pressed()  # every possible click at the keyboard
        # setting the right to continue the game on the button ENTER
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False
        # to output words about game ending and offer to start a new game
        pygame.display.update()


def show_health():
    """Draw current user's count of hearts

    Args:
        global variable health(int) - how many lives user have

    Returns:
        None
    """
    global health
    show = 0  # how many hearts we have already shown
    x = 20  # value of coordinate x of the heart at the display
    while show != health:
        display.blit(health_img, (x, 20))
        x += 40
        show += 1


def check_health():
    """Checking if user has any lives left or not

    Checks available lives and changes count of lives after collisions

    Args:
        global variable health(int) - how many lives user have

    Returns:
        True - if user still have lives
        False - if user's count of lives is equal zero
    """
    global health
    health -= 1
    if health == 0:
        return False
    else:
        return True


def hearts_plus(heart):
    """Adding new lives

    Increase the number of lives when dino make collision with a heart.
    Reborn heart by calling function return_self of class Objects.

    Args:
        heart(Object)

    global variables:
        health(int): current number of lives
        usr_x(int): x-position of a player
        usr_y(int): y-position of a player
        usr_width(int): player's width
        usr_height(int): player's height

    Returns:
        None
        calling return_self with new args for new heart
    """
    global health, usr_x, usr_y, usr_width, usr_height
    # if user couldn't catch the heart (it is passed to the left):
    if heart.x <= -heart.width:
        radius = display_width + random.randrange(10000, 12000)
        heart.return_self(radius, random.randrange(250, 400),
                          heart.width, heart.image)
    if usr_x <= heart.x <= usr_x + usr_width:
        if usr_y <= heart.y <= usr_y + usr_height:
            # if user could catch the heart:
            if health < 7:
                health += 1
            radius = display_width + random.randrange(10000, 12000)
            heart.return_self(radius, random.randrange(250, 400),
                              heart.width, heart.image)


if __name__ == '__main__':
    # the main three strings
    show_menu()
    pygame.quit()
    quit()
