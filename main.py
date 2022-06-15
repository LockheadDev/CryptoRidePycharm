from datetime import *
import threading
import tkinter.messagebox
from tkinter import *
from tkinter.constants import CENTER, COMMAND, Y
from tkinter.ttk import Frame, Label, Entry
from tkinter import ttk
from tkcalendar import DateEntry
from tktimepicker import AnalogPicker, SpinTimePickerModern, SpinTimePickerOld
from PIL import Image, ImageTk
from web3 import Web3
import BlockChainController as bcc
from classes import Ride, User
import os
import time


# TODO - UPDATE COST VALUE IN TREEVIEW AFTER BID


class Example(Frame):

    # INIT
    def __init__(self):
        # GUI ELEMENTS
        self.ride_id = 0
        self.current_avatar = 0
        self.current_location = None
        self.current_seats = None
        self.offer_list = ttk.Treeview
        self.thread = threading.Thread(target=self.checkContractDateTime, args=(30,))
        self.thread.start()

        # BACKEND ELEMENTS
        self.current_user = User("", "", "")
        self.all_users = []
        self.offer_rides = []

        super().__init__()
        self.initUI()

    # <editor-fold desc="Backend">
    def checkContractDateTime(self, segundos):
        while True:
            print("--CHECKING PUBLSIHED RIDES--")
            now = datetime.now()
            time_now_hour = str(now.hour)
            time_now_minute = str(now.minute)
            date_now_year = str(now.year)
            date_now_month = str(now.month)
            date_now_day = str(now.day)

            print("Hour: " + time_now_hour)
            print("Minute: " + time_now_minute)
            print("Year: " + date_now_year)
            print("Month: " + date_now_month)
            print("Day: " + date_now_day)

            for ride in self.offer_rides:
                print("Checking ride: " + str(ride.id))
                ride_time = ride.from_time.split(sep=':')
                ride_date = ride.date.split(sep='-')
                print(ride_time)
                print(ride_date)
                # TODO FIX FORMATS mont and day check console
                if int(ride_date[1]) < 10: ride_date[1].replace('0', '')
                if int(ride_date[2]) < 10: ride_date[2].replace('0', '')
                if (ride_time[0] == time_now_hour and ride_time[1] == time_now_minute):
                    print("time same")
                    if (ride_date[0] == date_now_year and ride_date[1] == date_now_month and ride_date[2] == date_now_day):
                        print("date same")
                        bcc.closeRide(ride.id, ride.driver.eth_address)
                        # TODO PAY CONTRACT
            time.sleep(segundos)

    def bid(self, user, amount, ride_id):
        if (ride_id == '' or amount == ''):
            tkinter.messagebox.showwarning(title="Warning!",
                                           message="Be sure to select a ride AND amount to be able to bid!")
            return
        ride_id = int(ride_id)
        amount = int(amount)
        print("Rideid:" + str(ride_id))
        print("Amount: " + str(amount))
        print("Bidding...")
        bid_state = bcc.bidForRide(user.eth_address, ride_id, amount)
        if not bid_state:
            tkinter.messagebox.showwarning(title="Warning!", message="Your bid must be higher than the highest bid!")
        else:
            user.passenger_rides.append(self.offer_rides[ride_id])
            self.updateMyRides(user)

    def saveProfile(self, username, eth_address, avatar_index):
        print("Saving Profile...")
        print(username + eth_address + str(avatar_index))
        for user in self.all_users:
            if user.eth_address == eth_address:
                self.current_user = user
                return
        self.current_user = User(username, eth_address, avatar_index)
        self.all_users.append(self.current_user)
        self.updateMyRides(self.current_user)

    def publishRide(self, ride=Ride(None, None, None, None, None, None, None)):
        if self.current_user.eth_address == '': return
        if ride.driver.driver_ride is not None:
            tkinter.messagebox.showwarning(title="Warning!",
                                           message="The driver can only have just one active ride offer!!")
            return
        self.offer_rides.append(ride)
        self.ride_id += 1
        self.updateOfferTreeView()
        bcc.publishRide(ride.driver.eth_address, ride.id, ride.from_time, ride.until_time, ride.location,
                        ride.base_cost, ride.av_seats)
        ride.driver.driver_ride = ride

    # </editor-fold>

    # <editor-fold desc="UI Elements">
    def changeAvatar(self, label, num):
        if (num + self.current_avatar > 4 or num + self.current_avatar < 0): return
        self.current_avatar += num

        new_image = Image.open(
            os.path.dirname(__file__).replace("\\", "/") + "/adol_" + str(self.current_avatar) + ".png", "r")
        new_image = new_image.resize((80, 80))
        img2 = ImageTk.PhotoImage(new_image)
        label.configure(image=img2)
        label.image = img2
        print("DebugLog: changing avatar " + str(self.current_avatar))

    def getImage(self, frame, path, size):
        ether_ico = Image.open(os.path.dirname(__file__).replace("\\", "/") + path, "r")
        ether_ico = ether_ico.resize(size)
        test = ImageTk.PhotoImage(ether_ico)
        label_ether_img = Label(frame, image=test)
        label_ether_img.image = test
        return label_ether_img

    def createTimePicker(self, frame):
        time_picker = SpinTimePickerModern(frame)
        time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Roboto", 16), hoverbg="#404040",
                                 hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#ffffff")
        time_picker.configure_separator(bg="#404040", fg="#ffffff")
        time_picker.addHours24()
        time_picker.addMinutes()
        return time_picker

    def createLocationDropDown(self, frame):
        self.current_location = StringVar(frame)
        self.current_location.set("")
        options = {
            "Álvaro Obregón",
            "Miguel Hidalgo",
            "Coyoacán",
            "Benito Juárez",
            "Magdalena Contreras",
            "Azcapotzalco",
            "Tlalpan",
            "Tlahuac",
            "Iztapalapa",
            "Venustiano Carranza",
            "Xochimilco",
            "Cuajimalpa",
            "Iztacalco",
            "Milpa Alta",
        }
        dropdown_location = OptionMenu(frame, self.current_location, *options)
        return dropdown_location

    def createAvSeatsDropDown(self, frame):
        self.current_seats = IntVar(frame)
        self.current_seats.set("")
        options = {
            1, 2, 3, 4, 5, 6
        }
        dropdown = OptionMenu(frame, self.current_seats, *options)
        return dropdown

    def getSelectedItem(self, treeview=ttk.Treeview):
        item_text = ""
        for item in treeview.selection():
            item_text = treeview.item(item, "text")
        return item_text

    def updateOfferTreeView(self):
        for i in self.offer_list.get_children():
            self.offer_list.delete(i)

        for ride in self.offer_rides:
            self.offer_list.insert('', 'end', text=str(ride.id), values=(
                str(ride.driver.avatar_index),
                str(ride.id),
                str(ride.date),
                str(ride.from_time),
                str(ride.until_time),
                str(ride.location),
                str(ride.av_seats),
                str(ride.base_cost)))

    def updateMyRides(self, user):
        for i in self.my_rides_list.get_children():
            self.my_rides_list.delete(i)
        for passenger_rides in user.passenger_rides:
            self.my_rides_list.insert('', 'end', text=str(passenger_rides.id), values=(
                str(passenger_rides.driver.avatar_index),
                str(passenger_rides.id),
                str(passenger_rides.date),
                str(passenger_rides.from_time),
                str(passenger_rides.until_time),
                str(passenger_rides.location)))

    def createListBoxRides(self, frame):
        tree = ttk.Treeview(frame, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=4)

        tree.column("# 1", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 1", text="Avatar")
        tree.column("# 2", anchor=CENTER, minwidth=0, width=32, stretch=NO)
        tree.heading("# 2", text="ID")
        tree.column("# 3", anchor=CENTER, minwidth=0, width=90, stretch=NO)
        tree.heading("# 3", text="Date")
        tree.column("# 4", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 4", text="From")
        tree.column("# 5", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 5", text="To")
        tree.column("# 6", anchor=CENTER, minwidth=0, width=80, stretch=YES)
        tree.heading("# 6", text="Location")

        # Insert the data in Treeview widget
        tree.insert('', 'end', text="-", values=('-', '-', '-', '-', '-', '-'))

        return tree

    def createListBoxOffer(self, frame):
        tree = ttk.Treeview(frame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=4)

        tree.column("# 1", anchor=CENTER, minwidth=0, width=60, stretch=YES)
        tree.heading("# 1", text="Avatar")
        tree.column("# 2", anchor=CENTER, minwidth=0, width=32, stretch=NO)
        tree.heading("# 2", text="ID")
        tree.column("# 3", anchor=CENTER, minwidth=0, width=90, stretch=NO)
        tree.heading("# 3", text="Date")
        tree.column("# 4", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 4", text="From")
        tree.column("# 5", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 5", text="To")
        tree.column("# 6", anchor=CENTER, minwidth=0, width=80, stretch=NO)
        tree.heading("# 6", text="Location")
        tree.column("# 7", anchor=CENTER, minwidth=0, width=40, stretch=YES)
        tree.heading("# 7", text="Seats")
        tree.column("# 8", anchor=CENTER, minwidth=0, width=80, stretch=YES)
        tree.heading("# 8", text="Cost")

        # Insert the data in Treeview widget
        tree.insert('', 'end', text="-", values=('-', '-', '-', '-', '-', '-', '-', '-'))

        return tree

    # </editor-fold>

    def initUI(self):
        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)
        self.master.title("CryptoRide")
        self.pack(fill=BOTH, expand=True)

        # MAIN FRAMES
        lefttopframe = LabelFrame(self, text="Ride Offer", padx=10, pady=10)
        righttopframe = LabelFrame(self, text="My Rides", padx=10, pady=10)
        leftbotframe = LabelFrame(self, text="Publish Ride", padx=10, pady=10)
        rightbotframe = LabelFrame(self, text="User", padx=10, pady=10)
        # PACK
        lefttopframe.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        righttopframe.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        leftbotframe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        rightbotframe.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Left Top Frame - OFFER RIDES
        label_offer_list = Label(lefttopframe, text="Select a ride from the list and bid the desired amount.")
        self.offer_list = self.createListBoxOffer(lefttopframe)
        label_bid = Label(lefttopframe, text="Amount: ")
        entry_bid = Entry(lefttopframe)
        btn_bid = Button(lefttopframe, text="Bid", command=lambda: self.bid(self.current_user, entry_bid.get(),
                                                                            self.getSelectedItem(self.offer_list)))

        label_offer_list.pack(side=TOP)
        self.offer_list.pack(side=TOP, padx=5, pady=5)
        label_bid.pack(side=LEFT, padx=5, pady=5)
        entry_bid.pack(side=LEFT, padx=5, pady=5)
        btn_bid.pack(side=LEFT, padx=5, pady=5)

        # Left Bot Frame - PUBLISH RIDE
        date_time_frame = Frame(leftbotframe)
        # Date entry
        label_publish_ride = Label(date_time_frame, text="Select the desired date and time to offer your ride")
        entry_date = DateEntry(date_time_frame)
        # Time entry
        # From:
        label_from_time_picker = Label(date_time_frame, text="From:")
        from_time_picker = self.createTimePicker(date_time_frame)
        # To:
        label_to_time_picker = Label(date_time_frame, text="To:")
        timepicker_to = self.createTimePicker(date_time_frame)
        # PACK
        label_publish_ride.pack(side=LEFT, expand=True, fill=BOTH)
        entry_date.pack(side=LEFT, expand=True, fill=BOTH)
        label_from_time_picker.pack(side=LEFT, expand=True, fill=BOTH)
        from_time_picker.pack(side=LEFT, expand=True, fill=BOTH)
        label_to_time_picker.pack(side=LEFT, expand=True, fill=BOTH)
        timepicker_to.pack(side=LEFT, expand=True, fill=BOTH)
        date_time_frame.pack()  # ---

        locations_seats_frame = Frame(leftbotframe)
        # Location entry
        label_location = Label(locations_seats_frame, text="Location:")
        dropdown_location = self.createLocationDropDown(locations_seats_frame)
        # Available seats entry
        label_av_seats = Label(locations_seats_frame, text="Available seats:")
        dropdown_av_seats = self.createAvSeatsDropDown(locations_seats_frame)
        # PACK
        label_location.pack(side=LEFT, padx=10, pady=10)
        dropdown_location.pack(side=LEFT, padx=10, pady=10)
        label_av_seats.pack(side=LEFT, padx=10, pady=10)
        dropdown_av_seats.pack(side=LEFT, padx=10, pady=10)
        locations_seats_frame.pack()

        cost_frame = Frame(leftbotframe)
        # Cost
        label_cost = Label(cost_frame, text="Cost:")
        entry_cost = Entry(cost_frame)
        label_ether_img = self.getImage(cost_frame, "/eth_ico.ico", (32, 32))
        # PACK
        label_cost.pack(side=LEFT, padx=10, pady=10)
        entry_cost.pack(side=LEFT, padx=10, pady=10)
        label_ether_img.pack(side=LEFT, padx=10, pady=10)
        cost_frame.pack()
        # Button to publish the ride!
        button_publish_ride = Button(leftbotframe, text="Publish ride offer",
                                     command=lambda: self.publishRide(
                                         Ride(
                                             int(self.ride_id),
                                             int(self.current_seats.get()),
                                             str(entry_date.get_date()),
                                             str(from_time_picker.hours24()) + ":" + str(from_time_picker.minutes()),
                                             str(timepicker_to.time()[0]) + ":" + str(timepicker_to.time()[1]),
                                             int(entry_cost.get()),
                                             str(self.current_location.get()),
                                             self.current_user
                                         )))
        button_publish_ride.pack()

        # Right Top Frame - MY RIDES
        label_my_rides = Label(righttopframe, text="My rides")
        self.my_rides_list = self.createListBoxRides(righttopframe)
        label_my_rides.pack()
        self.my_rides_list.pack(fill=BOTH, expand=YES)

        # Right Bot Frame
        select_avatar_frame = Frame(rightbotframe)
        user_frame = Frame(rightbotframe)
        save_load_frame = Frame(rightbotframe)
        # PACK
        select_avatar_frame.pack()
        user_frame.pack()
        save_load_frame.pack()
        # Avatar selector
        label_avatar_img = self.getImage(select_avatar_frame, "/adol_" + str(self.current_avatar) + ".png", (80, 80))
        button_left_user = Button(select_avatar_frame, text=" < ",
                                  command=lambda: self.changeAvatar(label_avatar_img, -1))
        button_right_user = Button(select_avatar_frame, text=" > ",
                                   command=lambda: self.changeAvatar(label_avatar_img, +1))
        # PACK
        button_left_user.pack(side=LEFT, expand=YES, padx=10, pady=10)
        label_avatar_img.pack(side=LEFT, expand=YES, padx=10, pady=10)
        button_right_user.pack(side=LEFT, expand=YES, padx=10, pady=10)
        # User
        label_username = Label(user_frame, text="Username:")
        entry_username = Entry(user_frame, width=45)
        label_eth_address = Label(user_frame, text="Ethereum address:")
        entry_eth_address = Entry(user_frame, width=45)
        # PACK
        label_username.grid(row=0, column=0, padx=10, pady=10)
        entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        label_eth_address.grid(row=1, column=0, padx=10, pady=10)
        entry_eth_address.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        # Save and load buttons

        button_save = Button(save_load_frame, text="Save profile",
                             command=lambda: self.saveProfile(entry_username.get(),
                                                              entry_eth_address.get(),
                                                              self.current_avatar
                                                              ))
        button_save.grid(row=0, column=1, padx=10, pady=10)


def exportWallet():
    print("Exporting Wallet...")
    # TODO IMPLEMENT


def loadWallet():
    print("Loading Wallet...")
    # TODO IMPLEMENT


def main():
    root = Tk()
    root.resizable(width=False, height=False)
    app = Example()
    root.mainloop()


def initBlockChain():
    bcc.deployContract()


if __name__ == '__main__':
    initBlockChain()
    main()
