'''
Author: Kyle Charters

Description:
    The gui module contains graphical user interface utilities

Contents:
    - Label
    - AlignedLabel
    - Button
    - TextButton

Notes:
    None
'''
import pygame

class Label(object):
    def __init__(self, font, text, antialias, color, location):
        '''
        Description:
            This gui element holds text
        
        Parameters:
            font: The text's font
            text: The text to display
            antialias: Whether or not to use antialiasing on the text
            color: The color of the text
            location: The location of the text
        
        Notes:
            This is essentially a class based wrapper for the pygame font.render method
        '''
        
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.location = location
        self.label = font.render(text, antialias, color)
    
    def width(self):
        return self.label.get_width()
    
    def height(self):
        return self.label.get_height()
    
    def setLocation(self, location):
        self.location = location
    
    def setText(self, text):
        self.text = text
        self.label = self.font.render(text, self.antialias, self.color)
    
    def setAntialias(self, antialias):
        self.antialias = antialias
        self.label = self.font.render(self.text, antialias, self.color)
    
    def setColor(self, color):
        self.color = color
        self.label = self.font.render(self.text, self.antialias, color)
    
    def render(self, surface):
        surface.blit(self.label, self.location)

class AlignedLabel(Label):
    def __init__(self, font, text, antialias, color, alignment, location, yoffset=0, xoffset=0):
        '''
        Description:
            This gui element holds text, and supports different alignments from the point
        
        Parameters:
            font: The text's font
            text: The text to display
            antialias: Whether or not to use antialiasing on the text
            color: The color of the text
            alignment: The alignment of the text
            location: The location of the text
            yoffset: The offset of location on the y-axis
            xoffset: The offset of location on the x-axis
        
        Notes:
            This class extends Label
            
            Alignment from point:
                0 = Text on right
                1 = Text in middle
                2 = Text on left
        '''
        
        super().__init__(font, text, antialias, color, location)
        self.yoffset = yoffset
        self.xoffset = xoffset
        self.setAlignment(alignment)
    
    def setText(self, text):
        super().setText(text)
        self.setAlignment(self.alignment)
    
    def setLocation(self, location):
        super().setLocation(location)
        self.setAlignment(self.alignment)
    
    def setAlignment(self, alignment):
        self.alignment = alignment
        
        self.xlocation = self.location[0]
        self.ylocation = self.location[1] - (self.label.get_height() / 2) + self.yoffset
        
        if self.alignment == 0:
            self.xlocation += self.xoffset
        elif self.alignment == 1:
            self.xlocation -= (self.label.get_width() / 2) - self.xoffset
        elif self.alignment == 2:
            self.xlocation -= self.label.get_width() - self.xoffset
    
    def render(self, surface):
        surface.blit(self.label, (self.xlocation, self.ylocation))

class Button(object):
    def __init__(self, rect):
        '''
        Description:
            This gui element detects mouse collision in a specified area
        
        Parameters:
            rect: The rectangle that the button occupies
        
        Notes:
            This class does not render anything
        '''
        
        self.rect = pygame.Rect(rect)
        self.selected = False
    
    def setLocation(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def move(self, x, y):
        self.rect = self.rect.move(x, y)
    
    def setDimension(self, width, height):
        self.rect.width = width
        self.rect.height = height
    
    def check(self, mousepos):
        self.selected = self.rect.collidepoint(mousepos)
        return self.selected

class TextButton(Button):
    def __init__(self, font, text, color, highlightcolor, rect):
        '''
        Description:
            This gui element detects mouse collision in a specified area, and renders a solid rectangle with text in the middle
        
        Parameters:
            font: The text's font
            text: The text to display
            color: The color of the button
            highlightccolor: The color of the button when the mouse collides with the rectangle
            rect: The rectangle that the button occupies
        
        Notes:
            None
        '''
        
        super().__init__(rect)
        
        self.label = AlignedLabel(font, text, True, (0, 0, 0), 1, self.rect.center)
        self.color = color
        self.highlightcolor = highlightcolor
    
    def getText(self):
        return self.label.text
    
    def setText(self, text):
        self.label.setText(text)
    
    def setCol(self, color, highlightcolor):
        self.color = color
        self.highlightcolor = highlightcolor
    
    def setLocation(self, x, y):
        super().setLocation(x, y)
        self.label.setLocation(self.rect.center)
    
    def move(self, x, y):
        super().move(x, y)
        self.label.setLocation(self.rect.center)
    
    def setDimension(self, dimension):
        super().setDimension(dimension)
        self.label.setDimension(self.rect.center)
    
    def update(self, mousepos, surface):
        self.check(mousepos)
        self.render(surface)
        
        return self.selected
    
    def render(self, surface):
        if self.selected:
            pygame.draw.rect(surface, self.highlightcolor, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        
        self.label.render(surface)