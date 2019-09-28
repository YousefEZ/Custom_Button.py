# Round_Button.py
Simple button that is a more visually customisable version of a tkinter button.

Main Class is called: Round_Button

External Dependencies:
======================

PIL (python-imaging library)

Capabiliies:
=============

+ Static Colour to Transformation Colour Animation.
+ Static Text Colour to Transformed Text Colour Animation.
+ Static Outline to Transformed Outline Colour Animation.
+ Function/Command Linking.
+ Size Adjustable
+ Background blendable.

Intialisation:
==============

+ top: Top level / root. The window in which the button is going to be placed. [Tkinter Object]
+ text: Text that is placed on the button. [String]
+ Size: Multiplier for the size. [Integer]
+ static_colour: Colour for the button when static. [Tuple,(R,G,B)]
+ static_t_colour: Colour for the text when the button is static. [Tuple,(R,G,B)]
+ transformation_colour: Colour for the button when cursor is over it. [Tuple,(R,G,B)]
+ transformation_t_colour: Colour for the text when the cursor is over the button. [Tuple,(R,G,B)]
+ background: Sets background colour of the button for blending with the window's background [Tuple,(#RGB)] DEF=#FFFFFF
+ static_outline : Sets outline of static image. [Tuple, (R,G,B)] DEF: static_colour value
+ trans_outline : Sets outline of transformed image. [Tuple, (R,G,B)] DEF: transformation_colour



Linking a Function:
===================

Random_Function = lambda:print('Hello World')
Button = Round_Button(root, text, 3, static_c, static_text_c, trans_c, trans_text_c, '#FFFFFF')
Button.connect_function(Random_Function)



