# gesture input program for first task
import pyglet
from pyglet.window import mouse
from Point import Point
from recognizer import dolar_recognizer
from recognizer import Unistroke
import Strokes


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
mouse_x, mouse_y = 0, 0
record = False
positions = []
circles = []
result_circles = []
prediction_label = pyglet.text.Label(text="", x=WINDOW_WIDTH/2, y=20,color=(100,100,255,155), anchor_x='center',anchor_y='center')


@window.event
def on_draw():
    window.clear()
    prediction_label.draw()
    for c in circles:
        c.draw()
    for r in result_circles:
        r.draw()


def check_input():
    for p in positions:
        sprite = pyglet.shapes.Circle(p.X,WINDOW_HEIGHT-p.Y,5,color=(100,100,255))
        result_circles.append(sprite)
            
        
def add_circle(x,y):
    sprite = pyglet.shapes.Circle(x,y,5,color=(255,100,100))
    circles.append(sprite)
    
    
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == mouse.LEFT and record == True:
        global positions
        positions.append(Point(x,WINDOW_HEIGHT-y))
        add_circle(x,y)
    
    
@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        #Start Recording
        global positions
        global record
        positions.clear()
        record = True
        circles.clear()
        result_circles.clear()
        
        
@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT:
        global record
        record = False
        
        result_t = dr.Recognize(positions,True)
        prediction_label.text = result_t.Name
        check_input() 
       
        
s = Strokes.Unistrokes
dr = dolar_recognizer(s)
pyglet.app.run()
    
