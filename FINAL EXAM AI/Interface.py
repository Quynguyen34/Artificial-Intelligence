import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
from tensorflow import expand_dims
import numpy as np
from keras.models import load_model

# Connect with camera
cap = cv2.VideoCapture(0)

# Load pre-trained model
model = load_model('Language.h5')

# Create array to save label
label = np.array(['ARABIC', 'BENGALI', 'CHINESE', 'ENGLISH', 'FRENCH', 'HINDI',
                  'INDONESIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'PORTUGUESE',
                  'RUSSIAN', 'SPANISH', 'THAI', 'TURKISH', 'VIETNAMESE'])

# Create an array to store component information
detail = np.array([
    'ARABIC is the language used by Arabic-speaking countries, ranked 5th in language popularity, with approximately 300 million speakers.',
    'BENGALI is the primary language of Bangladesh and certain regions in India, with around 230 million speakers.',
    'CHINESE is the most widely spoken language in the world, with approximately 1.3 billion speakers.',
    'ENGLISH is a global language and widely used in business, education, and international communication.',
    'FRENCH is the official language of many countries and widely used in culture, arts, and legal documents.',
    'HINDI is the official language of India and one of the most widely spoken languages in the world, with around 600 million speakers.',
    'INDONESIAN is the official language of Indonesia and widely used in communication, education, and media.',
    'ITALIAN is the official language of Italy and considered one of the most popular Romance languages.',
    'JAPANESE is the official language of Japan and one of the languages with the most complex writing systems in the world.',
    'KOREAN is the official language of South Korea and North Korea, with approximately 77 million speakers.',
    'PORTUGUESE is the official language of Portugal, Brazil, and several other countries worldwide.',
    'RUSSIAN is the official language of Russia and the 8th most widely spoken language in the world.',
    'SPANISH is the official language of Spain and many countries in Latin America.',
    'THAI is the official language of Thailand and the most widely spoken language in the Southeast Asia region.',
    'TURKISH is the official language of Turkey and the official language of the Turkish Republic of Northern Cyprus.',
    'VIETNAMESE is the official language of Vietnam and widely spoken within the Vietnamese community worldwide.'
])


class MyWindow:
    def __init__(self, master):
        self.master = master
        master.title("LANGUAGE DETECTION")

        # GUI components
        self.label = tk.Label(master)
        self.text_detail = tk.Text(master, height=5, width=69)
        self.text_detail.insert(tk.END, "LANGUAGE INFORMATION HERE:")
        self.text_detail.config(state="disabled")
        self.text_detail.config(bd=0, highlightbackground="white", bg="white")
        self.button_load = tk.Button(master, text="Load Image", bg="red", fg="white", command=self.load_image)
        self.button_start = tk.Button(master, text="Start Camera", bg="blue", fg="white", command=self.start_camera)
        self.button_stop = tk.Button(master, text="Stop Camera", command=self.stop_camera)
        self.camera_running = False

        # Application info
        self.text_info = tk.Text(master, height=1, width=39)
        self.text_info.insert(tk.END, "LANGUAGE DETECTION USING CNN NETWORK")
        self.text_info.config(state="disabled", font=("Arial", 16), fg="red")
        self.text_info0 = tk.Text(master, height=1, width=33)
        self.text_info0.insert(tk.END, "LECTURER: NGUYEN TRUONG THINH")
        self.text_info0.config(state="disabled", font=("Arial", 10), fg="black")
        self.text_info1 = tk.Text(master, height=1, width=40)
        self.text_info1.insert(tk.END, "STUDENT: NGUYEN NGOC QUY - ID: 20146056")
        self.text_info1.config(state="disabled", font=("Arial", 10), fg="black")

        # Layout
        self.label.place(x=100, y=100)
        self.text_detail.place(x=100, y=510)
        self.text_info.place(x=200, y=10)
        self.text_info0.place(x=315, y=42)
        self.text_info1.place(x=290, y=65)
        self.button_load.place(x=670, y=100, width=100, height=50)
        self.button_start.place(x=670, y=160, width=100, height=50)
        self.button_stop.place(x=670, y=220, width=100, height=50)

        # Display initial image
        image_init = Image.open("Info.jpg").resize((550, 400))
        photo = ImageTk.PhotoImage(image_init)
        self.label.config(image=photo)
        self.label.image = photo

        # Exit button and event handling
        root.protocol("WM_DELETE_WINDOW", root.quit)
        self.button_exit = tk.Button(root, bg="cyan", text="EXIT", command=root.destroy)
        self.button_exit.place(x=670, y=280, width=100, height=50)

    def load_image(self):
        # Open a file dialog to choose an image
        file_name = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', ('*.jpg', '*.jpeg', '*.png', '*.bmp'))])

        if file_name:
            # Open the image
            image_original = Image.open(file_name)

            # Convert the image to numpy array
            image = np.array(image_original)
            image = cv2.resize(image, (40, 40))
            image = image / 255.0
            image = expand_dims(image, axis=0)

            # Perform prediction
            prediction = model.predict(image)
            max_index = np.argmax(prediction, axis=1)
            max_label = label[max_index]
            max_detail = detail[max_index]

            # Display component details
            self.text_detail.config(state="normal")
            self.text_detail.delete("1.0", tk.END)
            self.text_detail.insert(tk.END, str(max_detail))
            self.text_detail.config(state="disabled")

            # Resize the image for display
            image_resized = image_original.resize((550, 400))

            # Use PIL to draw on the image
            draw = ImageDraw.Draw(image_resized)

            # Set font and size
            font = ImageFont.truetype("arial.ttf", 20)

            # Write text with the set font and size
            draw.text((0, 0), str(max_label), fill=(255, 0, 0), font=font)

            # Display the image on the label
            photo = ImageTk.PhotoImage(image_resized)
            self.label.config(image=photo)
            self.label.image = photo

    def start_camera(self):
        if not self.camera_running:
            # Open the camera
            self.cap = cv2.VideoCapture(0)
            self.camera_running = True
            self.update_frame()

    def stop_camera(self):
        if self.camera_running:
            # Stop the camera
            self.cap.release()
            self.camera_running = False

    def update_frame(self):
        if self.camera_running:
            ret, frame = self.cap.read()
            # Process the image to numpy array
            image = cv2.resize(frame, (40, 40))
            image = image / 255.0
            image = expand_dims(image, axis=0)

            # Perform prediction
            prediction = model.predict(image)
            max_index = np.argmax(prediction, axis=1)
            max_label = label[max_index]
            max_detail = detail[max_index]

            # Display the prediction directly on the Camera frame
            cv2.putText(frame, str(max_label), (50, 50 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Display component details
            self.text_detail.config(state="normal")
            self.text_detail.delete("1.0", tk.END)
            self.text_detail.insert(tk.END, str(max_detail))
            self.text_detail.config(state="disabled")

            if ret:
                # Display the image on the label
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = image.resize((550, 400), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo
                self.master.after(5, self.update_frame)

if __name__ == '__main__':
    root = tk.Tk()

    # Set window size
    root.geometry("800x600")

    # Open and convert the image to Tkinter format
    image = Image.open("bg.png")
    # Resize the image to match the window size
    image = image.resize((800, 600))

    photo = ImageTk.PhotoImage(image)

    # Create a Canvas widget and draw the image as the background of the canvas
    canvas = tk.Canvas(root, width=800, height=500)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    window = MyWindow(root)
    root.mainloop()
