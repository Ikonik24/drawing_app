import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Drawing App')
        self.root.configure(bg='#f4f4f4')

        # Fullscreen Toggle
        self.fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

        # Create Canvas
        self.canvas = tk.Canvas(self.root, bg='white', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Brush Settings
        self.brush_color = "black"
        self.brush_size = tk.IntVar(value=5)

        # Pillow Image to draw on
        self.image = Image.new("RGB", (self.root.winfo_width(), self.root.winfo_height()), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Tools Frame
        self.controls_frame = tk.Frame(self.root, bg='#f4f4f4', padx=10, pady=10)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Color Picker Button
        self.color_button = tk.Button(self.controls_frame, text="Pick Color", command=self.choose_color, bg='#444', fg='white', relief='flat')
        self.color_button.pack(side=tk.LEFT, padx=5)

        # Eraser Button
        self.eraser_button = tk.Button(self.controls_frame, text="Eraser", command=self.use_eraser, bg='#444', fg='white', relief='flat')
        self.eraser_button.pack(side=tk.LEFT, padx=5)

        # Clear All Button
        self.clear_button = tk.Button(self.controls_frame, text="Clear All", command=self.clear_canvas, bg='#444', fg='white', relief='flat')
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Save Button
        self.save_button = tk.Button(self.controls_frame, text="Save", command=self.save_image, bg='#444', fg='white', relief='flat')
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Open Button
        self.open_button = tk.Button(self.controls_frame, text="Open", command=self.open_image, bg='#444', fg='white', relief='flat')
        self.open_button.pack(side=tk.LEFT, padx=5)

        # Brush Size Slider
        self.slider = tk.Scale(self.controls_frame, from_=1, to=10, orient='horizontal', variable=self.brush_size, bg='#f4f4f4', highlightthickness=0)
        self.slider.pack(side=tk.LEFT, padx=10)

        # Footer
        self.footer = tk.Label(self.root, text="Open-Source Drawing App", bg='#f4f4f4', fg='black', font=('Arial', 12))
        self.footer.pack(side=tk.BOTTOM, pady=5)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)

        # Resize handling for canvas and image
        self.root.bind("<Configure>", self.resize_canvas)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen:
            self.resize_image_canvas()

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.resize_image_canvas()

    def resize_canvas(self, event):
        self.resize_image_canvas()

    def resize_image_canvas(self):
        self.canvas.config(width=self.root.winfo_width(), height=self.root.winfo_height() - 100)
        self.image = self.image.resize((self.root.winfo_width(), self.root.winfo_height() - 100))
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.brush_color = colorchooser.askcolor()[1]

    def use_eraser(self):
        self.brush_color = "white"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.root.winfo_width(), self.root.winfo_height() - 100), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((self.root.winfo_width(), self.root.winfo_height() - 100))
            self.draw = ImageDraw.Draw(self.image)
            self.canvas_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas_image, anchor="nw")

    def paint(self, event):
        x, y = event.x, event.y
        brush_size = self.brush_size.get()
        self.canvas.create_oval(x - brush_size, y - brush_size, x + brush_size, y + brush_size, fill=self.brush_color, outline=self.brush_color)
        self.draw.ellipse([x - brush_size, y - brush_size, x + brush_size, y + brush_size], fill=self.brush_color, outline=self.brush_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
