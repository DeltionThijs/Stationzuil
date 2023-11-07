import tkinter as tk
import csv
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

# Variabelen voor in de onderstaande functies
csv_bestand = "reviews.csv"
datum_tijd = datetime.now()
datum_tijd_str = datum_tijd.strftime("%Y-%m-%d %H:%M:%S")
# Tkinter variabelen
root = tk.Tk()
root.configure(bg="#FFFF00")
root.title("Moderator GUI")
text_box = tk.Text(root, background='Yellow', foreground='black')
text_box.pack()

# Functie om de gegevens naar de database te schrijven
def schrijf_naar_database(bericht, goedgekeurd, afgekeurd, moderator_naam, moderator_email):
    # Maak verbinding met de database
    conn = psycopg2.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port)
    cursor = conn.cursor()
    # Voer de SQL-query uit om de gegevens in de database in te voegen
    cursor.execute(
        "INSERT INTO berichten (bericht, goedgekeurd, afgekeurd, datum_tijd_goedgekeurd, moderator_naam, moderator_email) VALUES (%s, %s, %s, %s, %s, %s)",
        (bericht, goedgekeurd, afgekeurd, datum_tijd_str, moderator_naam, moderator_email))
    # Bevestig de wijzigingen en sluit de verbinding
    conn.commit()
    conn.close()

# Functie om de gegevens uit het CSV-bestand te lezen
def lees_berichten(csv_bestand):
    berichten = []
    with open(csv_bestand, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            berichten.append(row)
    return berichten

# Functie om de gegevens te herladen
def reload_data():
    # Lees de gegevens uit het CSV-bestand
    berichten = lees_berichten(csv_bestand)
    # Maak de tekstbox leeg
    text_box.delete("1.0", tk.END)
    # Werk de tekstbox bij met de nieuwe gegevens
    for bericht in berichten:
        text_box.insert(tk.END, bericht)
        text_box.insert(tk.END, "\n")

# Functie om de gegevens naar het CSV-bestand te schrijven
def flush_data():
    # Lees de gegevens uit de database
    berichten = lees_berichten(csv_bestand)
    # Maak de tekstbox leeg
    text_box.delete("1.0", tk.END)
    # Werk de tekstbox bij met de nieuwe gegevens
    for bericht in berichten:
        text_box.insert(tk.END, bericht)
        text_box.insert(tk.END, "\n")
    # Schrijf de gegevens naar het CSV-bestand
    with open(csv_bestand, 'w', newline='') as csvfile:
        csvfile.write(berichten)

# Functie om het afkeur bericht te printen
def goedkeuren():
    print("Het bericht is goedgekeurd")
    pass

# Functie om het afkeur bericht te printen
def afkeuren():
    print("Het bericht is afgekeurd")
    pass

# Functie om het laatste bericht uit het CSV-bestand te lezen
def lees_laatste_bericht(csv_bestand):
    with open(csv_bestand, 'r+') as csvfile:
        csvreader = csv.reader(csvfile)
        berichten = list(csvreader)
        laatste_bericht = berichten[-1]
    return laatste_bericht

# Functie om module 2 uit te voeren
def module_2(csv_bestand):
    berichten = lees_berichten(csv_bestand)
    laatste_bericht = lees_laatste_bericht(csv_bestand)

    # Goedkeur functie om de data te verzenden naar de database
    def goedkeur_button_click():
        goedgekeurd = True
        afgekeurd = False
        moderator_naam = moderator_naam_entry.get()
        moderator_email = moderator_email_entry.get()
        schrijf_naar_database(laatste_bericht, goedgekeurd, afgekeurd, moderator_naam, moderator_email)
        goedkeuren()

    # Afkeur functie om de data te verzenden naar de database
    def afkeur_button_click():
        goedgekeurd = False
        afgekeurd = True
        moderator_naam = moderator_naam_entry.get()
        moderator_email = moderator_email_entry.get()
        schrijf_naar_database(laatste_bericht, goedgekeurd, afgekeurd, moderator_naam, moderator_email)
        afkeuren()

    # Tkinter Label voor alle reviews
    name_label = tk.Label(root, text="Alle reviews tot nu toe!", background='Yellow', foreground='black')
    name_label.pack()
    # Herlaad knop in Tkinter voor het CSV bestand
    reload_button = tk.Button(root, text="Herladen", command=reload_data, background='Yellow', foreground='black')
    reload_button.pack()
    # Moderator Naam invulbox in Tkinter
    moderator_naam_label = tk.Label(root, text="Moderator naam:", background='Yellow', foreground='black')
    moderator_naam_label.pack()
    moderator_naam_entry = tk.Entry(root, background='Yellow', foreground='black')
    moderator_naam_entry.pack()
    # Moderator Email invulbox in Tkinter
    moderator_email_label = tk.Label(root, text="Moderator e-mail:", background='Yellow', foreground='black')
    moderator_email_label.pack()
    moderator_email_entry = tk.Entry(root,  background='Yellow', foreground='black')
    moderator_email_entry.pack()
    # Goedkeur knop in Tkinter
    goedkeur_button = tk.Button(root, text="Goedkeuren", command=goedkeur_button_click, background='Yellow', foreground='black')
    goedkeur_button.pack()
    # Afkeur knop in Tkinter
    afkeur_button = tk.Button(root, text="Afkeuren", command=afkeur_button_click, background='Yellow', foreground='black')
    afkeur_button.pack()
    # Maak de knop om de gegevens naar het CSV-bestand te schrijven
    flush_button = tk.Button(root, text="Leeg het tijdelijke reviewbestand!", command=flush_data, background='Yellow', foreground='black')
    flush_button.pack()

# Voer module 2 uit
reload_data()
module_2(csv_bestand)
root.mainloop()
