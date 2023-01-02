FUEL_PRICES = {
    "1950": 0.40,
    "1951": 0.45,
    "1952": 0.50,
    "1953": 0.55,
    "1954": 0.60,
    "1955": 0.65,
    "1956": 0.70,
    "1957": 0.75,
    "1958": 0.80,
    "1959": 0.85,
    "1960": 0.90,
}

AIRCRAFT_MODELS = [
    {
        'short_name': 'DC-3',
        'range': 2000,
        'speed': 300,
        'fuel_consumption': 20,
        'passenger_capacity': 21,
        'price': 0.5,
        'launch_date': '1935-12-17',
        'complete_name': 'Douglas DC-3',
    },
    {
        'short_name': 'DC-4',
        'range': 3500,
        'speed': 350,
        'fuel_consumption': 30,
        'passenger_capacity': 44,
        'price': 0.75,
        'launch_date': '1938-06-23',
        'complete_name': 'Douglas DC-4',
    },
    # ...
]

# The demand levels dictionary maps the number of passengers demand between two airports (given in thousands) to a percentage load factor
DEMAND_LEVELS = {
    0: 0.0,
    1: 0.2,
    2: 0.4,
    3: 0.6,
    4: 0.8,
    5: 1.0,
}