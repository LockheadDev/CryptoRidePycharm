import pickle
from datetime import *
import threading
import tkinter.messagebox
from tkinter import *
from tkinter.constants import CENTER
from tkinter.ttk import Frame, Label, Entry
from tkinter import ttk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from PIL import Image, ImageTk
import BlockChainController as bcc
from classes import Ride, User
import os
import time


# TODO - UPDATE COST VALUE IN TREEVIEW AFTER BID


class Example(Frame):

    # INIT
    def __init__(self):
        self.all_users = []
        self.offer_rides = []
        if os.path.getsize("all_users.pickle") > 0:
            with open("all_users.pickle", "rb") as f:
                self.all_users = pickle.load(f)
        if os.path.getsize("offer_rides.pickle") > 0:
            with open("offer_rides.pickle", "rb") as f:
                self.offer_rides = pickle.load(f)

        # GUI ELEMENTS
        self.label_avatar_img = Label()
        self.label_avatar_img_main = Label()
        self.widgets_publish_ride = []
        self.ride_id = 0
        self.current_avatar = 0
        self.current_location = None
        self.current_seats = None
        self.offer_list = ttk.Treeview
        self.thread = threading.Thread(target=self.checkContractDateTime, args=(30,))
        self.thread.start()
        self.isCreatingUser = False
        self.isLogging = False

        # BACKEND ELEMENTS
        self.current_user = User("", "", "", "")


        #vars
        self.username_var = StringVar()
        self.eth_address_var = StringVar()
        self.avatar_var = StringVar()
        self.username_var.set(self.current_user.username)
        self.eth_address_var.set(self.current_user.eth_address)
        self.avatar_var.set(self.current_user.avatar_index)
        super().__init__()
        self.avatar_var.trace("w",self.updateAvatar)
        self.initUI()


    # <editor-fold desc="Backend">
    def checkContractDateTime(self, segundos):
        while True:
            print("--CHECKING PUBLSIHED RIDES--")
            now = datetime.now()
            time_now_hour = now.hour
            time_now_minute = now.minute
            date_now_year = now.year
            date_now_month = now.month
            date_now_day = now.day

            print("Hour: " + str(time_now_hour))
            print("Minute: " + str(time_now_minute))
            print("Year: " + str(date_now_year))
            print("Month: " + str(date_now_month))
            print("Day: " + str(date_now_day))

            for ride in self.offer_rides:
                print("Checking ride: " + str(ride.id))
                ride_time = ride.from_time.split(sep=':')
                ride_date = ride.date.split(sep='-')
                print(ride_time)
                print(ride_date)
                if (int(ride_time[0]) <= time_now_hour and int(ride_time[1]) <= time_now_minute):
                    print("time same")
                    if (int(ride_date[0]) <= date_now_year and int(ride_date[1]) <= date_now_month and int(
                            ride_date[2]) <= date_now_day):
                        print("date same")
                        ride.driver.driver_ride = None
                        bcc.closeRide(ride.id, ride.driver.eth_address)
                        bcc.payRide(ride.id, ride.driver.eth_address)
                        self.deleteRideFromList(ride.id)
            time.sleep(segundos)

    def bid(self, user, amount, ride_id):
        print()
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
            self.offer_rides[int(ride_id)].base_cost = amount  # actualizamos precio dependiendo del highest bid
            self.updateMyRides(user)
            self.updateOfferTreeView()

    def loginWindow(self):
        if self.isLogging: return
        self.isLogging = True
        login_window = Toplevel()
        login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closingUserLogin(login_window))
        user_frame = Frame(login_window)
        save_load_frame = Frame(login_window)
        # PACK
        user_frame.pack()
        save_load_frame.pack()
        # User
        label_username = Label(user_frame, text="Username:")
        entry_username = Entry(user_frame, width=45)
        label_password = Label(user_frame, text="Password:")
        entry_password = Entry(user_frame, width=45, show="*")
        # PACK
        label_username.grid(row=0, column=0, padx=10, pady=10)
        entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        label_password.grid(row=1, column=0, padx=10, pady=10)
        entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        # Save and load buttons

        button_save = Button(save_load_frame, text="Login",
                             command=lambda: self.login(entry_username.get(),
                                                        entry_password.get(),
                                                        login_window))
        button_save.grid(row=0, column=0, padx=10, pady=10)

    def login(self, username, password, view):
        print("Logging...")
        for user in self.all_users:
            if user.username == username and user.password == password:
                self.current_user = user
                self.isLogging = False
                self.eth_address_var.set(user.eth_address)
                self.username_var.set(user.username)
                self.avatar_var.set(user.avatar_index)
                self.updateMyRides(user)
                print("->User avatar index: " + str(user.avatar_index))
                self.current_avatar = user.avatar_index
                self.avatar_var.set(user.avatar_index)
                view.destroy()
                return
        tkinter.messagebox.showwarning(title="Warning!", message="User not found!")

    def createUser(self, username, password, eth_address,avatar_index, view):
        print("Creating new user...")
        if (username == "" or password == "" or eth_address == ""):
            tkinter.messagebox.showwarning(title="Warning!", message="You must fill al fields correctly!")
            return
        for user in self.all_users:
            if user.eth_address == eth_address:
                tkinter.messagebox.showwarning(title="Warning!", message="This ethereum address is already in use!")
                return

        self.current_user = User(username, password, eth_address, avatar_index)
        self.all_users.append(self.current_user)
        self.isCreatingUser = False
        #SAVE USER IN FILE
        with open("all_users.pickle", "wb") as f:
            pickle.dump(self.all_users, f)
        view.destroy()

    def signUp(self):
        if self.isCreatingUser: return
        self.isCreatingUser = True
        print("Signing up...")
        sign_up_window = Toplevel()
        sign_up_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closingUserCreate(sign_up_window))
        sign_up_window.title = "New profile"

        select_avatar_frame = Frame(sign_up_window)
        user_frame = Frame(sign_up_window)
        save_load_frame = Frame(sign_up_window)
        # PACK
        select_avatar_frame.pack()
        user_frame.pack()
        save_load_frame.pack()
        # Avatar selector
        self.label_avatar_img = self.getImage(select_avatar_frame, "/adol_" + str(self.current_avatar) + ".png", (80, 80))
        button_left_user = Button(select_avatar_frame, text=" < ",
                                  command=lambda: self.changeAvatar(self.label_avatar_img, -1))
        button_right_user = Button(select_avatar_frame, text=" > ",
                                   command=lambda: self.changeAvatar(self.label_avatar_img, +1))
        # PACK
        button_left_user.pack(side=LEFT, expand=YES, padx=10, pady=10)
        self.label_avatar_img.pack(side=LEFT, expand=YES, padx=10, pady=10)
        button_right_user.pack(side=LEFT, expand=YES, padx=10, pady=10)
        # User
        label_username = Label(user_frame, text="Username:")
        entry_username = Entry(user_frame, width=45)
        label_password = Label(user_frame, text="Password:")
        entry_password = Entry(user_frame, width=45, show="*")
        label_eth_address = Label(user_frame, text="Ethereum address:")
        entry_eth_address = Entry(user_frame, width=45)

        # PACK
        label_username.grid(row=0, column=0, padx=10, pady=10)
        entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        label_password.grid(row=1, column=0, padx=10, pady=10)
        entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        label_eth_address.grid(row=2, column=0, padx=10, pady=10)
        entry_eth_address.grid(row=2, column=1, padx=10, pady=10, sticky="W")

        button_new_profile = Button(save_load_frame, text="Create user",
                                    command=lambda: self.createUser(entry_username.get(), entry_password.get(),
                                                                    entry_eth_address.get(),self.current_avatar, sign_up_window))
        button_new_profile.grid(row=0, column=0, padx=10, pady=10)

        sign_up_window.mainloop()

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
    def on_closingUserCreate(self, view):
        self.isCreatingUser = False
        view.destroy()
        pass

    def on_closingUserLogin(self, view):
        self.isLogging = False
        view.destroy()
        pass

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

    def deleteRideFromList(self, id):
        the_ride = None
        for ride in self.offer_rides:
            if (ride.id == id): the_ride = ride
        self.offer_rides.remove(the_ride)
        self.updateOfferTreeView()

    def getSelectedItem(self, treeview=ttk.Treeview):
        item_text = ""
        for item in treeview.selection():
            item_text = treeview.item(item, "text")
        return item_text

    def updateAvatar(self,*args):
        print("Updating Avatar..."+ str(self.avatar_var.get()))
        new_image = Image.open(
            os.path.dirname(__file__).replace("\\", "/") + "/adol_" + str(self.avatar_var.get()) + ".png", "r")
        new_image = new_image.resize((80, 80))
        img2 = ImageTk.PhotoImage(new_image)
        self.label_avatar_img.configure(image=img2)
        self.label_avatar_img.image = img2

    def updateOfferTreeView(self):
        #save offer rides
        with open("offer_rides.pickle", "wb") as f:
            pickle.dump(self.offer_rides, f)

        for i in self.offer_list.get_children():
            self.offer_list.delete(i)

        for ride in self.offer_rides:
            image_path = os.path.dirname(__file__).replace("\\", "/") + "/adol_" + str(ride.driver.avatar_index)+".png"
            image = tkinter.PhotoImage(file=image_path)
            self.offer_list.insert('', 'end',text=str(ride.id), values=(
                image,
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
        tree = ttk.Treeview(frame,selectmode='browse', columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=4)

        img_canada_flag = Image.open(os.path.dirname(__file__).replace("\\", "/") + "/adol_0.png")
        img_canada_flag = img_canada_flag.resize((42, 42))

        # Convert the JPG image to a PhotoImage instance that tkinter can use.
        image_tk = ImageTk.PhotoImage(img_canada_flag)

        # Insert the data in Treeview widget
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

        tree.insert('', 'end', text="-", values=('-', '-', '-', '-', '-', '-'))

        return tree

    def createListBoxOffer(self, frame):
        tree = ttk.Treeview(frame,selectmode='browse', columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=20)

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

        image_path = os.path.dirname(__file__).replace("\\", "/") + "/adol_0.png"
        print(image_path)

        img_canada_flag = Image.open(image_path)
        img_canada_flag.resize((20,20))
        image_tk = ImageTk.PhotoImage(img_canada_flag)
        tree.insert(parent='', index='end',image=image_tk, values=('-', '-', '-', '-', '-', '-', '-'))

        return tree

    def createLeftBotFrame(self, leftbotframe):
        _list = []
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
                                         )
                                     )
                                     )  # TODO ERASE LEFTBOTFRAME STATUS
        button_publish_ride.pack()

    def createRightTopFrame(self, righttopframe):
        label_my_rides = Label(righttopframe, text="My rides")
        self.my_rides_list = self.createListBoxRides(righttopframe)
        label_my_rides.pack()
        self.my_rides_list.pack(fill=BOTH, expand=YES)

    def createRightBotFrame(self, rightbotframe):
        select_avatar_frame = Frame(rightbotframe)
        user_frame = Frame(rightbotframe)
        login_sign_frame = Frame(rightbotframe)
        # PACK
        select_avatar_frame.pack()
        user_frame.pack()
        login_sign_frame.pack()
        # Avatar selector
        self.label_avatar_img = self.getImage(select_avatar_frame, "/adol_" + str(self.current_avatar) + ".png", (80, 80))

        # PACK
        self.label_avatar_img.pack(side=TOP, expand=YES, padx=10, pady=10)

        # User
        label_username = Label(user_frame, text="-USERNAME-",textvariable=self.username_var)
        label_eth_address = Label(user_frame, text="-ETHEREUM ADDRESS-",textvariable=self.eth_address_var)

        # PACK
        label_username.grid(row=0, column=0, padx=10, pady=10)

        label_eth_address.grid(row=1, column=0, padx=10, pady=10)

        # Save and load buttons
        button_login = Button(login_sign_frame, text="Login",
                              command=lambda: self.loginWindow())
        button_new_profile = Button(login_sign_frame, text="Sign Up",
                                    command=lambda: self.signUp())

        button_login.grid(row=0, column=0, padx=10, pady=10)
        button_new_profile.grid(row=0, column=1, padx=10, pady=10)

    def createLeftTopFrame(self, lefttopframe):
        label_offer_list = Label(lefttopframe, text="Select a ride from the list and bid the desired amount.")
        self.offer_list = self.createListBoxOffer(lefttopframe)
        label_bid = Label(lefttopframe, text="Amount: ")
        entry_bid = Entry(lefttopframe)
        btn_bid = Button(lefttopframe, text="Bid", command=lambda: self.bid(self.current_user, entry_bid.get(),
                                                                            self.getSelectedItem(self.offer_list)))

        label_offer_list.pack(side=TOP)
        self.offer_list.pack(expand=YES, fill=BOTH,side=TOP, padx=5, pady=5)
        label_bid.pack(side=LEFT, padx=5, pady=5)
        entry_bid.pack(side=LEFT, padx=5, pady=5)
        btn_bid.pack(side=LEFT, padx=5, pady=5)
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
        self.createLeftTopFrame(lefttopframe)

        # Left Bot Frame - PUBLISH RIDE
        self.createLeftBotFrame(leftbotframe)

        # Right Top Frame - MY RIDES
        self.createRightTopFrame(righttopframe)

        # Right Bot Frame -LOGIN
        self.createRightBotFrame(rightbotframe)

        if(len(self.offer_rides)>0):
            self.updateOfferTreeView()


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
