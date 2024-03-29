## ¬! v 1.00 SyberProjects
## ¬! 26/09/2019 @ 20:08 GMT

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk, features
import textwrap
from time import sleep
from queue import Queue
from threading import Thread

class Round_Button(tk.Label):

    def __init__(self, top, text, size, static_colour, static_t_colour, transformation_colour, transformation_t_colour, background:str='#FFFFFF', static_outline=None, trans_outline=None):

        '''

        :param top: Top level / root. The window in which the button is going to be placed. [Tkinter Object]
        :param text: Text that is placed on the button. [String]
        :param size: Multiplier for the size. [Integer]
        :param static_colour: Colour for the button when static. [Tuple,(R,G,B)]
        :param static_t_colour: Colour for the text when the button is static. [Tuple,(R,G,B)]
        :param transformation_colour: Colour for the button when cursor is over it. [Tuple,(R,G,B)]
        :param transformation_t_colour: Colour for the text when the cursor is over the button. [Tuple,(R,G,B)]
        :param background: Sets the background colour of the Button so it can blend with the window's background [Tuple, (RGB)] Defaults to WHITE (#FFFFFF)
        :param static_outline: outline colour of static image. [Tuple, (RGB)] Defaults to static_colour value.
        :param trans_outline: outline colour of transformed image. [Tuple, (RGB)] Defaults to transformation_colour value.

        '''

        ## Initialisation
        ## ==============

        tk.Label.__init__(self, top)  # Inherits the features of a label
        self.sc = static_colour
        self.tc = transformation_colour
        self.tsc = static_t_colour
        self.ttc = transformation_t_colour
        self.multi = size
        self.resoltuion = (int(35*size), int(10*size)) # 3.5 : 1 (W : H)
        self.text = text
        self.change_to_trans = False
        self.change_to_static = False

        self.static_outline = static_outline
        self.trans_outline = trans_outline
        if static_outline == None:
            self.static_outline = static_colour

        if trans_outline == None:
            self.trans_outline = transformation_colour


        self.create_custom_image() #Create static and transformed buttons
        self.create_lower_button() #Creates Lower Button
        self.connect_function()
        self.configure(image=self.Images[9]) #Inserts static button images
        self.configure(background=background)
        self.bind("<Enter>", self.on_enter) #Hover on capabilities
        self.bind("<Leave>", self.on_leave) #Hover off capabilities
        self.queue = Queue()
        self.Animator = Thread(target=self.Manage_Animation)
        self.Animator.start()


    def create_custom_image(self):

        decrement = -1
        while True:
            # < decrement > : Used for lowering the font size so that the text doesn't go off the screen.
            decrement += 1
            font = ImageFont.truetype("Assets/GentiumBasic-Bold.ttf", int(5.5 * self.multi) - decrement, encoding="unic")
            coords, Lines, line_height = self.draw_multiple_line_text(self.text, font, int(36 * self.multi), int(2 * self.multi), 12)
            if coords[-1][1] + line_height + 5 > self.resoltuion[1]:
                continue
            break

        self.images = [Image.new('RGBA', (self.resoltuion)) for i in range (10)]

        # Initialising the draw the ImageDraw.Draw object
        self.image_drawer = [ImageDraw.Draw(self.images[i]) for i in range (10)]
        self.image_colours = [[self.tc[i] + ((self.sc[i]-self.tc[i])//10)*x for i in range (3)] for x in range (10)]
        self.text_colours = [[self.ttc[i] + ((self.tsc[i] - self.ttc[i]) // 10) * x for i in range(3)] for x in range(10)]
        self.outline_colours = [[self.trans_outline[i] + ((self.static_outline[i] - self.trans_outline[i]) // 10) * x for i in range(3)] for x in range(10)]
        for i in range(10):

            # Puts the colours in a tuple for use.
            colour = (self.image_colours[i][0],self.image_colours[i][1],self.image_colours[i][2])
            textcolour = (self.text_colours[i][0], self.text_colours[i][1], self.text_colours[i][2])
            outline = (self.outline_colours[i][0], self.outline_colours[i][1], self.outline_colours[i][2])

            # Creates the base for both images (Rectangles)

            self.image_drawer[i].rectangle((int(5.5 * self.multi),0, self.resoltuion[0] - int(5.5 * self.multi), self.resoltuion[1]-1), outline=outline, width =2, fill=colour)

            # Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
            # 2 on both sides for 2 images.

            self.image_drawer[i].rectangle((self.resoltuion[0] - int(5.5 * self.multi), 0, self.resoltuion[0], self.resoltuion[1]-2),fill=(0, 0, 0, 0))
            self.image_drawer[i].ellipse((self.resoltuion[0] - int(10 * self.multi), 0, self.resoltuion[0]-1, self.resoltuion[1]-2),outline=outline, width=2, fill=colour)

            self.image_drawer[i].rectangle((0, 0, int(5.5 * self.multi), int(10 * self.multi)-2), fill=(0, 0, 0, 0))
            self.image_drawer[i].ellipse((0, 0, int(10 * self.multi), int(10 * self.multi)-2), outline=outline, width=2 ,fill=(colour))

            self.image_drawer[i].rectangle((int(5.5 * self.multi), 2, self.resoltuion[0] - int(5.5 * self.multi), self.resoltuion[1]-3), fill=colour)

            for x in range (len(coords)):
                self.image_drawer[i].text(coords[x], Lines[x], fill=textcolour, font=font, align='center')

        self.Images = [ImageTk.PhotoImage(self.images[i]) for i in range (10)]

    def create_lower_button(self):
        multi_d = 0.25
        multi = self.multi  - multi_d
        resoltuion = (int(35 * multi), int(10*multi))
        decrement = -1
        while True:
            # < decrement > : Used for lowering the font size so that the text doesn't go off the screen.
            decrement += 1
            font = ImageFont.truetype("Assets/GentiumBasic-Bold.ttf", int(5.5 * multi) - decrement,encoding="unic")
            coords, Lines, line_height = self.draw_multiple_line_text(self.text, font, int(36 * multi),int(2 * multi), 12)
            if coords[-1][1] + line_height + 5 > self.resoltuion[1]-(10*multi_d):
                continue
            break


        self.lower_button = Image.new('RGBA', (resoltuion))

        # Initialising the draw the ImageDraw.Draw object
        self.lower_drawer = ImageDraw.Draw(self.lower_button)

        colour = (self.image_colours[0][0], self.image_colours[0][1], self.image_colours[0][2])
        textcolour = (self.text_colours[0][0], self.text_colours[0][1], self.text_colours[0][2])
        outline = (self.outline_colours[0][0], self.outline_colours[0][1], self.outline_colours[0][2])

        # Creates the base for both images (Rectangles)


        # Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
        # 2 on both sides for 2 images.


        self.lower_drawer.rectangle((0, 0, resoltuion[0], resoltuion[1]-1), outline=outline, width=2,  fill=colour)

        # Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
        # 2 on both sides for 2 images.

        # Right side
        self.lower_drawer.rectangle((resoltuion[0] - int(5.5*multi), 0, resoltuion[0], resoltuion[1]),fill=(0, 0, 0, 0))
        self.lower_drawer.ellipse((resoltuion[0] - int(10*multi), 0, resoltuion[0], resoltuion[1]), outline=outline, width=2, fill=colour)

        # Left side
        self.lower_drawer.rectangle((0, 0, int(5.5 * multi), int(10 * multi)), fill=(0, 0, 0, 0))
        self.lower_drawer.ellipse((0, 0, int(10 * multi), int(10 * multi)), outline=outline, width=2, fill=(colour))

        self.lower_drawer.rectangle((int(5.5 * multi), 2, resoltuion[0] - int(5.5*multi), resoltuion[1]-3), fill=colour)

        for x in range(len(coords)):
            self.lower_drawer.text(coords[x], Lines[x], fill=textcolour, font=font, align='center')

        delta_x = (self.resoltuion[0] - resoltuion[0])//2
        delta_y = (self.resoltuion[1] - resoltuion[1])//2


        #Perfects the size for pasting.
        self.lower_button = self.lower_button.resize(size=(self.resoltuion[0] - delta_x*2, self.resoltuion[1] - delta_y*2))

        #Pasting Image ontop of transparent image with original resolution.
        self.Button = Image.new('RGBA', (self.resoltuion))
        self.Button.paste(self.lower_button, (delta_x, delta_y, self.resoltuion[0] - delta_x, self.resoltuion[1] - delta_y), self.lower_button)

        self.lower_button = ImageTk.PhotoImage(self.Button)



    def draw_multiple_line_text(self, text, font, text_start_width, text_start_height, Line_Width):
        ## Used for creating multi-line text. Splits the text across multiple lines if the text crosses the line width.

        y_text = text_start_height
        x_text = text_start_width
        lines = textwrap.wrap(text, width=int(Line_Width))
        Coords = []
        Lines = []
        line_height = 0
        for line in lines:
            line_width, line_height = font.getsize(line)
            coords = [(x_text - line_width) / 2, y_text]
            y_text += line_height
            Coords.append(coords)
            Lines.append(line)
        return Coords, Lines, line_height

    ## Animation Effect.
    ## Hovering.

    def on_enter(self,*args):
        #switches images to the transformed button.
        self.Q_Dump()
        self.queue.put('E')

    def Q_Dump(self):
        for i in range (self.queue.qsize()):
            self.queue.get_nowait()

    def on_leave(self,*args):
        #switches back to static image.
        self.Q_Dump()
        self.queue.put('L')

    def Manage_Animation(self):
        while True:
            Factor = self.queue.get()
            if Factor == 'E':
                self.change_sc()
            elif Factor == "L":
                self.change_tsc()


    def change_sc(self, si:int=9):
        self.change_to_static = True
        for i in range (si,0,-1):
            if self.change_to_trans == True:
                self.change_to_static = False
                self.change_tsc(i)
                break
            sleep(0.01)
            self.configure(image=self.Images[i])

        if self.change_to_static:
            self.change_to_static = False

    def change_tsc(self, si:int=0):

        self.change_to_trans = True
        for i in range (si, 10):
            if self.change_to_static == True:
                self.change_to_trans = False
                self.change_sc(i)
                break
            sleep(0.01)
            self.configure(image=self.Images[i])

        if self.change_to_trans:
            self.change_to_trans = False


    def connect_function(self, function=lambda:None):
        #Binds the button to a function.

        def connector(*args):
            self.configure(image=self.lower_button)
            function()

        def disconnector(*args):
            self.configure(image=self.Images[0])

        self.bind("<ButtonPress-1>", connector)
        self.bind("<ButtonRelease-1>", disconnector)


if __name__ == '__main__':
    def New_Function():
        print ('Functioning')

    app = tk.Tk()
    Background = ('#000000')
    app.configure(background = Background)

    Static_Colour = (0,0,0)
    Text_Transformation_Colour = (255,255,255)
    Transformation_Colour = (0,0,0)
    Text_Static_Colour = (125,125,125)

    Static_Outline = (125,125,125)
    Transformation_Outline = (255,255,255)

    Button = Round_Button(app, 'Login', 3, Static_Colour, Text_Static_Colour, Transformation_Colour, Text_Transformation_Colour, Background, Static_Outline, Transformation_Outline)
    Button.connect_function(New_Function)
    Button.grid(row=2, column=1, pady= 5, padx=10)


    Label1 = ttk.Label(app, text='Username')
    Label1.configure(background = Background)
    Label1.configure(foreground=('#FFFFFF'))
    Label1.grid(row=0,column=0, pady= 5, padx=10)

    Entry1 = ttk.Entry(app)
    Entry1.grid(row =0, column=1, pady= 5, padx=10)

    Label2 = ttk.Label(app, text='Password')
    Label2.configure(background = Background)
    Label2.configure(foreground = ('#FFFFFF'))
    Label2.grid(row=1, column=0, pady= 5, padx=10)

    Entry2 = ttk.Entry(app)
    Entry2.grid(row=1, column=1, pady= 5, padx=10)


    app.mainloop()
