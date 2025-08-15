import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb


# ---------- Instruction Screen ----------
def show_instructions():
    instruction_win = tk.Toplevel()
    instruction_win.geometry("600x450")
    instruction_win.title("Instructions - StegaSeal")
    instruction_win.config(bg="#1E1E1E")

    heading = Label(instruction_win, text="How to Use StegaSeal", font=("Arial", 18, "bold"), fg="yellow", bg="#1E1E1E")
    heading.pack(pady=(10, 5))  # Small space below heading

    instructions_text = """
      1️. Click 'Open Image' to select a PNG or JPG image.

      2️. Type your secret message in the white text box.

      3️. Enter the secret key (Default: 1234) in the password field.

      4️. Click 'Hide Data' to embed your message into the image.

      5️. Click 'Save Image' or 'Download Image' to save it.

      6️. To reveal a message, open the image and click 'Show Data' (with the same secret key).


         ⚠ Keep your key secret !!
"""
    Label(
        instruction_win,
        text=instructions_text,
        font=("Arial", 12),
        fg="white",
        bg="#1E1E1E",
        justify=LEFT
    ).pack(padx=20, pady=10)

    Button(instruction_win, text="Continue", font=("Arial", 12, "bold"), bg="green", fg="white",
           command=instruction_win.destroy).pack(pady=10)

    instruction_win.transient(win)
    instruction_win.grab_set()
    win.wait_window(instruction_win)


# ---------- Main App ----------
win = tk.Tk()
win.geometry('800x500')
win.title('StegaSeal: Image Stego Tool')
win.config(bg='#1E1E1E')

open_file = None


def enable_buttons():
    for btn in [btn_save, btn_hide, btn_show, btn_download]:
        btn.config(state="normal")


def open_img():
    global open_file
    open_file = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select Image',
        filetypes=(('PNG file', '*.png'), ('JPEG file', '*.jpg'), ('All files', '*.*'))
    )
    if open_file:
        img = Image.open(open_file)
        img = img.resize((240, 200))
        img = ImageTk.PhotoImage(img)
        lf1.configure(image=img)
        lf1.image = img
        text1.delete(1.0, tk.END)
        enable_buttons()


def hide():
    if not open_file:
        messagebox.showwarning("Warning", "Select an image first!")
        return

    msg = text1.get(1.0, tk.END).strip()
    if not msg:
        messagebox.showwarning("Warning", "Write a secret message to hide!")
        return

    password = code.get()
    if password == '1234':
        global hide_msg
        hide_msg = lsb.hide(str(open_file), msg)
        messagebox.showinfo('Success', 'Message hidden successfully! Please save or download the image')
    elif password == '':
        messagebox.showerror('Error', 'Please enter the secret key')
    else:
        messagebox.showerror('Error', 'Incorrect secret key! Please try again.')
        code.set('')


def save_img():
    if 'hide_msg' in globals():
        hide_msg.save('Secret_file.png')
        messagebox.showinfo('Success', 'Image saved successfully as Secret_file.png')
    else:
        messagebox.showerror('Error', 'No hidden message to save! Please hide a message first.')


def show():
    if not open_file:
        messagebox.showwarning("Warning", "Select an image first!")
        return

    password = code.get()
    if password == '1234':
        show_msg = lsb.reveal(open_file)
        if show_msg:
            text1.delete(1.0, tk.END)
            text1.insert(tk.END, show_msg)
        else:
            messagebox.showwarning("Warning", "No hidden message found in this image!")
    elif password == '':
        messagebox.showerror('Error', 'Please enter the secret key')
    else:
        messagebox.showerror('Error', 'Incorrect secret key! Please try again.')
        code.set('')


def download_img():
    if 'hide_msg' in globals():
        folder = filedialog.askdirectory(title='Select Folder to Save Image')
        if folder:
            save_path = os.path.join(folder, 'Download_Secret_Image.png')
            hide_msg.save(save_path)
            messagebox.showinfo('Downloaded', f'Image downloaded successfully at \n{save_path}')
    else:
        messagebox.showerror('Error', 'No hidden message to download! Please hide a message first.')


# ---------- UI ----------
logo_image = Image.open("lgo.png")
logo_image = logo_image.resize((60, 60))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = Label(win, image=logo_photo, bg="#1E1E1E")
logo_label.pack(pady=(10, 0))

heading = tk.Label(win, text='StegaSeal: Image Stego Tool', font=('Arial', 20, 'bold'),
                   bg='#1E1E1E', fg='white')
heading.pack(pady=(5, 10))

frame_main = tk.Frame(win, bg="#1E1E1E")
frame_main.pack(pady=5)

f1 = tk.Frame(frame_main, width=250, height=220, bd=5, bg='#2D2D2D')
f1.grid(row=0, column=0, padx=20)
lf1 = tk.Label(f1, bg='#2D2D2D')
lf1.place(x=0, y=0)

f2 = tk.Frame(frame_main, width=320, height=220, bd=5, bg='white')
f2.grid(row=0, column=1)
text1 = tk.Text(f2, font='arial 13 bold', wrap=tk.WORD)
text1.place(x=0, y=0, width=310, height=210)

tk.Label(win, text='SECRET KEY', font=('Arial', 12, 'bold'),
         bg='#1E1E1E', fg='yellow').pack(pady=5)
code = tk.StringVar()
e = tk.Entry(win, textvariable=code, bd=2, font=('Arial', 12), show='*')
e.pack(pady=5)

button_frame = tk.Frame(win, bg='#1E1E1E')
button_frame.pack(pady=10)

style = {"font": ('Arial', 12, 'bold'), "width": 13,
         "cursor": "hand2", "bd": 0, "relief": "flat", "fg": "white"}

btn_open = tk.Button(button_frame, text='Open Image', bg='#007BFF', command=open_img, **style)
btn_open.grid(row=0, column=0, padx=5)

btn_save = tk.Button(button_frame, text='Save Image', bg='#28A745', command=save_img, state="disabled", **style)
btn_save.grid(row=0, column=1, padx=5)

btn_hide = tk.Button(button_frame, text='Hide Data', bg='#DC3545', command=hide, state="disabled", **style)
btn_hide.grid(row=0, column=2, padx=5)

btn_show = tk.Button(button_frame, text='Show Data', bg='#FD7E14', command=show, state="disabled", **style)
btn_show.grid(row=0, column=3, padx=5)

btn_download = tk.Button(button_frame, text='Download Image', bg='#6F42C1', command=download_img, state="disabled", **style)
btn_download.grid(row=0, column=4, padx=5)

# Show instructions first
win.after(100, show_instructions)

win.mainloop()