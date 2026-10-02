import tkinter
import tkintermapview
from click import style
from colorama import Style
from numpy import insert
import phonenumbers
import opencage

# Make sure you have a key.py file with your 'key' variable defined
from key import key

from phonenumbers import geocoder
from phonenumbers import carrier

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from opencage.geocoder import OpenCageGeocode

root = tkinter.Tk()
root.geometry("500x500")

label1 = Label(text="Phone Number Tracker")
label1.pack()

def getresult():
    num = number.get('1.0', END).strip() # .strip() removes trailing newlines
    try:
        num1 = phonenumbers.parse(num)
    except:
        messagebox.showerror("Error", 'Number box is empty or the input is not numeric !!')
        return # Stops the execution if parsing fails
        

    location = geocoder.description_for_number(num1,'en')
    service_provider = carrier.name_for_number(num1, 'en')

    ocg = OpenCageGeocode(key)
    query = str(location)
    results = ocg.geocode(query) # Fixed typo: 'gecode' to 'geocode'

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    my_label = LabelFrame(root)
    my_label.pack(pady=20)

    map_widget = tkintermapview.TkinterMapView(my_label, width=450, corner_radius=0)
    map_widget.pack()

    map_widget.set_position(lat, lng)
    map_widget.set_marker(lat, lng, text = "Phone Location")
    map_widget.set_zoom(10)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack()

    # Clear previous results if any
    result.delete('1.0', END)

    result.insert(END, "The country of this number is: " + location)
    result.insert(END, '\n The sim card of this number is: ' + service_provider)

    # Fixed syntax spacing and concatenation below
    result.insert(END, "\n Latitude is: " + str(lat))
    result.insert(END, "\n Longitude is: " + str(lng))

number = Text(height=1)
number.pack()

# Fixed ttk styling parameters
style = Style()
style.configure("TButton", font=('calibri', 20, 'bold'), borderwidth='4')
style.map('TButton', foreground = [('active', '!disabled', 'green' )],
          background = [('active', 'black')]
          )

Button = Button(text='Search', command=getresult)
Button.pack(pady=10, padx=100)

result = Text(height=7)
result.pack()

root.mainloop()
