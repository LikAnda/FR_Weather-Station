import json
import base64
import requests
from tkinter import *
from urllib.request import urlopen

mainFont = ("Nordique Inline", 12)

baseUrl = "https://api.openweathermap.org/data/2.5/weather?q="
units = "metric"
apiKey = ""

def getData(cityName):

    global completUrl
    completUrl = str(str(baseUrl) + str(cityName) + "&units=" + units + "&appid=" + str(apiKey))
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
    weatherWindow.attributes('-alpha',0.5,)
    weatherWindow.configure(bg="#616161")

    iconUrl = str("http://openweathermap.org/img/wn/") + data["weather"][0]["icon"] + str("@2x.png")
    weatherIcon_byt = urlopen(iconUrl).read()
    weatherIcon_b64 = base64.encodebytes(weatherIcon_byt)
    weatherIcon = PhotoImage(data=weatherIcon_b64)
    weatherIconLabel = Label(weatherWindow, image=weatherIcon)

    temperature = data["main"]["temp"]
    temperatureLabel = Label(weatherWindow, text=(f"Température: {temperature}°C"), font=mainFont)

    weatherIconLabel.pack()
    temperatureLabel.pack()

    weatherWindow.resizable(False, False)
    weatherWindow.mainloop()

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