from csv_yielder import csv_yielder
from broadcast import make_sinksave

# custom file
cars_path = 'cars.csv'
car_headers = (
    'Car','MPG','Cylinders',
    'Displacement','Horsepower','Weight',
    'Acceleration','Model','Origin'
)
idx_carname = car_headers.index('Car')
car_converters = (
    # 'Chevrolet Chevelle Malibu','18.0','8',
    str, float, int,
    # '307.0','130.0','3504.',
    float, float, float,
    # '12.0','70','US'
    float, int, str
)

def car_parser(car):
    return [
        convert(item) 
        for convert, item
        in zip(car_converters, car)
    ]

def carname_contains(*values):
    def does_carname_contain(row):
        return all(
            value in row[idx_carname]
            for value in values
        )
    return does_carname_contain


if __name__ == '__main__':
    cars = csv_yielder(
        cars_path,
        row_parser = car_parser
    )
    sinksave = make_sinksave(
        save_path = 'selected_cars.csv',
        headers = car_headers,
        row_filter = carname_contains('Chevrolet', 'Carlo', 'Landau')
    )
    sinksave(cars)
