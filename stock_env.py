# -*- coding: utf-8 -*-
from datetime import date
import numpy as np
import csv
import requests
import random
import os.path
import pickle
import math
import tensorflow as tf
download_path = '../pickle'
import matplotlib.pyplot as plt


class Stock:

    VALID_ACTIONS = [0, 1, -1]

    def __init__(self):
        self.profit = 0
        self.count = 0
        self.bought = False
        self.my_list = None
        self.boughtStock = None
        self.boughtPrice = None

        # uncle_bob = db.Person.create(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
        # uncle_bob.save()
        #
        #
        # uncle_bob.update(name = "test")
        # query = db.Person.select(db.Person.name == 'Bob')
        #
        # for user in query:
        #   test =  user.name
        #
        # pass
        self.spec = type('',(object,),{'id':"Stock" })()
        with open('symbols.csv') as csvfile:
            self.symbols = list(csv.reader(csvfile))

    def getState(self):
        x = self.getX()
        index2 = int(x < 0)
        x = abs(x)

        margin = self.getX(margin=True)
        index3 = int(margin < 0)
        margin = abs(margin)


        result = math.pow(x, float(1)/3)
        if result >= 10:
            result = 10
        max = 399
        steps = float(10) / max

        result = round(result / steps)



        if margin >=50:
            margin = 50
        marginsteps = float(50) / max
        marginresult = round(margin/marginsteps)



        environment = np.zeros(shape=(2, 2, 2, 2, 400), dtype=np.uint8)
        environment[int(self.bought),index2 ,index3 , 0, result] = 1
        environment[int(self.bought), index2, index3, 1, marginresult] = 1
        reshape = np.reshape(environment, [80,80])

       # plt.imshow(reshape)
       # plt.show()

        return environment


    def getQuotes(self):
        statuscode = None
        my_list =None
        while statuscode != 200 or (not my_list or (len(my_list) < 2000 or  my_list[0][1] == my_list[1][1])):
            symbol = random.choice(self.symbols)[0]
            download_file = download_path + "/" + symbol + ".pickle"
            if  os.path.exists(download_file) and os.path.getsize(download_file) > 0:
                with open(download_file, 'rb') as f:
                    my_list = pickle.load(f)
                    statuscode = 200
            else:
                CSV_URL = "http://chart.finance.yahoo.com/table.csv?s=" + symbol + "&a=10&b=13&c=1800&d=10&e=13&f=2016&g=d&ignore=.csv"
                with requests.Session() as s:
                    download = s.get(CSV_URL)
                    statuscode = download.status_code
                    decoded_content = download.content.decode('utf-8')
                    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                    next(cr, None)
                    my_list = list(cr)
                    with open(download_file, 'wb') as f:
                        my_list = pickle.dump(my_list,f)
        return my_list



    def step(self, action, profit = False):
        reward = 0.0
        done = False
        state = self.my_list[self.index]
        close = state[6]

        #Stock is not profitable, so exit
        if not self.bought and action == -1:
            done = True

        #Sell Stock
        if self.bought and action == 1:
            done = True
            reward = ((((float(close) / (float(self.boughtStock) + 0.01))) * self.boughtPrice) - self.boughtPrice) * 100
            if profit:
                self.profit += reward
                self.count += 1
                print("Profit:", self.profit/self.count)
        #Buy Stock
        if not self.bought and action == 1:
            self.boughtStock = float(close)
            self.bought = True
            self.boughtPrice = 1

        if self.index >= 1:
            self.index -= 1
        else:
            self.index = 0
            done = True


        next_state =  self.getState()

        _ = None



        return [next_state, reward, done, _]




    def getX(self, margin = False):
        state = self.my_list[self.index]
        open = state[1]
        close = state[6]


        if self.bought and not margin:

                x = ((float(close) / (float(self.boughtStock) + 0.01)) * 100) - 100

        else:
            x = ((float(close) / (float(open) + 0.01)) * 100) - 100


        return x


    def reset(self):


        self.bought = False
        self.boughtPrice = None
        self.boughtStock = None
        self.my_list = self.getQuotes()
        self.index = random.choice(range(len(self.my_list)))
        environment = self.getState()


        return environment
