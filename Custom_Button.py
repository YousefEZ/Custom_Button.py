## ¬! v 1.00 SyberProjects
## ¬! 26/09/2019 @ 20:08 GMT

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk, features
import textwrap
from time import sleep
from threading import Thread

class Round_Button(tk.Label):

    def __init__(self, top, text, multi, static_colour, static_t_colour, transformation_colour, transformation_t_colour, background:str='#FFFFFF'):

        '''

        :param top: Top level / root. The window in which the button is going to be placed. [Tkinter Object]
        :param text: Text that is placed on the button. [String]
        :param multi: Multiplier for the size. [Integer]
        :param static_colour: Colour for the button when static. [Tuple,(R,G,B)]
        :param static_t_colour: Colour for the text when the button is static. [Tuple,(R,G,B)]
        :param transformation_colour: Colour for the button when cursor is over it. [Tuple,(R,G,B)]
        :param transformation_t_colour: Colour for the text when the cursor is over the button. [Tuple,(R,G,B)]
        :param background: Sets the background colour of the Button so it can blend with the window's background

        '''

        ## Initialisation
        ## ==============

        tk.Label.__init__(self, top)  # Inherits the features of a label
        self.sc = static_colour
        self.tc = transformation_colour
        self.tsc = static_t_colour
        self.ttc = transformation_t_colour
        self.multi = multi
        self.resoltuion = (int(35*multi), int(10*multi)) # 3.5 : 1 (W : H)
        self.text = text
        self.change_to_trans = False
        self.change_to_static = False

        self.create_custom_image() #Create static and transformed buttons
        self.create_lower_button() #Creates Lower Button
        self.connect_function()
        self.configure(image=self.Images[9]) #Inserts static button images
        self.configure(background=background)
        self.bind("<Enter>", self.on_enter) #Hover on capabilities
        self.bind("<Leave>", self.on_leave) #Hover off capabilities

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
        for i in range(10):

            # Puts the colours in a tuple for use.
            colour = (self.image_colours[i][0],self.image_colours[i][1],self.image_colours[i][2])
            textcolour = (self.text_colours[i][0], self.text_colours[i][1], self.text_colours[i][2])

            # Creates the base for both images (Rectangles)

            self.image_drawer[i].rectangle((0,0, self.resoltuion[0], self.resoltuion[1]), fill=colour)

            # Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
            # 2 on both sides for 2 images.

            self.image_drawer[i].rectangle((self.resoltuion[0] - int(5.5 * self.multi), 0, self.resoltuion[0], self.resoltuion[1]),fill=(0, 0, 0, 0))
            self.image_drawer[i].ellipse((self.resoltuion[0] - int(10 * self.multi), 0, self.resoltuion[0], self.resoltuion[1]),fill=colour)

            self.image_drawer[i].rectangle((0, 0, int(5.5 * self.multi), int(10 * self.multi)), fill=(0, 0, 0, 0))
            self.image_drawer[i].ellipse((0, 0, int(10 * self.multi), int(10 * self.multi)), fill=(colour))



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

        # Creates the base for both images (Rectangles)

        self.lower_drawer.rectangle((0, 0, resoltuion[0], resoltuion[1]), fill=colour)

        # Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
        # 2 on both sides for 2 images.

        # Right side
        self.lower_drawer.rectangle((resoltuion[0] - int(5.5*multi), 0, resoltuion[0], resoltuion[1]),fill=(0, 0, 0, 0))
        self.lower_drawer.ellipse((resoltuion[0] - int(10*multi), 0, resoltuion[0], resoltuion[1]), fill=colour)

        # Left side
        self.lower_drawer.rectangle((0, 0, int(5.5 * multi), int(10 * multi)), fill=(0, 0, 0, 0))
        self.lower_drawer.ellipse((0, 0, int(10 * multi), int(10 * multi)), fill=(colour))

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
        t1 = Thread(target=self.change_sc)
        t1.start()

    def on_leave(self,*args):
        #switches back to static image.
        t1 = Thread(target=self.change_tsc)
        t1.start()

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

    Static_Colour = (255,0,0)
    Text_Transformation_Colour = (255,255,255)
    Transformation_Colour = (0,0,255)
    Text_Static_Colour = (0,0,0)


    Button = Round_Button(app, 'Example', 3, Static_Colour, Text_Static_Colour, Transformation_Colour, Text_Transformation_Colour, Background)
    Button.connect_function(New_Function)
    Button.grid(row=0, column=0)

    app.mainloop()
