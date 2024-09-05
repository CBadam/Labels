import streamlit as st
import os
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np
from draw import *
import pandas as pd
import img2pdf


if 'filename' not in st.session_state:
    st.session_state.filename="prices.csv"
if 'df' not in st.session_state:
    st.session_state.df =pd.read_csv(st.session_state.filename, sep=',', encoding='utf-8')


price_bg_color = (237, 245, 255)  # Navy color, RGB format
white_color = (255, 255, 255)  # White color, RGB format
black_color = (0, 0, 0)  # Off Black color, RGB format

# Set image size in pixels
width = 1654
height = 2339

width_mm=210
height_mm=297

dpi=300 #Dots per inch
mm_to_inches=0.03937
mm_to_pixels_300=11,811023622047244
mm_to_pixels=width/width_mm

# Dimensions in mm
price_x=40*mm_to_pixels
price_y=35*mm_to_pixels
price_w=30*mm_to_pixels
price_h=9*mm_to_pixels

euro_width=2*mm_to_pixels

offset_x_price_int=20
price_int_x=price_x-offset_x_price_int
price_int_y=price_y
price_int_w=price_w/2
price_int_h=price_h



price_dec_x=price_x+price_int_w-offset_x_price_int/2
price_dec_y=price_y
price_dec_w=price_w/2
price_dec_h=price_h





stepx=65.5 *mm_to_pixels
stepy=35.5*mm_to_pixels
product_x=10*mm_to_pixels
product_y=25*mm_to_pixels
product_w=60*mm_to_pixels
product_h=9*mm_to_pixels



number_of_columns=3
number_of_rows=7

# Define the scaling factor
scaling_factor = 1.03
# Calculate the new size
new_width = int(width * scaling_factor)
new_height = int(height * scaling_factor)
new_size = (new_width, new_height)
# Calculate the crop box to the original size
new_left = (new_width - width) / 2
new_top = (new_height - height) / 2
new_right = new_left + width
new_bottom = new_top + height

def main():
    st.title("Tickets produits épicerie")
    number_of_products=len(st.session_state.df)
    cnt=0
    page_nbr=0
    images_with_bg=[]
    images_with_new_bg=[]
    images=[]
    while cnt<number_of_products:

        image_new = Image.new("RGB", (width, height), white_color)
        for r in range (number_of_rows):
        
            for c in range (number_of_columns):
                #price_rectangle= Rectangle(width=price_w, height=price_h, pos_x=price_x+c*stepx, pos_y=price_y+r*stepy, color=price_bg_color)
                #product_rectangle= Rectangle(width=product_w, height=product_h, pos_x=product_x+c*stepx, pos_y=product_y+r*stepy, color=price_bg_color)
                i=c+number_of_columns*r+page_nbr*number_of_columns*number_of_rows
                if cnt<number_of_products:
                    bordure_x=product_x+c*stepx+0.1*product_w
                    bordure_y=product_y+r*stepy+0.1*product_h
                    bordure_w=product_w*0.8
                    bordure_h=product_h*0.8
                    bordure_thick=4

                    bordure_int_x=bordure_x+bordure_thick
                    bordure_int_y=bordure_y+bordure_thick
                    bordure_int_w=bordure_w-bordure_thick*2
                    bordure_int_h=bordure_h-bordure_thick*2
                    product_bordure= Rectangle(width=bordure_w, height=bordure_h, pos_x=bordure_x, pos_y=bordure_y, color=black_color)
                    product_bordure2= Rectangle(width=bordure_int_w, height=bordure_int_h, 
                                                pos_x=bordure_int_x, pos_y=bordure_int_y, color=white_color)
                    product=st.session_state.df.loc[i,"product"]
                    price=st.session_state.df.loc[i,"price"]
                    price_int=str(int(price))
                    if int(price*100%100)!=0:
                        price_dec="€"+f'{(int(price*100%100))}'
                    else:
                        price_dec="€"
                    # product_text_start_x, product_text_start_y, product_font=text_frame(product, 
                    #             [product_x+c*stepx,product_y+r*stepy,product_x+product_w+c*stepx,product_y+product_h+r*stepy], 
                    #         "./arialbd.ttf", text_h_placement='center', text_v_placement='center',font_size=30)
                    product_text_start_x, product_text_start_y, product_font=text_frame(product, 
                                [bordure_int_x,bordure_int_y,bordure_int_x+bordure_int_w,bordure_int_y+bordure_int_h], 
                            "./arialbd.ttf", text_h_placement='center', text_v_placement='center',font_size=30)
                    product_text=Text(product, 
                                    [product_text_start_x,product_text_start_y], 
                                    black_color, 
                                    product_font)
                    # price_text_start_x, price_text_start_y, price_font=text_frame(price, 
                    #             [price_x+c*stepx,price_y+r*stepy,price_x+price_w+c*stepx,price_y+price_h+r*stepy], 
                    #         "./arialbd.ttf", text_h_placement='center', text_v_placement='center',font_size=50)
                    # price_text=Text(price, 
                    #                 [price_text_start_x,price_text_start_y], 
                    #                 black_color, 
                    #                 price_font)
                    price_int_text_start_x, price_int_text_start_y, price_int_font=text_frame(price_int, 
                                [price_int_x+c*stepx,price_int_y+r*stepy,price_int_x+price_int_w+c*stepx,price_int_y+price_int_h+r*stepy], 
                            "./arialbd.ttf", text_h_placement='right', text_v_placement='center',font_size=90)
                    price_int_text=Text(price_int, 
                                    [price_int_text_start_x,price_int_text_start_y], 
                                    black_color, 
                                    price_int_font)
                    price_dec_text_start_x, price_dec_text_start_y, price_dec_font=text_frame(price_dec, 
                                [price_dec_x+c*stepx,price_dec_y+r*stepy,price_dec_x+price_dec_w+c*stepx,price_dec_y+price_dec_h+r*stepy], 
                            "./arialbd.ttf", text_h_placement='left', text_v_placement='top',font_size=50)
                    price_dec_text=Text(price_dec, 
                                    [price_dec_text_start_x,price_dec_text_start_y], 
                                    black_color, 
                                    price_dec_font)
                    img_overlay = ImageOverlay('bar_code.png', int(bordure_int_x+10), int(bordure_int_y+140))
                    cnt+=1
                
        for rect in Rectangle.rectangles:
            image_new = rect.draw(image_new)
        for text in Text.texts:
            image_new = text.draw(image_new)
        for overlay_image in ImageOverlay.overlays:
            image_new = overlay_image.draw(image_new)
        
        # Resize the image
        resized_image = image_new.resize(new_size, Image.ANTIALIAS)
        # Crop the image to the original size
        cropped_image = resized_image.crop((new_left, new_top, new_right, new_bottom))
        st.image(cropped_image, caption='reconstructed image')
        images.append(cropped_image)
        page_nbr+=1
        Rectangle.clear_rectangles()
        Text.clear_texts()
        ImageOverlay.clear_overlays()
        
        
        # for i in range(len(st.session_state.df)):
        #     product=st.session_state.df.loc[i,"product"]
        #     price=st.session_state.df.loc[i,"price"]
        #     product_text_start_x, product_text_start_y, product_font=text_frame(product, 
        #                 [product_x,product_y,product_x+product_w,product_y+product_h], 
        #                "./arialbd.ttf", text_h_placement='center', text_v_placement='center')
        #     product_text=Text(product, 
        #                       [product_text_start_x,product_text_start_y], 
        #                       black_color, 
        #                       product_font)

    first_image = images[0]
    additional_images = images[1:]
    first_image.save("Document_final.PDF", save_all=True,append_images=additional_images)
    with open("Document_final.PDF", "rb") as file:
        st.download_button(
            label="Download Document Final",
            data=file,
            file_name="Document_final.PDF",
        )




if __name__ == "__main__":
    main()
