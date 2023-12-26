
import requests
from faker import Faker
from random import uniform, randint, choice
from datetime import timedelta

faker = Faker()

API_URL = 'http://127.0.0.1:8000'  # Replace with the actual URL of your API

# Function to create fake port data
def create_port():
    port_data = {
        'name': faker.city(),
        'country': faker.country(),
        'daily_cost': round(uniform(100, 1000), 2),
        'category': choice(['Small', 'Medium', 'Large'])
    }
    return port_data

# Function to create fake ship data
def create_ship():
    ship_data = {
        'name': faker.name(),
        'displacement': randint(500, 10000),
        'port_of_registry': faker.city(),
        'type': choice(['Cargo', 'Passenger', 'Military']),
        'captain': faker.name()
    }
    return ship_data

# Function to create fake visit data
def create_visit(ship_id, port_id):
    arrival_date = faker.date_time_this_decade(before_now=True, after_now=False)
    visit_data = {
        'ship_id': ship_id,
        'port_id': port_id,
        'date_of_arrival': arrival_date,
        'date_of_departure': arrival_date + timedelta(days=randint(1, 5)),
        'purpose': faker.text(max_nb_chars=200),
        'number_of_passengers': randint(1, 5000)
    }
    return visit_data

# Function to post data to the API
def post_data(endpoint, data):
    response = requests.post(f'{API_URL}{endpoint}', json=data)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f'Error {response.status_code}: {response.content}')
        return None

# Generate and post ports data
ports = [post_data('/ports/', create_port()) for _ in range(10)]

# Generate and post ships data
ships = [post_data('/ships/', create_ship()) for _ in range(10)]

# Generate and post visits data
for ship in ships:
    for port in ports:
        visit = create_visit(ship['id'], port['id'])
        post_data('/visits/', visit)
