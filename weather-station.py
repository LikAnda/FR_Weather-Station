import base64
import requests
from tkinter import *
import urllib.request
from tkinter import messagebox
from urllib.request import urlopen

try:
    urllib.request.urlopen("https://www.google.com/")
except:
    messagebox.showerror(title="Erreur", icon="error" ,message="Vous n'êtes pas connecté à internet")
    exit()

mainFont = ("Nordique Inline", 12)
bgDisplayColor = "#807777"
fgDisplayColor = "#FFFFFF"

baseUrl = "https://api.openweathermap.org/data/2.5/weather?q="
units = "metric"
apiKey = ""

def checkError(data):
    errorCode = data["cod"]
    print(f"Cod: {errorCode}")
    if errorCode == "404":
        messagebox.showerror(title=f"Erreur {errorCode}", message="La ville n'a pas été trouvé")
        main()
    return errorCode

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
    dataToDisplay = getData(city)
    print(dataToDisplay)
    
    if checkError(dataToDisplay) != 200:
        print("Error cod != 200")
        return

    global weatherWindow
    weatherWindow = Tk()
    weatherWindow.geometry("400x225")
    weatherWindow.title(f"Météo de la ville de {city}")
    weatherWindow.configure(bg=bgDisplayColor)

    nameData = dataToDisplay["name"]
    titleLabel = Label(weatherWindow, text=(f"{nameData}:"), font=mainFont, bg=bgDisplayColor, fg=fgDisplayColor)

    iconUrl = str("http://openweathermap.org/img/wn/") + dataToDisplay["weather"][0]["icon"] + str("@2x.png")
    weatherIcon_byt = urlopen(iconUrl).read()
    weatherIcon_b64 = base64.encodebytes(weatherIcon_byt)
    weatherIcon = PhotoImage(data=weatherIcon_b64)
    weatherIconLabel = Label(weatherWindow, image=weatherIcon, bg=bgDisplayColor)

    temperature = dataToDisplay["main"]["temp"]
    temperatureLabel = Label(weatherWindow, text=(f"Température: {temperature}°C"), font=mainFont, bg=bgDisplayColor, fg=fgDisplayColor)
    temperatureFeel = dataToDisplay["main"]["feels_like"]
    temperatureFeelLabel = Label(weatherWindow, text=f"Ressenti: {temperatureFeel}°C", font=mainFont, bg=bgDisplayColor, fg=fgDisplayColor)

    titleLabel.pack()
    weatherIconLabel.pack()
    temperatureLabel.pack()
    temperatureFeelLabel.pack()

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