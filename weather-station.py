import json
import requests
from tkinter import *

mainFont = ("Nordique Inline", 12)

baseUrl = "https://api.openweathermap.org/data/2.5/weather?q="
apiKey = ""

def getData(cityName):

    global completUrl
    completUrl = str(str(baseUrl) + str(cityName) + "&appid=" + str(apiKey))
    print(f"Complete Url: {completUrl}")

    response = requests.get(completUrl)
    data  = response.json()

    return data

def displayWeather():
    city = str(cityEntry.get())

    mainWindow.destroy()
    data = getData(city)
    print(data)

    weatherWindow = Tk()
    weatherWindow.geometry("400x225")
    weatherWindow.title(f"Météo de la ville de {city}")

def main():

    global mainWindow
    mainWindow = Tk()
    mainWindow.geometry("425x225")
    mainWindow.title("Weather Station")

    mainWindow.wm_attributes('-transparentcolor','#000000')

    global cityEntry
    mainLabel = Label(mainWindow, text="Station Météo", font=("Nordique Inline", 20))
    cityEntryLabel = Label(mainWindow, text="Nom de la ville/village:", font=mainFont)
    cityEntry = Entry(mainWindow)
    searchButton = Button(mainWindow, text="Rechercher", command=lambda: displayWeather())

    mainLabel.grid(row=0, column=1)

    cityEntryLabel.grid(row=1, column=0, padx=5)
    cityEntry.grid(row=1, column=1, padx=5, pady=20)
    searchButton.grid(row=1, column=2, padx=5)
    
    mainWindow.resizable(False, False)
    mainWindow.mainloop()

main()