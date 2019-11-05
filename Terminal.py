import numpy as np
import pandas as pd
import matplotlib
import math
import random
import statsmodels
import pandas_datareader
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
from colorama import Fore, Back, Style
import os.path
from os import path

#Global Variables
portfolio = []
if(path.exists("assets.txt")):
    f = open("assets.txt", "r")
    contents = f.read()
    portfolio = contents.split()
    f.close()


def normalized_returns(tickers):
    #tickers = input("Type tickers (format: 't1 t2 t3 t4 ... tn')").split()

    new_data = pd.DataFrame()  # defining new_data as dataframe object with pandas
    start_date = input("When is the start date? (yyyy-mm-dd) ")
    for t in tickers:
        new_data[t] = wb.DataReader(t, data_source='yahoo', start=start_date)['Adj Close']  # going through each ticker and
        # getting closing price info
        # with wb as datareader object

    ((new_data / new_data.iloc[0]) * 100).plot(figsize=(15, 6))  # plot normalized returns based on start date
    plt.show()

def asset_info(tickers):
    #information about the stock
    if tickers[0] == 'portfolio':
        tickers = portfolio
    for t in tickers:
        print("           " + Fore.BLUE + t + Fore.RESET)
        current_price = si.get_live_price(t)
        current_price = np.round(current_price, 2)
        print("Current Price: " + str(current_price) + "    ")




print(Fore.GREEN + "Welcome to the Untitled Terminal!" + Fore.RESET + Fore.YELLOW +"\nFor a list of commands, type 'help' !" + Fore.RESET)
while 1:
    print(Fore.MAGENTA + "Untitled Terminal> " + Fore.RESET, end="")
    line = input()
    line = line.split()
    firstQuery = line[0]
    if firstQuery == "nret":
        line.pop(0)
        normalized_returns(line)
    elif firstQuery == 'exit':
        break
    elif firstQuery == 'help':
        #print list of all possible commands

        print(Fore.YELLOW, end="")
        print("nret [ticker 1] [ticker 2] ... [ticker n]", end="")
        print(Fore.CYAN, end="")
        print(" -- displays line graph of the normalized returns of the listed assets from a specified start date", end="")
        print(Fore.RESET)

        print(Fore.YELLOW, end="")
        print("info [ticker 1] [ticker 2] ... [ticker n]", end="")
        print(Fore.CYAN, end="")
        print(" -- lists basic information of listed assets in the terminal output", end="")
        print(Fore.RESET)

        print(Fore.YELLOW, end="")
        print("exit", end="")
        print(Fore.CYAN, end="")
        print(" -- exits out of the terminal", end="")
        print(Fore.RESET)


    elif firstQuery == 'info':
        line.pop(0)
        asset_info(line)

    elif firstQuery == 'appendport':
        print("List the tickers to all assets you would like to add to the portfolio")
        print("(e.g. 'TSLA GM GE F WMT FIT')")
        new_line = input("If you would like to go back, type 'back'\n")
        new_line = new_line.split()
        if new_line[0] == 'back':
            continue
        if path.exists("assets.txt"):
            f = open("assets.txt", "a+")
        else:
            f = open("assets.txt", "w+")
        for t in new_line:
            if t in portfolio:
                print(t + " is already in your portfolio!")
                continue
            f.write(t + "\n")
            portfolio.append(t)
        f.close()

    elif firstQuery == 'delport':
        if not path.exists("assets.txt"):
            print("You have not created a portfolio. To do so, type 'appendport'.")
            continue
        delquery = input("Are you sure you want to delete your portfolio? This change cannot be undone.\n(y/n)\n")
        if delquery == 'y':
            os.remove("assets.txt")
            portfolio = []
            print("The porfolio was DELETED")
        else:
            print("The portfolio was NOT deleted")

    elif firstQuery == 'delasset':
        if len(line) == 1:
            print("Input format not recognized.")
            continue
        line.pop(0)
        if line[0] in portfolio:
            portfolio.remove(line[0])
            f = open("assets.txt", "w+")
            for t in portfolio:
                f.write(t + "\n")
        else:
            print("Asset " + Fore.YELLOW + line[0] + Fore.RESET + " not found in your portfolio")

    elif firstQuery == 'portfolio':
        for t in portfolio:
            print(t)


    else:
        print(Fore.RED + Style.BRIGHT + line[0] + Style.RESET_ALL + Fore.LIGHTRED_EX + " is not a recognized command." + Fore.RESET)









