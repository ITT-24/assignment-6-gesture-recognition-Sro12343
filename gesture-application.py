# application for task 3
import sys
import pyglet
from pyglet.window import mouse
from game_logic import game_logic
        
  
number_of_symbols = 4      
nostalgia_mode = False  
if len(sys.argv) > 1:
    if int(sys.argv[1]) <= 15 and int(sys.argv[1]) > 0:
        number_of_symbols = int(sys.argv[1])
     
#For the pourpose of grading this Assignment the Nostalgia mode should be turned off!
if len(sys.argv) > 2:
    if str(sys.argv[2]) == "True":
        nostalgia_mode = True
    print(nostalgia_mode)

        
WINDOW_WIDTH = 1220
WINDOW_HEIGHT = 760
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
game = game_logic(WINDOW_WIDTH,WINDOW_HEIGHT, number_of_symbols-1,nostalgia_mode)


@window.event
def on_draw():
    window.clear()    
    game.draw()


def update(dt):
     game.countdown(dt)
    

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    game.on_mouse_drag(x,y,buttons)

    pass

    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        #Start Recording
        game.press()
        
        
@window.event
def on_mouse_release(x, y, button, modifiers):    
    if button == mouse.LEFT:
        game.release()
        
    

game.music_player.play()    
pyglet.clock.schedule_interval(update, 1/60) 
pyglet.app.run()
    
