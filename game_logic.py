import pyglet
from pyglet.window import mouse
from Point import Point
from recognizer import dolar_recognizer
import Strokes_game
import os.path

class game_logic():
    def __init__(self,WINDOW_WIDTH,WINDOW_HEIGHT, max_index,nostalgia_mode):

        #nostalgia_mode
        self.nostalgia_mode = nostalgia_mode


        #saving the window size
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        #seting up the countdown variables
        self.countdown_active = False
        self.label_contdown = 0.0
        
        
        #seting up the Progress counting.
        self.index=0
        self.max_index =max_index

        #seting up the recording variables
        self.record = False
        self.positions = []
        self.circles = []
        self.result_circles = []

        #seting up the background image
        self.current_dir = os.path.dirname(__file__)
        self.background_p = os.path.join(self.current_dir,'assets','b.png')
        self.background = pyglet.image.load(self.background_p)
        self.background_image = pyglet.sprite.Sprite(img=self.background)

        #seting up the example Guestures
        self.size = 112
        self.shapes_list = []
        self.shapes_p = os.path.join(self.current_dir,'assets','shapes.png')
        self.shapes = pyglet.image.load(self.shapes_p)
        self.create_shapes()
        
        #seting up the Text Labels
        self.speach = ["Lets see how you will handle this Spell.", "That was not quite correct, lets try again.","Well done!","Good Work. You may go now."]
        self.speach_label = pyglet.text.Label(text=self.speach[0], x=self.WINDOW_WIDTH/2, y=30,color=(100,100,255,155), anchor_x='center',anchor_y='center')
        self.points_label = pyglet.text.Label(text=str(self.index+1)+"/"+str(self.max_index+1), x=WINDOW_WIDTH-116, y=WINDOW_HEIGHT-82,color=(0,0,0,155), anchor_x='center',anchor_y='center')
        
        #seting up the backround music
        self.music_p = os.path.join(self.current_dir, 'assets','music.mp3')
        self.music = pyglet.media.load(self.music_p)
        self.music_player = pyglet.media.Player()
        self.music_player.queue(self.music)
        self.music_player.loop = True

        #seting up the feedback sound effects
        self.success_sfx_p = os.path.join(self.current_dir, 'assets','success.mp3')
        self.success_sfx = pyglet.media.load(self.success_sfx_p)
        self.wrong_sfx_p = os.path.join(self.current_dir, 'assets','wrong.mp3')
        self.wrong_sfx = pyglet.media.load(self.wrong_sfx_p)
        self.sfx_player = pyglet.media.Player()
        self.sfx_player.loop = False

        #seting up the feedback colors
        self.collor_correct = (210,204,0,100)
        self.collor_false = (200,0,0,200)
        self.color = self.collor_false = (200,0,0,100)

        #seting up the recognizer
        self.s = Strokes_game.Unistrokes
        self.dr = dolar_recognizer(self.s)

        
    def countdown(self,dt):
        
        if self.countdown_active:        
            if self.label_contdown > 0:
                self.label_contdown -=dt 
            else:
                if self.index < self.max_index:
                    self.countdown_active = False
                    self.speach_label.text = self.speach[0]   
                    self.index += 1  
                    self.points_label.text=str(self.index+1)+"/"+str(self.max_index+1)           
                    self.result_circles.clear()
                    self.circles.clear()
                else:
                    pyglet.app.exit()
            pass     
            
    def create_shapes(self):
        for y in range(3, -1, -1):
            for x in range(4):
                if(y != 3):
                    
                    region = self.shapes.get_region(self.size*x+3, self.size*y+12, self.size, self.size)
                else: 
                    region = self.shapes.get_region(self.size*x+3, self.size*y+14, self.size, self.size-14)
                sprite = pyglet.sprite.Sprite(region, x=self.WINDOW_WIDTH/2-self.size*2+50,y=self.WINDOW_HEIGHT/2-self.size*2-100)
                sprite.scale = 4
                self.shapes_list.append(sprite)      
                  
    def draw(self):
        self.background_image.draw()
        self.shapes_list[self.index].draw()
        self.speach_label.draw()
        self.points_label.draw()
        
        for c in self.circles:
            c.draw()
        for r in self.result_circles:
            r.draw()
            
    def check_input(self):
        for p in self.positions:
            sprite = pyglet.shapes.Circle(p.X,self.WINDOW_HEIGHT-p.Y,10,color=self.color)
            self.result_circles.append(sprite)
    def add_circle(self,x,y):
        sprite = pyglet.shapes.Circle(x,y,5,color=(255,100,100))
        self.circles.append(sprite)
        
    def on_mouse_drag(self,x,y,buttons):
        if buttons == mouse.LEFT and self.record == True:
            global positions
            self.positions.append(Point(x,self.WINDOW_HEIGHT-y))
            self.add_circle(x,y)
 
 
    def press(self):
        self.positions.clear()
        self.record = True
        self.result_circles.clear()
        self.circles.clear()
        
    def release(self):
        self.record = False
        
        self.result_t = self.dr.Recognize(self.positions,True)
        print(self.s[self.index].Name+" "+ self.result_t.Name)
        if(self.result_t.Name == self.s[self.index].Name) and self.nostalgia_mode == False:
            self.sfx_player.queue(self.success_sfx)
            self.sfx_player.play()
            self.color = self.collor_correct
            if self.index +1 <= self.max_index:
                self.speach_label.text = self.speach[2]
                self.label_contdown = 2.0
            else:
                self.speach_label.text = self.speach[3]     
                self.label_contdown = 4.0
            self.countdown_active = True 
        else:
            self.color = self.collor_false
            self.sfx_player.queue(self.wrong_sfx)
            self.sfx_player.play()

            self.speach_label.text = self.speach[1]   
        self.check_input() 