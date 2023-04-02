import subprocess

import customtkinter
import tkinter as tk
import os

output_dir = "output/"


def create_slider_and_label(master, text, variable, command, from_, to):
    label = customtkinter.CTkLabel(master=master, text=text, justify=customtkinter.LEFT)
    label.pack(pady=10, padx=10)
    slider = customtkinter.CTkSlider(master=master, variable=variable, command=command, from_=from_, to=to)
    slider.pack(pady=10, padx=10)
    slider.set(0.5)
    return label, slider


def slider1_callback(value):
    print(value)
    label_1.configure(text=f"J: {value:.2f}")


def slider2_callback(value):
    print(value)
    label_2.configure(text=f"b: {value:.2f}")


def slider3_callback(value):
    print(value)
    label_3.configure(text=f"k_e: {value:.2f}")


def slider4_callback(value):
    print(value)
    label_4.configure(text=f"k_t: {value:.2f}")


def slider_z_callback(value):
    print(value)
    label_z.configure(text=f"z: {value:.2f}")


def slider_p_callback(value):
    print(value)
    label_p.configure(text=f"p: {value:.2f}")


def slider_k_callback(value):
    print(value)
    label_k.configure(text=f"k: {value:.2f}")


def segment_callback(value):
    print(value)
    renderType.set(value)


def render_step():
    # k_t
    # ---------------------------
    # jLs^3+(jR+bL)s^2+(bR + k_ek_t)s

    denominator, numerator = calculating_g()
    z = var_z.get()
    p = var_p.get()
    k = var_k.get()

    octave_code = "pkg load control\n" \
                    "clf;\n" \
                    "s = tf('s');\n" \
                    "g = " + numerator + "/(" + denominator + ");\n" \
                    "g_ctrl = zpk(" + str(z) + ", " + str(p) + ", " + str(k) + ");\n" \
                    "controller = g * g_ctrl / (1 + g * g_ctrl);\n" \
                    "step(controller);\n" \
                    "xlabel('Time (s)');\n" \
                    "ylabel('Amplitude');\n" \
                    "print -dsvg step.svg\n" \

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.chdir(output_dir)
    output = subprocess.check_output(['octave', '-q', '--eval', octave_code])
    os.chdir("..")

    # check if output finished successfully
    if output.decode("utf-8").find("error") != -1:
        print("Error while running octave, please make sure octave is installed and in your PATH variable.")
        return

    print("File saved to:", os.path.join(output_dir, "step.svg"))
    subprocess.Popen(['open', os.path.join(output_dir, "step.svg")])


def calculating_g():
    r = 0.06727
    l = 0.001882
    j = var_1.get()
    b = var_2.get()
    k_e = var_3.get()
    k_t = var_4.get()
    coefficient_1 = str(j * l)
    coefficient_2 = str(j * r + b * l)
    coefficient_3 = str(b * r + k_e * k_t)
    numerator = str(k_t)
    denominator = coefficient_1 + "*s^3 + " + coefficient_2 + "*s^2 + " + coefficient_3 + "*s"
    return denominator, numerator


def render_impulse():
    pass


def render_root_locus():
    pass


def render_poles():
    pass


def render():
    if renderType.get() == "Step":
        render_step()
    elif renderType.get() == "Impulse":
        render_impulse()
    elif renderType.get() == "Root Locus":
        render_root_locus()
    elif renderType.get() == "Poles":
        render_poles()
    else:
        print("Unknown render type")


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x900")
app.title("Control Systems: Electric Motor")

# make minimal window size
app.minsize(400, 900)

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=10, fill="both", expand=True)

# create a label for the frame
label = customtkinter.CTkLabel(master=frame_1, text="Motor Parameters", justify=customtkinter.LEFT)
label.pack(pady=10, padx=10)

from_1: float = 1
to_1: float = 1.5
var_1 = tk.DoubleVar()
var_1.set(from_1)
label_1, slider_1 = create_slider_and_label(frame_1, "J: " + str(var_1.get()), var_1, slider1_callback, from_1,
                                            to_1)

from_2: float = 1.5
to_2: float = 2
var_2 = tk.DoubleVar()
var_2.set(from_2)
label_2, slider_2 = create_slider_and_label(frame_1, "b: " + str(var_2.get()), var_2, slider2_callback, from_2,
                                            to_2)

from_3: float = 1.5
to_3: float = 2
var_3 = tk.DoubleVar()
var_3.set(from_3)
label_3, slider_3 = create_slider_and_label(frame_1, "k_e: " + str(var_3.get()), var_3, slider3_callback, from_3,
                                            to_3)

from_4: float = 1.5
to_4: float = 2
var_4 = tk.DoubleVar()
var_4.set(from_4)
label_4, slider_4 = create_slider_and_label(frame_1, "k_t: " + str(var_4.get()), var_4, slider4_callback, from_4,
                                            to_4)

# extra sliders for the controller

# label for the controller parameters
label = customtkinter.CTkLabel(master=frame_1, text="Controller Parameters", justify=customtkinter.LEFT)
label.pack(pady=10, padx=10)

# z parameter
from_z: float = -10
to_z: float = 10
var_z = tk.DoubleVar()
var_z.set(from_z + to_z)
label_z, slider_z = create_slider_and_label(frame_1, "z: " + str(var_z.get()), var_z, slider_z_callback, from_z,
                                            to_z)

# p parameter
from_p: float = -10
to_p: float = 10
var_p = tk.DoubleVar()
var_p.set(from_p + to_p)
label_p, slider_p = create_slider_and_label(frame_1, "p: " + str(var_p.get()), var_p, slider_p_callback, from_p,
                                            to_p)

# k parameter
from_k: float = 0
to_k: float = 100
var_k = tk.DoubleVar()
var_k.set(from_k)
label_k, slider_k = create_slider_and_label(frame_1, "k: " + str(var_k.get()), var_k, slider_k_callback, from_k,
                                            to_k)

# create a segmented button
renderType = customtkinter.StringVar()
renderType.set("Step")
segmented_button = customtkinter.CTkSegmentedButton(master=app, values=["Step", "Impulse", "Root Locus", "Poles"],
                                                    command=segment_callback)
segmented_button.set(renderType.get())
segmented_button.pack(pady=20, padx=10)

# impulse, step, root locus to render
# show poles for controller tf = G * G_ctrl / (1 + G * G_ctrl) by applying poles command -> closed loop system


# create a button
button = customtkinter.CTkButton(master=app, text="Render", command=render)
button.pack(pady=20, padx=10)

app.mainloop()
