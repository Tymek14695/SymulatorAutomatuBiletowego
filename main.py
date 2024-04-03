from colorama import Fore, Back
#import keyboard
import os
import time
import datetime
from random import randint

print(Back.BLUE + 'TatraBus' + 1000 * ' ')
time.sleep(3)

def report(msg):
    with open('reports.log', 'a', encoding='utf-8') as file:
        file.write(f'{datetime.datetime.now()}    {msg}\n')
report('')
report('Started simulator')


def renderText(lines):
    if lines != []:
        with open('screen.txt', 'w', encoding='utf-8') as file:
            file.write('')
        with open('screen.txt', 'a', encoding='utf-8') as file:
            for line in lines:
                file.write(line + '\n')
    else:
        with open('screen.txt', 'r', encoding='utf-8') as file:
            print(file.read())

def animation(frame):
    for line in range(3):
        for char in range(30):
            print(Fore.CYAN + '█', end='')
        print()
    for line in range(2):
        for char in range(30):
            print(Fore.BLACK + '█', end='')
        print()
    for i in range(len('██████████████████████████████')):
        if (i + frame) % 3 == 0:
            print(Fore.BLACK + '█', end='')
        else:
            print(Fore.WHITE + '█', end='')
    print()
    for line in range(2):
        for char in range(30):
            print(Fore.BLACK + '█', end='')
        print()
    time.sleep(0.1)
    #report(f'Played frame {frame} of animation')


def reportActivity():
    print(Fore.GREEN, '==========')


def prnt(text):
    print(Fore.GREEN + str(text))


def loadScene(title):
    for frame in range(10):
        animation(frame)
        os.system('cls' if os.name=='nt' else 'clear')
    reportActivity()
    print(Fore.BLACK + str(title))
    report(f'Cleared console and loaded scene {title}')

def getPricelist():
    priceList = []
    loadScene('Pobieranie danych z cennika')
    with open('cennik.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            reader = ''
            i = 0
            while line[i] != '-':
                reader += line[i]
                i += 1
            #while reading 'cennik.txt', program interprets characters on the left side of '-' as data

            priceList.append(float(reader))
        loadScene('Zapisywanie cennika')
    report(f'Imported price list {priceList}')
    return priceList


    

class Ticket:
    loadScene('BILET')
    def __init__(self, rodzaj, przejazdy, ulga, ilosc): #tworzenie nowego biletu i kalkulowanie jego ceny
        loadScene('Wpisywanie danych')
        self.kind, self.rides, self.discount, self.amount = rodzaj, przejazdy, ulga, ilosc
        #loadScene('Weryfikacja cennika')
        pricelist = getPricelist()
        report(f'Loaded pricelist: {pricelist}')
        loadScene('Kalkulowanie ceny')
        if self.kind == 'jednorazowy':
            x = float(pricelist[0])
            self.price = (x * self.amount) * (1 - self.discount)
        elif self.kind == 'wielorazowy':
            x = float(pricelist[1]) * self.rides
            self.price = (x * self.amount) * (1 - self.discount)
        else:
            x = float(pricelist[2])
            self.price = (x * self.amount) * (1 - self.discount)
        report(f'Calculated price: {self.price}')
        report(f'Created new object of Ticket class {self}')
        #loadScene('Zapisano bilet')

    def printData(self):
        print(Fore.WHITE + self.kind, self.rides, self.discount, self.amount, self.price)

def printTickets():
    for i in range(len(cart)):
        with open(f'bilet{i + 1}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        with open(f'bilet{i + 1}.txt', 'a', encoding='utf-8') as file:
            file.write('+\n')
            file.write(f'| Rodzaj: {cart[i].kind}\n')
            file.write(f'| Ulga: {cart[i].discount * 100}%\n')
            file.write(f'| Cena: {cart[i].price}\n')
            file.write('|\n')
            file.write('| Imię posiadacza: ................\n')
            file.write('| Nazwisko posiadacza: ................\n')
            file.write('|\n')
            file.write(f'|Numer biletu/data pobrania: {randint(1, 9999)}/{datetime.datetime.now()}\n')
            file.write('+')
        os.system(f'start bilet{i + 1}.txt' if os.name=='nt' else f'open bilet{i + 1}.txt')
    report('Printed tickets')



def payment():
    loadScene('Płatność')
    summaryPrice, coinsWorth = 0, 0
    for items in cart:
        summaryPrice += items.price
    print(Fore.WHITE + 'Razem do zapłaty:', summaryPrice)
    while coinsWorth < summaryPrice:
        coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        coin = float(input('>> '))
        if coin in coins:
            coinsWorth += coin
        else:
            print(Fore.RED + 'Nie ma takiej monety!')
        print('Saldo:', coinsWorth)
    widthdraw = coinsWorth - summaryPrice
    print(Fore.WHITE + 'Płatność zaakceptowana, wydaję resztę równą', round(widthdraw, 2), '...')
    report(f'Finished payment of {summaryPrice} with {coinsWorth} worth of coins and {widthdraw} widthdraw')
    printTickets()
    


def showCart():
    loadScene('Koszyk')
    print('Rodzaj   Przejazdy    Ulga    Ilość   Cena')
    for items in cart:
        items.printData()
        #print(items.kind, items.rides, items.discount, items.amount)
    main() if str(input('Czy chcesz kupić kolejny bilet? [t/n]>> ')) == 't' else payment()
    report('Downloaded cart content')



cart = []
def main():
    report('Opened new instance of simulator')
    loadScene('Nowotarskie Linie Autobusowe')

    print(Fore.WHITE + 'Witaj w biletomacie! \nWybierz rodzaj biletu:')
    print(Fore.WHITE + '1 - bilety jednorazowe\n2 - bilety wielorazowe\n3 - bilety miesięczne')
    try:
        ticketkind = int(input('>> '))
    except ValueError:
        print(Fore.RED + 'Wprowadź właściwe dane!')
        time.sleep(5)
        main()
    report(f'Got input from user: type = {ticketkind}')
    if ticketkind == 2:
        loadScene('Ilość przejazdów')

        try:
            ticketRides = int(input('Ile przejazdów chcesz wykonać korzystając z tego biletu? >> '))
        except ValueError:
            print(Fore.RED + 'Wprowadź właściwe dane!')
            time.sleep(5)
            main()
        report(f'Got input from user: rides = {ticketRides}')
    loadScene('Ulgi')

    print(Fore.WHITE + 'Wybierz rodzaj ulgi:')
    print('0 - brak ulgi')
    print('1 - ulga 37% dla nauczycieli i seniorów 60+')
    print('2 - ulga 50% dla uczniów i studentów')
    print('3 - ulga 63% dla osób niepełnosprawnych i funkcjonariuszy bezpieczeństwa')
    try:
        ticketDiscount = int(input('>> '))
    except ValueError:
        print(Fore.RED + 'Wprowadź właściwe dane!')
        time.sleep(5)
        main()
    report(f'Got input from user: discount = {ticketDiscount}')
    loadScene('Ilość')

    print(Fore.WHITE + 'Ile biletów dodać do koszyka?')
    try:
        ticketAmount = int(input('>> '))
    except ValueError:
        print(Fore.RED + 'Wprowadź właściwe dane!')
        time.sleep(5)
        main()
    report(f'Got input from user: amount = {ticketAmount}')
    loadScene('Przypisywanie danych')
    
    if ticketkind == 1:
        kind = 'jednorazowy'
        ticketRides = 1
    elif ticketkind == 2:
        kind = 'wielorazowy'
    else:
        kind = 'miesięczny'
        ticketRides = -1
    if ticketDiscount == 0:
        discount = 0.0
    elif ticketDiscount == 1:
        discount = 0.37
    elif ticketDiscount == 2:
        discount = 0.5
    else:
        discount = 0.63
    rides = ticketRides
    amount = ticketAmount
    price = 0
    report('Saved data from user')
    loadScene('Generowanie biletu')
    bilet = Ticket(kind, rides, discount, amount)
    report(f'Created new object of Ticket class: {bilet}')
    loadScene('Wygenerowano bilet')
    #bilet.kind, bilet.rides, bilet.discount, bilet.price = kind, rides, discount, price
    report(f'Inserted data into ticket')
    loadScene('Dodawanie biletu do koszyka')
    cart.append(bilet)
    report('Added this ticket to the cart')
    loadScene('Kontynuacja')
    cmd = input(Fore.WHITE + 'Czy chcesz kupić kolejny bilet? [t/n]>> ')
    if cmd == 't':
        main()
        report('User intended to continue')
    else:
        report('User proceeded to cart')
        showCart()
    
main()

report('Code executed successfully')
report('')
 
    #Autor: Tymoteusz Szarlej
#Projekt powstał w ramach ćwiczeń projektowych
#Wszelkie prawa zastrzeżone

