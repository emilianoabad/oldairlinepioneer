def calculate_flight_time(distance, speed):
    """
    Calculates the flight time for a given distance and speed.

    Parameters:
        distance (int): The distance to be traveled in kilometers.
        speed (int): The speed at which the distance will be traveled in kilometers per hour.

    Returns:
        int: The flight time in hours.
    """
    return distance / speed

def calculate_profits_and_costs(flight):
    """
    Calculates the profits and costs for a given flight.
    Parameters:
        demand (int): The demand for the flight in thousands of passengers.
        load_factor (float): The load factor for the flight as a percentage.
        distance (int): The distance of the flight in kilometers.
        aircraft (Aircraft): The aircraft used for the flight.
        fuel_price (float): The price of fuel in dollars per gallon.
    Returns:
        tuple: A tuple containing the profits and costs for the flight in dollars.
    """
    demand = flight.demand
    load_factor = flight.load_factor
    distance = flight.distance
    aircraft = flight.aircraft
    fuel_price = flight.fuel_price
    passenger_revenue = demand * load_factor * 100
    fuel_cost = distance * aircraft.model["fuel_consumption"] * fuel_price / 100
    maintenance_cost = aircraft.model["price"] * 0.01
    total_cost = fuel_cost + maintenance_cost
    profits = passenger_revenue - total_cost
    return profits, total_cost