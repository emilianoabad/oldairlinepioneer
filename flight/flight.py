class Flight:
    def __init__(self, flight_number, departure_airport, arrival_airport, distance, demand):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.distance = distance
        self.demand = int(demand / 1000)  # Convert demand to an integer between 0 and 5
        self.passengers = 0
        self.load_factor = 0
        self.profits = 0
        self.costs = 0

    def add_passengers(self, passengers):
        self.passengers += passengers
        self.load_factor = self.passengers / (self.aircraft.model["passenger_capacity"] * self.demand)

    def calculate_ticket_price(self):
        base_price = self.distance / 100  # base price is $1 per 100 km
        demand_factor = (1 + self.demand)  # demand factor increases with demand
        ticket_price = base_price * demand_factor  # final ticket price is the base price multiplied by the demand factor
        return ticket_price
