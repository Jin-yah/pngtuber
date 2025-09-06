from PIL import ImageTk, Image
import tkinter as tk
import keyboard
import sounddevice as sd
import time as tm
import numpy as np
import os
import sys
import traceback

# ---------------------------
# Create Root Window
# ---------------------------
control_window = tk.Tk()
control_window.withdraw()

# ---------------------------
# Global Settings and Preloading
# ---------------------------
accessories = './model/accessories'
accessory_list = os.listdir(accessories)
accessory_index = 0
arm_wait_time = 0
mouth_wait_time = tm.time()
key_pressed = False

background_path = './model/base.png'
mouth_path = './model/mouth_open.png'
eye_path = './model/eyes_closed.png'
arm_path = './model/arm_up.png'
arm_down_path = './model/!nothing.png'

faces = './model/face_states'
face_list = os.listdir(faces)
face_index = 0

try:
    for path in [os.path.join(accessories, "!nothing.png"), os.path.join(faces, "!nothing.png")]:
        if not os.path.exists(path):
            Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(os.path.join(path))

    accessory_images = {
        file: ImageTk.PhotoImage(Image.open(os.path.join(accessories, file)), master=control_window)
        for file in accessory_list
    }
    if "!nothing.png" not in accessory_images:
        accessory_images["!nothing.png"] = ImageTk.PhotoImage(
            Image.open(os.path.join(accessories, "!nothing.png")), master=control_window
        )

    face_images = {
        file: ImageTk.PhotoImage(Image.open(os.path.join(faces, file)), master=control_window)
        for file in face_list
    }
    if "!nothing.png" not in face_images:
        face_images["!nothing.png"] = ImageTk.PhotoImage(
            Image.open(os.path.join(faces, "!nothing.png")), master=control_window
        )

    background_image = ImageTk.PhotoImage(Image.open(background_path), master=control_window)
    mouth_image = ImageTk.PhotoImage(Image.open(mouth_path), master=control_window)
    eye_image = ImageTk.PhotoImage(Image.open(eye_path), master=control_window)
    arm_image = ImageTk.PhotoImage(Image.open(arm_path), master=control_window)
    arm_down_image = ImageTk.PhotoImage(Image.open(arm_down_path), master=control_window)
    accessory_image = accessory_images["!nothing.png"]
    face_image = face_images["!nothing.png"]

except Exception as e:
    print(e)

# ---------------------------
# Create the Model Window
# ---------------------------
model_window = tk.Toplevel(control_window)
model_window.title("Model Window")

def on_close():
    global blink_task, microphone_stream

    if blink_task:
        model_window.after_cancel(blink_task)

    if microphone_stream is not None:
        microphone_stream.stop()
        microphone_stream.close()

    keyboard.unhook_all()
    control_window.quit()
    control_window.destroy()

model_window.protocol("WM_DELETE_WINDOW", on_close)

canvas = tk.Canvas(
    model_window,
    width=background_image.width(),
    height=background_image.height(),
    bg='#12ff06'
)
canvas.pack()

background_id = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
accessory_id = canvas.create_image(0, 0, anchor=tk.NW, image=accessory_image, state=tk.HIDDEN)
face_overlay_id = canvas.create_image(0, 0, anchor=tk.NW, state=tk.HIDDEN)
mouth_id = canvas.create_image(0, 0, anchor=tk.NW, image=mouth_image, state=tk.HIDDEN)
eye_id = canvas.create_image(0, 0, anchor=tk.NW, image=eye_image, state=tk.HIDDEN)
arm_id = canvas.create_image(0, 0, anchor=tk.NW, image=arm_image, state=tk.HIDDEN)
arm_down_id = canvas.create_image(0, 0, anchor=tk.NW, image=arm_down_image, state=tk.NORMAL)

# ---------------------------
# Blinking Animation
# ---------------------------
blink_task = None

def cycle_blink():
    global blink_task
    canvas.itemconfig(eye_id, state=tk.NORMAL)
    blink_task = model_window.after(250, cycle_open)

def cycle_open():
    global blink_task
    canvas.itemconfig(eye_id, state=tk.HIDDEN)
    blink_task = model_window.after(4000, cycle_blink)

# ---------------------------
# Accessory and Face Management
# ---------------------------
def update_accessory(accessory_name):
    if accessory_name == "!nothing.png":
        canvas.itemconfig(accessory_id, state=tk.HIDDEN)
    else:
        canvas.itemconfig(accessory_id, image=accessory_images[accessory_name], state=tk.NORMAL)

def update_face(face_name):
    if face_name == "!nothing.png":
        canvas.itemconfig(face_overlay_id, state=tk.HIDDEN)
    else:
        canvas.itemconfig(face_overlay_id, image=face_images[face_name], state=tk.NORMAL)

# ---------------------------
# Keyboard Handling
# ---------------------------
def on_key_press(event):
    global accessory_index, face_index, arm_wait_time, key_pressed

    if event.event_type == "down":
        key_pressed = True
        if arm_wait_time == 0:
            arm_wait_time = tm.time()
    else:
        key_pressed = False

    if event.event_type == keyboard.KEY_DOWN and event.name == 'f1':
        accessory_index = (accessory_index + 1) % len(accessory_list)
        accessory = accessory_list[accessory_index]
        update_accessory(accessory)

    elif event.event_type == keyboard.KEY_DOWN and event.name == 'f2':
        face_index = (face_index + 1) % len(face_list)
        face = face_list[face_index]
        update_face(face)
        

    if not key_pressed:
        canvas.itemconfig(arm_down_id, state=tk.NORMAL) 
        canvas.itemconfig(arm_id, state=tk.HIDDEN)
        arm_wait_time = 0

    elif key_pressed and tm.time() - arm_wait_time < 0.5:
        canvas.itemconfig(arm_down_id, state=tk.HIDDEN)
        canvas.itemconfig(arm_id, state=tk.NORMAL)
    else:
        canvas.itemconfig(arm_down_id, state=tk.NORMAL) 
        canvas.itemconfig(arm_id, state=tk.HIDDEN)

keyboard.hook(on_key_press)

# ---------------------------
# Microphone / Mouth Movement
# ---------------------------
microphone_stream = None

def on_microphone_activity(indata, frames, time_info, status):
    global mouth_wait_time
    audio_level = np.max(np.abs(indata))
    sound_threshold = 0.10
    if audio_level > sound_threshold:
        canvas.itemconfig(mouth_id, state=tk.NORMAL)
        mouth_wait_time = tm.time()
    elif audio_level < sound_threshold and tm.time() - mouth_wait_time > 0.25:
        canvas.itemconfig(mouth_id, state=tk.HIDDEN)

def init_microphone():
    global microphone_stream
    try:
        if microphone_stream is not None:
            microphone_stream.stop()
            microphone_stream.close()

        microphone_stream = sd.InputStream(callback=on_microphone_activity, channels=1)
        microphone_stream.start()
    except Exception as e:
        print("Error starting microphone stream:", e)

init_microphone()

# ---------------------------
# Start the Loop
# ---------------------------
if __name__ == "__main__":
    try:
        cycle_blink()
        control_window.mainloop()
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write("Error occurred:\n")
            f.write(traceback.format_exc())
        print("An error occurred. Check error_log.txt for details.")
