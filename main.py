import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def detect_faces():
    global filepath
    filepath = filedialog.askopenfilename()
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    start_time = cv2.getTickCount()
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    end_time = cv2.getTickCount()
    elapsed_time = (end_time - start_time) / cv2.getTickFrequency()

    for x, y, w, h in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imwrite("output_image.jpg", image)
    
    show_original_image(filepath)
    show_detected_faces(filepath)
    show_detection_info(len(faces), elapsed_time)


def save_image():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
    )
    if save_path:
        result_image = cv2.imread("output_image.jpg")
        cv2.imwrite(save_path, result_image)


def show_detection_info(num_faces, elapsed_time):
    text_variant = (
        f"{num_faces} лицо"
        if (num_faces % 10 == 1 and num_faces % 100 != 11)
        else f"{num_faces} лица"
        if (2 <= num_faces % 10 <= 4 and not (10 <= num_faces % 100 <= 14))
        else f"{num_faces} лиц"
    )

    info_text = (
        f"Обнаружено лиц: {text_variant}; Время обнаружения: {elapsed_time:.2f} секунд"
    )
    info_label.config(text=info_text)


root = tk.Tk()
root.title("Детектор лиц")

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

button_detect = tk.Button(root, text="Выбрать изображение", command=detect_faces)
button_detect.grid(row=1, column=0)

button_save = tk.Button(root, text="Сохранить", command=save_image)
button_save.grid(row=1, column=1)

info_label = tk.Label(root, text="Обнаружено лиц: 0; Время обнаружения: 0.00 секунд")
info_label.grid(row=2, column=0, columnspan=2)

filepath = None


def show_original_image(filepath):
    original = (
        Image.open(filepath)
        if filepath
        else Image.new("RGB", (500, 500), color="white")
    )
    original = original.resize((250, 250), Image.ANTIALIAS)
    original = ImageTk.PhotoImage(original)
    original_panel = tk.Label(root, image=original)
    original_panel.image = original
    original_panel.grid(row=0, column=0)


def show_detected_faces(filepath):
    result_image = (
        Image.open("output_image.jpg")
        if filepath
        else Image.new("RGB", (500, 500), color="white")
    )
    result_image = result_image.resize((250, 250), Image.ANTIALIAS)
    result_image = ImageTk.PhotoImage(result_image)
    result_panel = tk.Label(root, image=result_image)
    result_panel.image = result_image
    result_panel.grid(row=0, column=1)


root.mainloop()
