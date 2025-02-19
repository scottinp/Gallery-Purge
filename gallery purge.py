#FOLDER_PATH = "/Users/scottin/Downloads/gallery purge/Tests/"
#FOLDER_PATH = "/Users/scottin/Pictures/Photos Library.photoslibrary/originals/1/"
FOLDER_PATH = ""

from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
import os
import random 
import shutil #move files
import cv2 #video playback
register_heif_opener()


VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.heic')
max_width, max_height = 500, 500
IMAGE_PATH = ""
files = []


def iterate():
    global IMAGE_PATH
    global count, countLabel, length
    if 'video_capture' in globals() and video_capture.isOpened():
        video_capture.release()

    if files:
        IMAGE_PATH = os.path.join(FOLDER_PATH, random.choice(files))



        count += 1
        countLabelText = f"{count} / {length}"  
        countLabel.config(text=countLabelText)

        print(IMAGE_PATH)
        load_media()
    else:
        print("No more images/videos to review.")
        ttk.Label(mainframe, text="No more images/videos to review.").grid(column=2, row=2, sticky=W)

def delete():
    if IMAGE_PATH:
        deleted_folder = os.path.join(FOLDER_PATH, "Deleted")

        if not os.path.exists(deleted_folder):
            os.makedirs(deleted_folder)
        
        # keep subdirectory structure in "Deleted"
        relative_path = os.path.relpath(IMAGE_PATH, FOLDER_PATH)  # Get relative path
        destination_path = os.path.join(deleted_folder, relative_path)  

        # make sub directs if needed
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        shutil.move(IMAGE_PATH, destination_path)
        files.remove(IMAGE_PATH)

        iterate()

def keep():
    if IMAGE_PATH:
        files.remove(IMAGE_PATH)
        iterate()

def load_media():
    global img_label, img, video_capture

    # clear
    img_label.config(image=None)
    img_label.image = None

    # videos
    if IMAGE_PATH.lower().endswith(('.mp4', '.avi', '.mov')):
        # open video
        video_capture = cv2.VideoCapture(IMAGE_PATH)

        def update_video():
            ret, frame = video_capture.read()
            if ret:
                #make rgb
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                #resize
                original_width, original_height = frame.shape[1], frame.shape[0]
                aspect_ratio = original_width / original_height
                if original_width > original_height:
                    # Resize based on width
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    # Resize based on height
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)

                # Resize 
                frame = cv2.resize(frame, (new_width, new_height))

                #convert to img
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                img_label.config(image=img)
                img_label.image = img

                # update every 25 ms which is about 40 fps
                img_label.after(25, update_video)  
            else:
                # Release the video capture object when the video ends
                video_capture.release()

        update_video()
    else:
        # images
        image = Image.open(IMAGE_PATH)

        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(image)
        img_label.config(image=img)
        img_label.image = img


# Title of application
root = Tk()
root.title("Gallery Purge")

# Frame widget, holds contents
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#part 2
def begin():

    global img_label
    global FOLDER_PATH
    global files
    global count

    #get path and set
    FOLDER_PATH = entry.get()
    #files = [f for f in os.listdir(FOLDER_PATH) if f.lower().endswith(VALID_EXTENSIONS)]
    for root, _, filenames in os.walk(FOLDER_PATH):
        for filename in filenames:
            if filename.lower().endswith(VALID_EXTENSIONS):
                files.append(os.path.join(root, filename))  # Get full file path

    #Del old buttons
    pathLabel.destroy()
    beginButton.destroy()

    # Buttons
    ttk.Button(mainframe, text="Delete", command=delete).grid(column=1, row=3, sticky=W)
    ttk.Button(mainframe, text="Keep", command=keep).grid(column=3, row=3, sticky=W)

    # Image/Video
    img_label = Label(mainframe)
    img_label.grid(column=1, row=2, columnspan=3, pady=10)

    #Labels
    count = 0
    global length 
    length = len(files)
    countLabelText = str(count) + " / " + str(length)

    global countLabel 
    countLabel = ttk.Label(mainframe, text=countLabelText)
    countLabel.grid(column=2, row=1, sticky=W)

    # initialize 
    iterate()



pathLabel = ttk.Label(mainframe, text="PATH to photo/images")
pathLabel.grid(column=2, row=1, sticky=W)

beginButton = ttk.Button(mainframe, text="Begin", command=begin)
beginButton.grid(column=2, row=3, sticky=W)

entry = tk.Entry(mainframe, width=30)
entry.grid(column=2, row=2, sticky=W)

root.mainloop()