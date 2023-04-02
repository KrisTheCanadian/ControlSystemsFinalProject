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


def render():
    # k_t
    # ---------------------------
    # jLs^3+(jR+bL)s^2+(bR + k_ek_t)s

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

    octave_code = "pkg load control\n" \
                  "clf;\n" \
                  "s = tf('s');\n" \
                  "g = " + numerator + "/(" + denominator + ");\n" \
                                                            "step(g);\n" \
                                                            "print -dsvg step.svg\n"

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


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x500")
app.title("Control Systems: Electric Motor")

# make minimal window size
app.minsize(400, 500)

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=10, fill="both", expand=True)

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

# create a button
button = customtkinter.CTkButton(master=app, text="Render", command=render)
button.pack(pady=20, padx=10)

app.mainloop()
