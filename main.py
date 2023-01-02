import sys
sys.path.append("airline/")
sys.path.append("aircraft/")
sys.path.append("flight/")
sys.path.append('.')


import os

from airline import Airline
from aircraft import Aircraft
from flight import Flight
from constants import FUEL_PRICES, DEMAND_LEVELS, AIRCRAFT_MODELS
from helper_functions import calculate_flight_time, calculate_profits_and_costs

def main():
    # Initialize the game
    print("  /$$$$$$  /$$           /$$ /$$                                ")
    print(" /$$__  $$|__/          | $$|__/                                ")
    print("| $$  \ $$ /$$  /$$$$$$ | $$ /$$ /$$$$$$$   /$$$$$$             ")
    print("| $$$$$$$$| $$ /$$__  $$| $$| $$| $$__  $$ /$$__  $$            ")
    print("| $$__  $$| $$| $$  \__/| $$| $$| $$  \ $$| $$$$$$$$            ")
    print("| $$  | $$| $$| $$      | $$| $$| $$  | $$| $$_____/            ")
    print("| $$  | $$| $$| $$      | $$| $$| $$  | $$|  $$$$$$$            ")
    print("|__/  |__/|__/|__/      |__/|__/|__/  |__/ \_______/            ")                                                                                                                                                                                            
    print(" /$$$$$$$  /$$                                                  ")
    print("| $$__  $$|__/                                                  ")
    print("| $$  \ $$ /$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ ")
    print("| $$$$$$$/| $$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$")
    print("| $$____/ | $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$$$$$$$| $$  \__/")
    print("| $$      | $$| $$  | $$| $$  | $$| $$_____/| $$_____/| $$      ")
    print("| $$      | $$|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$      ")
    print("|__/      |__/ \______/ |__/  |__/ \_______/ \_______/|__/      ")
    print("")                                                       
    print("Welcome to Airline Pioneer!")
    print("")
    print("Select an airline to manage:")
    print("1. American Airlines (based in DFW)")
    print("2. PanAm (based in JFK)")
    print("3. Lufthansa (based in FRA)")
    print("4. Air France (based in CDG)")
    print("5. Varig (based in GRU)")
    print("")
    selection = input("Enter the number of the airline you want to manage: ")
    selection = str(selection)
    if selection == "1":
        airline = Airline("American Airlines", "DFW", 15000000, FUEL_PRICES)
    elif selection == "2":
        airline = Airline("PanAm", "JFK", 15000000, FUEL_PRICES)
    elif selection == "3":
        airline = Airline("Lufthansa", "FRA", 15000000, FUEL_PRICES)
    elif selection == "4":
        airline = Airline("Air France", "CDG", 15000000, FUEL_PRICES)
    elif selection == "5":
        airline = Airline("Varig", "GRU", 15000000, FUEL_PRICES)
    else:
        print("Invalid selection. Exiting game.")
        return
    # Initialize command to an empty string
    command = ""

    # Main game loop
    while True:
         # Get user input
        command = input("Enter a command: ").strip()

        # Handle aircraft catalogue command
        if command == "aircraft catalogue":
            print("Aircraft Catalogue:")
            print("Short Name | Range (km) | Speed (km/h) | Fuel Consumption (kg/h) | Passengers | Price ($M) | Launch Date | Complete Name")
            for model in AIRCRAFT_MODELS:
                print("{} | {} | {} | {} | {} | {} | {} | {}".format(model["short_name"], model["range"], model["speed"], model["fuel_consumption"], model["passenger_capacity"], model["price"], model["launch_date"], model["complete_name"]))

        # Handle aircraft fleet command
        elif command == "aircraft fleet":
            print("Aircraft Fleet:")
            print("Short Name | Range (km) | Speed (km/h) | Fuel Consumption (kg/h) | Passengers | Price ($M) | Launch Date | Complete Name | Registration Prefix | Assigned Flight")
            for aircraft in airline.fleet:
                print("{} | {} | {} | {} | {} | {} | {} | {} | {} | {}".format(aircraft.model.short_name, aircraft.model.range, aircraft.model.speed, aircraft.model.fuel_consumption, aircraft.model.passenger_capacity, aircraft.model.price, aircraft.model.launch_date, aircraft.model.complete_name, aircraft.registration_prefix, aircraft.assigned_flight))

        # Handle aircraft sell command
        elif command.startswith("aircraft sell"):
            words = command.split()
            if len(words) < 2:
                print("Invalid command. Please specify the registration prefix of the aircraft you want to sell.")
            else:
                registration_prefix = words[2]
                success = airline.sell_aircraft(registration_prefix)
                if not success:
                    print("Sell failed. The specified aircraft does not exist in your fleet.")

       # Handle aircraft buy command
        elif command.startswith("aircraft buy"):
            words = command.split()
            if len(words) < 3:
                print("Invalid command. Please specify the short name of the aircraft you want to buy and the quantity (optional).")
            else:
                short_name = str(words[2])
                model = next((model for model in AIRCRAFT_MODELS if model["short_name"] == short_name), None)
                if model is None:
                    print("Invalid short name. Please enter a valid short name.")
                else:
                    if len(words) >= 5:
                        try:
                            quantity = int(words[4])
                        except ValueError:
                            print("Invalid quantity. Please enter a valid quantity.")
                    else:
                        quantity = 1
                    cost = model["price"] * quantity
                    if cost > airline.bank_balance:
                        print("You don't have enough money to buy {} aircraft of this model.".format(quantity))
                    else:
                        for i in range(quantity):
                            aircraft = Aircraft(
                                model=model,
                                registration_prefix=airline._generate_registration_prefix(),
                                range=model['range'],
                                speed=model['speed'],
                                fuel_consumption=model['fuel_consumption'],
                                passenger_capacity=model['passenger_capacity'],
                                price=model['price'],
                                launch_date=model['launch_date'],
                                complete_name=model['complete_name'],
                                short_name=model['short_name'],
                            )
                            airline.buy_aircraft(aircraft, quantity)


        # Handle flight create command
        elif command.startswith("flight create"):
            words = command.split()
            if len(words) < 3:
                print("Invalid command. Please specify the departure and arrival airports.")
            else:
                departure_airport = words[2]
                arrival_airport = words[3]
                # Call the create_flight method of the airline object
                result = airline.create_flight(departure_airport, arrival_airport)
                # If the create_flight method returns a string, it is an error message
                if isinstance(result, str):
                    print(result)
                # If the create_flight method returns a flight number, it means the flight was successfully created
                else:
                    print("Flight created successfully. Flight number: {}".format(result))


        # Handle list flights command
        elif command == "flight list":
            print("Flight List:")
            print("Flight Number | Departure Airport | Arrival Airport | Distance (km) | Demand")
            for flight in airline.flights:
                print("{} | {}-{} | Distance: {} | {}".format(flight.flight_number, flight.departure_airport["code"], flight.arrival_airport["code"], flight.distance, flight.demand))


        # Handle flight cancel command
        elif command.startswith("flight cancel"):
            words = command.split()
            if len(words) < 2:
                print("Invalid command. Please specify the flight number of the flight you want to cancel.")
            else:
                flight_number = words[2]
                success = airline.cancel_flight(flight_number)
                if success:
                    print(f"Flight {flight_number} was successfully cancelled.")
                else:
                    print(f"Flight {flight_number} does not exist.")


        # Handle aircraft assign command
        elif command.startswith("aircraft assign"):
            words = command.split()
            if len(words) < 3:
                print("Invalid command. Please specify the registration prefix of the aircraft you want to assign and the flight number.")
            else:
                registration_prefix = words[2]
                flight_number = words[3]
                success = airline.assign_aircraft(registration_prefix, flight_number)
                if not success:
                    print("Aircraft assignment failed. The specified aircraft or flight do not exist.")

        # Handle balance command
        elif command == "balance":
            print("Current balance: ${}".format(airline.bank_balance))

        # Handle fuel price command
        elif command == "fuel price":
            year = 1950 + airline.fuel_price_index
            fuel_price = FUEL_PRICES[str(year)]
            print("Current fuel price: ${} per gallon".format(fuel_price))

       # Handle end turn command
        elif command == "end turn":
            profits = 0
            costs = 0 
            # Simulate the next month of operations
            for aircraft in airline.fleet:
                if aircraft.assigned_flight:  # Only consider aircraft with an assigned flight
                    flight = None
                    for f in airline.flights:  # Find the Flight object with the matching flight number
                        if f.flight_number == aircraft.assigned_flight:
                            flight = f
                            break
                    if flight is None:
                        print("Error: Flight not found")
                        continue
                    demand = DEMAND_LEVELS[flight.demand]  # Get the demand for the flight
                    flight.demand = demand
                    # Get the current year as a string
                    current_year = list(FUEL_PRICES.keys())[airline.fuel_price_index % len(FUEL_PRICES)]
                    # Get the fuel price for the current year
                    flight.fuel_price = FUEL_PRICES[current_year]
                    # Calculate profits and costs for this flight
                    flight_profits, flight_costs = airline.calculate_profits_and_costs(demand, flight.load_factor, flight.distance, aircraft, flight.fuel_price)
                    profits += flight_profits
                    costs += flight_costs
            # Get the next fuel price index
            airline.fuel_price_index = next(iter(FUEL_PRICES), airline.fuel_price_index)
            # Update bank balance with profits and costs for the month
            airline.bank_balance += profits
            airline.bank_balance -= costs

            # Calculate and print results for the month
            print("Results for the month:")
            print("Total profits: ${}".format(profits))
            print("Total costs: ${}".format(costs))
            print("Net income: ${}".format(profits - costs))
            print("Bank balance: ${}".format(airline.bank_balance))


        # Handle invalid command
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    main()