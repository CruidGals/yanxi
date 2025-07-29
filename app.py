import tkinter as tk
from tkinter import ttk

from scripts.generate_whats_new import generate_whats_new_html
from scripts.generate_research import generate_research_html
from scripts.generate_teaching import generate_teaching_html
from scripts.generate_service import generate_service_html
from scripts.generate_personal import generate_personal_html

def gen_personal_command():
    generate_personal_html(selected_option.get())

# Create main window
root = tk.Tk()
root.title("WordPress Creator")
root.geometry("300x270")

# Buttons
button1 = tk.Button(root, text="Generate What's New HTML", command=generate_whats_new_html)
button1.pack(pady=5)

button2 = tk.Button(root, text="Generate Research HTML", command=generate_research_html)
button2.pack(pady=5)

button3 = tk.Button(root, text="Generate Teaching HTML", command=generate_teaching_html)
button3.pack(pady=5)

button4 = tk.Button(root, text="Generate Service HTML", command=generate_service_html)
button4.pack(pady=5)

button4 = tk.Button(root, text="Generate Personal Page HTML", command=gen_personal_command)
button4.pack(pady=5)

# Label to show output
label = tk.Label(root, text="Choose option for personal page:")
label.pack(pady=5)

# Dropdown menu
options = ["Tea", "Taiji", "Quote"]
selected_option = tk.StringVar()
selected_option.set(options[0])  # default value
dropdown = ttk.OptionMenu(root, selected_option, options[0], *options)
dropdown.pack(pady=5)

# Run the application
root.mainloop()
