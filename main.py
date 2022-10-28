import datetime
import imutils
import cv2
import os
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


def movement_detector(carpeta,carpetanueva):
    file_title = file_title_grid.get()
    min_area = float(min_area_grid.get())
    contrast = float(contrast_grid.get())
    brightness = int(brightness_grid.get())
    speed = float(speed_grid.get())
    time_that_has_to_pass = float(time_that_has_to_pass_grid.get())
    with open(f'{carpetanueva}/{file_title}.txt', 'w') as f:
        for i,video in enumerate(os.listdir(carpeta)):
            displayedText.set(f"Analizando archivo {i+1} de {len(os.listdir(carpeta))}")
            label.update_idletasks()
            f.write(f"{video}:\n")
            video = str(f"{carpeta}/{video}")
            firstFrame = None
            vs = cv2.VideoCapture(video)
            if not vs.isOpened():
                f.write(f"El archivo no es un vídeo o no se puede abrir.\n\n")
                continue
            fps = vs.get(cv2.CAP_PROP_FPS)
            frames = 1
            while True:
                frame = vs.read()
                frame = frame[1]
                owlIs = False
                if frame is None:
                    break
                if firstFrame is None:
                    frames -= 1
                    last_message = False
                    time_without_change = 0
                frames += 1
                time_without_change +=1
                if (frames-1) % (fps * speed) == 0:
                    frame = imutils.resize(frame, width=500)
                    new_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    new_image[:,:,2] = np.clip(contrast * new_image[:,:,2] + brightness, 0, 255)
                    new_image = cv2.cvtColor(new_image, cv2.COLOR_HSV2BGR)
                    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)
                    if frames == 0:
                        duration = 0
                    else:
                        duration = frames / fps
                    duration-=0.040000
                    time = str(datetime.timedelta(seconds=duration))
                    if firstFrame is None:
                        firstFrame = gray
                        owlWas = False
                        f.write(f"No hay actividad: {time}\n")
                    frameDelta = cv2.absdiff(firstFrame, gray)
                    thresh1 = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh1, None, iterations=2)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)
                    for c in cnts:
                        if cv2.contourArea(c) < min_area:
                            continue
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        owlIs = True
                    if owlIs != owlWas:
                        time_without_change = 0
                        if (owlIs == True) and (last_message == False):
                            f.write(f"Empieza a haber actividad: {time}\n")
                            last_message = True
                    if (owlIs == False) and (time_without_change > fps * time_that_has_to_pass) and (last_message == True):
                        f.write(f"Deja de haber actividad: {time}\n")
                        last_message = False
                    owlWas = owlIs
            vs.release()
            f.write(f"Acaba el vídeo: {time}\n\n")
    messagebox.showinfo(message="El proceso ha finalizado con éxito.")


def browse_button():
    global old_folder_path
    filename = filedialog.askdirectory()
    old_folder_path = filename
    button_videos_folder_label.config(text=filename)
    print(filename)

def browse_button2():
    global new_folder_path
    filename = filedialog.askdirectory()
    new_folder_path = filename
    button_txt_folder_label.config(text=filename)
    print(filename)



file_title_grid_position = (1,0)
file_title_grid_label_position = (0,0)
brightness_grid_position = (3,0)
brightness_grid_label_position = (2,0)
contrast_grid_position = (5,0)
contrast_grid_label_position = (4,0)
speed_grid_position = (5,1)
speed_grid_label_position = (4,1)
button_videos_folder_position = (0,1)
button_videos_folder_label_position = (1,1)
button_txt_folder_position = (2,1)
button_txt_folder_label_position = (3,1)
min_area_grid_position = (7,0)
min_area_grid_label_position = (6,0)
time_that_has_to_pass_grid_position = (7,1)
time_that_has_to_pass_grid_label_position = (6,1)
main_button_position = (8,0)
label_position = (8,1)
padx=5
pady=5
window = Tk()
window.title("Detector de movimiento")
file_title_grid = ttk.Entry()
file_title_grid_label = ttk.Label(text="Nombre del archivo")
file_title_grid_label.grid(row=file_title_grid_label_position[0],column=file_title_grid_label_position[1],padx=padx,pady=pady)
file_title_grid.grid(row=file_title_grid_position[0],column=file_title_grid_position[1],padx=padx,pady=pady)
file_title_grid.insert(END,"buhos_log")
brightness_grid = ttk.Entry()
brightness_label = ttk.Label(text="Brillo")
brightness_label.grid(row=brightness_grid_label_position[0],column=brightness_grid_label_position[1],padx=padx,pady=pady)
brightness_grid.grid(row=brightness_grid_position[0],column=brightness_grid_position[1],padx=padx,pady=pady)
brightness_grid.insert(END,50)
old_folder_path = os.getcwd()
button_videos_folder = ttk.Button(text="Seleccionar carpeta de los vídeos",command=browse_button)
button_videos_folder_label = ttk.Label(text=old_folder_path)
button_videos_folder_label.grid(row=button_videos_folder_label_position[0],column=button_videos_folder_label_position[1],padx=padx,pady=pady)
button_videos_folder.grid(row=button_videos_folder_position[0],column=button_videos_folder_position[1],padx=padx,pady=pady)
new_folder_path = os.getcwd()
button_txt_folder = ttk.Button(text="Seleccionar carpeta donde guardar el txt",command=browse_button2)
button_txt_folder_label = ttk.Label(text=new_folder_path)
button_txt_folder_label.grid(row=button_txt_folder_label_position[0],column=button_txt_folder_label_position[1],padx=padx,pady=pady)
button_txt_folder.grid(row=button_txt_folder_position[0], column=button_txt_folder_position[1],padx=padx,pady=pady)
contrast_grid = ttk.Entry()
contrast_label = ttk.Label(text="Contraste")
contrast_label.grid(row=contrast_grid_label_position[0],column=contrast_grid_label_position[1],padx=padx,pady=pady)
contrast_grid.grid(row=contrast_grid_position[0],column=contrast_grid_position[1],padx=padx,pady=pady)
contrast_grid.insert(END,1.25)
speed_grid = ttk.Entry()
speed_label = ttk.Label(text="Velocidad")
speed_label.grid(row=speed_grid_label_position[0],column=speed_grid_label_position[1],padx=padx,pady=pady)
speed_grid.grid(row=speed_grid_position[0],column=speed_grid_position[1],padx=padx,pady=pady)
speed_grid.insert(END,1)
min_area_grid = ttk.Entry()
min_area_label = ttk.Label(text="Área mínima")
min_area_label.grid(row=min_area_grid_label_position[0],column=min_area_grid_label_position[1],padx=padx,pady=pady)
min_area_grid.grid(row=min_area_grid_position[0],column=min_area_grid_position[1],padx=padx,pady=pady)
time_that_has_to_pass_grid = ttk.Entry()
time_that_has_to_pass_label = ttk.Label(text="Tiempo que debe pasar sin actividad para que cuente que el búho se ha ido")
time_that_has_to_pass_label.grid(row=time_that_has_to_pass_grid_label_position[0],column=time_that_has_to_pass_grid_label_position[1],padx=padx,pady=pady)
time_that_has_to_pass_grid.grid(row=time_that_has_to_pass_grid_position[0],column=time_that_has_to_pass_grid_position[1],padx=padx,pady=pady)
time_that_has_to_pass_grid.insert(END,0)
min_area_grid.insert(END,500)
main_button = ttk.Button(text="Ejecutar",command=lambda: movement_detector(old_folder_path,new_folder_path))#centro
main_button.grid(row=main_button_position[0],column=main_button_position[1],padx=padx,pady=pady)
displayedText = StringVar()
label = ttk.Label(textvariable=displayedText)
label.grid(row=label_position[0],column=label_position[1],padx=padx,pady=pady)

window.mainloop()