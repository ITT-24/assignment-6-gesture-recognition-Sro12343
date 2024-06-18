# application for task 3



# gesture input program for first task
import pyglet
from pyglet.window import mouse
from Point import Point
from recognizer import dolar_recognizer
from recognizer import Unistroke
import Strokes
import os.path



from keras.models import load_model
import numpy as np
from scipy.signal import resample


WINDOW_WIDTH = 1220
WINDOW_HEIGHT = 760
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
mouse_x, mouse_y = 0, 0
record = False
positions = []
positions_2 = []
circles = []
result_circles = []

current_dir = os.path.dirname(__file__)


from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
model_p = 'LSTM_64_model.h5'
model = load_model(model_p, compile=False)

# Recompile the model with a new optimizer
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
#
#model_p = os.path.join(current_dir,'LSTM_32_model.keras')
#if os.path.isfile(model_p):
#    model = load_model(model_p) 
#    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#else:
#    print("Model file not found.")





background_p = os.path.join(current_dir,'assets','b.png')
background = pyglet.image.load(background_p)
background_image = pyglet.sprite.Sprite(img=background)

shapes_list = []
shapes_p = os.path.join(current_dir,'assets','shapes.png')
shapes = pyglet.image.load(shapes_p)

speach = ["Lets see how you will handle this Spell.", "That was not quite correct, lets try again.","Well done!","Good Work. You may go now."]
speach_label = pyglet.text.Label(text=speach[0], x=WINDOW_WIDTH/2, y=30,color=(100,100,255,155), anchor_x='center',anchor_y='center')

label_contdown = 0.0
countdown_active = False
size = 112
index=0
max_index =3
points_label = pyglet.text.Label(text=str(index+1)+"/"+str(max_index+1), x=WINDOW_WIDTH-116, y=WINDOW_HEIGHT-82,color=(0,0,0,155), anchor_x='center',anchor_y='center')

for y in range(3, -1, -1):
    for x in range(4):
        if(y != 3):
            
            region = shapes.get_region(size*x+3, size*y+12, size, size)
        else: 
            region = shapes.get_region(size*x+3, size*y+14, size, size-14)
        sprite = pyglet.sprite.Sprite(region, x=WINDOW_WIDTH/2-size*2+50,y=WINDOW_HEIGHT/2-size*2-100)
        sprite.scale = 4
        shapes_list.append(sprite)
        
music_p = os.path.join(current_dir, 'assets','music.mp3')
music = pyglet.media.load(music_p)
music_player = pyglet.media.Player()
music_player.queue(music)
music_player.loop = True


success_sfx_p = os.path.join(current_dir, 'assets','success.mp3')
success_sfx = pyglet.media.load(success_sfx_p)
wrong_sfx_p = os.path.join(current_dir, 'assets','wrong.mp3')
wrong_sfx = pyglet.media.load(wrong_sfx_p)
sfx_player = pyglet.media.Player()
sfx_player.loop = False

@window.event
def on_draw():
    window.clear()
    background_image.draw()
    shapes_list[index].draw()
    speach_label.draw()
    points_label.draw()
    
    for c in circles:
        c.draw()
    for r in result_circles:
        r.draw()
    
    #global edit_img
    #window.clear()
    #show_img = cv2glet(edit_img, 'BGR')
    #show_img.blit(0, 0, 0)
    pass



def update(dt):
    global countdown_active
    global label_contdown
    global index
    if countdown_active:        
        if label_contdown > 0:
            label_contdown -=dt 
        else:
            countdown_active = False
            speach_label.text = speach[0]   
            index += 1  
            points_label.text=str(index+1)+"/"+str(max_index+1)           
            result_circles.clear()
            circles.clear()
        pass          
#    global record
#    if record == True:
#        #check if mouse position changed from last time.
#        if positions != []:
#            if positions[-1].X != mouse_x or positions[-1].Y != mouse_y:
#                #add mouse position to list of positions.
#                positions.append(Point(mouse_x,mouse_y))
#                #and create a circle at the current mouse position.
#                draw_circle(mouse_x,mouse_y)
#                print(record)
#        else:
#            positions.append(Point(mouse_x,mouse_y))
#            draw_circle(mouse_x,mouse_y)
    
def check_input():
    for p in positions:
        sprite = pyglet.shapes.Circle(p.X,WINDOW_HEIGHT-p.Y,5,color=(100,100,255))
        result_circles.append(sprite)
    print(len(positions))    
        
def add_circle(x,y):
    
    sprite = pyglet.shapes.Circle(x,y,5,color=(255,100,100))
    circles.append(sprite)
    


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == mouse.LEFT and record == True:
        global positions
        global positions_2
        positions.append(Point(x,WINDOW_HEIGHT-y))
        positions_2.append([x,WINDOW_HEIGHT-y])
        add_circle(x,y)
        #print("Point("+str(x) + ","+ str(y)+"),")
    
    pass
    
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
        positions_2.clear()
        record = True
        result_circles.clear()
        circles.clear()
        
        print("activate")
        
@window.event
def on_mouse_release(x, y, button, modifiers):
    global countdown_active
    global speach_label
    global label_contdown
    
    if button == mouse.LEFT:
        global record
        record = False
        print("reached")
        result_t = dr.Recognize(positions,True)
        print("result: ")
        print(result_t.Name)
        
        
        NUM_POINTS = 50
        resampled = resample(positions_2, NUM_POINTS)
        resampled_array = np.array(resampled)
        resampled_array = resampled_array.reshape(1, 50, 2)
        prediction = model.predict(resampled_array)
        prediction= np.argmax(prediction, axis=1)
        prediction_name = s[np.argmax(prediction)].Name
        print("--->")
        print(prediction_name)
        print(np.argmax(prediction))
        
        
        if(result_t.Name == s[index].Name):
            sfx_player.queue(success_sfx)
            sfx_player.play()
            if index +1 <= 3:
                print("this")
                speach_label.text = speach[2]
                label_contdown = 2.0
                countdown_active = True
            else:
                speach_label.text = speach[3]      
        else:
            sfx_player.queue(wrong_sfx)
            sfx_player.play()
            
            print("that")
            speach_label.text = speach[1]   
        check_input() 
        #Send recorded points to recognizer. Display results(name, score and time.)
  
    
    
s = Strokes.Unistrokes
#print(s[0].Name)
dr = dolar_recognizer(s)

music_player.play()
        
    

pyglet.clock.schedule_interval(update, 1/60) 

pyglet.app.run()
    
