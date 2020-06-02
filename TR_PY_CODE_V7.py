import csv
from serial import *
from time import sleep
from datetime import datetime
import hashlib
import numpy as np
import matplotlib.pyplot as plt
import keyboard

class Graphes:

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    colors = ['b', 'r', 'g']

    def __init__(self, step, x_width):
        self.fig = plt.figure(figsize=(10, 10))
        self.init_fig()
        self.show_credits()
        self.axs = [self.fig.add_subplot(311), self.fig.add_subplot(312), self.fig.add_subplot(313)]
        self.fig.tight_layout(pad=5.0)
        self.init_axs()
        self.timestamp = [0, ]
        self.step = step
        self.x_width = x_width
        self.y_axs = [[], [], []]
        self.statistics = [None, None, None]
        self.last_values = [None, None, None]

    def init_fig(self):
        self.fig.canvas.toolbar.pack_forget()
        self.fig.set_facecolor('lavender')

    def init_axs(self):
        self.axs[0].set_ylabel("Temperature (C)", fontsize=14)
        self.axs[1].set_ylabel("Pression (bar)", fontsize=14)
        self.axs[2].set_ylabel("Debit (m^3/s)", fontsize=14)

        for ax in self.axs:
            ax.set_xlabel("temps (s)")
            ax.xaxis.set_label_coords(1.04, -0.025)
            ax.grid(True)
            ax.set_facecolor((0.9, 0.9, 0.9))

    def show_credits(self):
        credits_title ="""
plateforme temps réels permettant la mesure du temps du contrôle
et la manipulationdes mesures prises par des capteurs de
température,pression et volume à l’aide d’une carte Arduino."""
        credits_names="""
Le projet est réalisé par :
Lamiae Touti
Oumniya Ramdi 
Ayoub Boulehfa
Oussama Moudnib
"""
        credits_MTR='Encadré par H.Medromi'
        plt.text(0.5, 1, credits_title, ha='center', va='center', fontsize=15)
        plt.text(0.0, 0, credits_names, ha='center', va='center', fontsize=10)
        plt.text(1, 0, credits_MTR, ha='center', va='center', fontsize=11)
        plt.axis('off')
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.pause(3)
        plt.clf()

    def update(self, donnees):
        for i, (value, ax, y_values, color) in enumerate(zip(donnees, self.axs, self.y_axs, self.colors)):
            y_values.append(value)
            ax.plot(self.timestamp, y_values, color=color, antialiased=True)
            x_min, x_max = max(0, self.timestamp[-1] - self.x_width), max(self.timestamp[-1], self.x_width)
            ax.set_xlim(left=x_min, right=x_max)
            ax.xaxis.set_ticks(np.arange(x_min, x_max, self.step))

            if self.last_values[i]:
                self.last_values[i].set_visible(False)
            self.last_values[i] = ax.text(self.timestamp[-1] + self.step/10, value, value)
    
            if self.statistics[i]:
                self.statistics[i].set_visible(False)
            statistics_string = 'MIN: ' + "{:.2f}".format(min(y_values)) + '  ||  MAX: ' + "{:.2f}".format(max(y_values)) + '  ||  AVG: ' + "{:.2f}".format(np.mean(y_values))
            self.statistics[i] = ax.annotate(statistics_string, (0.25, -0.18), xycoords='axes fraction', va='top', fontsize=12, bbox=self.props)

        plt.pause(self.step)
        self.timestamp.append(self.timestamp[-1] + self.step)

class BaseDonnees:

    def __init__(self, name):
        try:
            self.file = open(name + '.csv', mode='w')
            self.writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.writer.writerow(["Date", "Temperature", "Pression", "Debit"])
        except:
            print("Error opening database")

    def write(self, temperature, pression, debit):
        self.writer.writerow([datetime.now().strftime("%H:%M:%S"), str(temperature), str(pression), str(debit)])
        self.file.flush()

    def close(self):
        self.file.close()

class SerialPort:

    def __init__(self):
        com = "com" + SerialPort.get_numero_port()
        self.file = Serial(port=com, baudrate=9600, timeout=1, writeTimeout=1)

    def get_numero_port():
        port = input("Entrez le numéro de port COM connecté à l'arduino: ")
        correct = False
        while not correct:
            try:
                correct = int(port) >= 0
                if not correct:
                    raise ValueError
            except ValueError:
                port = input("Erreur: veuillez enter un entier positif: ")
        return port

    def get_data(self):
        return self.file.readline()[0: -5].split()

    def close(self):
        self.file.close()

class Identification:

    username = "21232f297a57a5a743894a0e4a801fc3"
    password = "b7fb5f77d7c3efd9358ea1c55bb74734"

    def __init__(self):
        while True:
            username = input("Identifiant: ")
            password = input("Mot de passe: ")
            if hashlib.md5(username.encode()).hexdigest() != Identification.username or hashlib.md5(password.encode()).hexdigest() != Identification.password:
                print("Les informations d'identification sont invalides, veuillez reessayer.\n")
            else:
                break

if __name__ == "__main__":
    serial_port = None
    base_donnees = None
    Identification()
    try:
        serial_port = SerialPort()
        graphes = Graphes(2, 60)
        
        base_donnees = BaseDonnees("database")

        while True:
            donnees = serial_port.get_data()
            if donnees:
                donnees = list(map(lambda s: float(s), donnees))
                graphes.update(donnees)
                base_donnees.write(*donnees)
                
    except:
        if serial_port:
            serial_port.close()
        if base_donnees:
            base_donnees.close()
        print("Une erreur est survenue")
