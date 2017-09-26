import tkinter as tk
from tkinter import ttk
import random
import time
from PIL import ImageTk, Image

HUGE_FONT = ("Verdana", 25, "bold")
LARGE_FONT = ("Verdana", 12)
SMALL_ITALIC_FONT = ("times", 10, "italic")
TIMER_FONT = ("Menlo", 16)

perfect_notes = ['A','B','C','D','E','F','G']
sharp_notes = ['A#','C#','D#','F#','G#']
flat_notes = ['Ab','Bb','Db','Eb', 'Gb']

triad_groups = ['123', '234', '345', '456']

class GuitarTrainerApp (tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Guitar Trainer")

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, ChordsPage, ScalesPage):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, controller):
		frame = self.frames[controller]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		header_label = tk.Label(self, text="Welcome to the Guitar Training App!", font=HUGE_FONT)
		header_label.pack(pady=10, padx=10)

		img = ImageTk.PhotoImage(Image.open("guitar_cat.jpeg"))
		img_label = tk.Label(self, image=img)
		img_label.image = img
		img_label.pack()


		selection_label = tk.Label(self, text="Select practice mode", font=LARGE_FONT)
		selection_label.pack(pady=10, padx=10)

		chords_button = tk.Button(self, text="CHORDS", command=lambda: controller.show_frame(ChordsPage))
		chords_button.pack()

		scales_button = tk.Button(self, text="SCALES", command=lambda: controller.show_frame(ScalesPage))
		scales_button.pack()

		created_by_label = tk.Label(self, text="Created by Brent Marieb", font=SMALL_ITALIC_FONT)
		created_by_label.pack(pady=10, padx=10)

class PracticePage(tk.Frame):

	timer_max = 10
	timer_count = 10

	stop_timer = False

	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)

		header_label = self.get_header_label()
		header_label.pack(pady=10, padx=10)

		key_message = tk.Message(self,font=(HUGE_FONT), justify=tk.CENTER)
		key_message.pack(fill='x')
		self.random_key_message(key_message)

		counter_message = tk.Message(self, fg="#42c5f4", bg="black", font=TIMER_FONT)
		counter_message.pack(pady=10)
		self.decrement_counter_message(counter_message)

		stop_timer_button = tk.Button(self, highlightbackground="red", text="Stop timer", width=15)
		stop_timer_button.config(command=lambda: self.flip_stop_timer(stop_timer_button))
		stop_timer_button.pack()

		randomize_button = tk.Button(self, fg="green",text="Randomize", width=15, command=self.reset_counter)
		randomize_button.pack()

		options_button = tk.Button(self, text="Options", command=self.options_popup)
		options_button.pack()

		menu_button = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(StartPage))
		menu_button.pack()

	def get_random_note_and_key(self):
	    notes = list(perfect_notes)
	    key = "Major"
	    random_int = random.randint(0,1)
	    if random_int:
	        notes += sharp_notes
	    else:
	        notes += flat_notes
	    random_int = random.randint(0,1)
	    if random_int:
	        key = "minor"
	    random_note = random.choice(notes)
	    return random_note, key

	def get_header_label():
		pass

	def get_specific_key_type(self):
		pass

	def get_specific_key_label(self, popup):
		pass

	def pack_options_checkboxes(self, popup):
		pass

	def options_callback(self):
		pass

	def options_popup(self):
		popup = tk.Toplevel()

		popup.wm_title("Options")

		timer_label = tk.Label(popup, text="Timer value:")
		timer_label.pack(side="top", fill="x", pady=10)

		timer_entry = ttk.Entry(popup)
		timer_entry.insert(0,self.timer_max)
		timer_entry.pack()
		timer_entry.focus_set()

		specific_label = self.get_specific_key_label(popup)
		specific_label.pack(side="top", fill="x", pady=10)

		self.pack_options_checkboxes(popup)

		

		def callback():
			timer_time = timer_entry.get()
			if int(timer_time) > 0:
				PracticePage.timer_max = int(timer_time)

			self.triad_choices = []
			
			if self.first_triad_var.get():
				self.triad_choices.append("123")
			if self.second_triad_var.get():
				self.triad_choices.append("234")
			if self.third_triad_var.get():
				self.triad_choices.append("345")
			if self.fourth_triad_var.get():
				self.triad_choices.append("456")
			popup.destroy()

		exit_button = tk.Button(popup, text="Okay", command=callback)
		exit_button.pack()

	def reset_counter(self):
		PracticePage.timer_count = 0

	def flip_stop_timer(self, button):
		if PracticePage.stop_timer:
			PracticePage.stop_timer = False
			button.config(text="Stop timer", highlightbackground="red")
		else:
			PracticePage.stop_timer = True
			button.config(text="Start timer", highlightbackground="green")

	def random_key_message(self,message):
		def randomize_key():
			random_note, key = self.get_random_note_and_key()
			specific_type = self.get_specific_key_type()
			message.config(text="\n%s %s\n%s" % (random_note, key, specific_type))
			message.after(1000, check_counter)
		def check_counter():
			if PracticePage.timer_count > 1:
				message.after(1000, check_counter)
			else:
				randomize_key()
		randomize_key()

	def decrement_counter_message(self, message):
		def decrement_count():
			if not PracticePage.stop_timer:
				PracticePage.timer_count -= 1
			if PracticePage.timer_count <= 0:
				PracticePage.timer_count = int(PracticePage.timer_max)
			message.config(text=str(PracticePage.timer_count))
			message.after(1000, decrement_count)
		decrement_count()

class ChordsPage(PracticePage):

	triad_choices = []

	def __init__(self, parent, controller):
		PracticePage.__init__(self, parent, controller)

		self.first_triad_var = tk.BooleanVar()
		self.second_triad_var = tk.BooleanVar()
		self.third_triad_var = tk.BooleanVar()
		self.fourth_triad_var = tk.BooleanVar()

	def get_header_label(self):
		return tk.Label(self, text="Chord Training", font=LARGE_FONT)


	def get_specific_key_type(self):
		triad = ""
		if self.triad_choices:
			triad = random.choice(self.triad_choices)
		return triad

	def get_specific_key_label(self, popup):
		triad_label = tk.Label(popup, text="Choose the strings you'd like to play the triad:")
		return triad_label

	def pack_options_checkboxes(self, popup):
		check1 = tk.Checkbutton(popup, text='123', variable=self.first_triad_var)
		check1.pack()
		check2 = tk.Checkbutton(popup, text='234', variable=self.second_triad_var)
		check2.pack()
		check3 = tk.Checkbutton(popup, text='345', variable=self.third_triad_var)
		check3.pack()
		check4 = tk.Checkbutton(popup, text='456', variable=self.fourth_triad_var)
		check4.pack()

	def options_callback(self):
		self.triad_choices = []
			
		if self.first_triad_var.get():
			self.triad_choices.append("123")
		if self.second_triad_var.get():
			self.triad_choices.append("234")
		if self.third_triad_var.get():
			self.triad_choices.append("345")
		if self.fourth_triad_var.get():
			self.triad_choices.append("456")

	def decrement_counter_message(self, message):
		def decrement_count():
			message.config(text=str(PracticePage.timer_count))
			message.after(10, decrement_count)
		decrement_count()

class ScalesPage(PracticePage):
	

	scale_choices = []

	def __init__(self, parent, controller):
		PracticePage.__init__(self, parent, controller)

		self.pentatonic_var = tk.BooleanVar()
		self.diatonic_var = tk.BooleanVar()
		self.blues_var = tk.BooleanVar()
		

	def get_header_label(self):
		return tk.Label(self, text="Scale Training", font=LARGE_FONT)

	def get_specific_key_type(self):
		scale = ""
		if self.scale_choices:
			scale = random.choice(self.triad_choices)
		return scale

	def get_specific_key_label(self, popup):
		scale_label = tk.Label(popup, text="Scale type:")
		return scale_label

	def pack_options_checkboxes(self, popup):
		check1 = tk.Checkbutton(popup, text='Pentatonic', variable=self.pentatonic_var)
		check1.pack()
		check2 = tk.Checkbutton(popup, text='Diatonic', variable=self.diatonic_var)
		check2.pack()
		check3 = tk.Checkbutton(popup, text='Blues', variable=self.blues_var)
		check3.pack()

	def options_callback(self):
		self.scale_choices = []
		if self.pentatonic_var.get():
			self.scale_choices.append("Pentatonic")
		if self.diatonic_var.get():
			self.scale_choices.append("Diatonic")
		if self.blues_var.get():
			self.scale_choices.append("Blues")




app = GuitarTrainerApp()
app.geometry("800x600")
app.mainloop()

