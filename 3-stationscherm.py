import tkinter as tk
from tkinter import ttk
import psycopg2
import requests
from dotenv import load_dotenv
import os
load_dotenv()
# Maak het hoofdvenster
root = tk.Tk()
root.title("Stationshalscherm")
root.configure(bg="#FFFF00")
# stations
stations = ['Amsterdam', 'Utrecht', 'Den Haag']
# De dotenv protectie voor het niet exposen van gevoelige gegeven
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
# PostgreSQL-databaseconfiguratie
db_params = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': host,
    'port': port
}
# OpenWeatherMap API-sleutel
api_key = os.getenv("API_KEY2")
# Verbindingsparameters voor de database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Functie om faciliteiten voor een station op te halen
def haal_faciliteiten_op(stations):
    query = "SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service WHERE station_city = %s"
    cursor.execute(query, (stations,))
    resultaat = cursor.fetchone()
    if resultaat:
        return resultaat
    else:
        return (False, False, False, False)  # Geen gegevens gevonden, geef lege waarden terug

# Functie om weersvoorspelling op te halen van OpenWeatherMap API
def haal_weersvoorspelling_op(stations):
    latitude = 52.379189
    longitude = 4.899431

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    respons = requests.get(url)
    data = respons.json()

    weer = data['weather'][0]['description']
    temperatuur = data['main']['temp'] - 273.15  # Temperatuur in Celsius

    return f"Weer: {weer}, Temperatuur: {temperatuur:.2f}°C"


# Functie om het geselecteerde station te wijzigen
def selecteer_station():
    geselecteerd_station = station_var.get()
    faciliteiten = haal_faciliteiten_op(geselecteerd_station)
    weer = haal_weersvoorspelling_op(geselecteerd_station)

    faciliteiten_label.config(text=f"Faciliteiten: OV-fietsen: {faciliteiten[0]}, Lift: {faciliteiten[1]}, Toilet: {faciliteiten[2]}, P+R: {faciliteiten[3]}")
    weer_label.config(text=weer)

# Functie om berichten op te halen en weer te geven
def haal_en_toon_berichten(stations):
    query = "SELECT bericht FROM berichten ORDER BY datum_tijd_goedgekeurd DESC LIMIT 5"
    cursor.execute(query, (stations))
    resultaten = cursor.fetchall()

    for index, resultaat in enumerate(resultaten):
        bericht_label = tk.Label(root, text=f"Bericht {index+1}: {resultaat[0]}", foreground='black', background='Yellow')
        bericht_label.pack()



# Voegt een label en een keuzelijst toe om het station te selecteren
station_label = tk.Label(root, text="Selecteer een station:", foreground='black', background='Yellow')
station_label.pack()
station_var = tk.StringVar()
station_var.set(stations[0])
station_dropdown = ttk.Combobox(root, textvariable=station_var, values=stations, foreground='black', background='Yellow')
station_dropdown.pack()
station_select_button = tk.Button(root, text="selecteer", command=selecteer_station, foreground='black', background='Yellow')
station_select_button.pack()


# Voegt labels toe voor de faciliteiten, weer en berichten
berichten_label = tk.Label(root, text="Laatste 5 berichten:", foreground='black', background='Yellow')
berichten_label.pack()
haal_label = tk.Label(root, foreground='black', background='Yellow', command=haal_en_toon_berichten(stations))
haal_label.pack()
faciliteiten_label = tk.Label(root, text="Faciliteiten:",foreground='black', background='Yellow')
faciliteiten_label.pack()
weer_label = tk.Label(root, text="Weersvoorspelling:", foreground='black', background='Yellow')
weer_label.pack()

# Start de GUI
root.mainloop()
# Sluit de databaseverbinding
cursor.close()
conn.close()
