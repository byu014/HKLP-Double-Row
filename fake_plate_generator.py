import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

from img_utils import *
from jittering_methods import *

fake_resource_dir  = sys.path[0] + "/fake_resource/" 
output_dir = sys.path[0] + "/test_plate/"

fake_resource_dir  = sys.path[0] + "/fake_resource/" 
output_dir = sys.path[0] + "/test_plate/"
number_dir = [fake_resource_dir + "/numbers/",fake_resource_dir + "/numbers1/" ]
letter_dir = [fake_resource_dir + "/letters/" ,fake_resource_dir + "/letters1/"]
plate_dir = fake_resource_dir + "/plate_background_use/"

# character_y_size = 113
character_y_size = 140
plate_y_size = 328

class FakePlateGenerator():
    def __init__(self, plate_size):

        self.dst_size = plate_size

        self.numbers = self.load_image(number_dir[0], character_y_size)
        self.letters = self.load_image(letter_dir[0], character_y_size)
        # self.numbers = self.load_imageInv(number_dir, character_y_size)
        # self.letters = self.load_imageInv(letter_dir, character_y_size)

        self.numbers_and_letters = dict(self.numbers, **self.letters)

        #we only use blue plate here
        self.plates = self.load_image(plate_dir, plate_y_size)
    
        for i in self.plates.keys():
            self.plates[i] = cv2.cvtColor(self.plates[i], cv2.COLOR_BGR2BGRA)

        #positions
        self.character_position_x_listTop = [270,420]
        self.character_position_x_listBotStart = [130,200,270,340]      
        self.character_position_x_listBotRest = [] 
    
    def get_radom_sample(self, data):
        keys = list(data.keys())
        i = random.randint(0, len(data) - 1)
        key = keys[i]
        value = data[key]

        #注意对矩阵的深拷贝
        return key, value.copy()

    def load_image(self, path, dst_y_size):
        img_list = {}
        current_path = sys.path[0]

        listfile = os.listdir(path)     

        for filename in listfile:
            img = cv2.imread(path + filename, -1)
            
            height, width = img.shape[:2]
            x_size = int(width*(dst_y_size/height))+50
            img_scaled = cv2.resize(img, (x_size, dst_y_size), interpolation = cv2.INTER_CUBIC)
            
            img_list[filename[:-4]] = img_scaled

        return img_list

    def add_character_to_plateBottom(self, character, plate, x):
        h_plate, w_plate = plate.shape[:2]
        h_character, w_character = character.shape[:2]

        start_x = x - int(w_character/2)
        # start_y = int((h_plate - h_character)/2)
        start_y = h_plate//2

        a_channel = cv2.split(character)[3]
        ret, mask = cv2.threshold(a_channel, 100, 255, cv2.THRESH_BINARY)

        overlay_img(character, plate, mask, start_x, start_y)

    def add_character_to_plateTop(self, character, plate, x):
        h_plate, w_plate = plate.shape[:2]
        h_character, w_character = character.shape[:2]

        start_x = x - int(w_character/2)
        # start_y = int((h_plate - h_character)/2)
        start_y = 20

        a_channel = cv2.split(character)[3]
        ret, mask = cv2.threshold(a_channel, 100, 255, cv2.THRESH_BINARY)

        overlay_img(character, plate, mask, start_x, start_y)

    def generate_one_plate(self):
        #self.character_position_x_list = self.character_position_x_listOG
        _, plate_img = self.get_radom_sample(self.plates)
        plate_name = ""

        num = random.randint(3, 102)#6
        num = 6 if num >= 6 else num

        #i = (len(self.character_position_x_list) - num)//2 - 1
        
        i = 6 - num
        character, img = self.get_radom_sample(self.letters)
        self.add_character_to_plateTop(img, plate_img, self.character_position_x_listTop[0])
        plate_name += "%s"%(character,)

        character, img = self.get_radom_sample(self.letters)
        self.add_character_to_plateTop(img, plate_img, self.character_position_x_listTop[1])
        plate_name += "%s"%(character,)

        #self.character_position_x_list = [x.__sub__(10) for x in self.character_position_x_list]

        #makes sure first digit does not start with a 0
        self.character_position_x_listBotRest.clear()
        for j in range(1,4):
            self.character_position_x_listBotRest.append(self.character_position_x_listBotStart[i] + j*150)
        while True:
            character, img =  self.get_radom_sample(self.numbers)
            if int(character) != 0:
                self.add_character_to_plateBottom(img, plate_img, self.character_position_x_listBotStart[i])
                plate_name += character
                break

        for j in range(4,num+1):
            character, img =  self.get_radom_sample(self.numbers)
            self.add_character_to_plateBottom(img, plate_img, self.character_position_x_listBotRest[j-4])
            plate_name += character

        #转换为RBG三通道
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGRA2BGR)
  
        #转换到目标大小
        plate_img = cv2.resize(plate_img, self.dst_size, interpolation = cv2.INTER_AREA)

        return plate_img, plate_name

if __name__ == "__main__":
    # fake_resource_dir  = sys.path[0] + "/fake_resource/" 
    # output_dir = sys.path[0] + "/test_plate/"
    img_size = (240, 180)#80, 60

    fake_plate_generator = FakePlateGenerator( img_size)
    reset_folder(output_dir)
    numImgs = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    for i in range(0, numImgs):
        #random font
        font = random.randint(0,1)
        fake_plate_generator.numbers = fake_plate_generator.load_image(number_dir[font], character_y_size)
        fake_plate_generator.letters = fake_plate_generator.load_image(letter_dir[font], character_y_size)
        plate, plate_name = fake_plate_generator.generate_one_plate()
        plate = jittering_color(plate)
        plate = add_noise(plate)
        plate = jittering_blur(plate)
        plate = jittering_scale(plate)

        save_random_img(output_dir, plate)
