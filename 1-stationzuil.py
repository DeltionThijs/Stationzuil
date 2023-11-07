import datetime
import random
import tkinter as tk

#Maak een tkinter GUI
window = tk.Tk()
window.configure(bg="#FFFF00")
window.title("Review App")

def submit_review():
    # Haalt de ingevoerde bericht- en naamgegevens op
    message = message_entry.get()
    name = name_entry.get()
    wanneer_ingezonden = "Datum ingezonden"
    stations = ['Amsterdam Centraal', 'Utrecht Centraal', 'Den Haag Centraal']  # Lijst van stations

    if len(message) > 140:
        result_label.config(text='Fout: uw bericht mag maximaal 140 tekens zijn.')
    elif len(message.strip()) == 0:
        result_label.config(text='Fout: u moet een bericht invullen.')
    else:
        # Kiest een willekeurig station uit de lijst
        station = random.choice(stations)
        review = f'{message},{name},{station},{wanneer_ingezonden},{datetime.datetime.now()}\n'
        # Voegt het bericht toe aan het CSV-bestand
        with open('reviews.csv', 'a+') as reviews_file:
            reviews_file.write(review)
        result_label.config(text='Bericht is succesvol ingediend!')

# Maak en configureer de widgets voor het invoeren van berichten
message_label = tk.Label(window, text="Laat hier uw bericht achter:", background='Yellow', foreground='black')
message_label.pack()

message_entry = tk.Entry(window, width=75, foreground='black', background='Yellow')
message_entry.pack()

name_label = tk.Label(window, text="Wat is je naam?", background='Yellow', foreground='black')
name_label.pack()

name_entry = tk.Entry(window, width=75, foreground='black', background='Yellow')
name_entry.pack()

submit_button = tk.Button(window, text="Submit", command=submit_review, background='Yellow', foreground='black')
submit_button.pack()

result_label = tk.Label(window)
result_label.pack()

# Start de tkinter GUI-loop
window.mainloop()