## ¬! v 1.00 SyberProjects
## ¬! 26/09/2019 @ 20:08 GMT

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk, features
import textwrap

class Round_Button(tk.Label):

    def __init__(self, top, text, multi, static_colour, static_t_colour, transformation_colour, transformation_t_colour):

        '''

        :param top: Top level / root. The window in which the button is going to be placed. [Tkinter Object]
        :param text: Text that is placed on the button. [String]
        :param multi: Multiplier for the size. [Integer]
        :param static_colour: Colour for the button when static. [Tuple,(R,G,B)]
        :param static_t_colour: Colour for the text when the button is static. [Tuple,(R,G,B)]
        :param transformation_colour: Colour for the button when cursor is over it. [Tuple,(R,G,B)]
        :param transformation_t_colour: Colour for the text when the cursor is over the button. [Tuple,(R,G,B)]

        '''

        ## Initialisation
        ## ==============

        tk.Label.__init__(self, top)  # Inherits the features of a label
        self.sc = static_colour
        self.tc = transformation_colour
        self.tsc = static_t_colour
        self.ttc = transformation_t_colour
        self.multi = multi
        self.aspect_ratio = (int(35*multi), int(10*multi)) # 3.5 : 1 (W : H)
        self.text = text

        self.create_custom_image() #Create static and transformed buttons
        self.configure(image=self.original_image) #Inserts static button images

        self.bind("<Enter>", self.on_enter) #Hover on capabilities
        self.bind("<Leave>", self.on_leave) #Hover off capabilities

    def create_custom_image(self):
        self.original_image = Image.new('RGBA', (self.aspect_ratio))
        self.changed_image = Image.new('RGBA', (self.aspect_ratio))


        #Initialising the draw the ImageDraw.Draw object
        self.original_draw = ImageDraw.Draw(self.original_image)
        self.changed_draw =  ImageDraw.Draw(self.changed_image)

        #Creates the base for both images (Rectangles)
        self.original_draw.rectangle((0,0, self.aspect_ratio[0],self.aspect_ratio[1]), fill = self.sc)
        self.changed_draw.rectangle((0, 0, self.aspect_ratio[0], self.aspect_ratio[1]), fill=self.tc)

        #Create a rectangle to remove the unwanted areas of colour, and adds an elipses to give a round effect.
        #2 on both sides for 2 images.
        self.changed_draw.rectangle((self.aspect_ratio[0] - int(5.5*self.multi), 0, self.aspect_ratio[0], self.aspect_ratio[1]),fill=(215, 0, 0, 0))
        self.changed_draw.ellipse((self.aspect_ratio[0] - int(10*self.multi), 0, self.aspect_ratio[0], self.aspect_ratio[1]),fill=self.tc)

        self.changed_draw.rectangle((0, 0, int(5*self.multi), int(10*self.multi)), fill=(0, 0, 0, 0))
        self.changed_draw.ellipse((0, 0, int(10*self.multi), int(10*self.multi)), fill=(self.tc))

        self.original_draw.rectangle((self.aspect_ratio[0] - int(5.5*self.multi), 0, self.aspect_ratio[0], self.aspect_ratio[1]),fill=(0, 0, 0, 0))
        self.original_draw.ellipse((self.aspect_ratio[0] - int(10*self.multi), 0, self.aspect_ratio[0], self.aspect_ratio[1]),fill=self.sc)

        self.original_draw.rectangle((0, 0, int(5.5*self.multi), int(10*self.multi)), fill=(0, 0, 0, 0))
        self.original_draw.ellipse((0, 0, int(10*self.multi), int(10*self.multi)), fill=self.sc)

        decrement = -1
        while True:
            #< decrement > : Used for lowering the font size so that the text doesn't go off the screen.
            decrement += 1
            font = ImageFont.truetype("Assets/GentiumBasic-Bold.ttf", int(5.5*self.multi)-decrement, encoding="unic")
            coords, Lines, line_height = self.draw_multiple_line_text(self.text, font, int(36*self.multi), int(2*self.multi), 12)
            if coords[-1][1] + line_height + 5 > self.aspect_ratio[1]:
                continue
            for i in range (len(coords)):
                self.original_draw.text(coords[i], Lines[i], fill=self.tsc, font=font, align='center')
                self.changed_draw.text(coords[i], Lines[i], fill=self.ttc, font=font, align='center')
            break


        self.original_image = ImageTk.PhotoImage(self.original_image)
        self.changed_image = ImageTk.PhotoImage(self.changed_image)


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

    def on_enter(self,*args):
        #switches images to the transformed button.
        self.configure(image=self.changed_image)


    def on_leave(self,*args):
        #switches back to static image.
        self.configure(image=self.original_image)

    def connect_function(self, function):
        #Binds the button to a function.

        def connector(*args):
            function()

        self.bind("<Button-1>", connector)


if __name__ == '__main__':
    def New_Function():
        print ('Functioning')

    app = tk.Tk()
    Static_Colour = (255,0,0)
    Text_Static_Colour = (255,255,255)
    Transformation_Colour = (0,0,255)
    Text_Transformation_Colour = (0,0,0)
    Button = [Round_Button(app, 'ExampleTeeset', 7, Static_Colour, Text_Static_Colour, Transformation_Colour, Text_Transformation_Colour) for i in range (4)]

    [Button[x].connect_function(New_Function) for x in range (4)]

    Button[0].grid(row=0, column=0)
    Button[1].grid(row=0, column=1)
    Button[2].grid(row=1, column=0)
    Button[3].grid(row=1, column=1)
    app.mainloop()
