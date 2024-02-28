import pyglet
import random
from pyglet.graphics import Batch
from pyglet.window import key
from pyglet.gl import Config
from math import pi

# Settings and initialization
window = pyglet.window.Window(width= 1600, height=900, caption= "Ping Pong")
window.set_location(150, 100)
window.set_mouse_visible(False)

batch = Batch()
input = {'W': False, 'S': False, 'Enter': False}
ball_state = {'On': False, 'Off': True}
player_speed = 15
ai_speed= 15
ball_speedx = 17
ball_speedy = 17

# Graphics
ball = pyglet.shapes.Circle(window.width/2, window.height/2, 15, color= (255, 255, 255), batch=batch)
player = pyglet.shapes.Rectangle(0, window.height/2-75, 20, 150, (50, 225, 30), batch=batch)
ai = pyglet.shapes.Rectangle(window.width-20, window.height/2-75, 20, 150, (255, 225, 30), batch=batch)
score1 = pyglet.text.Label('0',
                          font_size=36,
                          x=window.width-36, y=window.height-36,
                          anchor_x='center', anchor_y='center',
                          batch = batch)
score2 = pyglet.text.Label('0',
                          font_size=36,
                          x=36, y=window.height-36,
                          anchor_x='center', anchor_y='center',
                          batch = batch)
label = pyglet.text.Label('Press \'Enter\' to start the game.',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                          color=(255, 60, 60, 0),
                          batch = batch)

# Game Loop
@window.event
def on_draw()-> None:
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol: int, modifiers:int) -> None:
    match symbol:
        case key.W:
            input['W'] = True
        case key.S:
            input['S'] = True
        case key.RETURN:
            ball_state["On"] = True
        case key._1:
            ball_state["On"] = False
@window.event
def on_key_release(symbol:int, modifiers:int) -> None:
    match symbol:
        case key.W:
            input['W'] = False
        case key.S:
            input['S'] = False

def update(dt:float)-> None:
    global ball_speedy, ball_speedx
    # Player movement
    if input['W'] and (player.y + player_speed > window.height-player.height) == False:
        player.y += player_speed
    if input['S'] and (player.y-player_speed < 0) == False:
        player.y -= player_speed
    
    # Ball movement
    if ball_state["On"] == True:
        label.color = (255, 60, 60, 0)
        if ball.x-ball.radius + ball_speedx < player.x:
            ball_state["On"] = False
            ball.x = window.width/2
            ball.y = random.randint(0, window.height-100)
            ai.y = window.height/2
            score1.text = str(int(score1.text) + 1)
        if ball.x-ball.radius + ball_speedx > ai.x + ai.width:
            ball_state["On"] = False
            ball.x = window.width/2
            ball.y = random.randint(0, window.height-100)
            ai.y = window.height/2
            score2.text = str(int(score2.text) + 1)

        if ball.x-ball.radius + ball_speedx < player.x + player.width and player.y < ball.y < player.y + player.height:
            ball_speedx = -ball_speedx
        if ball.x+ball.radius > ai.x and ai.y < ball.y < ai.y + ai.height:  
            ball_speedx = -ball_speedx

        if ball.y-ball.radius + ball_speedy < 0:
            ball_speedy = -ball_speedy
        if ball.y+ball.radius+ball_speedy > window.height: 
            ball_speedy = -ball_speedy

        ball.y += ball_speedy
        ball.x += ball_speedx

        # AI movement
        if ball.y-ball.radius > ai.y + ai.height/2 and (ai.y + ai_speed > window.height-ai.height) == False:
            ai.y += ai_speed
        if ball.y-ball.radius < ai.y + ai.height/2 and (ai.y-ai_speed < 0) == False:
            ai.y -= ai_speed
    else:
        label.color = (255, 60, 60, 255)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()