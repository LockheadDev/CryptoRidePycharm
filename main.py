from tkinter import *
from tkinter.constants import CENTER, COMMAND, Y
from tkinter.ttk import Frame, Label, Entry
from tkinter import ttk
from tkcalendar import DateEntry
from tktimepicker import AnalogPicker, SpinTimePickerModern, SpinTimePickerOld
from PIL import Image, ImageTk


class Example(Frame):

    def __init__(self):
        #CLASS global variables
        self.current_avatar = 0
        super().__init__()
        self.initUI()

    def changeAvatar(self,label,num):
        if(num+self.current_avatar > 4 or num+self.current_avatar<0):return
        self.current_avatar += num

        new_image =Image.open("C:\\Users\\hrswf\\PycharmProjects\\CryptoRidePycharm\\adol_" + str(self.current_avatar) + ".png")
        new_image = new_image.resize((80,80))
        img2 = ImageTk.PhotoImage(new_image)
        label.configure(image=img2)
        label.image =img2
        print("DebugLog: changing avatar " + str(self.current_avatar))

    def getImage(self,frame,path,size):
        ether_ico = Image.open(path)
        ether_ico = ether_ico.resize(size)
        test = ImageTk.PhotoImage(ether_ico)
        label_ether_img = Label(frame, image=test)
        label_ether_img.image = test
        return  label_ether_img

    def createTimePicker(self,frame):
        time_picker = SpinTimePickerModern(frame)
        time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Roboto", 16), hoverbg="#404040",
                                 hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#ffffff")
        time_picker.configure_separator(bg="#404040", fg="#ffffff")
        time_picker.addHours24()
        time_picker.addMinutes()
        return time_picker

    def createLocationDropDown(self,frame):
        variable = StringVar(frame)
        variable.set("Select")
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
        dropdown_location = OptionMenu(frame, variable, *options)
        return dropdown_location

    def createAvSeatsDropDown(self,frame):
        variable = IntVar(frame)
        variable.set("Select")
        options = {
            1,2,3,4,5,6
        }
        dropdown = OptionMenu(frame, variable, *options)
        return dropdown

    def createListBox(self, frame):
        tree = ttk.Treeview(frame, column=("c1", "c2", "c3"), show='headings', height=5)

        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="FName")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="LName")

        # Insert the data in Treeview widget
        tree.insert('', 'end', text="1", values=('1', 'Joe', 'Nash'))
        tree.insert('', 'end', text="2", values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', text="3", values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', text="4", values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', text="5", values=('5', 'Stephan', 'Heyward'))

        return tree

    def initUI(self):
        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)

        self.master.title("CryptoRide")
        self.pack(fill=BOTH, expand=True)

        # MAIN FRAMES
        lefttopframe = LabelFrame(self, text="Ride Offer", padx=15, pady=15)
        righttopframe = LabelFrame(self, text="My Rides", padx=15, pady=15)
        leftbotframe = LabelFrame(self, text="Publish Ride", padx=15, pady=15)
        rightbotframe = LabelFrame(self, text="User", padx=15, pady=15)
            #PACK
        lefttopframe.grid(row=0, column=0, sticky="nsew")
        righttopframe.grid(row=0, column=1, sticky="nsew")
        leftbotframe.grid(row=1, column=0, sticky="nsew")
        rightbotframe.grid(row=1, column=1, sticky="nsew")

        # Left Top Frame - OFFER RIDES
        offerlistview = self.createListBox(lefttopframe)
        offerlistview.grid(row=0, column=0)
        btnbid = Button(lefttopframe, text="Bid", command=bid)
        btnbid.grid(row=1, column=0)

        # Left Bot Frame - PUBLISH RIDE
        date_time_frame = Frame(leftbotframe)
            #Date entry
        publishridelabel = Label(date_time_frame, text = "Select the desired date and time to offer your ride")
        dateentry = DateEntry(date_time_frame)
            #Time entry
                #From:
        label_from_time_picker = Label(date_time_frame,text = "From:")
        from_time_picker = self.createTimePicker(date_time_frame)
                #To:
        label_to_time_picker = Label(date_time_frame,text = "To:")
        timepicker_to = self.createTimePicker(date_time_frame)
            #PACK
        publishridelabel.pack(side=LEFT, expand=True, fill=BOTH)
        dateentry.pack(side=LEFT, expand=True, fill=BOTH)
        label_from_time_picker.pack(side = LEFT, expand = True, fill = BOTH)
        from_time_picker.pack(side = LEFT, expand = True, fill = BOTH)
        label_to_time_picker.pack(side = LEFT, expand = True, fill = BOTH)
        timepicker_to.pack(side = LEFT, expand = True, fill = BOTH)
        date_time_frame.pack()  # ---

        locations_seats_frame = Frame(leftbotframe)
            #Location entry
        label_location = Label(locations_seats_frame, text="Location:")
        dropdown_location = self.createLocationDropDown(locations_seats_frame)
            #Available seats entry
        label_av_seats =Label(locations_seats_frame, text="Available seats:")
        dropdown_av_seats = self.createAvSeatsDropDown(locations_seats_frame)
            #PACK
        label_location.pack(side=LEFT, padx=10, pady=10)
        dropdown_location.pack(side=LEFT, padx=10, pady=10)
        label_av_seats.pack(side=LEFT, padx=10, pady=10)
        dropdown_av_seats.pack(side=LEFT, padx=10, pady=10)
        locations_seats_frame.pack()

        cost_frame = Frame(leftbotframe)
            #Cost
        label_cost = Label(cost_frame, text="Cost:")
        entry_cost = Entry(cost_frame)
        label_ether_img = self.getImage(cost_frame,"C:\\Users\\hrswf\\PycharmProjects\\CryptoRidePycharm\\eth_ico.ico",(32,32)) #TODO - MAKE RELATIVE PATH
            #PACK
        label_cost.pack(side=LEFT, padx=10, pady=10)
        entry_cost.pack(side=LEFT, padx=10, pady=10)
        label_ether_img.pack(side=LEFT, padx=10, pady=10)
        cost_frame.pack()
            #Button to publish the ride!
        button_publish_ride = Button(leftbotframe, text="Publish ride offer", command=publishRide)
        button_publish_ride.pack()

        # Right Top Frame
        myrideslistview = self.createListBox(righttopframe)
        myrideslistview.pack()

        # Right Bot Frame
        select_avatar_frame = Frame(rightbotframe)
        select_avatar_frame.pack()
            # Avatar selector

        label_avatar_img = self.getImage(select_avatar_frame,"C:\\Users\\hrswf\\PycharmProjects\\CryptoRidePycharm\\adol_"+str(self.current_avatar) + ".png",(80,80))
        button_left_user = Button(select_avatar_frame, text=" < ",command=lambda: self.changeAvatar(label_avatar_img, -1))
        button_right_user =Button(select_avatar_frame,text= " > ",command=lambda:self.changeAvatar(label_avatar_img,+1))
            #PACK
        button_left_user.pack(side=LEFT, expand=YES, padx=10, pady=10)
        label_avatar_img.pack(side=LEFT, expand=YES, padx=10, pady=10)
        button_right_user.pack(side=LEFT, expand=YES, padx=10, pady=10)

def bid():
    print("bidding")
    #TODO IMPLEMENT

def publishRide():
    print("Publishing ride...")
    #TODO IMPLEMENT
def main():
    root = Tk()
    root.geometry("1000x600+100+100")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()