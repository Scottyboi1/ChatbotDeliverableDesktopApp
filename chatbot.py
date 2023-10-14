import os
import tkinter as tk
from vertexai.language_models import TextGenerationModel

# Set the path to your service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred.json"

# Initialize the chatbot model
model = TextGenerationModel.from_pretrained("text-bison")

# Function to get the chatbot response
def get_response(grade_level, subject):
    user_input = input_entry.get()
    
    # Define prompts for different grade levels and subjects
    prompts = {
        "elementary": "Explain how to solve this {} question on an elementary school level. ".format(subject) + user_input,
        "middle": "Explain how to solve this {} question on a middle school level. ".format(subject) + user_input,
        "high": "Explain how to solve this {} question on a high school level. ".format(subject) + user_input,
    }
    
    # Use the appropriate prompt based on the selected grade level
    prompt = prompts.get(grade_level, user_input)
    
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    response = model.predict(prompt, **parameters)
    response_text.set(response.text)
    
    # Display the response in the Text widget
    response_display.config(state="normal")
    response_display.delete(1.0, "end")
    response_display.insert("end", response.text)
    response_display.config(state="disabled")

# Create the main window
window = tk.Tk()
window.title("Chatbot Tutor")

# Set a fixed window size
window.geometry("1300x550")  # Set your desired size

# Disable resizing
window.resizable(0, 0)

# Color codes for subjects
subject_colors = {"science": "green", "math": "#728FCE", "history": "#966F33", "english": "red"}

# Create a sidebar frame for subject and grade level selection
sidebar_frame = tk.Frame(window)
sidebar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Create a subject selection frame inside the sidebar
subject_frame = tk.Frame(sidebar_frame)
subject_frame.grid(row=0, column=0)

subject_label = tk.Label(subject_frame, text="Select Subject")
subject_label.grid(row=0, column=0, sticky="w")

# Create radio buttons to select the subject
subject = tk.StringVar()
subject.set("science")  # Default to science

# Add a variable to store the selected subject color
selected_subject_color = tk.StringVar()
selected_subject_color.set("green")

# Function to set the selected subject color
def set_selected_subject_color(subject_value):
    selected_subject_color.set(subject_colors[subject_value])

# Set a common width for subject radio buttons
button_width = 15

science_button = tk.Radiobutton(subject_frame, text="Science", variable=subject, value="science", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg=subject_colors["science"], command=lambda: set_selected_subject_color(subject.get()), width=button_width)
math_button = tk.Radiobutton(subject_frame, text="Math", variable=subject, value="math", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg=subject_colors["math"], command=lambda: set_selected_subject_color(subject.get()), width=button_width)
english_button = tk.Radiobutton(subject_frame, text="English", variable=subject, value="english", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg=subject_colors["english"], command=lambda: set_selected_subject_color(subject.get()), width=button_width)
history_button = tk.Radiobutton(subject_frame, text="History", variable=subject, value="history", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg=subject_colors["history"], command=lambda: set_selected_subject_color(subject.get()), width=button_width)

science_button.grid(row=1, column=0, sticky="w")
math_button.grid(row=2, column=0, sticky="w")
english_button.grid(row=3, column=0, sticky="w")
history_button.grid(row=4, column=0, sticky="w")

# Create a grade level selection frame inside the sidebar
grade_level_frame = tk.Frame(sidebar_frame)
grade_level_frame.grid(row=1, column=0, pady=(20, 0))

grade_level_label = tk.Label(grade_level_frame, text="Select Grade Level")
grade_level_label.grid(row=0, column=0, sticky="w")

# Create radio buttons to select the grade level
grade_level = tk.StringVar()
grade_level.set("middle")  # Default to middle school

# Set a common width for grade level radio buttons
grade_button_width = 15

elementary_button = tk.Radiobutton(grade_level_frame, text="Elementary School", variable=grade_level, value="elementary", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, width=grade_button_width)
middle_button = tk.Radiobutton(grade_level_frame, text="Middle School", variable=grade_level, value="middle", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, width=grade_button_width)
high_button = tk.Radiobutton(grade_level_frame, text="High School", variable=grade_level, value="high", relief=tk.RAISED, borderwidth=2, padx=10, pady=10, width=grade_button_width)

elementary_button.grid(row=1, column=0, sticky="w")
middle_button.grid(row=2, column=0, sticky="w")
high_button.grid(row=3, column=0, sticky="w")

# Create an input entry field on the main window
input_entry = tk.Entry(window, width=40, relief=tk.RAISED, borderwidth=4, bg="white", foreground="black", font=("Helvetica", 16))
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="n")



# Create a button to get the response next to the menus
get_response_button = tk.Button(sidebar_frame, text="Get Response", command=lambda: get_response(grade_level.get(), subject.get()), relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg="white")
get_response_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Create a Text widget with Comic Sans MS font to display the response
response_text = tk.StringVar()
response_display = tk.Text(window, height=10, width=50, background="green", highlightbackground="brown", highlightcolor="brown", highlightthickness=4, foreground="white", font=("Comic Sans MS", 12))
response_display.grid(row=0, column=1, padx=10, pady=10, sticky="w")
response_display.config(state="disabled")

# Add a robot image on the right-hand side of the application
robot_image = tk.PhotoImage(file="robot.png")  # Adjust the path to your robot image
robot_label = tk.Label(window, image=robot_image)
robot_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

# Start the Tkinter main loop
window.mainloop()
