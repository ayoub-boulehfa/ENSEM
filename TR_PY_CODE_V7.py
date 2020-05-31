#this code was created bye ENSEM students
from serial import *
import os
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt


print("""plateforme temps réels permettant la mesure du temps du contrôle et la manipulation des mesures prises par des capteurs de température, pression et volume à l’aide d’une carte Arduino.
Le projet est réalisé par :
-	Lamiae Touti
-	Oumniya Ramdi 
-	Ayoub Boulehfa
-	Oussama Moudnib
\t                 Encadré par H.Medromi""")
sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')
com="com"+str(input("Entrez le numéro de port COM connecté à l'arduino:"))
i=-1
plt.axis([0, 10, 0, 100])
plt.axis([0, 2, 0, 50])
plt.scatter(i,0,color='r',label="Temp")
plt.scatter(i,0,color='b',label="Pres")
plt.scatter(i,0,color='g',label="Debit")
plt.legend()
i=0
try:
    with Serial(port=com, baudrate=9600, timeout=1, writeTimeout=1) as port_serie:
        while True:
            ligne = port_serie.readline()
            ligne = str(ligne)
            ligne=ligne[2:-5]
            L=ligne.split()
            if L != [] :
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                Temp=L[0]
                Pres=L[1]
                debit=L[2]
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Temperature \t: \t"+str(Temp)+"\nPression \t: \t"+str(Pres)+"\nDébit \t\t: \t"+str(debit))
                file_object = open('base de données.txt', 'a')
                file_object.write(str(current_time)+"\t\tTemperature \t:"+str(Temp)+"\tPression \t:"+str(Pres)+"\tDébit \t"+str(debit)+"\n")
                file_object.close()
                plt.axis([0, i+2, 0, 50])
                plt.scatter(i,Temp,color='r',label="Temp")
                plt.scatter(i,Pres,color='b',label="Pres")
                plt.scatter(i,debit,color='g',label="Debit")
                i+=1
                plt.pause(0.01)
                               
                
                
except:
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("aucune carte n'est connecté au port "+com)

time.sleep(5)
