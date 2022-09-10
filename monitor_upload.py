import os
from datetime import datetime
import cv2
import time
import argparse
from upload_v2 import upload_file

parser = argparse.ArgumentParser()
parser.add_argument("IN_FOLDER")
parser.add_argument("OUT_FOLDER")
parser.add_argument("SAVE_TO_FIREBASE", type=bool)
args = parser.parse_args()
print(args)

IN_FOLDER = args.IN_FOLDER
OUT_FOLDER = args.OUT_FOLDER
SAVE_TO_FIREBASE = args.SAVE_TO_FIREBASE

def load_data():
    reset = True
    t= True
    while t:
        if reset:
            all_files = []
            start = datetime.now()
            reset = False
            new_scene = True
        files = os.listdir(IN_FOLDER)
        new_files = list(set(files) - set(all_files))
        if new_files:
            print("adding files")
            all_files.extend(new_files)
            time.sleep(0.1)
            if new_scene:
                image_input_file = IN_FOLDER + all_files[int(len(files) / 2)]
                image = cv2.imread(image_input_file)
                image_ouput_file = OUT_FOLDER + start.strftime("%Y-%m-%d_%H-%M-%S") + '_image.jpg'
                cv2.imwrite(image_ouput_file, image)
                new_scene = False

                if SAVE_TO_FIREBASE:
                    print('Uploading image...')
                    upload_file(image_ouput_file)
        else:
            time.sleep(0.1)
            if ((
                    datetime.now() - start).total_seconds() > 6):  # if less than 3 seconds have passed and we have new files
                print('RESET')
                for file in all_files:
                    os.remove(os.path.join(IN_FOLDER, file))
                reset = True
                t = False


# if __name__ == "__main__":
#     load_data()
