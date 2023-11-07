import tkinter as tk
import requests

# Maak het hoofdvenster
root = tk.Tk()
root.configure(bg="#FFFF00")
root.title("NS Arrivals")
root.geometry("500x500")

# Definieer de stations
utrecht = 'ut'
apeldoorn = 'apd'
amsterdam = 'asd'
stations = [utrecht, apeldoorn, amsterdam]

# Functie om aankomsten op te halen en weer te geven
def get_arrivals():
    station = station_listbox.get(station_listbox.curselection())  # Haal het geselecteerde station op
    url = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/arrivals?station={station}"

    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": "d21c11c455cf4b238048aafb0178a7e7"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    result_text.delete("1.0", tk.END)  # Verwijder vorige resultaten

    for arrival in data["payload"]["arrivals"]:
        train_number = arrival["origin"]
        planned_track = arrival["plannedTrack"]
        result_text.insert(tk.END, f"Treinnummer: {train_number}\n")
        result_text.insert(tk.END, f"Vertrekspoor: {planned_track}\n")
        result_text.insert(tk.END, "-----------\n")

# Label voor het selecteren van een station
station_label = tk.Label(root, width=75, text="Station:", foreground='black', background='Yellow')
station_label.pack()

# Lijstbox voor het selecteren van een station
station_listbox = tk.Listbox(root, width=75, foreground='black', background='Yellow')
station_listbox.pack()

for station in stations:
    station_listbox.insert(tk.END, station)

# Knop om aankomsten op te halen
get_arrivals_button = tk.Button(root, width=75, text="Get Arrivals", command=get_arrivals, foreground='black', background='Yellow')
get_arrivals_button.pack(pady=4)

# Tekstvak om aankomstresultaten weer te geven
result_text = tk.Text(root, width=75, foreground='black', background='Yellow')
result_text.pack()

# Start de GUI
root.mainloop()
