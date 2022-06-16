import BlockChainController as bcc
class User:
    def __init__(self, username,password, eth_address, avatar_index):
        self.username = username
        self.password = password
        self.eth_address = eth_address
        self.avatar_index = avatar_index
        self.driver_ride = None
        self.passenger_rides = []


class Ride:
    def __init__(self, id, av_seats, date, from_time, until_time, base_cost, location, driver=User("","","","")):
        self.id = id
        self.av_seats = av_seats
        self.driver = driver
        self.date = date
        self.from_time = from_time
        self.until_time = until_time
        self.base_cost = base_cost
        self.location = location
