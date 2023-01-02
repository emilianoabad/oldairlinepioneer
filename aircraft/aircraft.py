class Aircraft:
    def __init__(self, model, registration_prefix, range, speed, fuel_consumption, passenger_capacity, price, launch_date, complete_name, short_name):
        self.model = model
        self.registration_prefix = registration_prefix
        self.range = range
        self.speed = speed
        self.fuel_consumption = fuel_consumption
        self.passenger_capacity = passenger_capacity
        self.price = price
        self.launch_date = launch_date
        self.complete_name = complete_name
        self.short_name = short_name
        self.assigned_flight = None
