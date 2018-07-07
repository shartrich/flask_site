from tkinter import *
import pymysql
import urllib.request
import urllib
import time
import re
import random
from tkinter import messagebox
import csv
import datetime



class GUI:
    def __init__(self):
        
        self.tup = urllib.request.urlretrieve('http://ev9.evenue.net/evenue/linkID=gatech/images/groupMenu/default.gif', 'GTLogo.gif')
        self.win = Tk()
        self.resList = []
        self.cards = []
        self.openDB()
        cur = self.DB.cursor()
        sql = "select * from SystemInfo"
        cur.execute(sql)
        s = cur.fetchone()
        self.systemInfo = [s[0], s[1], float(s[2]), s[3]]
        cur.close()
        self.DB.close()
     
        self.createLog()
    
    def createLog(self):
        self.win.wm_title("GT Trains")
        self.logFrame = Frame(self.win)
        

        self.logT = Frame(self.logFrame, bg = "Navy")
        self.logB = Frame(self.logFrame)

        b1 = Button(self.logB, text="Cancel", width = 15, command = self.cancel)
        b1.grid(row = 1, column = 1)
        b2 = Button(self.logB, text="Login", width = 15, command = self.login)
        b2.grid(row = 1, column = 2)
        b2 = Button(self.logB, text="Register", width = 15, command = self.register)
        b2.grid(row = 1, column = 3)

        self.pic = PhotoImage(file = 'GTLogo.gif')
        imageLabel = Label(self.logT, image = self.pic)
        imageLabel.grid(row = 1, column = 2, rowspan = 6)
        l1 = Label(self.logT, text = "Username: ", width = 10, bg = 'Yellow')
        l1.grid(row = 7, column = 1, sticky = W)
        l2 = Label(self.logT, text = "Password: ", width = 10, bg = 'Yellow')
        l2.grid(row = 8, column = 1, sticky = W)

        self.s1 = StringVar()
        self.s2 = StringVar()
        
        self.e1 = Entry(self.logT, textvariable = self.s1, width = 30)
        self.e1.grid(row = 7, column = 2, sticky = W)
        self.e2 = Entry(self.logT, textvariable = self.s2, width = 30)
        self.e2.grid(row = 8, column = 2, sticky = W)
        
        self.logB.grid(column = 1, row = 2, sticky = S)
        self.logT.grid(column = 1, row = 1)
        #self.logSave = self.logFrame
        self.logFrame.pack()

    def createReg(self):
        self.win.wm_title("GT Trains Registration")
        self.regFrame = Frame(self.win)
        self.regT = Frame(self.regFrame, bg = "Orange")
        self.regB = Frame(self.regFrame)

        b4 = Button(self.regB, text="Cancel", width = 25, command = self.back)
        b4.grid(row = 1, column = 1)
        b5 = Button(self.regB, text="Register", width = 25, command = self.registerNew)
        b5.grid(row = 1, column = 2)

        self.pic = PhotoImage(file = 'GTLogo.gif')
        imageLabel = Label(self.regT, image = self.pic)
        imageLabel.grid(row = 1, column = 1, rowspan = 4)
        l3 = Label(self.regT, text = "Email Address: " , width = 10, bg = 'Yellow', padx = 5, pady = 5)
        l3.grid(row = 1, column = 2, sticky = E)
        l4 = Label(self.regT, text = "Username:" , width = 10, bg = 'Yellow', padx = 5, pady = 5)
        l4.grid(row = 2, column = 2, sticky = E)

        l5 = Label(self.regT, text = "Password: ", width = 10, bg = 'Yellow', padx = 5, pady = 5)
        l5.grid(row = 3, column = 2, sticky = E)
        l6 = Label(self.regT, text = "Confirm Password: ", width = 15, bg = 'Yellow', padx = 5, pady = 5)
        l6.grid(row = 4, column = 2, sticky = E)

        self.s3 = StringVar()
        self.s4 = StringVar()
        self.s5 = StringVar()
        self.s6 = StringVar()
        self.e3 = Entry(self.regT, textvariable = self.s3, width = 30)
        self.e4 = Entry(self.regT, textvariable = self.s4, width = 30)
        self.e5 = Entry(self.regT, textvariable = self.s5, width = 30)
        self.e6 = Entry(self.regT, textvariable = self.s6, width = 30)
        self.e3.grid(row = 1, column = 3)
        self.e4.grid(row = 2, column = 3)
        self.e5.grid(row = 3, column = 3)
        self.e6.grid(row = 4, column = 3)

        self.regB.grid(column = 1, row = 2, sticky = S+E)
        self.regT.grid(column = 1, row = 1)
        self.regFrame.pack()

    def registerNew(self):
        if self.s5.get() == self.s6.get() and self.s4.get() != '' and self.s5.get() != '' and self.s3.get() != '':
            
            self.checkForPerson()
            
            

        elif self.s3.get() == '':
            messagebox.showwarning(title="Error", message="You must enter a valid email address")
        elif self.s4.get() == '':
            messagebox.showwarning(title="Error", message="You must enter a username")
        elif self.s5.get() == '':
            messagebox.showwarning(title="Error", message="You must enter a password")
        elif self.s5.get() != self.s6.get():
            messagebox.showwarning(title="Error", message="Your passwords do not match")
            
    def checkForPerson(self):
        
        self.openDB()
        cur = self.DB.cursor()
        
        
        sql = """SELECT * FROM User
                 WHERE Username LIKE %s"""

       
        opt = cur.execute(sql, (self.s4.get(),))
        if opt == 0:
            cur.close()
            self.regNewUser()
        else:
            cur.close()
            self.DB.close()
            messagebox.showwarning(title="Error", message="That username is already in use. Try another")

    def regNewUser(self):
        cur = self.DB.cursor()
        cur1 = self.DB.cursor()
        sql = """INSERT INTO cs4400_Team_6.User (Username, Password)
                 VALUES (%s, %s)"""
        sql2 = "Insert Into cs4400_Team_6.Customer (Username, Email, isStudent) VALUES (%s, %s, 0)"
        
        cur.execute(sql, (self.s4.get(),self.s5.get()))
        cur1.execute(sql2, (self.s4.get(), self.s3.get()))
        cur1.close()
        cur.close()
        self.DB.commit()
        self.back()
        messagebox.showinfo(message = "Registration Successful!")
        #self.back()
        
    def cancel(self):
        self.win.destroy()
        
    def back(self):
        self.regFrame.destroy()
        self.createLog()
        
    def openDB(self):
        self.DB = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306, user='cs4400_Team_6', passwd='FA7g46jg', db='cs4400_Team_6')
        
        
    def closeDB(self):
        self.DB.close()

    def loadLog(self):
        self.regFrame.destroy()
        self.createLog()
        
    def login(self):
        self.openDB()
        cur = self.DB.cursor()
        sql = """SELECT * FROM cs4400_Team_6.User WHERE Username LIKE %s"""
        num = cur.execute(sql, (self.s1.get()))
        if num == 0:
             messagebox.showwarning(title="Error", message="Password is incorrect for that username")
             cur.close()
             self.DB.close()
        else:
            match = cur.fetchone()
            if self.s2.get().lower() == match[1].lower() and self.s1.get().lower() == match[0].lower():
                cur.close()
                
                self.liveUser = match
                messagebox.showinfo(message = "Login Successful!")
                self.curUser = self.s1.get()
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                man="SELECT Username FROM Management"
                cust="SELECT Username FROM Customer"
                
                cur=self.DB.cursor()
                cur1=self.DB.cursor()
                man2=cur.execute(man)
                cust2=cur1.execute(cust)
                manList=[]
                for i in cur:
                        j=list(i)
                        manList.append(j)
                manList2=sum(manList,[])
                custList=[]
                for i in cur1:
                        j=list(i)
                        custList.append(j)
                custList2=sum(custList,[])
                manFinal=[]
                custFinal=[]
                for i in manList2:
                        j=i.lower()
                        manFinal.append(j)
                for i in custList2:
                        j=i.lower()
                        custFinal.append(j)
                cur.close()
                cur1.close()
                self.DB.close()
                if self.curUser.lower() in manFinal:                        
                        self.toMan()
                elif self.curUser.lower() in custFinal:
                        self.toCustFu()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            else:
                #self.s1.get() == match[0] and self.s2.get() != match[1]:
                messagebox.showwarning(title="Error", message="Password does not match the username")
                cur.close()
                self.DB.close()

            
    def toMan(self):
        try:
            self.logFrame.destroy()
        except:
            pass
        self.custFunctionalities1()
    def register(self):
        self.logFrame.destroy()
        self.createReg()

    def travelExtras(self):
        #print(123)
        self.tExF = Frame(self.win)
        f1 = Frame(self.tExF)
        f2 = Frame(self.tExF)
        f3 = Frame(self.tExF)

        l3 = Label(f1, text = "Travel Extras & Passenger Info" , fg = 'Gold', font="helvetica 25 bold")
        l3.grid(sticky = E+W+S+N)
        

        l4 = Label(f2, text = "Number of Baggage: ", font="helvetica 10 bold")
        l4.grid(column = 1, row = 1)
        self.bagC = StringVar()
        trio = tuple(range(0, self.systemInfo[0]+1))
        opt_menu = OptionMenu(f2, self.bagC, *trio)
        opt_menu.grid(row = 1, column = 2)
        
        l3 = Label(f2, text = "Every passenger can bring up to {} baggage. {} free of charge, {} for $30 per bag".format(self.systemInfo[0], self.systemInfo[1], self.systemInfo[0]-self.systemInfo[1]))
        l3.grid(row = 2, column = 1, columnspan = 2)

        l4 = Label(f2, text = "Passenger Name:", font="helvetica 10 bold")
        l4.grid(column = 1, row = 3)
        self.pName = StringVar()
        pNameEntry = Entry(f2, textvariable = self.pName)
        pNameEntry.grid(row = 3, column = 2,sticky = W)

        b4 = Button(f3, text="Back", width = 25, command = self.backTE)
        b4.grid(row = 1, column = 1)
        b5 = Button(f3, text="Next", width = 25, command = self.travelExNext)
        b5.grid(row = 1, column = 2)     

        f1.grid(row = 1)
        f2.grid(row = 3, sticky = E+W)
        f3.grid(row = 5)
        self.tExF.pack()

    def travelExNext(self):
        if self.bagC.get() != '' and self.pName.get() != '':
            self.curRes['Bags'] = int(self.bagC.get())
            self.curRes['Passenger'] = self.pName.get()
            self.resList.append(self.curRes)
            self.tExF.destroy()
            self.makeRes()
        else:
            messagebox.showwarning(title="Oops", message="You must select a number of bags and give a name")

    def MRtoST(self):
        self.resWin.destroy()
        self.SearchTrains()
    def makeRes(self):
        
        self.resWin = Frame(self.win)
        f1 = Frame(self.resWin)
        f2 = Frame(self.resWin)
        f3 = Frame(self.resWin)
        f4 = Frame(self.resWin)
        f5 = Frame(self.resWin)

        l1 = Label(f1, text = "Make Reservation" , fg = 'Gold', font="helvetica 25 bold")
        l1.grid(sticky = E+W+S+N)

        l2 = Label(f2, text = "Currently Selected", font="helvetica 10 bold")
        l2.grid(column = 1, row = 2)

        l3 = Label(f3, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l3.grid(column = 3, row = 1)
        l4 = Label(f3, text = "Time (Duration)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l4.grid(column = 4, row = 1)
        l5 = Label(f3, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l5.grid(column = 5, row = 1)
        l6 = Label(f3, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l6.grid(column = 6, row = 1)
        l7 = Label(f3, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l7.grid(column = 7, row = 1)
        l8 = Label(f3, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l8.grid(column = 8, row = 1)
        l9 = Label(f3, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l9.grid(column = 9, row = 1)
        l10 = Label(f3, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l10.grid(column = 10, row = 1)
        l11 = Label(f3, text = "Remove",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
        l11.grid(column = 11, row = 1)
        self.dates = []
        bTotPrice = 0
        priceSum = 0
        i = 2
        for trip in self.resList:
            Label(f3, text = trip['Train']).grid(row = i, column = 3)
            Label(f3, text = trip['Date']+" : "+trip['Time']).grid(row = i, column = 4)
            Label(f3, text = trip['From']).grid(row = i, column = 5)
            Label(f3, text = trip['Arrives']).grid(row = i, column = 6)
            Label(f3, text = trip['Class']).grid(row = i, column = 7)
            Label(f3, text = trip['Price']).grid(row = i, column = 8)
            Label(f3, text = trip['Bags']).grid(row = i, column = 9)
            Label(f3, text = trip['Passenger']).grid(row = i, column = 10)
            self.dates.append(trip['Date'])
            Button(f3, text = "Remove", command=(lambda: self.remItem(trip))).grid(row = i, column = 11)

            bPrice = 0
            if trip['Bags']>self.systemInfo[1]:
                bPrice = 30*(trip['Bags']-self.systemInfo[1])
            priceSum = priceSum+trip['Price']+bPrice
            i = i+1

        self.openDB()
        sql = "select CardNumber,NameOnCard,ExpirationDate,CVV from cs4400_Team_6.PaymentInformation where CustomerUsername like %s;"
        cur1 = self.DB.cursor()
        cur1.execute(sql, (self.curUser))
        self.PInfo = cur1
        cur1.close()
        cur2 = self.DB.cursor()
        sql2 = "select IsStudent from cs4400_Team_6.Customer where username like %s"
        cur2.execute(sql2, (self.curUser))
        isStudent = cur2
        cur2.close()
        self.DB.close()
        l4list = []
        for card in self.PInfo:
                self.cards.append(card[0])
                l4list.append(str(card[0])[-4:])


            
        if isStudent == 1:
            self.Tprice = priceSum*(1-self.systemInfo[2])
            Label(f4, text = 'Student Discount Applied').grid(row = 12, column = 1)
        else:
            self.Tprice = priceSum
        self.tup = tuple(l4list)
        Label(f4, text = 'Total Cost: ').grid(row = 13, column = 1, sticky=W)
        Label(f4, text = self.Tprice).grid(row = 13, column = 2, columnspan = 2)
        Label(f4, text = 'Use Card: ').grid(row = 14, column = 1, sticky=W)
        self.cardOpt = StringVar()
        #self.cardOpt.set(tup)
        C = self.cards
        try:
            menu = OptionMenu(f4, self.cardOpt, *self.tup)#need reference for self card info variables
            menu.grid(row = 14, column = 2, sticky = W)
        except:
            pass
        bCard = Button(f4, text = 'Add Card', fg ='blue', command = self.payment)
        bCard.grid(row = 14, column = 3, sticky = W)

        bCont = Button(f4, text = 'Continue Adding Another Train', fg ='blue', command = self.MRtoST)
        bCont.grid(row = 15, column = 1, sticky = W)

        B1 = Button(f5, text = 'Back', command = self.makeResBack)
        B1. grid(row = 1, column = 1)
        B2 = Button(f5, text = 'Submit', command = self.makeResSub)
        B2. grid(row = 1, column = 2)
        
        f1.grid(row = 1, sticky = N+S+E+W)
        f2.grid(row = 2, sticky = W)
        f3.grid(row = 3, sticky = N+S+E+W)
        f4.grid(row = 4, sticky = W)
        f5.grid(row = 5)
        
        self.resWin.pack()

    def remItem(self, rem):
        self.resList.remove(rem)
        self.resWin.destroy()
        self.makeRes()
        

    def makeResBack(self):
        del self.resList[len(self.resList)-1]
        self.resWin.destroy()
        self.travelExtras()
    def makeResSub(self):
        if self.cardOpt.get() != '':
            for c in self.cards:
                if str(c)[-4:] == self.cardOpt.get():
                    resCard = c
            sql = "insert into Reservation (StartDate, EndDate, IsCancelled, CustomerUsername, CardNumber, TotalCost) values(%s, %s, 0, %s, %s, %s);"
            self.openDB()
            cur = self.DB.cursor()
            cur.execute(sql, (min(self.dates), max(self.dates), self.curUser, resCard, self.Tprice))
            cur.close()
            cur1 = self.DB.cursor()
            sql2="SELECT max(ReservationID) FROM Reservation WHERE customerUsername=%s;"
            cur1.execute(sql2, (self.curUser))
            self.lastID = cur1.fetchone()[0]
            cur1.close()
            tripSQL = """insert into Reserves(ReservationID, TrainNumber, DepartDate, PassengerName, NumberofBaggage, DepartsFrom, Class, ArrivesAt) Values
            (%s, %s, %s, %s, %s, %s, %s, %s)"""
            for trip in self.resList:
                cur2 = self.DB.cursor()
                cur2.execute(tripSQL, (self.lastID, trip['Train'], trip['Date'], trip['Passenger'], trip['Bags'], trip['From'], trip['Class'], trip['Arrives']))
                cur2.close()
            self.DB.commit()
            self.DB.close()
            self.resWin.destroy()
            self.confirmPage()
        else:
            messagebox.showwarning(title="Oops", message="You must select a valid card")
            
        
    def payment(self):
        self.resWin.destroy()
        self.payInfo()
        
    def payInfo(self):
        
        self.payWin = Frame(self.win)
        f1 = Frame(self.payWin)
        f2 = Frame(self.payWin)
        f3 = Frame(self.payWin)
        l1 = Label(f1, text = "Payment Information" , fg = 'Gold', font="helvetica 25 bold")
        l1.grid(sticky = N+S+E+W)

        l2 = Label(f2, text = "Add Card", font="helvetica 16 bold")
        l2.grid(row = 1, column = 1)
        
        l3 = Label(f2, text = "Name on Card: ")
        l3.grid(row = 2, column = 1)
        l4 = Label(f2, text = "Card Number: ")
        l4.grid(row = 3, column = 1)

        l5 = Label(f2, text = "CVV: ", width = 10)
        l5.grid(row = 4, column = 1, sticky = E)
        l6 = Label(f2, text = "Expiration Date: ")
        l6.grid(row = 5, column = 1, sticky = E)
        
        self.cardName = StringVar()
        self.cardNum = StringVar()
        self.CVV = StringVar()
        self.expDate = StringVar()
        e3 = Entry(f2, textvariable = self.cardName)
        e4 = Entry(f2, textvariable = self.cardNum)
        e5 = Entry(f2, textvariable = self.CVV)
        e6 = Entry(f2, textvariable = self.expDate)
        e3.grid(row = 2, column = 2)
        e4.grid(row = 3, column = 2)
        e5.grid(row = 4, column = 2)
        e6.grid(row = 5, column = 2)
        addSub = Button(f2, text = 'Add Card', command = self.addCard)
        addSub.grid(row = 6, column = 1)


        l7 = Label(f3, text = "Delete Card", font="helvetica 16 bold")
        l7.grid(row = 1 , column = 1, columnspan = 2)

        l8 = Label(f3, text = 'Card Number: ')
        l8.grid(row = 2, column = 1)
        
        
        self.delCardOpt = StringVar()
        C = self.cards
        try:
            menu = OptionMenu(f3, self.delCardOpt, *self.tup)
            menu.grid(row = 2, column = 2)
            delSub = Button(f3, text = 'Delete Card', command = self.delCard)
            delSub.grid(row = 6, column = 1)
        except:
            pass
        f1.grid(row = 1, column = 1, columnspan = 2)
        f2.grid(row = 2, column = 1)
        f3.grid(row = 2, column = 2)
        self.payWin.grid()
        

    def addCard(self):
        curDate = time.strftime("%m/%Y")
        if re.match('(\d{2}[/]\d{4})', self.expDate.get()) == None:
            messagebox.showwarning(title="Invalid Expiration", message="Expiration date must be in format MM/YYYY")
        elif int(curDate[-4:]) > int(self.expDate.get()[-4:]):
            messagebox.showwarning(title="Invalid Expiration Date", message="Card is expired.")            
        elif int(curDate[-4:]) == int(self.expDate.get()[-4:]) and int(self.expDate.get()[0:2])<int(curDate[0:2]):
            messagebox.showwarning(title="Invalid Expiration Date", message="Card is expired.")
        elif len(self.CVV.get()) > 4 or len(self.CVV.get()) < 3:
            messagebox.showwarning(title="Invalid CVV", message="CVV is the 3 or 4 digit code on the back of your card")
        elif len(self.cardNum.get()) != 16:
            messagebox.showwarning(title="Invalid Card Number", message="Card Number can only be 16 digits")
        elif self.cardName.get() == '' or len(self.cardName.get()) > 50:
            messagebox.showwarning(title="Invalid Card Name", message="Invalid Name")
        else:
            sql = 'insert into cs4400_Team_6.PaymentInformation values(%s, %s, %s, %s, %s);'
            self.openDB()
            cur1 = self.DB.cursor()
            cur1.execute(sql, (int(self.cardNum.get()), self.cardName.get(), self.expDate.get(), int(self.CVV.get()), self.curUser))
            self.DB.commit()
            cur1.close()
            self.DB.close()
            self.payWin.destroy()
            self.makeRes()

    def delCard(self):
        if self.delCardOpt.get() != '':
            for c in self.cards:
                if str(c)[-4:] == self.delCardOpt.get():
                    delCard = c
            self.openDB()
            sql1 = "select CardNumber from Reservation where CardNumber = %s"
            curCheck = self.DB.cursor()
            
            curCheck.execute(sql1, (delCard))
            inUse = curCheck.fetchone()
            curCheck.close()
            if inUse == None:
                sql = 'delete from cs4400_Team_6.PaymentInformation where CardNumber = %s;'
                cur2 = self.DB.cursor()
                cur1 = self.DB.cursor()
                cur1.execute(sql, (delCard))
                self.DB.commit()
                cur1.close()
                self.payWin.destroy()
                self.makeRes()
            else:
                messagebox.showwarning(title="Error", message="You cannot delete a card already in use in an existing transaction.")
            #self.DB.close()
            
        else:
            messagebox.showwarning(title="Error", message="You must select a card to delete a card")


####################################################################################################
    def Connect(self):

                try:
                        data=pymysql.connect(host="academic-mysql.cc.gatech.edu", user="cs4400_Team_6", passwd="FA7g46jg", db="cs4400_Team_6")
                        return(data)
                except:
                        messagebox.showwarning(title="Error", message="Error. Please check your internet connection")

    def toCustFu(self):
        self.logFrame.destroy()
        self.custFunctionalities()
    def custFunctionalities(self):
                #self.root.withdraw()
                
                self.cfroot= Frame(self.win)
                self.win.wm_title("Choose Functionality")

                
                label1=Label(self.cfroot, text="Choose Functionality", fg="gold", font="helvetica 20 bold")
                button1=Button(self.cfroot, text="View Train Schedule",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", borderwidth=0, command=self.toViewTrainSchedule)
                button2=Button(self.cfroot, text="Make A New Reservation",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command=self.toSearchTrains)
                button3=Button(self.cfroot, text="Update A Reservation",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command = self.updateReservation)
                button4=Button(self.cfroot, text="Cancel A Reservation",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command = self.cancelARes1)
                button5=Button(self.cfroot, text="Give a Review",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command = self.giveReviewGUI)
                button6=Button(self.cfroot, text="View a Review",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command = self.viewReviewGUI)
                button7=Button(self.cfroot, text="Add School Information (Student Discount)",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command=self.toAddSchoolInfo)
                logout=Button(self.cfroot, text="Log Out", command = self.logout)

                label1.pack()
                button1.pack()
                button2.pack()
                button3.pack()
                button4.pack()
                button5.pack()
                button6.pack()
                button7.pack()
                logout.pack()
                self.cfroot.pack()
    def logout(self):
        try:
            self.cfroot.destroy()
        except:
            self.cfroot2.destroy()
        self.createLog()
    def toViewTrainSchedule(self):
        self.cfroot.destroy()
        self.viewTrainSchedule()        
    def toAddSchoolInfo(self):
        self.cfroot.destroy()
        self.addSchoolInfo()
    def toSearchTrains(self):
        self.cfroot.destroy()
        self.SearchTrains()
        
    def addSchoolInfo(self):
                
                self.siroot= Frame(self.win)
                self.win.wm_title("Add School Info")

                label1=Label(self.siroot, text="Add School Info",fg="gold", font="helvetica 25 bold")
                label2=Label(self.siroot, text="School Email Address", font="helvetica 20 bold")
                label3=Label(self.siroot, text= "Your School Email Address Ends with .edu",font="helvetica 15")
                button1=Button(self.siroot, text="Back", command=self.backAddSchoolInfo)
                button2=Button(self.siroot, text="Submit", command=self.checkAddSchoolInfo)
                self.entrySI=Entry(self.siroot)

                label1.grid(row=0, column=2, sticky=W)
                label2.grid(row=1, column=2, sticky=W)
                label3.grid(row=2, column=2,sticky=W)
                self.entrySI.grid(row=1, column=3, sticky=W)
                button1.grid(row=3, column=2)
                button2.grid(row=3, column=3)
                self.siroot.pack()

    def checkAddSchoolInfo(self):
                self.sInfo=self.entrySI.get()
                userN=self.curUser


                for i in range(len(self.sInfo)):
                        j=len(self.sInfo)-3
                        end=self.sInfo[j:j+3]

                if end=="edu":
                        sql="UPDATE Customer SET IsStudent=1 WHERE Username=%s"
                        self.openDB()
                        cursor=self.DB.cursor()
                        cursor.execute(sql,(userN))
                        self.DB.commit()
                        cursor.close()
                        self.DB.close()
                        messagebox.showerror("You have successfully entered your school information")

                else:
                        messagebox.showerror("Your student email needs to end in 'edu'")
                

    def backAddSchoolInfo(self):
                self.siroot.destroy()
                self.custFunctionalities()

    def viewTrainSchedule(self):
                
                self.vtroot=Frame(self.win)
                self.win.wm_title("View Train Schedule")

                label1=Label(self.vtroot, text="View Train Schedule", fg="gold", font="helvetica 25 bold")
                label2=Label(self.vtroot, text="Train Number", font="helvetica 15")
                self.entryT=Entry(self.vtroot)
                button1=Button(self.vtroot, text="Search", font="helvetica 15", command=self.viewTrainSchedule1)
                button2=Button(self.vtroot, text="Back", command=self.backViewTrain)
                
                label1.grid(row=0, column=1, sticky=E)
                label2.grid(row=1, column=0, sticky=W)
                self.entryT.grid(row=1, column=1, sticky=E)
                button1.grid(row=2, column=0)
                button2.grid(row=2, column=1)
                self.vtroot.pack()
                
    def toViewTrainSchedule1(self):
        self.vtroot.destroy()
        self.viewTrainSchedule1()
    def backViewTrain(self):
                self.vtroot.destroy()
                self.custFunctionalities()
                
    def viewSchedule(self):
                self.cfroot.withdraw()
                self.vtroot.decoinify()

    def viewTrainSchedule1(self):
                
                train=self.entryT.get()
                sql1="SELECT TrainNumber FROM Stop"
                self.openDB()
                cursor=self.DB.cursor()
                cursor.execute(sql1)
                trainNum=[]
                for i in cursor:
                        j=list(i)
                        trainNum.append(j)
                train1=train.lower()
                cursor.close()
                
                newTrain=sum(trainNum,[])
                finalTrain=[]
                for i in newTrain:
                        finalTrain.append(i.lower())
                if train1 in finalTrain:
                        sql="SELECT * FROM Stop WHERE TrainNumber=%s"
                        self.openDB()
                        cursor2=self.DB.cursor()
                        
                        cursor2.execute(sql,(train1))
                        self.vtroot.destroy()
                        self.vtroot1=Frame(self.win)
                        self.win.wm_title("View Train Schedule")

                        label1=Label(self.vtroot1, text="View Train Schedule", fg="gold", font="helvetica 25 bold")
                        label2=Label(self.vtroot1, text="Train (Train Number)", font="helvetica 15")
                        label3=Label(self.vtroot1, text="Arrival Time", font="helvetica 15")
                        label4=Label(self.vtroot1, text="Departure Time", font="helvetica 15")
                        label5=Label(self.vtroot1, text="Station", font="helvetica 15")

                        label1.grid(row=0, column=2)
                        label2.grid(row=1, column=0, padx=15)
                        label3.grid(row=1, column=1)
                        label4.grid(row=1, column=2)
                        label5.grid(row=1, column=3,padx=10)
                                
                        sList=[]                      
                        numList=[]
                        aTime=[]
                        dTime=[]

                        for i in cursor2:
                                sList.append(i[0])
                                numList.append(i[1])
                                aTime.append(i[2])
                                dTime.append(i[3])

                        for i in range(len(sList)):
                                sLabel=Label(self.vtroot1, text=sList[i])
                                sLabel.grid(row=i+2, column=3)
                        for i in range(len(aTime)):
                                aLabel=Label(self.vtroot1, text=aTime[i])
                                aLabel.grid(row=i+2, column=1)
                        for i in range(len(dTime)):
                                dLabel=Label(self.vtroot1, text=dTime[i])
                                dLabel.grid(row=i+2, column=2)

                        numLabel=Label(self.vtroot1, text=numList[1])
                        numLabel.grid(row=2, column=0)

                        bButton=Button(self.vtroot1, text="Back", command=self.viewTrainScheduleBack)
                        bButton.grid(row=len(sList)+2, column=3)
                        self.vtroot1.pack()
                        cursor2.close()
                        self.DB.close()
                else:
                        messagebox.showerror("Please enter a valid train number")
                        


    def viewTrainScheduleBack(self):
                self.vtroot1.destroy()
                self.viewTrainSchedule()
                
                                                                    
    def SearchTrains(self):
                self.curRes = {}
                self.sroot=Frame(self.win)
                self.win.wm_title("Search Trains")
                self.curRes = {}
                sql="SELECT Name FROM Stop"
                self.openDB()
                cursor=self.DB.cursor()
                cursor.execute(sql)
                station=[]
                for i in cursor:
                        j=list(i)
                        station.append(j)
                newStation=sum(station,[])
                uniqueStation=[]
                [uniqueStation.append(item) for item in newStation if item not in uniqueStation]
                newList=tuple(uniqueStation)
                cursor.close()
                self.DB.close()
                self.variable=StringVar(self.sroot)
                self.variable.set(uniqueStation[0]) #default value
                self.variable1=StringVar(self.sroot)
                self.variable1.set(uniqueStation[0]) #default value

                label1=Label(self.sroot, text="Search Train", fg="gold", font="helvetica 25 bold")
                label2=Label(self.sroot, text="Departs From", font="helvetica 15")
                label3=Label(self.sroot, text="Arrives At", font="helvetica 15")
                label4=Label(self.sroot, text="Departure Date", font="helvetica 15")
                label5=Label(self.sroot, text="Enter date in form YYYY-MM-DD", font="helvetica 10")
                button1=Button(self.sroot, text="Find Trains", command=self.toSelectDeparture)
                dropdown1=OptionMenu(self.sroot, self.variable, *newList)
                dropdown2=OptionMenu(self.sroot, self.variable1, *newList)
                self.ED = StringVar()
                self.entryD=Entry(self.sroot, textvariable = self.ED)               

                label1.grid(row=0, column=1, sticky=W)
                label2.grid(row=1, column=0, sticky=W)
                label3.grid(row=2, column=0, sticky=W)
                label4.grid(row=3, column=0, sticky=W)
                label5.grid(row=4, column=0)
                dropdown1.grid(row=1, column=1, sticky=E)
                dropdown2.grid(row=2, column=1, sticky=E)
                self.entryD.grid(row=3, column=1, sticky=E)
                button1.grid(row=4, column=1)
                self.sroot.pack()

    def toSelectDeparture(self):
        self.curRes['From'] = self.variable.get()
        self.curRes["Arrives"] = self.variable1.get()
        self.curRes["Date"] = self.ED.get()
        self.sroot.destroy()
        self.selectDeparture()
        
    def selectDeparture(self):
                if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", self.ED.get()) != None and self.variable.get() != self.variable1.get():
                        self.sdroot=Frame(self.win)
                        self.win.wm_title("Select Departure")
                        
                        label1=Label(self.sdroot, text="Select Departure", fg="gold", font="helvetica 25 bold")
                        label2=Label(self.sdroot, text="Train (Train Number)", font="helvetica 15")
                        label3=Label(self.sdroot, text="Time (Duration)", font="helvetica 15")
                        label4=Label(self.sdroot, text="1st Class Price", font="helvetica 15")
                        label5=Label(self.sdroot, text="2nd Class Price", font="helvetica 15")

                        label1.grid(row=0, column=2)
                        label2.grid(row=1, column=0, padx=15)
                        label3.grid(row=1, column=1)
                        label4.grid(row=1, column=2)
                        label5.grid(row=1, column=3,padx=10)

                        arrive=self.variable1.get()
                        depart=self.variable.get()
                        
                        info="SELECT A.TrainNumber, B.TrainNumber, A.ArrivalTime, B.DepartureTime FROM Stop A, Stop B WHERE A.Name=%s AND B.Name=%s AND A.TrainNumber=B.TrainNumber AND B.DepartureTime<A.ArrivalTime"
                        self.openDB()
                        cursor=self.DB.cursor()
                        cursor.execute(info,(arrive,depart))
                        numList=[]
                        arrList=[]
                        depList=[]
                        #self.sdroot.pack()

                        for i in cursor:
                                numList.append(i[0])
                                arrList.append(i[2])
                                depList.append(i[3])
                        priceList=[]
                        cursor.close()
                        self.DB.close()
                        for i in numList:
                                price="SELECT 1stClassPrice, 2ndClassPrice FROM TrainRoute WHERE TrainNumber=%s"
                                self.openDB()
                                curs=self.DB.cursor()
                                curs.execute(price,(i))
                                self.DB.close()
                                for j in curs:
                                        priceList.append(j)

                        for i in range(len(numList)):
                                label=Label(self.sdroot, text=numList[i], font="helvetica 15")
                                label.grid(row=i+2, column=0)

                        for i in range(len(arrList)):
                                m=str(arrList[i])
                                n=str(depList[i])
                                label=Label(self.sdroot, text=n+"-"+m, font="helvetica 15")
                                label.grid(row=i+2, column=1)

                        self.radiovar1=IntVar()
                        
                        for i in range(len(priceList)):
                                rbutton=Radiobutton(self.sdroot, text="$"+str(priceList[i][0]), variable=self.radiovar1, value=i+1, font="helvetica 15")
                                rbutton.grid(row=i+2, column=2)
                                rbutton2=Radiobutton(self.sdroot, text="$"+str(priceList[i][1]), variable=self.radiovar1, value=-1*(i+1))
                                rbutton2.grid(row=i+2, column=3)
                        back=Button(self.sdroot, text="Back", command=self.BackToSearch)
                        back.grid(row=len(priceList)+2, column=0)

                        search=Button(self.sdroot, text="Search", command = self.toTE)
                        search.grid(row=len(priceList)+2, column=1)
                        self.sdroot.pack()


                else:
                        messagebox.showwarning(title="Error", message="You must enter a valid date and select a valid route")
                        self.SearchTrains()


    def backTE(self):
        self.tExF.destroy()
        self.selectDeparture()
        
    def toTE(self):
        if self.radiovar1.get() > 0:
                self.curRes['Class'] = 'First'
                bl = True
        elif self.radiovar1.get() < 0:
                self.curRes['Class'] = 'Second'
                bl = False
        for alp in app.sdroot.children.values():
            if alp.grid_info()['row'] == (abs(self.radiovar1.get())+1) and alp.grid_info()['column'] == 0:
                self.curRes['Train'] = alp['text']

            if alp.grid_info()['row'] == (abs(self.radiovar1.get())+1) and alp.grid_info()['column'] == 1:
                self.curRes['Time'] = alp['text']
            if bl == True and alp.grid_info()['row'] == (abs(self.radiovar1.get())+1) and alp.grid_info()['column'] == 2:
                self.curRes['Price'] = int(alp['text'][1:])
            if bl == False and alp.grid_info()['row'] == (abs(self.radiovar1.get())+1) and alp.grid_info()['column'] == 3:
               self.curRes['Price'] = int(alp['text'][1:])
        
        self.sdroot.destroy()
        self.travelExtras()
        
    def BackToSearch(self):
                try:
                    self.sdroot.destroy()
                except:
                    self.sroot.destroy()
                self.SearchTrains()

    def custFunctionalities1(self):
                self.cfroot2=Frame(self.win)
                self.win.wm_title("Choose Functionality")
               
                label1=Label(self.cfroot2, text="Choose Functionality", fg="gold", font="helvetica 20 bold")
                button1=Button(self.cfroot2, text="View Revenue Report",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", borderwidth=0, command=self.revReport)
                button2=Button(self.cfroot2, text="View Popular Route Report",bg="gold", fg="white", font="helvetica 15", width=40, relief="flat", command=self.popReport)
                logout=Button(self.cfroot2, text="Log Out", command = self.logout2)

                label1.pack()
                button1.pack()
                button2.pack()
                logout.pack()
                self.cfroot2.pack()
    def logout2(self):
        self.cfroot2.destroy()
        self.createLog()
    def toRev(self):
        self.cfroot2.destroy()
        self.revReport()
    def toPopRoute(self):
        self.cfroot2.destroy()
        self.SearchTrains()

    def backTo(self):
        self.win4.destroy()
        self.custFunctionalities1()
        
    def revReport(self):
        #Functionality
        curTime = str(datetime.date.today())
        month = int(curTime[5:7])
        fMonth = month-3
        sMonth = month-2
        tMonth = month-1
        year = int(curTime[:4])
        sql = "SELECT SUM(TotalCost) FROM Reservation WHERE EXTRACT(Year FROM StartDate)=%s AND EXTRACT(Month FROM StartDate)=%s"
        self.data = self.Connect()
        cursor = self.data.cursor()
        cursor1 = self.data.cursor()
        cursor2 = self.data.cursor()
        cursor.execute(sql,(year,fMonth))
        for i in cursor:
            fMonth1 = (i[0])
        cursor1.execute(sql,(year,sMonth))
        for i in cursor1:
            sMonth1 = (i[0])
        cursor2.execute(sql,(year,tMonth))
        for i in cursor2:
            tMonth1 = (i[0])
        #self.nickswin3.withdraw()
        self.nickswin4 = Toplevel(self.win)
        self.nickswin4.title('Revenue Report')
        self.nickstLabel4 = Label(self.nickswin4, text = "Revenue Report")
        self.nicksrLabel4 = Label(self.nickswin4, text = "Month")
        self.nickscLabel4 = Label(self.nickswin4, text = "Revenue")
        #self.nicksbButton4 = Button(self.nickswin4, text = "Back to Choose Functionality", command = self.toMan)
        self.nicksjanLabel = Label(self.nickswin4, text = "January")
        self.nicksfebLabel = Label(self.nickswin4, text = "February" )
        self.nicksmarchLabel = Label(self.nickswin4, text = "March")
        self.nicksmarchLabel1 = Label(self.nickswin4, text = tMonth1)
        self.nicksfebLabel1 = Label(self.nickswin4, text = sMonth1)
        self.nicksjanLabel1 = Label(self.nickswin4, text = fMonth1)
        self.nickstLabel4.grid(row = 0, columnspan = 2)
        self.nicksrLabel4.grid(row = 1, column = 0)
        self.nickscLabel4.grid(row = 1, column = 1)
        #self.nicksbButton4.grid(row = 5, columnspan = 2)
        self.nicksjanLabel.grid(row = 2, column = 0)
        self.nicksfebLabel.grid(row = 3, column = 0)
        self.nicksmarchLabel.grid(row = 4, column =0)
        self.nicksjanLabel1.grid(row = 2, column = 1)
        self.nicksfebLabel1.grid(row = 3, column = 1)
        self.nicksmarchLabel1.grid(row = 4, column =1)

    def confToF(self):
        self.comRoot.destroy()
        self.custFunctionalities()
        
    
    def confirmPage(self):
                self.comRoot= Frame(self.win)
                self.win.wm_title("Confirmation Page")
                user=self.curUser


                label1=Label(self.comRoot, text="Confirmation", fg="gold", font="helvetica 20 bold")
                label2=Label(self.comRoot, text="Reservation ID", font="helvetica 15")
                label3=Label(self.comRoot, text="Thank you for your purchase. Please save reservation ID for your records",font="helvetica 15")
                button1=Button(self.comRoot, text="Go back to choose functionalities", command = self.confToF)

                label1.grid(row=0, column=1, sticky=W)
                label2.grid(row=1, column=0, sticky=W)
                label3.grid(row=2, column=0, sticky=W)
                button1.grid(row=3, column=0, sticky=W)
                label4=Label(self.comRoot, text=self.lastID, font="helvetica 15")
                label4.grid(row=1, column=1)
                self.comRoot.pack()
####################################################################################################################
    def viewReviewGUI(self):
        self.nickswin = Toplevel(self.win)
        self.nickswin.title('View Review')
        self.nickstLabel = Label(self.nickswin, text = "View Review")
        self.nickstnLabel = Label(self.nickswin, text = "Train Number")
        self.nickstnEntry = Entry (self.nickswin, width = 30)
        #self.nicksbButton = Button(self.nickswin, text = "Back")
        self.nicksnButton = Button(self.nickswin, text = "Next", command = self.trainNumCheck)
        self.nickstLabel.grid(row = 0, columnspan = 2)
        self.nickstnLabel.grid(row = 1, column = 0)
        self.nickstnEntry.grid(row = 1, column = 1)
        #self.nicksbButton.grid(row = 2, column = 0)
        self.nicksnButton.grid(row = 2, column = 1)

    def trainNumCheck(self):
        self.data = self.Connect()
        cursor = self.data.cursor()
        trainNum = self.nickstnEntry.get()
        sql0 = "SELECT TrainNumber FROM Review WHERE TrainNumber=%s"
        tnCheck = cursor.execute(sql0,(trainNum))
        if tnCheck != False:
            self.viewReview()
        if tnCheck == False:
            messagebox.showwarning(title="Error", message="Error. Train number is not valid.")
            self.nickstnEntry.delete(0,END)
            
    def viewReview(self):
        #GUI
        self.nickswin.withdraw()
        self.nickswin1 = Toplevel(self.win)
        self.nickswin1.title('View Review')
        self.nickstLabel1 = Label(self.nickswin1, text = "View Review")
        self.nicksrLabel = Label(self.nickswin1, text = "Rating")
        self.nickscLabel = Label(self.nickswin1, text = "Comment")
        #self.bButton1 = Button(self.win1, text = "Back to Choose Functionality", command = self.backButton1)
        self.nickstLabel1.grid(row = 0, columnspan = 2)
        self.nicksrLabel.grid(row = 1, column = 0)
        self.nickscLabel.grid(row = 1, column = 1)
        #self.bButton1.grid(row = 2, columnspan = 2)
        #Functionality
        self.data = self.Connect()
        trainNum = self.nickstnEntry.get()
        sql1 = "SELECT Rating, Comment FROM Review WHERE TrainNumber = %s"
        cursor = self.data.cursor()
        cursor.execute(sql1,(trainNum))
        ratingList = []
        commentList = []
        for i in cursor:
            ratingList.append(i[0])
            commentList.append(i[1])
        for i in range(len(ratingList)):
            ratingLabel = Label(self.nickswin1, text = ratingList[i])
            ratingLabel.grid(row = i+2, column = 0, sticky=W)
        for i in range(len(commentList)):
            commentLabel = Label(self.nickswin1, text = commentList[i])
            commentLabel.grid(row = i+2, column = 1, sticky=W)
       
    
    def giveReviewGUI(self):
        self.nickswin2 = Toplevel(self.win)
        self.nickswin2.title('Give Review')
        self.nicksopvar = StringVar(self.nickswin2)
        self.nicksopvar.set("Very Good")
        self.nickstLabel2 = Label(self.nickswin2, text = "Give Review")
        self.nickstnLabel2 = Label(self.nickswin2, text ="Train Number")
        self.nicksrLabel2 = Label(self.nickswin2, text = "Rating")
        self.nickscLabel2 = Label(self.nickswin2, text = "Comment")
        self.nickstEntry2 = Entry(self.nickswin2, width = 30)
        self.nickscEntry2 = Entry(self.nickswin2, width = 30)
        self.nicksrOptionMenu = OptionMenu(self.nickswin2, self.nicksopvar, "Very Good", "Good", "Neutral", "Bad", "Very Bad")
        self.nickssButton2 = Button(self.nickswin2, text = "Submit", command = self.giveReview)
        self.nickstLabel2.grid(row = 0, columnspan = 2)
        self.nickstnLabel2.grid(row = 1, column = 0)
        self.nicksrLabel2.grid(row = 2, column = 0)
        self.nickscLabel2.grid(row = 3, column = 0)
        self.nickstEntry2.grid(row = 1, column = 1)
        self.nickscEntry2.grid(row =3, column = 1)
        self.nicksrOptionMenu.grid(row = 2, column = 1)
        self.nickssButton2.grid(row=4, columnspan = 2)

    def giveReview(self):
        self.data = self.Connect()
        trainNum = self.nickstEntry2.get()
        comment = self.nickscEntry2.get()
        #CHANGE USER VARIABLE TO SELF.USER.GET()
        user = "USERNAME"
        sql1 = "SELECT TrainNumber FROM TrainRoute WHERE TrainNumber=%s"
        sql2 = "INSERT INTO Review (Comment,Rating,TrainNumber,CustomerUsername) VALUES (%s, %s,%s,%s)"
        rating = self.nicksopvar.get()
        cursor = self.data.cursor()
        tnCheck = cursor.execute(sql1,(trainNum))
        if tnCheck == True:
            cursor.execute(sql2,(comment,rating,trainNum,user))
            self.nickswin2.withdraw()
            #ADD CODE TO TAKE BACK TO FUNCTIONALITIES MENU
        if tnCheck == False:
            messagebox.showwarning(title="Error", message="Error. Train number is not valid.")
            self.nickstEntry2.delete(0,END)
            self.nickscEntry2.delete(0,END)
        

##    def manFunc(self):
##        self.nickswin3 = Toplevel(self.root)
##        self.nickswin3.title('Choose Functionality')
##        self.nickstLabel3 = Label(self.nickswin3, text = "Choose Functionality")
##        self.nicksrButton3 = Button(self.nickswin3, text = "View Revenue Report", command = self.revReport)
##        self.nicksprButton3 = Button(self.nickswin3, text = "View Popular Route Report")
##        self.nickslButton3 = Button(self.nickswin3, text = "Logout", command = self.logout)
##        self.nickstLabel3.grid(row = 0)
##        self.nicksrButton3.grid(row = 1)
##        self.nicksprButton3.grid(row = 2)
##        self.nickslButton3.grid(row = 3)
##
##    def revReport(self):
##        self.nickswin3.withdraw()
##        self.nickswin4 = Toplevel(self.root)
##        self.nickswin4.title('Revenue Report')
##        self.nickstLabel4 = Label(self.nickswin4, text = "Revenue Report")
##        self.nicksrLabel4 = Label(self.nickswin4, text = "Month")
##        self.nickscLabel4 = Label(self.nickswin4, text = "Revenue")
##        self.nicksbButton4 = Button(self.nickswin4, text = "Back to Choose Functionality", command = self.backButton)
##        self.nicksjanLabel = Label(self.nickswin4, text = "January")
##        self.nicksfebLabel = Label(self.nickswin4, text = "February")
##        self.nicksmarchLabel = Label(self.nickswin4, text = "March")
##        self.nickstLabel4.grid(row = 0, columnspan = 2)
##        self.nicksrLabel4.grid(row = 1, column = 0)
##        self.nickscLabel4.grid(row = 1, column = 1)
##        self.nicksbButton4.grid(row = 5, columnspan = 2)
##        self.nicksjanLabel.grid(row = 2, column = 0)
##        self.nicksfebLabel.grid(row = 3, column = 0)
##        self.nicksmarchLabel.grid(row = 4, column =0)
##
##
##    def backButton(self):
##        self.nickswin4.withdraw()
##        self.manFunc()
##        
##    def popTrains(self):
##        pass
    def canToFunc(self):
        self.can1.destroy()
        self.custFunctionalities()
    def cancelARes1(self):
        try:
            self.cfroot.destroy()
        except:
            pass
        self.can1 = Frame(self.win)
        l3 = Label(self.can1, text = "Travel Extras & Passenger Info" , fg = 'Gold', font="helvetica 16 bold")
        l3.grid(sticky = E+W+S+N, row = 1,column = 1, columnspan = 3)

        Label(self.can1, text = "Reservation ID: ").grid(row = 2,column = 1,sticky = E)
        self.canIDVar = StringVar()
        canE = Entry(self.can1, textvariable = self.canIDVar, width = 10)
        canE.grid(row = 2, column = 2,sticky = W)
        Button(self.can1, text = "Back", command = self.canToFunc, width = 10).grid(row = 3,column = 2)
        Button(self.can1, text = "Search", command = self.cancelRes2, width = 10).grid(row = 2,column = 3)
        self.can1.pack()
        
    def cancelRes2(self):
                self.canID = self.canIDVar.get()      
                sql="SELECT TrainNumber, DepartsFrom, ArrivesAt, Class, NumberOfBaggage, PassengerName, DepartDate FROM Reserves WHERE ReservationID=%s"
                self.openDB()
                cursor=self.DB.cursor()
                cursor.execute(sql, (self.canID))
                user = self.curUser
                tNum=[]
                Dep=[]
                Arr=[]
                Class=[]
                Bags=[]
                pName=[]
                dDate=[]
                self.dictList=[]
                                
                for i in cursor:
                        aDict={}
                        tNum.append(i[0])
                        aDict["Train"]=i[0]
                        Dep.append(i[1])
                        aDict["dCity"]=i[1]
                        Arr.append(i[2])
                        aDict["aCity"]=i[2]
                        Class.append(i[3])
                        aDict["Class"]=i[3]
                        Bags.append(i[4])
                        aDict["Bags"]=i[4]
                        pName.append(i[5])
                        aDict["Passenger"]=i[5]
                        dDate.append(i[6])
                        aDict["DepDate"]=i[6]
                        self.dictList.append(aDict)
                cursor.close()
                sql1="SELECT CustomerUsername FROM Reservation WHERE ReservationID=%s"
                curs=self.DB.cursor()
                curs.execute(sql1, (self.canID))
                custList=[]
                for i in curs:
                        j=list(i)
                        custList.append(j)
                newList=sum(custList,[])
                user1=user.lower()
                finalList=[]
                for i in newList:
                        finalList.append(i.lower())
                curs.close()
                
                if user1 in finalList:
                        try:
                            self.can1.destroy()
                        except:
                            pass
                        self.mainCan = Frame(self.win)
                        self.can2 = Frame(self.mainCan)
                        self.can3 = Frame(self.mainCan)
                        
                        self.win.wm_title("Cancel Reservation")

                        label1=Label(self.can2, text="Cancel Reservation", fg="gold", font="helvetica 20 bold")
                        label1.grid(row=0, column=5)
                        label2=Label(self.can2, text="Select", bg='darkgrey', highlightthickness=2, highlightcolor='black')
                        label2.grid(column=1, row=1)
                        l3 = Label(self.can2, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l3.grid(column = 3, row = 1)
                        l4 = Label(self.can2, text = "Time and Date of Departure",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l4.grid(column = 4, row = 1)
                        l5 = Label(self.can2, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l5.grid(column = 5, row = 1)
                        l6 = Label(self.can2, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l6.grid(column = 6, row = 1)
                        l7 = Label(self.can2, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l7.grid(column = 7, row = 1)
                        l8 = Label(self.can2, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l8.grid(column = 8, row = 1)
                        l9 = Label(self.can2, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l9.grid(column = 9, row = 1)
                        l10 = Label(self.can2, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l10.grid(column = 10, row = 1)

                        tList=[]

                        for i in range(len(tNum)):
                                sq="SELECT A.ArrivalTime, B.DepartureTime FROM Stop A, Stop B WHERE A.name=%s AND B.Name=%s AND A.TrainNumber=B.TrainNumber AND A.TrainNumber=%s AND B.DepartureTime<A.ArrivalTime"
                                cursor1=self.DB.cursor()
                                cursor1.execute(sq, (Arr[i], Dep[i], tNum[i]))
                                for i in cursor1:
                                        tList.append(i)
                                cursor1.close()
                        
                        for i in range(len(tNum)):
                                labela=Label(self.can2, text=tNum[i])
                                labela.grid(row=i+2, column=3)

                        for i in range(len(tList)):
                                m=str(tList[i][0])
                                n=str(tList[i][1])
                                p=str(dDate[i])
                                label=Label(self.can2, text=p+"   "+n+"-"+m, font="helvetica 15")
                                label.grid(row=i+2, column=4)

                        for i in range(len(Arr)):
                                labelb=Label(self.can2, text=Arr[i])
                                labelb.grid(row=i+2, column=6)
                        for i in range(len(Dep)):
                                labelb=Label(self.can2, text=Dep[i])
                                labelb.grid(row=i+2, column=5)
                        for i in range(len(Class)):
                                labelc=Label(self.can2, text=Class[i])
                                labelc.grid(row=i+2, column=7)

                                labeld=Label(self.can2, text=Bags[i])
                                labeld.grid(row=i+2, column=9)

                                labele=Label(self.can2, text=pName[i])
                                labele.grid(row=i+2, column=10)
                        pList=[]

                        for i in range(len(Class)):
                                if Class[i]=="First":
                                        sq1="SELECT 1stClassPrice FROM TrainRoute WHERE TrainNumber=%s"
                                        curs2=self.DB.cursor()
                                        curs2.execute(sq1,(tNum[i]))
                                        for j in curs2:
                                                pList.append(j)
                                elif Class[i]=="Second":
                                        sq1="SELECT 2ndClassPrice FROM TrainRoute WHERE TrainNumber=%s"
                                        curs2=self.DB.cursor()
                                        curs2.execute(sq1,(tNum[i]))
                                        for j in curs2:
                                                pList.append(j)
                                        curs2.close()
                        #self.rCancelVar=IntVar()
                        for i in range(len(pList)):
                                labelf=Label(self.can2, text=pList[i])
                                labelf.grid(row=i+2, column=8)
                                
                                #rbutton=Radiobutton(self.can2, variable=self.rCancelVar, value=i, font="helvetica 15")
                                #rbutton.grid(row=i+2, column=1)
                                
                        Label(self.can3, text = "Total Cost of Reservation: ").grid(row = 1, column = 1,sticky = W)
                        Label(self.can3, text = "Date of Cancelation: ").grid(row = 2, column = 1, sticky = W)
                        Label(self.can3, text = "Amount to be Refunded: ").grid(row = 3, column = 1, sticky = W)

                        self.openDB()
                        curse = self.DB.cursor()
                        sql= "select TotalCost,StartDate from Reservation where ReservationID = %s"
                        curse.execute(sql, (self.canID))
                        M = curse.fetchone()
                        curse.close()
                        self.DB.close()
                        self.mymatch = M[0]
                        self.myday = str(M[1])
                        self.mycurDate = time.strftime("%Y-%m-%d")
                        self.refund = 0
                        if self.mycurDate>self.myday:
                            messagebox.showwarning(title="Error", message="You cannot cancel a trip you have already done")
                        else:
                            depVal = int(str(app.myday)[5:7])*30 + int(str(app.myday)[8:10])+int(str(app.myday)[0:4])*365
                            curVal = int(str(app.mycurDate)[5:7])*30 + int(str(app.mycurDate)[8:10])+int(str(app.mycurDate)[0:4])*365
                            if depVal - curVal > 7:
                                self.refund = .8*self.mymatch- 50
                            elif depVal - curVal > 1:
                                self.refund = int(.5*self.mymatch - 50)
                            else:
                                self.refund = 0
                        if self.refund < 0:
                            self.refund = 0
                            

                        Label(self.can3, text = self.mymatch).grid(row = 1, column = 2, sticky = W)
                        Label(self.can3, text = time.strftime("%m/%d/%Y")).grid(row = 2, column = 2, sticky = W)
                        Label(self.can3, text = self.refund).grid(row = 3, column = 2, sticky = W)


                        bButton=Button(self.can3, text="Back", command=self.BackToCancelID)
                        bButton.grid(row=4, column=1, sticky = W)
                        sButton=Button(self.can3, text="Cancel It", command=self.cancelIt)
                        sButton.grid(row=4, column=2, sticky = W)

                        for i in range(len(self.dictList)):
                                self.dictList[i]["Price"]=pList[i][0]
                                self.dictList[i]["Time"]=str(tList[i][1])+"-"+str(tList[i][0])
                        self.can2.pack(side = TOP)
                        self.can3.pack(side = BOTTOM)
                        self.mainCan.pack()
                        
                       
                else:
                        messagebox.showwarning(title="Error", message="Please enter a valid reservation ID")
                
                
    def BackToCancelID(self):
        self.mainCan.destroy()
        self.cancelARes1()

    def cancelIt(self):
        self.openDB()
        cur = self.DB.cursor()
        sql = "Update Reservation set TotalCost=%s where ReservationID = %s"
        cur.execute(sql, (self.mymatch - self.refund, self.canID))
        cur.close()
        sql2 = "Update Reservation set IsCancelled = 1 where ReservationID = %s"
        cur2 = self.DB.cursor()
        cur2.execute(sql2, (self.canID))
        cur2.close()
        self.DB.commit()
        self.DB.close()

        messagebox.showinfo(message = "Trip has been cancelled!")
        self.mainCan.destroy()
        self.custFunctionalities()
        
    def updateReservation(self):
                try:
                    self.cfroot.destroy()
                except:
                    pass
                self.upDate=Frame(self.win)
                
                label1=Label(self.upDate, text="Update Reservation", fg="gold", font="helvetica 20 bold")
                label2=Label(self.upDate, text="Reservation ID", font="helvetica 15")
                self.IDentry=Entry(self.upDate)
                sButton=Button(self.upDate, text="Search", font="helvetica 15", command=self.updateRes)
                bButton=Button(self.upDate, text="Back", font="helvetica 15", command=self.backToF)

                label1.grid(row=0, column=1)
                label2.grid(row=1, column=0)
                self.IDentry.grid(row=1, column=1)
                sButton.grid(row=1, column=2)
                bButton.grid(row=2, column=1)

                self.upDate.pack()
                
    def backToF(self):
                
                self.upDate.destroy()
                self.custFunctionalities()

    def updateRes(self):
                self.upResID= self.IDentry.get()
                #user=self.userEntry.get()
                user = self.curUser
                resID=self.IDentry.get()

                sql="SELECT A.TrainNumber, A.DepartsFrom, A.ArrivesAt, A.Class, A.NumberOfBaggage, A.PassengerName, A.DepartDate FROM Reserves A, Reservation B WHERE A.ReservationID=B.ReservationID AND A.ReservationID=%s AND B.IsCancelled = 0;"
                self.openDB()
                cursor=self.DB.cursor()
                cursor.execute(sql, (resID))
                
                tNum=[]
                Dep=[]
                Arr=[]
                Class=[]
                Bags=[]
                pName=[]
                dDate=[]
                self.dictList=[]
                                
                for i in cursor:
                        aDict={}
                        tNum.append(i[0])
                        aDict["Train"]=i[0]
                        Dep.append(i[1])
                        aDict["dCity"]=i[1]
                        Arr.append(i[2])
                        aDict["aCity"]=i[2]
                        Class.append(i[3])
                        aDict["Class"]=i[3]
                        Bags.append(i[4])
                        aDict["Bags"]=i[4]
                        pName.append(i[5])
                        aDict["Passenger"]=i[5]
                        dDate.append(i[6])
                        aDict["DepDate"]=i[6]
                        self.dictList.append(aDict)
                cursor.close()
                sql1="SELECT CustomerUsername FROM Reservation WHERE ReservationID=%s AND IsCancelled=0"
                curs=self.DB.cursor()
                curs.execute(sql1, (resID))
                custList=[]
                for i in curs:
                        j=list(i)
                        custList.append(j)
                newList=sum(custList,[])
                user1=user.lower()
                finalList=[]
                for i in newList:
                        finalList.append(i.lower())
                curs.close()
                
                if user1 in finalList:
                        self.upDate.destroy()
                        self.upDate2=Frame(self.win)
                        self.win.wm_title("Update Reservation")

                        label1=Label(self.upDate2, text="Update Reservation", fg="gold", font="helvetica 20 bold")
                        label1.grid(row=0, column=5)
                        label2=Label(self.upDate2, text="Select", bg='darkgrey', highlightthickness=2, highlightcolor='black')
                        label2.grid(column=1, row=1)
                        l3 = Label(self.upDate2, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l3.grid(column = 3, row = 1)
                        l4 = Label(self.upDate2, text = "Time and Date of Departure",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l4.grid(column = 4, row = 1)
                        l5 = Label(self.upDate2, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l5.grid(column = 5, row = 1)
                        l6 = Label(self.upDate2, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l6.grid(column = 6, row = 1)
                        l7 = Label(self.upDate2, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l7.grid(column = 7, row = 1)
                        l8 = Label(self.upDate2, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l8.grid(column = 8, row = 1)
                        l9 = Label(self.upDate2, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l9.grid(column = 9, row = 1)
                        l10 = Label(self.upDate2, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l10.grid(column = 10, row = 1)

                        tList=[]

                        for i in range(len(tNum)):
                                sq="SELECT A.ArrivalTime, B.DepartureTime FROM Stop A, Stop B WHERE A.name=%s AND B.Name=%s AND A.TrainNumber=B.TrainNumber AND A.TrainNumber=%s AND B.DepartureTime<A.ArrivalTime"
                                cursor1=self.DB.cursor()
                                cursor1.execute(sq, (Arr[i], Dep[i], tNum[i]))
                                for i in cursor1:
                                        tList.append(i)
                                cursor1.close()
                        
                        for i in range(len(tNum)):
                                labela=Label(self.upDate2, text=tNum[i])
                                labela.grid(row=i+2, column=3)

                        for i in range(len(tList)):
                                m=str(tList[i][0])
                                n=str(tList[i][1])
                                p=str(dDate[i])
                                label=Label(self.upDate2, text=p+"   "+n+"-"+m, font="helvetica 15")
                                label.grid(row=i+2, column=4)

                        for i in range(len(Arr)):
                                labelb=Label(self.upDate2, text=Arr[i])
                                labelb.grid(row=i+2, column=6)
                        for i in range(len(Dep)):
                                labelb=Label(self.upDate2, text=Dep[i])
                                labelb.grid(row=i+2, column=5)
                        for i in range(len(Class)):
                                labelc=Label(self.upDate2, text=Class[i])
                                labelc.grid(row=i+2, column=7)

                                labeld=Label(self.upDate2, text=Bags[i])
                                labeld.grid(row=i+2, column=9)

                                labele=Label(self.upDate2, text=pName[i])
                                labele.grid(row=i+2, column=10)
                        pList=[]

                        for i in range(len(Class)):
                                if Class[i]=="First":
                                        sq1="SELECT 1stClassPrice FROM TrainRoute WHERE TrainNumber=%s"
                                        curs2=self.DB.cursor()
                                        curs2.execute(sq1,(tNum[i]))
                                        for j in curs2:
                                                pList.append(j)
                                elif Class[i]=="Second":
                                        sq1="SELECT 2ndClassPrice FROM TrainRoute WHERE TrainNumber=%s"
                                        curs2=self.DB.cursor()
                                        curs2.execute(sq1,(tNum[i]))
                                        for j in curs2:
                                                pList.append(j)
                                        curs2.close()
                        self.rVar=IntVar()
                        for i in range(len(pList)):
                                labelf=Label(self.upDate2, text=pList[i])
                                labelf.grid(row=i+2, column=8)
                                
                                rbutton=Radiobutton(self.upDate2, variable=self.rVar, value=i, font="helvetica 15")
                                rbutton.grid(row=i+2, column=1)

                        bButton=Button(self.upDate2, text="Back", command=self.Back)
                        bButton.grid(row=len(pList)+2, column=1)
                        sButton=Button(self.upDate2, text="Next", command=self.searchUpdate)
                        sButton.grid(row=len(pList)+2, column=2)

                        for i in range(len(self.dictList)):
                                self.dictList[i]["Price"]=pList[i][0]
                                self.dictList[i]["Time"]=str(tList[i][1])+"-"+str(tList[i][0])
                        self.upDate2.pack()
                       
                else:
                        messagebox.showwarning(title="Error", message="Please enter a valid reservation ID associated with your username")
                
                self.DB.close()
                
    def Back(self):
                self.upDate2.destroy()
                self.updateReservation()

    def searchUpdate(self):

                val=self.rVar.get()


                #user=self.userEntry.get()
                user = self.curUser
                resID=self.upResID

                self.upDate2.destroy()
                self.upDate3=Frame(self.win)
                self.win.wm_title("Update Reservation")
                
                label3=Label(self.upDate3, text="Current Train Ticket", fg="black", font="helvetica 17 bold")
                label3.grid(row=1, column=0)
                label1=Label(self.upDate3, text="Update Reservation", fg="gold", font="helvetica 20 bold")
                label1.grid(row=0, column=5)
                l3 = Label(self.upDate3, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l3.grid(column = 3, row = 2)
                l4 = Label(self.upDate3, text = "Time and Date of Departure", bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l4.grid(column = 4, row = 2)
                l5 = Label(self.upDate3, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l5.grid(column = 5, row = 2)
                l6 = Label(self.upDate3, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l6.grid(column = 6, row = 2)
                l7 = Label(self.upDate3, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l7.grid(column = 7, row = 2)
                l8 = Label(self.upDate3, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l8.grid(column = 8, row = 2)
                l9 = Label(self.upDate3, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l9.grid(column = 9, row = 2)
                l10 = Label(self.upDate3, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                l10.grid(column = 10, row = 2)


                labela=Label(self.upDate3, text=self.dictList[val]["Train"])
                labela.grid(row=3, column=3)
                labelb=Label(self.upDate3, text=str(self.dictList[val]["DepDate"])+"  "+self.dictList[val]["Time"])
                labelb.grid(row=3, column=4)
                labelc=Label(self.upDate3, text=self.dictList[val]["dCity"])
                labelc.grid(row=3, column=5)
                labeld=Label(self.upDate3, text=self.dictList[val]["aCity"])
                labeld.grid(row=3, column=6)
                labele=Label(self.upDate3, text=self.dictList[val]["Class"])
                labele.grid(row=3, column=7)
                labelf=Label(self.upDate3, text=self.dictList[val]["Price"])
                labelf.grid(row=3, column=8)
                labelg=Label(self.upDate3, text=self.dictList[val]["Bags"])
                labelg.grid(row=3, column=9)
                labelh=Label(self.upDate3, text=self.dictList[val]["Passenger"])
                labelh.grid(row=3, column=10)
                
                labeli=Label(self.upDate3, text="New Departure Date")
                labeli.grid(row=4, column=3)

                labelq=Label(self.upDate3, text="Please enter your date in the form YYYY-MM-DD", font="helvetica 15")
                labelq.grid(row=5, column=3)
                

                self.entryB=Entry(self.upDate3)
                self.entryB.grid(row=4, column=4)

                checkB=Button(self.upDate3, text="Search Availability", command=self.searchUpdate2)
                checkB.grid(row=4, column=5)
                self.upDate3.pack()

    def searchUpdate2(self):

                self.val=self.rVar.get()
                #user=self.userEntry.get()
                user = self.curUser
                resID=self.upResID
                self.date=self.entryB.get()
                todayDate=time.strftime("%Y-%m-%d")


                if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", self.date)!=None and self.date>todayDate:
                        self.upDate3.destroy()
                        self.upDate4=Frame(self.win)
                        self.win.wm_title("Update Reservation")
                        
                        label3=Label(self.upDate4, text="Current Train Ticket", fg="black", font="helvetica 17 bold")
                        label3.grid(row=1, column=0)
                        label1=Label(self.upDate4, text="Update Reservation", fg="gold", font="helvetica 20 bold")
                        label1.grid(row=0, column=5)
                        l3 = Label(self.upDate4, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l3.grid(column = 0, row = 2)
                        l4 = Label(self.upDate4, text = "Time and Date of Departure",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l4.grid(column = 1, row = 2)
                        l5 = Label(self.upDate4, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l5.grid(column = 2, row = 2)
                        l6 = Label(self.upDate4, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l6.grid(column = 3, row = 2)
                        l7 = Label(self.upDate4, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l7.grid(column = 4, row = 2)
                        l8 = Label(self.upDate4, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l8.grid(column = 5, row = 2)
                        l9 = Label(self.upDate4, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l9.grid(column = 6, row = 2)
                        l10 = Label(self.upDate4, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l10.grid(column = 7, row = 2)


                        labela=Label(self.upDate4, text=self.dictList[self.val]["Train"])
                        labela.grid(row=3, column=0)
                        labelb=Label(self.upDate4, text=str(self.dictList[self.val]["DepDate"])+"   "+self.dictList[self.val]["Time"])
                        labelb.grid(row=3, column=1)
                        labelc=Label(self.upDate4, text=self.dictList[self.val]["dCity"])
                        labelc.grid(row=3, column=2)
                        labeld=Label(self.upDate4, text=self.dictList[self.val]["aCity"])
                        labeld.grid(row=3, column=3)
                        labele=Label(self.upDate4, text=self.dictList[self.val]["Class"])
                        labele.grid(row=3, column=4)
                        labelf=Label(self.upDate4, text=self.dictList[self.val]["Price"])
                        labelf.grid(row=3, column=5)
                        labelg=Label(self.upDate4, text=self.dictList[self.val]["Bags"])
                        labelg.grid(row=3, column=6)
                        labelh=Label(self.upDate4, text=self.dictList[self.val]["Passenger"])
                        labelh.grid(row=3, column=7)
                        
                        labeli=Label(self.upDate4, text="New Departure Date")
                        labeli.grid(row=5, column=0)

                        entryB=Label(self.upDate4, text=self.date)
                        entryB.grid(row=5, column=1)

                        labelj=Label(self.upDate4, text="Updated Train Ticket",fg="black", font="helvetica 17 bold")
                        labelj.grid(row=7, column=0)

                        l31 = Label(self.upDate4, text = "Train (Train Number)",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l31.grid(column = 0, row = 8)
                        l41 = Label(self.upDate4, text = "Time and Date of Departure",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l41.grid(column = 1, row = 8)
                        l51 = Label(self.upDate4, text = "Departs From",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l51.grid(column = 2, row = 8)
                        l61 = Label(self.upDate4, text = "Arrives At",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l61.grid(column = 3, row = 8)
                        l71 = Label(self.upDate4, text = "Class",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l71.grid(column =4, row = 8)
                        l81 = Label(self.upDate4, text = "Price",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l81.grid(column = 5, row = 8)
                        l91 = Label(self.upDate4, text = "Total Bags",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l91.grid(column = 6, row = 8)
                        l101 = Label(self.upDate4, text = "Passenger Name",bg = 'darkgrey', highlightthickness=2, highlightcolor='black')
                        l101.grid(column = 7, row = 8)

                        la=Label(self.upDate4, text=self.dictList[self.val]["Train"])
                        la.grid(row=9, column=0)
                        lb=Label(self.upDate4, text=self.date+"  "+self.dictList[self.val]["Time"])
                        lb.grid(row=9, column=1)
                        lc=Label(self.upDate4, text=self.dictList[self.val]["dCity"])
                        lc.grid(row=9, column=2)
                        ld=Label(self.upDate4, text=self.dictList[self.val]["aCity"])
                        ld.grid(row=9, column=3)
                        le=Label(self.upDate4, text=self.dictList[self.val]["Class"])
                        le.grid(row=9, column=4)
                        lf=Label(self.upDate4, text=self.dictList[self.val]["Price"])
                        lf.grid(row=9, column=5)
                        lg=Label(self.upDate4, text=self.dictList[self.val]["Bags"])
                        lg.grid(row=9, column=6)
                        lh=Label(self.upDate4, text=self.dictList[self.val]["Passenger"])
                        lh.grid(row=9, column=7)

                        li=Label(self.upDate4, text="Change Fee")
                        li.grid(row=10, column=0)

                        #DONT FORGET TO CHANGE THE CHANGE FEE 
                        lj=Label(self.upDate4, text="$"+str(self.systemInfo[3]))
                        lj.grid(row=10, column=1)

                        lk=Label(self.upDate4, text="Updated Total Cost:")
                        lk.grid(row=11, column=0)

                        self.Cost=int(self.dictList[self.val]["Price"])+self.systemInfo[3]

                        ll=Label(self.upDate4, text=self.Cost)
                        ll.grid(row=11, column=1)

                        bacButton=Button(self.upDate4, text="Back", command=self.Fback)
                        bacButton.grid(row=12, column=0)

                        upButton=Button(self.upDate4, text="Update", command=self.UpdateSys)
                        upButton.grid(row=12, column=1)
                        self.upDate4.pack()

                        
                else:
                        messagebox.showerror("Please make sure your date is in the correct form and is after today's date")
                        

    def Fback(self):
                self.upDate4.destroy()
                self.updateReservation()

    def UpdateSys(self):

                resID=self.upResID

                sql="UPDATE Reserves SET DepartDate=%s WHERE ReservationID=%s AND TrainNumber=%s"
                self.openDB()
                cursor=self.DB.cursor()
                cursor.execute(sql, (self.date, resID, self.dictList[self.val]["Train"]))
                cursor.close()
                sql2="UPDATE Reservation SET TotalCost=%s WHERE ReservationID=%s"
                curs=self.DB.cursor()
                curs.execute(sql2, (self.Cost, resID))
                curs.close()
                self.DB.commit()
                self.DB.close()
                messagebox.showinfo(message = "Update Successful!")
                self.upDate4.destroy()
                self.custFunctionalities()
                
    def popReport(self):
                self.popRoot = Toplevel(self.win)
                self.popRoot.title('View Popular Route Report')
                #self.popRoot=
                #self.popRoot.title("View Popular Route Report")

                todayDate=time.strftime("%Y-%m-%d")
                EMonth=int(todayDate[5:7])-3
                MMonth=int(todayDate[5:7])-2
                LMonth=int(todayDate[5:7])-1

                if EMonth==0:
                        EDate=todayDate[0:5]+"01"+todayDate[7:10]
                        MDate=todayDate[0:5]+"02"+todayDate[7:10]
                        LDate=todayDate[0:5]+"03"+todayDate[7:10]
                elif EMonth==-1:
                        EDate=str(int(todayDate[0:5])-1)+"12"+todayDate[7:10]
                        MDate=todayDate[0:5]+"01"+todayDate[7:10]
                        LDate=todayDate[0:5]+"02"+todayDate[7:10]                       
                elif EMonth==-2:
                        EDate=str(int(todayDate[0:5])-1)+"11"+todayDate[7:10]
                        MDate=str(int(todayDate[0:5])-1)+"12"+todayDate[7:10]
                        LDate=todayDate[0:5]+"01"+todayDate[7:10] 
                elif EMonth==-3:
                        EDate=str(int(todayDate[0:5])-1)+"10"+todayDate[7:10]
                        MDate=str(int(todayDate[0:5])-1)+"11"+todayDate[7:10]
                        LDate=str(int(todayDate[0:5])-1)+"12"+todayDate[7:10]
                else:
                        if int(todayDate[5:7])<=9:
                                EDate=todayDate[0:5]+"0"+str(int(todayDate[5:7])-3)+todayDate[7:10]
                                MDate=todayDate[0:5]+"0"+str(int(todayDate[5:7])-2)+todayDate[7:10]
                                LDate=todayDate[0:5]+"0"+str(int(todayDate[5:7])-1)+todayDate[7:10]
                        else:
                                EDate=todayDate[0:5]+str(int(todayDate[5:7])-3)+todayDate[7:10]
                                MDate=todayDate[0:5]+str(int(todayDate[5:7])-2)+todayDate[7:10]
                                LDate=todayDate[0:5]+str(int(todayDate[5:7])-1)+todayDate[7:10]

                
                        

                sql="""SELECT A.TrainNumber, COUNT(A.TrainNumber) FROM Reserves A, Reservation B WHERE EXTRACT(Month FROM A.DepartDate)=%s AND EXTRACT(Year FROM A.DepartDate)=%s AND A.ReservationID=B.ReservationID AND B.IsCancelled<>%s GROUP BY A.TrainNumber ORDER BY COUNT(A.ReservationID) DESC"""

                self.openDB()
                curse=self.DB.cursor()
                curse.execute(sql,(int(EDate[5:7]),int(EDate[0:4]),int(1)))


                sql2="""SELECT A.TrainNumber, COUNT(A.TrainNumber) FROM Reserves A, Reservation B WHERE EXTRACT(Month FROM A.DepartDate)=%s AND EXTRACT(Year FROM A.DepartDate)=%s AND A.ReservationID=B.ReservationID AND B.IsCancelled<>%s GROUP BY A.TrainNumber ORDER BY COUNT(A.ReservationID) DESC"""
                
                curse2=self.DB.cursor()
                curse2.execute(sql2, (int(MDate[5:7]),int(MDate[0:4]),int(1)))

                sql3="""SELECT A.TrainNumber, COUNT(A.TrainNumber) FROM Reserves A, Reservation B WHERE EXTRACT(Month FROM A.DepartDate)=%s AND EXTRACT(Year FROM A.DepartDate)=%s AND A.ReservationID=B.ReservationID AND B.IsCancelled<>%s GROUP BY A.TrainNumber ORDER BY COUNT(A.ReservationID) DESC"""
                
                curse3=self.DB.cursor()
                curse3.execute(sql3, (int(LDate[5:7]),int(LDate[0:4]),int(1)))
                

                label1=Label(self.popRoot, text="View Popular Route Report", fg="gold", font="helvetica 20 bold")
                label1.grid(column=1, row=0)

                label2=Label(self.popRoot, text="Month")
                label2.grid(column=0, row=1)

                label3=Label(self.popRoot, text="Train Number")
                label3.grid(column=1, row=1)

                label4=Label(self.popRoot, text="Number of Reservations")
                label4.grid(column=2, row=1)

                eList=[]
                mList=[]
                lList=[]
        

                for i in curse:
    
                        eList.append(i)
                curse.close()
                for i in curse2:
 
                        mList.append(i)
                curse2.close()
                for i in curse3:
    
                        lList.append(i)
                curse3.close()
                months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

                
                label=Label(self.popRoot, text=months[int(EDate[5:7])-1])
                label.grid(row=2, column=0)

                labela=Label(self.popRoot, text=eList[0][0])
                labela.grid(row=2, column=1)
                labelb=Label(self.popRoot, text=eList[1][0])
                labelb.grid(row=3, column=1)
                labelc=Label(self.popRoot, text=eList[2][0])
                labelc.grid(row=4, column=1)

                labelaa=Label(self.popRoot, text=eList[0][1])
                labelaa.grid(row=2, column=2)
                labelba=Label(self.popRoot, text=eList[1][1])
                labelba.grid(row=3, column=2)
                labelca=Label(self.popRoot, text=eList[2][1])
                labelca.grid(row=4, column=2)

                labeld=Label(self.popRoot, text=months[int(MDate[5:7])-1])
                labeld.grid(row=5, column=0)


                labela1=Label(self.popRoot, text=mList[0][0])
                labela1.grid(row=5, column=1)
                labelb1=Label(self.popRoot, text=mList[1][0])
                labelb1.grid(row=6, column=1)
                labelc1=Label(self.popRoot, text=mList[2][0])
                labelc1.grid(row=8, column=1)

                labela1a=Label(self.popRoot, text=mList[0][1])
                labela1a.grid(row=5, column=2)
                labelb1a=Label(self.popRoot, text=mList[1][1])
                labelb1a.grid(row=6, column=2)
                labelc1a=Label(self.popRoot, text=mList[2][1])
                labelc1a.grid(row=8, column=2)
                
                labele=Label(self.popRoot, text=months[int(LDate[5:7])-1])
                labele.grid(row=9, column=0)
                
                labela2=Label(self.popRoot, text=lList[0][0])
                labela2.grid(row=9, column=1)
                labelb2=Label(self.popRoot, text=lList[1][0])
                labelb2.grid(row=10, column=1)
                labelc2=Label(self.popRoot, text=lList[2][0])
                labelc2.grid(row=11, column=1)

                labela2a=Label(self.popRoot, text=lList[0][1])
                labela2a.grid(row=9, column=2)
                labelb2a=Label(self.popRoot, text=lList[1][1])
                labelb2a.grid(row=10, column=2)
                labelc2a=Label(self.popRoot, text=lList[2][1])
                labelc2a.grid(row=11, column=2)

                self.DB.close()
           
        
        
                
app = GUI()
