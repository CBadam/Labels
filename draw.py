from PIL import Image, ImageDraw, ImageOps, ImageFont

class Rectangle:
    rectangles = []
    def __init__(self, width, height, pos_x, pos_y, color, opacity=1.0,fill=True):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.opacity = opacity
        self.fill=fill
        Rectangle.rectangles.append(self)

    def draw(self, base_image):
        overlay = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        rect_position = (self.pos_x, self.pos_y)
        rect_size = (self.width, self.height)
        if self.fill:
            overlay_draw.rectangle([rect_position, (rect_position[0] + rect_size[0], rect_position[1] + rect_size[1])],
                               fill=(self.color[0], self.color[1], self.color[2], int(self.opacity*255)))
        else:
            overlay_draw.rectangle([rect_position, (rect_position[0] + rect_size[0], rect_position[1] + rect_size[1])],
                               fill=None)
        return Image.alpha_composite(base_image.convert('RGBA'), overlay)
    
    @classmethod
    def clear_rectangles(cls):
        cls.rectangles = []

class Text:
    texts = []
    def __init__(self, text, position, color, font):
        self.text = text
        self.position = position
        self.color = color
        self.font = font
        Text.texts.append(self)

    def draw(self, base_image):
        overlay = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.text(self.position, self.text, fill=self.color, font=self.font)
        return Image.alpha_composite(base_image.convert('RGBA'), overlay)
    @classmethod
    def clear_texts(cls):
        cls.texts = []

def text_frame(text, framebox, font_type, text_h_placement='center', text_v_placement='center',font_size=15):
    done = False
    while True:
        # Load a font and calculate text size
        font = ImageFont.truetype(font_type, font_size)
        (left_text, top_text, right_text, bottom_text) = font.getbbox(text, anchor='lt')
        text_width = right_text - left_text
        text_height = bottom_text - top_text
        # Exit loop if font size fits
        if done:
            break
        # Check if text exceeds frame boundaries
        if (text_width > framebox[2] - framebox[0]) or (text_height > framebox[3] - framebox[1]):
            # Decrease font size if text exceeds boundaries
            font_size -= 1
            done = False
        else:
            done=True
    # Calculate starting point coordinates for text (for centered text)
    text_width2, text_height2 = font.getsize(text)
    match text_h_placement:
        case 'center':
            text_start_x = int((framebox[2] + framebox[0]) / 2) - int(text_width2 / 2)
        case 'left':
            text_start_x = framebox[0]
        case 'right':
            text_start_x = framebox[2] - text_width2
        case _:
            text_start_x = int((framebox[2] + framebox[0]) / 2) - int(text_width2 / 2)
    match text_v_placement:
        case 'center':
            text_start_y = int((framebox[3] + framebox[1]) / 2) - int(text_height / 2) - int(text_height2 - text_height)
        case 'top':
            text_start_y = framebox[1] - int(text_height2 - text_height)
        case 'bottom':
            text_start_y = framebox[3] - text_height - int(text_height2 - text_height)
        case _:
            text_start_y = int((framebox[3] + framebox[1]) / 2) - int(text_height / 2) - int(text_height2 - text_height)
    return text_start_x, text_start_y, font

