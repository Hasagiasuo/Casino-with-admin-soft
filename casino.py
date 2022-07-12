import sqlite3
from time import sleep
from random import randint
from pyfiglet import Figlet
from getpass import getpass


#START
def start():
  connect_db()
  start = Figlet(font = 'slant')
  print(start.renderText('CASINO'))
  while True:
    qu = input('[*]Hi, what u wanna?\n[*]Log in or sign up?\n[l/s]\n')
    if qu == 'l':
      login()
      break
    elif qu == 's':
      create()
      break
    elif qu == 'a':
      admin()
      break
    else:
      print('[!]Please, using only [l/s]!\nTry again after 1 second!\n')
      sleep(1)

#DATA_BASE
def connect_db():
  global db, cur
  db = sqlite3.connect('game.db')
  cur = db.cursor()

  #CREATE TABLE
  cur.execute("""
    CREATE TABLE IF NOT EXISTS menu(
      login TEXT,
      password TEXT,
      cash INT
    ) 
  """)
  db.commit()

#LOGIN
def login():
  bbb = 0
  login = input('[*]Enter login!\n')
  while bbb != 10:
      password = getpass(f'[*]{login} enter u`r password!\n')
      user_password = cur.execute(f"SELECT password FROM menu WHERE login = '{login}'")
      for pasw in user_password:
        pasw
      if password == pasw[0]:
        user_choice(login)
        break
      elif password != pasw[0]:
          bbb += 1
          print(f'[!] Uncorrect password! Try again after 2 second!\n[*]{bbb} for 4!\n')
          if password == pasw[0]:
            user_choice(login)
            break
          elif bbb == 4:
            print('[!]Try later!')
            break
          sleep(1)

#users
def users_info(login):
  info = cur.execute(f"SELECT login, password, cash FROM menu WHERE login = '{login}'")
  for log, passw, cash in info:
    print(f'[!]U`r login: {log}\n[!]U`r password: {passw}\n[!]U`r cash: {cash}\n')
  sleep(3)
  question = input('[*]What will do?\n--1)Play casino [c];\n--2)Edit password [e];\n--3)Exit [x]\n')
  if question == 'c':
    game(login)
  elif question == 'e':
    ed_pasw(login)
  elif question == 'x':
    exit()

def ed_pasw(login):
  a = 8
  for i in range(3):
    i += 1
    password1 = getpass('[*]Enter new password: ')
    if len(password1) >= a:
      print('[+]')
      break
    elif len(password1) <= a:
      print(f'[!]Password should have 8 symbol and more!\n[!]{i} tryes for 3\n')
  password = getpass('[*]Enter new password again: ')
  if password1 == password:
    cur.execute(f"UPDATE menu SET password = '{password}' WHERE login = '{login}'")
    db.commit()
    print('[!]Good, u`r password edit!')
    user_choice(login)
  elif password1 != password:
    for tryes in range(3):
      tryes += 1
      password = getpass('[*]Try again: ')
      if password1 == password:
        cur.execute(f"UPDATE menu SET password = '{password}' WHERE login = '{login}'")
        db.commit()
        print('[!]Good, u`r password edit!\n')
        user_choice(login)
        break
      elif password1 != password:
        print(F'[!]Uncorrect! Try again!\n[*]{tryes} for 3!')
    if password1 != password:
      print('[!]Try later!')
      exit()

def user_choice(login):
  for tryes in range(3):
    tryes += 1
    q = input(f'[*]{login} u`r connected!\nWhat u wanna?\n--1)To play into casino [c]!\n--2)Cheak u`r details [d]!\n--3)Edit password [e]!\n--4)Quit [q]\n')
    if q == 'c':
      game(login)
      break
    elif q == 'd':
      users_info(login)
      break
    elif q == 'e':
      ed_pasw(login)
      break
    elif q == 'q':
      exit()
      break
    else:
      input(f'[*]Please, using only [c/d/e/q]!\n[*]{tryes} for 3! Try after 2 second!')
      sleep(2)

#GAME
def game(login):
  print(f'[!]Hey, {login}, welcome into game!\n')
  ques = input('[*]U realy wanna play?\n-[!]For 1 game pay 100, but can win 200\n[y/n]\n')
  if ques == 'y':
    while True:
      cash_user = cur.execute(f'SELECT cash FROM menu WHERE login = "{login}"')
      for cashs in cash_user:
        cashs = cashs[0]
      if cashs == 0:
        print('[!]Sorry, u haven`t money!')
        exit()
        break
      cur.execute(f"UPDATE menu SET cash = {cashs - 100} WHERE login = '{login}'")
      db.commit()
      casino = randint(1, 2)
      if casino == 1:
        cur.execute(f'UPDATE menu SET cash = {cashs + 100} WHERE login = "{login}"')
        db.commit()
        all_cash = cur.execute(f'SELECT cash FROM menu WHERE login = "{login}"')
        for cassh in all_cash:
          cassh = cassh[0]
        print(f'[!]U win!!!\n-U`r balance = {cassh}')
        sleep(3)
        print('[!]Right now cash been reg at u`r account!\n[!]')
        print('[!]If u wanna go seting enter [s]!\n')
      else:
        all_cash = cur.execute(f'SELECT cash FROM menu WHERE login = "{login}"')
        for cassh in all_cash:
          cassh = cassh[0]
        print(f'[!]Sry, u lose(((\n[!]U`r balance = {cassh}')
        sleep(3)
        print('[!]If u wanna go seting enter [s]!\n')
      accept = input('[!]U wanna play again?\n[y/n]\n')
      if accept == 'n':
        user_choice(login)
        break
  elif ques == 'n':
    user_choice(login)
  else:
    print(f'[!]{login} try again!')
    sleep(2)

#CREATE NEW USERS
def create():
  a = 8
  b = 4
  for t in range(3):
    t += 1
    login = input('[*]Enter new login:\n')
    if len(login) >= b:
      print('[+]')
      break
    elif len(login) <= b:
      print(f'[!]Login should be 4 symbol and more!\n[!]{t} tryes for 3\n')
  for i in range(3):
    i += 1
    password = getpass('[*]Enter new password:\n')
    if len(password) >= a:
      print('[+]')
      break
    elif len(password) <= a:
      print(f'[!]Password should have 8 symbol and more!\n[!]{i} tryes for 3\n')
  cash = 300
  cur.execute(f"INSERT INTO menu VALUES (?, ?, ?)", (login, password, cash))
  db.commit()
  print('[!]U succesful sign up!\n[!]U start with 300 into balance for good time!\n')
  user_choice(login)

#ADMIN
def admin():
  print('[!]Be responsible!')
  sleep(2)
  tr = 0
  a = 0
  while True:
    question = input('[*]What u want see?\n--[!]Ifno for all users - [u]\n--[!]Cash ones user - [c]\n--[!]Delete user - [d]\n--[!]Exit - [e]\n[u/c/d/e]\n')
    if question == 'u':
      all_users = cur.execute(f'SELECT login, password FROM menu')
      for l, p in all_users:
        a += 1
        print(f'{a}. login = {l}; password = {p} |||')
        sleep(1)
      admin()
      break
    elif question == 'd':
      all_user = cur.execute('SELECT login FROM menu')
      for i in all_user:
        print(f'---{i[0]}')
      delete = input('[!]Enter login, who wanna delete:\n')
      cur.execute(f'DELETE FROM menu WHERE login = "{delete}"')
      db.commit()
      print('[!]User been deleted!\n')
      admin()
      break
    elif question == 'e':
      exit()
      break
    elif question == 'c':
      all_user = cur.execute('SELECT login FROM menu')
      for i in all_user:
        print(f'---{i[0]}')
      c_user = input('Who`s cash wanna look?\n')
      all_cash = cur.execute(f'SELECT cash FROM menu WHERE login = "{c_user}"')
      for c in all_cash:
        print(f'--Cash {c_user} = {c[0]}')
      admin()
      break
    else:
      tr += 1
      if tr == 5:
        break
      else:
        if tr == 4:
          print('[!]U have last try!')
          sleep(1)
        print('[!]Please using only [u/c/d/e]!\n[*]Try again after 2 second!\n')
        sleep(2)
    

#EXIT
def exit():
  print('[!]GOODBYE[!]')
  bbb = 10

#MAIN
def main():
  try:
    start()
  except KeyboardInterrupt:
    print('\n[!]BEEN ERROR[!]')


if __name__ == '__main__':
  main()