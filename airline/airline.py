from aircraft import Aircraft
from flight import Flight
from constants import FUEL_PRICES
import math
import json


class Airline:
    def __init__(self, name, base_airport, bank_balance, fuel_prices):
        self.name = name
        self.initials = "".join([x[0] for x in self.name.split()])
        self.base_airport = base_airport
        self.bank_balance = bank_balance
        self.fleet = []
        self.flights = []
        self.flight_counter = 0  # Initialize the counter
        self.fuel_prices = fuel_prices
        self.fuel_price_index = len(FUEL_PRICES) % len(fuel_prices)

    def buy_aircraft(self, model, quantity):
        cost = model.price * quantity
        if cost > self.bank_balance:
            print("You don't have enough money to buy {} aircraft of this model.".format(quantity))
        else:
            self.bank_balance -= cost
            for i in range(quantity):
                aircraft = Aircraft(
                    model=model,
                    registration_prefix=self._generate_registration_prefix(),
                    range=model.range,
                    speed=model.speed,
                    fuel_consumption=model.fuel_consumption,
                    passenger_capacity=model.passenger_capacity,
                    price=model.price,
                    launch_date=model.launch_date,
                    complete_name=model.complete_name,
                    short_name=model.short_name,
                )
                self.fleet.append(aircraft)
            print("You have bought {} aircraft of model {}. Your bank balance is now ${}.".format(quantity, model.complete_name, self.bank_balance))


    def sell_aircraft(self, registration_prefix):
        for aircraft in self.fleet:
            if aircraft.registration_prefix == registration_prefix:
                self.fleet.remove(aircraft)
                self.bank_balance += aircraft.model["price"] * 0.9  # Sell for 90% of the original price
                return True
        return False

    def create_flight(self, departure_airport, arrival_airport):
        # Read the data from the airports.json file
        with open("data/airports.json", "r") as f:
            airports_data = json.load(f)

        # Check if the departure airport is valid
        departure_airport_found = False
        for airport in airports_data:
            if airport["code"] == departure_airport:
                departure_airport_data = airport
                departure_airport_found = True
        if not departure_airport_found:
            return ("Error: Invalid departure airport code")

        # Check if the arrival airport is valid
        arrival_airport_found = False
        for airport in airports_data:
            if airport["code"] == arrival_airport:
                arrival_airport_data = airport
                arrival_airport_found = True

        if not arrival_airport_found:
                    return ("Error: Invalid arrival airport code")

        # Check if a flight with the same departure and arrival airports already exists
        existing_flight = None
        for q in self.flights:
            if q.departure_airport["code"] == departure_airport and q.arrival_airport["code"] == arrival_airport:
                existing_flight = q
                return ("A flight from {} to {} already exists. The number is {}.".format(q.departure_airport["name"], q.arrival_airport["name"], q.flight_number))

        for q in self.flights:
            if q.departure_airport["code"] == arrival_airport and q.arrival_airport["code"] == departure_airport:
                existing_flight = q  
                return ("A flight from {} to {} already exists. The number is {}.".format(q.departure_airport["name"], q.arrival_airport["name"], q.flight_number))
                
        self.flight_counter += 1  # Increment the counter
        flight_number = f"{self.initials}-{str(self.flight_counter).zfill(4)}"  # Generate flight number

        def haversine(lat1, lon1, lat2, lon2):
            # Convert degrees to radians
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            # Calculate the difference between the two coordinates
            lat_diff = lat2 - lat1
            lon_diff = lon2 - lon1
            # Calculate the Haversine formula
            a = math.sin(lat_diff / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2
            c = 2 * math.asin(math.sqrt(a))
            # Multiply by the Earth's radius to get the distance in kilometers
            distance = 6371 * c
            return distance

        # Assign Real Data to the Airports
        distance = haversine(departure_airport_data['latitude'], departure_airport_data['longitude'], arrival_airport_data['latitude'], arrival_airport_data['longitude'])
        demand = distance * 0.1
        flight = Flight(flight_number, departure_airport_data, arrival_airport_data, distance, demand)
        self.flights.append(flight)
        return flight_number

    def cancel_flight(self, flight_number):
        for flight in self.flights:
            if flight.flight_number == flight_number:
                self.flights.remove(flight)
                for aircraft in self.fleet:
                    if aircraft.assigned_flight == flight_number:
                        aircraft.assigned_flight = None
                return True
        return False

    def assign_aircraft(self, registration_prefix, flight_number):
        for aircraft in self.fleet:
            if aircraft.registration_prefix == registration_prefix and aircraft.assigned_flight is None:
                aircraft.assigned_flight = flight_number
                return True
        return False
    
    def calculate_ticket_price(self, demand, distance):
        # Calculate the ticket price based on demand and distance
        # You can use the demand and distance to come up with your own formula for calculating the ticket price
        # For example:
        return distance * demand * 0.5


    def calculate_profits_and_costs(self, demand, load_factor, distance, aircraft, fuel_price):
        # Calculate the ticket price based on demand and distance
        ticket_price = self.calculate_ticket_price(demand, distance)

        # Calculate the number of passengers based on demand and aircraft's passenger capacity
        passengers = demand * load_factor * aircraft.passenger_capacity

        # Calculate the profits and costs
        profits = passengers * ticket_price
        costs = fuel_price * aircraft.fuel_consumption * distance / 100
        return profits, costs


    def _generate_registration_prefix(self):
        """Generate a unique aircraft registration prefix for the airline."""
        prefix = self.initials + "-"
        existing_prefixes = [x.registration_prefix for x in self.fleet]
        for i in range(1000):
            new_prefix = prefix + str(i).zfill(3)
            if new_prefix not in existing_prefixes:
                return new_prefix
        raise Exception("Could not generate a unique registration prefix. Please try again.")
