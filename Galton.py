import random
import os
import time
import pdb
import matplotlib.pyplot as plt

'''
Galton.py:
Im Rahmen des Programmierprojekts, soll ein Galton-Bret erstellt werden.

Hierzu wurde objektorientiert das Brett in den Parametern Kugelanzahl und Brett-Stufen initialisiert.
Die Methode Bernoulli soll simulieren, dass mit einer fünfzig-prozentigen Wahrscheinlichkeit die Kugeln bei
Kontakt mit einem Knoten nach links oder rechts wandern.

Die Methode "ergebnis_ausgeben" zeigt in der Konsole, wie viele Kugeln im jeweiligen finalen Fach landen.
Selbsterklärend wird bei "simulate" der Prozess durchlaufen, bis alle Kugeln im letzten Fach sind.
Hierbe wird auch bei jeder Kugel der Verlauf in einer txt-Datei "galton.txt" gespeichert.
Diese wird nach Beendigung der user_abfrage gelöscht.

Zur Optimierung des Progammes wurde Debugging Methoden mittels der Bibliothek "pdb" verwendet.
Ebenso bei der Laufzeitoptimierung, hier wurde die "time"-Bibliothek verwendet.

Rein zur Visualisierung wurde am Ende zu kosmetischen Zwecken die Bibliothek matplotlib.pyplot verwendet.


'''
class Brett:
    def __init__(self, ebenen: int):
        self.ebenen = ebenen
        self.knoten = [0] * (self.ebenen + 1)
        self.kugel = 0

        #Ausgabe einer Visualisierung der Brettstruktur
    def brett_printen(self) -> None:
        for i in range(self.ebenen + 1):
            print(' ' * (self.ebenen - i) + 'o ' * (i + 1))

        #Ausgabe der Anzahl der Kugeln nachdem alle durchgelaufen sind
    def ergebnis_ausgeben(self) -> None:
        print("\n Kugeln in der letzten Ebene: \n")
        print(self.knoten)

        #Bernoulli-Experiment pro Knoten + Eintrag des Pfades in txt Datei
    def bernoulli(self, file):
        position = 0
        path = []
        for i in range(self.ebenen):
            dir = random.choice([0,1])
            if dir == 1:
                path.append("rechts")
            elif dir == 0:
                path.append("links")
            position += dir
        file.write(", ".join(path))
        self.knoten[position] += 1
        self.kugel +=1


    def simulate(self, num_balls:int) -> None:
        file = open("galton.txt", "x")
        for i in range(int(num_balls)):
            file.write(f"{i+1}: ")
            self.bernoulli(file)
            file.write("\n")
        self.ergebnis_ausgeben()

#User-Abfrage, welchen Pfad welche Kugel zurückgelegt hat
def user_abfrage():
    print("\nDrücken Sie 'q' zum Verlassen")
    anfrage = input("Von welcher Kugel wollen Sie den Pfad wissen? Bitte nur ganze Zahlen eingeben: ")
    if anfrage == 'q':
        return False
    #Exception-Handling, falls Index Out of Range
    try:
        with open("galton.txt", "r") as file:
            lines = file.readlines()
            if 0 < int(anfrage) <= len(lines):
                print(lines[int(anfrage) - 1].strip())
            else:
                print(f"Ungültige Eingabe. Bitte eine Zahl innerhalb des Bereichs eingeben. (1 - {num_balls})")
    #Test, ob File kreiert wurde
    except FileNotFoundError:
        print("Die Datei existiert nicht.")
    #Falls Eingabe weder q noch int
    except ValueError:
        print("Bitte eine gültige Zahl eingeben.")
    return True
if __name__ == "__main__":
    try:
        rows = int(input("Anzahl der Reihen: "))
        num_balls = int(input("Anzahl der Kugeln: "))

        galton_board = Brett(rows)
        print("Form des aufgespannten Bretts: \n")
        galton_board.brett_printen()

        start = time.time()
        galton_board.simulate(num_balls)
        end = time.time()
        time = end - start

        while user_abfrage() == True:
            pass

    #Datei Löschen für weitere Versuche, auch bei KeyBoardInterrupt bei zu großen Eingaben
    except KeyboardInterrupt:
        print("Programmabbruch! Lösche die Datei.")
    finally:
        if os.path.exists("galton.txt"):
            os.remove("galton.txt")
            print("Datei gelöscht.")
        else:
            print("Die Datei existiert nicht")
    print(f"Zeit in Sekunden: {time}")

    ### Visualisierung
    x_axis = range(1, rows +2)
    y_axis = galton_board.knoten
    plt.bar(x_axis, y_axis)
    plt.show()
