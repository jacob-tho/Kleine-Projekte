import random
import pdb

#TO DO:Bugs fixen: CPU platzieren, User Inputs


class Schiffe:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(10)]  #board initialisieren
        self.enemy_board = [[0] * 10 for _ in range(10)]
        self.ships = {2: 1, 3: 1, 4: 1, 5: 1}  # Startwerte für Schifflänge (key) und Anzahl (value)
        self.player_guesses = set() #
        self.cpu_guesses = set()
        self.player_ships_remaining = 14 #Anzahl der Schiffselemente, siehe 196
        self.cpu_ships_remaining = 14
        self.cpu_previous_hit = None
        self.cpu_previous_direction = None

#BOARD STIMMT NOCH NICHT UND IST INKOMPATIBEL

    def place_ship(self, x, y, length, direction, board):
        '''
        Koordinaten werden übergeben, Länge des Schiffs, Richtung und auf welches Feld
        '''
        if direction == 'horizontal':
            #per default nach rechts
            for i in range(length):
                if x + i >= 10 or board[y][x + i] != 0:
                    return False  #Außerhalb des Felds
                if self.board[y][x + i] != 0:
                    return False #Collision
            for i in range(length):
                board[y][x + i] = int(f"{length}")
        elif direction == 'vertical':
            #per Default nach unten
            for i in range(length):
                if y + i >= 10 or board[y + i][x] != 0:
                    return False  #Außerhalb des Felds
                if self.board[y + i][x] != 0:
                    return False #Collision
            for i in range(length):
                board[y + i][x] = int(f"{length}")
        else:
            return False  #Weder horizontal noch vertikal
        self.ships[length] -= 1
        return True  #Erfolgreich platziert

    def all_ships_placed(self):
        '''
        Sind alle Schiffe platziert?
        '''
        return all(count == 0 for count in self.ships.values())

    def place_enemy_ships(self):
        '''
        Platziert zufällig, bis alle platziert sind. Mit Collision-Check.
        '''

        for length in self.ships.keys():
            while self.ships[length] > 0:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                direction = random.choice(['horizontal', 'vertical'])
                if self.place_ship(x, y, length, direction, board = self.enemy_board):
                    break
                    #for i in range(length):
                    #    self.enemy_board[y + i][x] = length
                    # Macht keinen Sinn, löschen
                else:
                    continue  #Nochmal, falls nicht geklappt

        #Das klappt alles, aber es wird irgendwie nicht ausgegeben :/
        #DAS HIER FIXEN
        return self.enemy_board

    def player_shot(self):
        '''
        Da müsste alles passen.
        '''
          while True:
              try:
                  user_input = input("X-Koordinate (0-9) oder 'quit' zum Abbruch: ")
                  if user_input.lower() == "quit":
                      exit()
                  x = int(user_input)
                  y = int(input("Y-Koordinate (0-9): "))
                  if not (0 <= x < 10 and 0 <= y < 10):
                      print("Koordinaten sind nicht innerhalb des Feldes, bitte nochmal!")
                      continue
                  if (x, y) in self.player_guesses:
                      print("Die Eingabe wurde bereits gemacht")
                      continue
                  return x, y
              except ValueError:
                  print("Bitte gebe ganze Zahlen ein.")


    def cpu_shot(self):
        '''
        Intelligentes schießen, erst random, dann mit System. In Kommentaren näher erklärt
        '''
          if self.cpu_previous_hit:
            #Wenn getroffen, bleib in der Nähe
            x, y = self.cpu_previous_hit
            if self.cpu_previous_direction == 'horizontal':
                if x + 1 < 10 and (x + 1, y) not in self.cpu_guesses:
                    return x + 1, y
                elif x - 1 >= 0 and (x - 1, y) not in self.cpu_guesses:
                    return x - 1, y
            elif self.cpu_previous_direction == 'vertical':
                if y + 1 < 10 and (x, y + 1) not in self.cpu_guesses:
                    return x, y + 1
                elif y - 1 >= 0 and (x, y - 1) not in self.cpu_guesses:
                    return x, y -
        #Wenn nicht getroffen, random schießen
          while True:
              x = random.randint(0, 9)
              y = random.randint(0, 9)
              if (x, y) not in self.cpu_guesses:
                  return x, y

    def update_board(self, board, x, y, hit):
        """
        Wenn Treffer: X, Wenn daneben: O, Wenn versenkt: -
        hit als arg ist Indikator
        """
        if hit:
            if board[y][x] != 'X':
                ship_length = board[y][x]
                board[y][x] = 'X'
                sunk = True
                for i in range(ship_length):
                    if x + i < 10 and board[y][x + i] != 'X':
                        sunk = False
                        break
                    if y + i < 10 and board[y + i][x] != 'X':
                        sunk = False
                        break
                if sunk:
                    for i in range(ship_length):
                        if x + i < 10:
                            board[y][x + i] = '-'
                        if y + i < 10:
                            board[y + i][x] = '-'
        else:
            board[y][x] = 'o'


    #DIESE FUNKTION KLAPPT NICHT. Für eigenes Board ist okay (nimm das in der Main)
    #Aber ich bekomme das cpu board nicht hin...
    #Die Methode rauschmeißen oder grundlegend ändern
    def print_board(self, board):
        print("   A B C D E F G H I J")
        for i in range(10):
            row = " ".join(cell for cell in board[i])
            print(f"{i}  {row}")
            #Nur eine der beiden Methoden!!! Leider funktionieren beide nicht so gut :(
    def get_board(self, board):
        return board

    def player_turn(self):
        """
        Player's turn to shoot.
        """
        print("\nDein Schuss:")
        x, y = self.player_shot()
        self.player_guesses.add((x, y))
        #Sepichere Eingaben in einer Liste, dass man nicht mehrmals die gleiche Koordinate trifft
        hit = self.enemy_board[y][x] != 0
        self.update_board(self.enemy_board, x, y, hit)
        #get_board klappt nicht. Nach jedem Schuss neuen Board-State ausgeben lassen
        self.get_board(self.enemy_board)
        if hit:
            print("Treffer!")
            self.cpu_ships_remaining -= 1
            if self.cpu_ships_remaining == 0:
                print("Glückwunsch, du hast gewonnen!")
                return True
        else:
            print("Daneben!")
        return False

    def cpu_turn(self):

        print("\nCPU schießt:")
        x, y = self.cpu_shot()
        self.cpu_guesses.add((x, y)) #Hier auch wieder Duplikate
        hit = self.board[y][x] != 0
        self.update_board(self.board, x, y, hit)
        #get_board klappt nicht
        self.get_board(self.board)
        if hit:
            print("Treffer!")
            self.player_ships_remaining -= 1
            if self.player_ships_remaining == 0:
                print("Du hast verloren!")
                return True
            self.cpu_previous_hit = (x, y)
            if (x + 1, y) in self.cpu_guesses:
                self.cpu_previous_direction = 'horizontal'
            elif (x - 1, y) in self.cpu_guesses:
                self.cpu_previous_direction = 'horizontal'
            elif (x, y + 1) in self.cpu_guesses:
                self.cpu_previous_direction = 'vertical'
            elif (x, y - 1) in self.cpu_guesses:
                self.cpu_previous_direction = 'vertical'
        else:
            print("Miss!")
            #Wenn nicht getroffen, wieder auf None zurück
            self.cpu_previous_hit = None
            self.cpu_previous_direction = None
        return False

    def play(self):
        while True:
            if self.player_turn():
                break
            if self.cpu_turn():
                break


if __name__ == "__main__":

    game = Schiffe()
    def eigenes_platzieren():

        print("Platzierungsphase...")

        while not game.all_ships_placed():
            for i in range(len(game.ships.keys())):
                #Zu allen inputs Exception
                print(f"Platziere Schiff mit Länge {list(game.ships.keys())[i]}")
                x = int(input("X-Koordinate: "))
                y = int(input("Y-Koordinate: "))
                length = list(game.ships.keys())[i]
                #hierzu wiederholen, wenn falsche inputs
                direction = input("Enter direction (horizontal or vertical): ").lower()
                #Nach jedem Platzieren Board zeigen
                if game.place_ship(x, y, length, direction, board = game.board):
                    print("Ship placed successfully!")
                else:
                    print("Invalid placement! Please try again.")

            print("Updated game board")
            for row in game.get_board(game.board):
                print(row)
                
    eigenes_platzieren()
    print("\nEnemy CPU board:")
    #DAS HIER IST DER DEBUGGER, GANZ WICHTIG UND BENUTZEN
    #pdb.set_trace() #Es klappt alles, nur das ausgeben nicht. Zeile 156
    game.place_enemy_ships()
    game.get_board(board = game.enemy_board)
    game.play()
'''

TO-DO: Gegner platziert und board ausgeben (zum checken)
        Board updaten, alle Fehler ausradieren
'''
