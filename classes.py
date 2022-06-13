class User:
    def __init__(self, username, eth_address, avatar_index):
        self.username = username
        self.eth_address = eth_address
        self.avatar_index = avatar_index
        self.driver_ride = None
        self.passenger_rides = []


class Ride:
    def __init__(self, id, av_seats, driver, passengers, from_time, until_time, base_cost):
        self.id = id
        self.driver = driver
        self.passengers = passengers
        self.av_seats = av_seats
        self.from_time = from_time
        self.until_time = until_time
        self.base_cost = base_cost
