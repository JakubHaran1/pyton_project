import os
import random
import time


class Player:
    row_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    column_key = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","10 "]
    banned_symbols = ["<",".",">","?","/",";",":",'""',"[","{","]","}","\\","+","=","-","_",")","(","*","&","^","%","$","#","@","!","`","~","''"]
    
    def __init__(self, name):
        self.name = name
       
        self.ships = [['F3'], ['A6'], ['D1'], ['H9'], ['F7', 'F8'], ['C7', 'D7'], ['H4', 'I4'], ['C2', 'C3', 'C4'], ['H2', 'I2', 'J2'], ['D5', 'E5', 'F5', 'G5']] #wyczyścić 
        self.board_shot = self.board_maker()
        self.board_get = self.board_maker()
        self.protect_zone = []

    # Inicjacja tablicy
    def board_maker(self):
        row_value = []
        board = {}
        
        # Wypełnianie tablicy
        for i in range(10): #liczba kolumn i wierszy
            board[self.row_key[i]] = ["|0|"] * 10
            
        return board

    # Wyświetlanie tablicy
    def print_board(self,board):
        # Wyświetlanie zmiennych kolumnowych
        print("   ",*self.column_key)
        for row in self.row_key: 
            print(row, end="")
            for el in board[row]:
                print(el,end="")
            print()
            
        print()
    
    #funkcja określająca typ statku na podstawie aktualnej długości głównej tablicy statkowej
    def type_ship(self,length_ship):
        category = 0

        if length_ship < 4:
            category = 1
        elif length_ship < 7:
            category = 2
        elif length_ship < 9:
            category = 3
        elif length_ship == 9:
            category = 4
        
        return category

    def add_protect_field(self,zone,arr,el):
        zone = arr.strip() + el.strip()
        self.protect_zone.append(zone)

    def field_protector(self,orientation,ship):
        min_value = ship[0]
        max_value = ship[0]
        index_el = ""
        first_zone = ""
        second_zone = ""

        # Wyliczanie zabezpieczonych pól:
        if orientation == "row":

            # Ustalanie wartości
            for el in ship:
                #Znalezienie najmniejszej i największej wartości (w zależności od orientacji) 
                if int(min_value[1:]) > int(el[1:]): min_value = el
                else: max_value = el
            
                # Zmienna pomocnicza do wyliczenia górnego i dolnego bezpiecznego pola 
                index_el = self.row_key.index(f" {el[:1]} ")
                
                # Wyliczanie górnego pola
                if index_el != 0:
                    self.add_protect_field(first_zone, self.row_key[index_el - 1 ], el[1:])
                    
                # Wyliczanie dolnego pola
                if index_el != len(self.row_key) - 1:
                    self.add_protect_field(second_zone, self.row_key[index_el + 1 ], el[1:])
                    
                    
            # Wyliczanie "dodatkowych" bocznych pól
            # Pole lewe skrajne
            index_el = self.column_key.index(f"{min_value[1:]} ")
            if index_el != 0:
                self.add_protect_field(min_value, min_value[:1], self.column_key[index_el - 1].strip())
                
            
            # Pole prawe skrajne
            index_el = self.column_key.index(f"{max_value[1:]} ")
            if index_el != len(self.column_key) - 1:
                self.add_protect_field(max_value, max_value[:1], self.column_key[index_el + 1].strip())
        else:  
            for el in ship:
                
                #Znalezienie najmniejszej i największej wartości (w zależności od orientacji)
                if min_value[:1] > el[:1]: min_value = el
                else: max_value = el

                # Zmienna pomocnicza do wyliczenia lewego i prawego bezpiecznego pola 
                index_el = self.column_key.index(f"{el[1:]} ")
                
                # wyliczenie lewego zabezpieczonego pola
                if index_el != 0:
                    self.add_protect_field(first_zone ,el[:1], self.column_key[index_el - 1 ] )
                
                # Wyliczanie prawego zabezpieczonego pola
                if index_el != len(self.column_key) - 1:
                    self.add_protect_field(second_zone, el[:1], self.column_key[index_el + 1 ])

            # Wyliczanie "dodatkowego" górnego i dolnego pola
            # Pole górne
            index_el = self.row_key.index(f" {min_value[:1]} ")
            if index_el != 0:
                self.add_protect_field(min_value, self.row_key[index_el - 1].strip(), min_value[1:])

            # Pole dolne 
            index_el = self.row_key.index(f" {max_value[:1]} ")
            if index_el != len(self.row_key) - 1:
                self.add_protect_field(max_value, self.row_key[index_el + 1].strip(), max_value[1:])

    def draw_ship(self,ship,board,shot,miss):
        try:
            arr =""
            for el in ship:
                # dodać try aby nie wywalało errora jak w złej kolejności
                key = el[:1]
                value = int(el[1:])
                arr = board[f" {key} "]
                if shot == 0: arr[value-1] = "🚢 "
                elif shot ==1 and miss == 0: arr[value-1] = "🔥 "
                elif shot == 1 and miss == 1: arr[value-1] = "🚩 "
        except:
            print("Nie właściwy strzał - nie można nanieść strzału na plansze...")
    
    def check_shot(self,shot):
        for ship in self.ships:
            for el in ship:
                if shot == el:
                    get = shot
                    ship_remove = ship
                    return [get,ship_remove]
               
        get = ""
        ship_remove = "False"
        return [get, ship_remove ]



                    
            

class Ai(Player):
    def __init__(self,name):
        super().__init__(name)
        self.stategy = False
        self.first_shot = ""
        self.current_shot = ""
        self.direction = "" #bazowa zmienna kierunku
       
        self.correct_direction = "" #poprawny kierunek
        self.sink_ship = False
        self.fired_field = [""]
        self.wrong_directions = [""] #będą tu znajdywać się niewłaściwe kierunki dla danego pierwszego strzału aby wyeliminować sprawdzanie kilku krotne
    
    def create_ship(self, orientation):
        # Dodać sprawdzanie czy nie jest już zajęte pole i czy nie znajduje się w safety field!
        size = self.type_ship(len(self.ships))
        ship = []
        first_el = ""
        c = True
        while c == True:
            # Inicjacja pierwszego elementu statku:
            row = random.choice(self.row_key).strip()
            column = random.choice(self.column_key).strip()
            if int(column) + size <= len(self.column_key):
                first_el = row + column
                c = False
                ship.append(first_el)

        if orientation == "row" and size > 1:
            #Dołączanie kolejnych elementów składowych statku:
            i = 0
            while len(ship) != size:
                i+=1
                el = row + str(int(column) + i)
                ship.append(el)

        elif orientation == "column" and size > 1:
            i = 0
            index_el = self.row_key.index(f" {row} ")

            while len(ship) != size:
                i += 1
                el = self.row_key[index_el + i].strip() + column
                ship.append(el)



        return ship
    
    def reset_strategy(self):
        self.stategy = False
        self.first_shot = ""
        self.current_shot = ""
        self.direction = "" #bazowa zmienna kierunku
        self.correct_direction = "" #poprawny kierunek
        self.sink_ship = False  
        self.wrong_directions = [""]




    def check_direction(self):
        # losuj kierunek do momentu aż nie będzie w wrong direction
        while self.direction in self.wrong_directions:
            if self.first_shot[0][:1] == "A":
                if self.first_shot[0][1:] == "1":
                    self.direction = random.choice(["bottom","right"])
                    
                elif self.first_shot[0][1:] == "10":
                    self.direction = random.choice(["bottom","left"])
                    
                else: self.direction = random.choice(["bottom","left","right"])

            elif self.first_shot[0][:1] == "J":

                    if self.first_shot[0][1:] == "1":
                        self.direction = random.choice(["top","right"])
                        
                    elif self.first_shot[0][1:] == "10":
                        self.direction = random.choice([ "top", "left"])
                        
                    
                    else: self.direction = random.choice(["top","left","right"])
            else:
                    self.direction = random.choice(["bottom","top","left","right"])

    def aiming(self,shot_type,direction):
        
        shot = ""
        if direction == "top":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row - 1].strip()
            shot = row + shot_type[0][1:]

        elif direction == "bottom":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row + 1].strip()
            shot = row + shot_type[0][1:]
            
        
        elif direction == "right":
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column + 1].strip()
            shot = shot_type[0][:1] + column


            

        elif direction == "left":
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column - 1].strip()
            shot = shot_type[0][:1] + column
        
        

        return shot
    
    

    def shooting_ai(self):
        shot = ""
        #strzelanie losowe
        if self.stategy == False:
            while shot in self.fired_field:
                shot = random.choice(self.row_key).strip()
                shot = shot + random.choice(self.column_key).strip()
                
                
            
        
        elif self.stategy == "I":
            # Sprawdzanie w którym kierunku strzelać
            self.check_direction()
            shot = self.aiming(self.first_shot, self.direction)
        elif self.stategy == "II":
            
            shot = self.aiming(self.current_shot,self.correct_direction)
        
        elif self.stategy == "III":
            match self.correct_direction:
                case "top":
                    self.correct_direction = "bottom"
                case "left":
                    self.correct_direction = "right"
                case "bottom":
                    self.correct_direction = "top"
                case "right":
                    self.correct_direction = "left"
            
            shot = self.aiming(self.current_shot,self.correct_direction)

        self.fired_field.append(shot)
        return [shot]
        
        

    #strzelanie 
    #losowanie czy column czy row
    # potem losowanie columny lub row 
    # gdy traf 
        # (zapamiętaj traf) 
        #  spróbuj w lewo/prawo/góra dół / gdy traf idziesz w dół...
        # gdy nie traf zacznij od prawo/góra - to co ostatnio nie było traf 
    
    
                


            

    
       
        

            


class Batleship:
    def __init__(self):
        self.players = self.create_player()
        self.pre_game()
        self.start_game() 
        self.play_game()
        
    # Tworzenie graczy
    def create_player(self):
        print("---GRA W STATKI---")
        players = []
        name = input(f"Podaj imię gracza nr. 1: ")
        players.append(Player(name))
        players.append(Ai("Ai")) #Player pierwsze
        
        

        return(players)

    # Zmiana graczy 
    def switch_player(self, current):
        if current == self.players[0]:
            active = self.players[1]
            no_active = self.players[0]
            return [active,no_active]
        else:
            active = self.players[0]
            no_active = self.players[1]
            return [active, no_active]
        
    
    # Instrukcja gry 
    def pre_game(self):
        os.system('cls')
        print("---GRA W STATKI---",end='\n\n')
        print("Zasady:")
        print("Masz do wyboru: cztery jednomasztowce, trzy dwumasztowce, dwa trzymasztowce i jeden czteromasztowiec")
        print("Musisz rozmieszczać pojedyncze statki w obrębie jednego wiersza lub kolumny tzn. nie wolno ci postawić np.dwumasztowca na [A1,B2]")
        print("Statki nie mogą się stykać")
        print("Posiadasz dwie plansze:",end='\n\n')
        print("-strzelnicza na której będziesz zaznaczać swoje strzały") #board_shot
        self.players[0].print_board(self.players[0].board_shot)
        print("-celownicza na której będą zaznaczane twoje statki oraz strzały i trafienia drugiego gracza/Ai") #board_get
        self.players[0].print_board(self.players[0].board_get)
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE: ")
        os.system("cls") 



    def start_game(self):
        for player in self.players:
            if player.name != "Ai":
                while len(player.ships) != 10:
                    print(f"Uwaga! Uzupełnianie tablicy celowniczej statkami gracza:{player.name}")
                    orientation = "row"
                    size = player.type_ship(len(player.ships))
                    print("To jest twoja tablica ze statkami:")
                    player.print_board(player.board_get)
                    ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                    ship = ship.upper()
                    os.system('cls')
                    
                    try:
                        if ship == "": raise Exception("Uwaga! Nie podano pozycji statku!")

                        # Sprawdzannie czy znajdują się niedozwolone symbole
                        if not any(symbol.strip() in ship for symbol in player.banned_symbols):
                            # Dzielenie statku na poszczególne "frakcje"
                            ship = ship.split(",")
                        else:
                            raise Exception("W pozycji znajdują się niedozwolone symbole!!")

                        # Sprawdzanie długości statku
                        if len(ship) != size: raise Exception("Niepoprawna długość statku!!")

                        # Sprawdzanie czy wszystkie klucze są unikalne i nie znajduja się w safety_zone ani ships
                        for el in ship:
                            if player.ships.count(el) > 1: raise Exception(f"Wartość {el} występuje w deklaracji statku więcej niż jeden raz")

                            el = el.replace(" ","")
                            if f" {el[:1]} " not in player.row_key:
                                raise Exception(f"Niepoprawna wartość na pozycji wierszowej - {el[:1]} w {el}! Mają to być litery od A-J")
                            
                            if f"{el[1:]} " not in player.column_key:
                                raise Exception(f"Niepoprawna wartość na pozycji kolumnowej - {el[1:]} w {el}! Mają to być cyfry od 1-10")

                            if el in player.protect_zone:
                                raise Exception(f"Pozycja {el} jest pozycją chronioną innego statku!")
                            
                            for boat in player.ships: 
                                if el in boat:
                                    raise Exception(f"Na pozycji {el} jest już umiejscowiony statek!")


                        # Ustalenie pozycji statku
                        if len(ship) > 1:
                            # Przypisywanie wiersza do zmiennej pomocniczej - row
                            row = ship[0][:1] # Litera pierwszej części statku 
                            
                            # Przypisywanie kolumny do zmiennej pomocniczej - column
                            column = ship[0][1:] # Cyfra pierwszej części statku
                            
                            # Sprawdzanie w jakiej orientacji jest statek - na bazie drugiej części statku
                            if ship[1][:1] == row:
                                orientation = "row"
                            elif ship[1][1:] == column:
                                orientation = "column"
                            else: raise Exception("Statek musi znajdywać się w pozycji poziomej lub pionowej (te same kolumny lub wiersze) !!")
                            previous_el = ""
                            # Sprawdzanie czy pozycja jest utrzymywana i czy elementy składowe statku znajdują się koło siebie
                            if orientation == "row": 
                                for el in ship:
                                    if el[:1] != row: raise Exception("Statek nie jest umiejscowiony poziomo!!")
                                    if previous_el == "":
                                        previous_el = ship[0][1:]
                                    elif int(el[1:]) == int(previous_el) + 1:
                                        previous_el = el[1:]
                                    else:
                                        raise Exception("Elementy składowe statku nie są koło siebie!")
                                    
                                    
                            else:
                                for el in ship:
                                    if el[1:] != column: raise Exception("Statek nie jest umiejscowiony pionowo!!")
                                    
                                    if previous_el == "":
                                        previous_el = player.row_key.index(f" {ship[0][:1]} ")
                                    elif el[:1] == player.row_key[previous_el + 1].strip():
                                        previous_el = player.row_key.index(f" {el[:1]} ")
                                    else:
                                        raise Exception("Elementy składowe statku nie są koło siebie!")
                        
                        player.ships.append(ship)
                        
                    except Exception as e:
                        print(f"Uwaga! Błąd w deklaracji statku: {e}")
                        continue

                    player.field_protector(orientation,ship)
                    player.draw_ship(ship,player.board_get,0,0)
            
                    
            else:
                while len(player.ships) != 10:
                    try:
                        orientations = ["row","column"]
                        orientation = random.choice(orientations)
                        ship = player.create_ship(orientation)
                        # Tutaj to sprawdzanie
                        for el in ship:
                            if el in player.protect_zone:
                                raise Exception
                            
                            for boat in player.ships: 
                                if el in boat:
                                    raise Exception

                        player.ships.append(ship)
                        player.field_protector(orientation, ship)
                        
                    except Exception:
                        continue

                
                
    def play_game(self):
        os.system("cls")
        print("Rozpoczynamy grę! Podawaj koordynaty gdzie twoja załoga ma strzelać (np. A1)",end='\n')
        
        active_player = self.players[0]
        no_active = self.players[1]
        while self.players[0].ships != [] or self.players[1].ships != []:
            print(f"Strzały oddaje {active_player.name}")
            active_player.print_board(active_player.board_shot)
            
            get = ""
            shot = ""
            if active_player.name != "Ai":
                shot = [input("Podaj koordynaty statku przeciwnika: ").upper()]
                
            else:
                print("AI")
                # TWORZENIE STRZAŁÓW W ZALEŻNOŚCI OD ZMIENNYCH
                # 1.Losowy strzał
                # 2. Sprawdzanie kierunku 
                shot = active_player.shooting_ai()
                print(f"to jest strzał AI: {shot}")
                

            for ship in no_active.ships:
                if get != "":
                    break #aby po znalezieniu juz nie sprawdzało
                for el in ship:
                    if shot[0] == el:
                        ship.remove(el)
                        get = shot
                        ship_remove = ship
                        break
                    
                
            if get != "":
                print(f"Gratulację! Gracz {active_player.name} trafił!")
                active_player.draw_ship(shot,active_player.board_shot,1,0)
                active_player.print_board(active_player.board_shot)
                
                
                if len(ship_remove) == 0:
                    no_active.ships.remove([])
                    print("UWAGA STATEK ZATONĄŁ!")
                    # Resetowanie strategii gdy statek zatonął
                    if active_player.name == "Ai":
                        active_player.sink_ship = True
                    
                print("Przysługuje mu kolejny strzał!")
                next_step = input("Enter aby przejść dalej...")
                # Zmiana zmiennych w zależności czy traf 
                
                if active_player.name == "Ai":
                    # Dla losowych strzałów:
                    if active_player.stategy == False:
                        active_player.stategy = "I" #przechodzenie do sprawdzania kierunku
                        active_player.first_shot = shot

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()
                        
                        
                        # Dla sprawdzania kierunku
                    elif active_player.stategy == "I":
                        active_player.stategy = "II" #Przechodzenie do zatapiania statku
                        #Zapisywanie właściwego kierunku
                        active_player.correct_direction = active_player.direction 
                        # Zapisywanie current shot - potrzebne do funkcji zatapiającej
                        active_player.current_shot = shot
                        print(active_player.current_shot)

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()
                        # Dla zatapiania statku i poprawania zatapiania
                    elif active_player.stategy == "II":
                        active_player.current_shot = shot

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()

                    elif  active_player.stategy == "III":
                        active_player.stategy = "II"
                        active_player.current_shot = shot
                        if active_player.sink_ship == True:
                            active_player.reset_strategy()

            else:
                print("Pudło!!",end='\n')
                active_player.draw_ship(shot,active_player.board_shot, 1, 1)
                active_player.print_board(active_player.board_shot)
                next_step = input("Enter aby przejść dalej...")
                print("Następuje zmiana gracza...")
                # Zmiana zmiennych w zależności  czy nie TRAF
                # Dla losowych strzałów: brak 
                # Dla sprawdzania kierunku
                if active_player.name == "Ai":
                    if active_player.stategy == "I":
                        active_player.wrong_directions.append(active_player.direction)
                    # Dla zatapiania statku
                    elif active_player.stategy == "II":
                        active_player.current_shot = active_player.first_shot
                        active_player.stategy = "III"

                [active_player, no_active] = self.switch_player(active_player)
            
            
                    

         
            
           
            
        os.system("cls")
        


                
batleship = Batleship()