import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import ImageTk, Image

# membaca data dari file
def selectPic():
    global img
    try:
        filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                                              filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
        if filename:
            img = Image.open(filename)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            lbl_show_pic['image'] = img
            entry_pic_path.delete(0, END)
            entry_pic_path.insert(0, filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def process_image():
    try:
        img_path = entry_pic_path.get()
        if img_path:
            open = np.ones((5, 5))
            close = np.ones((20, 20))
            
            citra = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
           
            if citra is None:
                raise ValueError("Failed to read the image.")

            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Failed to read the image.")
            
            # mengkonversi bentuk BGR ke HSV
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # menentukan rentang warna orange
            lower_orange1 = np.array([0, 50, 50])
            upper_orange1 = np.array([17, 255, 255])

            # menentukan batas warna hsv orange dan ambang batas gambar hsv
            orangemask1 = cv2.inRange(hsv_img, lower_orange1, upper_orange1)

            # menentukan rentang warna orange kedua di hsv
            lower_orange2 = np.array([200, 50, 50])
            upper_orange2 = np.array([210, 255, 255])

            # menentukan batas warna hsv orange dan ambang batas gambar hsv kedua
            orangemask2 = cv2.inRange(hsv_img, lower_orange2, upper_orange2)

            # pembacaan final untuk warna orange
            orangemask = orangemask1 + orangemask2
            maskOpen = cv2.morphologyEx(orangemask, cv2.MORPH_OPEN, open)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, close)

            maskFinal = maskClose
            cnt_o = 0
            for o in orangemask:
                cnt_o += list(o).count(255)
            print("Orange ", cnt_o)
            #cv2.imshow('BGR Orange', orangemask)
            cv2.imshow('Orange', cnt_o)

            # menentukan rentang warna hijau
            lower_green = np.array([50, 50, 50])
            upper_green = np.array([70, 255, 255])

            # menentukan rentang warna hijau kedua di hsv
            greenmask = cv2.inRange(hsv_img, lower_green, upper_green)

            # pembacaan final untuk warna hijau
            #cv2.imshow('BGR Hijau', greenmask)
            cnt_g = 0
            for g in greenmask:
                cnt_g += list(g).count(255)
            print("Hijau ", cnt_g)

            # menentukan rentang warna setengah matang
            lower_yellow = np.array([25, 50, 50])
            upper_yellow = np.array([35, 255, 255])
            yellowmask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

            # pembacaan final untuk warna setengah matang
            #cv2.imshow('BGR Kuning', yellowmask)
            cnt_y = 0
            for y in yellowmask:
                cnt_y += list(y).count(255)
            print("Kuning", cnt_y)

            # perhitungan kematangan
            tot_area = cnt_o + cnt_y + cnt_g
            rperc = cnt_o / tot_area
            yperc = cnt_y / tot_area
            gperc = cnt_g / tot_area

            # penyesuaian batas buah
            glimit = 0.5
            ylimit = 0.6

            if gperc > glimit:
                print("Buah Mentah")
                cv2.imshow("Buah Mentah", img)
            elif yperc > ylimit:
                print("Buah Setengah Matang")
                cv2.imshow("Buah Setengah Matang", img)
            else:
                print("Buah Matang")
                cv2.imshow("Buah Matang", img)

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
frame = tk.Frame(root, bg='red')

lbl_pic_path = tk.Label(frame, text='Image Path:', padx=25, pady=25, font=('verdana', 16,),bg='red')
lbl_show_pic = tk.Label(frame, bg='red')
entry_pic_path = tk.Entry(frame, font=('verdana', 16))
btn_browse = tk.Button(frame, text='Select Image', bg='orange', fg='#ffffff', font=('courier', 16))
btn_process = tk.Button(frame, text='Process', bg='orange', fg='#ffffff', font=('courier', 16))

root.title("Deteksi Kematangan Buah Pepaya")

btn_browse['command'] = selectPic
btn_process['command'] = process_image

frame.pack()

lbl_pic_path.grid(row=0, column=0)
entry_pic_path.grid(row=0, column=1, padx=(0, 20))
lbl_show_pic.grid(row=1, column=0, columnspan=2)
btn_browse.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
btn_process.grid(row=3, column=0, columnspan=2, padx=10, pady=10)



root.mainloop()