import cv2
import genanki
import time
import glob
import random
import os
from autoocr import AutoOCR
from PIL import Image
import tempfile
import numpy as np

# Initialization (Edit this part only)
lang = 'bangla'                # Set your own language
current_dir = 'C:/qna_test/'    # Give your own directory
tess_dir = 'C:/Program Files/Tesseract-OCR'        # Set the tessaract directory

Anki_model_seed_value = 2
Anki_deck_seed_value = 3
Anki_low_lim = 1000000000
Anki_up_lim = 9999999999
red_color = (0,0,255)
green_color = (0,255,0)
blue_color = (255,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX

# Seed value generation
random.seed(Anki_model_seed_value)
model_val = random.randint(Anki_low_lim, Anki_up_lim)
random.seed(Anki_deck_seed_value)
deck_val = random.randint(Anki_low_lim, Anki_up_lim)

class bbox():
    def __init__(self):
        self.bbox_points = []
        self.text_points = []
        self.boxed_img = []
        self.button_down = False
        self.temp_img = []
        self.color = blue_color
        self.bbtext = "default"
        self.bbcolor = blue_color


    def cropEvent(self, event, x, y, flags, param):
        '''
        Mouse pressing recording event used by bounding_box_crop() function

        Parameters
        ----------
        event : any button or input's current state (Pressed or unpressed)
        x : x-coordinate of the image
        y : y-coordinate of the image
        flags : Some user defined conditions
        param : User defined parameters like here is image is given
        '''

        # Mouse was not pressed, but you are pressing now
        if (self.button_down == False) and (event == cv2.EVENT_LBUTTONDOWN):
            self.button_down = True
            self.bbox_points = [(x, y)]
            # print(f"bbox Points:{self.bbox_points}")
            self.text_points = [(x - 10, y - 10)]

        elif (self.button_down == True) and (event == cv2.EVENT_MOUSEMOVE):
            self.temp_img = param.copy()
            # self.temp_img = np.array(self.temp_img)
            point = (x, y)
            cv2.rectangle(self.temp_img, self.bbox_points[0], point, self.bbcolor, 1)
            cv2.putText(self.temp_img, self.bbtext, self.text_points[0], font, 1, self.bbcolor)
            cv2.imshow("Bounding box generation - Press C to go next", self.temp_img)

        elif (event == cv2.EVENT_LBUTTONUP):
            self.button_down = False
            self.bbox_points.append((x, y))
            cv2.rectangle(self.temp_img, self.bbox_points[0], self.bbox_points[1], self.bbcolor, 1)
            cv2.putText(self.temp_img, self.bbtext, self.text_points[0], font, 1, self.bbcolor)
            cv2.imshow("Bounding box generation - Press C to go next", self.temp_img)

    def bounding_box_crop(self, img: list, type: str, sn: int):
        '''
        Creates bounding box according to the type (Question or Answer)

        Parameters
        ----------
        self : to access class initialized variables
        img : Given Image where bounding box will be drawn
        type : Depending on different type colors of the bboxes are going to change
                for Questions -> Red color, for Answers -> Green color
        sn : Serial Number of the current question or answer

        Return
        ------
        images of the bounding box region and the whole modified image as Mat 
        '''
        
       
        bbox_image = []

        if type == 'q':
            self.bbcolor = red_color
            self.bbtext = "Q" + str(sn)
        elif type == 'a':
            self.bbcolor = green_color
            self.bbtext = "A" + str(sn)

        cv2.namedWindow("Bounding box generation - Press C to go next")
        # cv2.imshow("Bounding box generation - Press C to go next", self.boxed_img)
        self.temp_img = img.copy()

        while True:
            cv2.setMouseCallback("Bounding box generation - Press C to go next", self.cropEvent, img)
            cv2.imshow("Bounding box generation - Press C to go next", self.temp_img)
            time.sleep(0.1)
            key = cv2.waitKey(1)
            if key == ord("c"):
                self.boxed_img = self.temp_img.copy()
                cv2.destroyAllWindows()
                mod_img = self.boxed_img
                x1 = self.bbox_points[0][0]
                x2 = self.bbox_points[1][0]
                y1 = self.bbox_points[0][1]
                y2 = self.bbox_points[1][1]
                print(f'x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2}')
                bbox_image = self.boxed_img[y1:y2, x1:x2]
                return bbox_image, mod_img
            
            elif key == 27:
                break

        
    

## Genanki part
qNa_model = genanki.Model(
    model_val,
    'Q&A',
    fields = [
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])
    
qNa_deck = genanki.Deck(
    deck_val,
    'BCS QnA'
)



### Main Running part ###
if __name__ == '__main__':
    oa = AutoOCR(lang=lang)
    oa.set_datapath(tess_dir)

    for file in glob.glob(current_dir + '*.JPG'):
        file = os.path.normpath(file)
        out_img = []
        
        print(file)
        img = cv2.imread(file)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # somekind of Thresholding
        # pytesseract or any kind of OCR software that reads Bangla/English

        # # loop through quesetions or answers untill 'Esc' is pressed
        # loop = True
        # def key_capture_thread():
        #     global loop
        #     a = keyboard.read_key()
        #     if a == "esc":
        #         loop = False

        # # seperate threading for capturing the key    
        # th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

        bbox = bbox()

        count = 1
        while True:
            print("running")
            # For each question
            x = bbox.bounding_box_crop(img=img, type="q", sn=count)
            if x == None:
                break
            else:
                ques_img, img = x
                ans_img, img = bbox.bounding_box_crop(img=img, type='a', sn=count)

            
            ques_img = np.array(ques_img)
            ans_img = np.array(ans_img)
             
            ques_img = Image.fromarray(ques_img)
            ans_img = Image.fromarray(ans_img)

            q_img = tempfile.TemporaryFile(delete=False)
            a_img = tempfile.TemporaryFile(delete=False)
           
            ques_img.save(q_img, 'jpeg')
            ans_img.save(a_img, 'jpeg')
            file1 = q_img.name
            file2 = a_img.name
            q_img.close()
            a_img.close()


            ques_txt = oa.get_text(file1)
            ans_txt = oa.get_text(file2)
            print(ques_txt)
            print(ans_txt)
            os.remove(file1)
            os.remove(file2)

            note = genanki.Note(
                qNa_model,
                [
                    ques_txt, ans_txt
                ]
            )
            qNa_deck.add_note(note)
            
        os.chdir(current_dir)
        genanki.Package(qNa_deck).write_to_file('qna.apkg')
        print("done saving successfully")

    
