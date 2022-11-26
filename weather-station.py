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
lang = "fr"

def checkApiKey():
    global apiKey

    apiKey = apiKeyEntry.get()
    checkApiUrl = str(str("https://api.openweathermap.org/data/2.5/weather?appid=") + str(apiKey))

    checkResponse = requests.get(checkApiUrl)
    checkData = checkResponse.json()
    print(f"Check data: {checkData}")
    
    if checkData["cod"] == "400":
        print(f"Valid API ({apiKey})")
        apiKeyWindow.destroy()
        main()
    else:
        print(f"Invalid API ({apiKey})")
        messagebox.showerror(title="Invalid API", message="L'API entré est invalide")
        exit()

def checkError(data):
    errorCode = data["cod"]
    print(f"Cod: {errorCode}")
    if errorCode == "404":
        messagebox.showerror(title=f"Erreur {errorCode}", message="La ville n'a pas été trouvé")
        main()
    return errorCode

def getData(cityName):

    global completUrl
    completUrl = str(str(baseUrl) + str(cityName) + "&units=" + str(units) + "&lang=" + str(lang) + "&appid=" + str(apiKey))
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
    weatherWindow.geometry("400x275")
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

    minTemp = dataToDisplay["main"]["temp_min"]
    minTempLabel = Label(weatherWindow, text=f"Température minimale: {minTemp}°C", font=mainFont, bg=bgDisplayColor, fg=fgDisplayColor)
    maxTemp = dataToDisplay["main"]["temp_max"]
    maxTempLabel  = Label(weatherWindow, text=f"Température maximale: {maxTemp}°C", font=mainFont, bg=bgDisplayColor, fg=fgDisplayColor)

    titleLabel.pack(pady=(5,0))
    weatherIconLabel.pack()
    temperatureLabel.pack()
    temperatureFeelLabel.pack()

    minTempLabel.pack(pady=(10, 0))
    maxTempLabel.pack(pady=(0,10))

    weatherWindow.resizable(False, False)
    weatherWindow.mainloop()

def main():

    global mainWindow
    mainWindow = Tk()
    mainWindow.geometry("425x225")
    mainWindow.title("Weather Station")

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

def getApiKey():

    global apiKeyWindow
    apiKeyWindow = Tk()
    apiKeyWindow.title("API key")

    global apiKeyEntry
    infoLabel = Label(apiKeyWindow, text="Veuillez entrer une clé d'API valide:", font=mainFont)
    apiKeyEntry = Entry(apiKeyWindow, width=30, font=mainFont)
    checkApiButton = Button(apiKeyWindow, text="Valider", font=mainFont, command=checkApiKey)

    infoLabel.pack(padx=20, pady=2)
    apiKeyEntry.pack(padx=20, pady=2)
    checkApiButton.pack(padx=20, pady=(4,6))

    apiKeyWindow.mainloop()

getApiKey()