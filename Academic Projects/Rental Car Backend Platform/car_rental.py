from datetime import (datetime, timedelta)

class Car:
    id = 0
    make = ''
    model = ''
    hourly_price = 0
    daily_price = 0
    weekly_price = 0
    is_rented = False
    rent_type_id = 0
    rent_start_time = None
    rent_end_time = None
    renter_id = None

    def __init__(self, id, make, model, hourly_price):
        self.id = id
        self.make = make
        self.model = model
        self.hourly_price = hourly_price
        self.daily_price = hourly_price * 3
        self.weekly_price = self.daily_price * 7

    def __str__(self):
        car_str = "{id}. Make: {make}, Model: {model}, Hourly Rate: {hourly}, Daily Rate: {daily}, Weekly Rate: {weekly}".format(id=self.id, make=self.make, model=self.model, hourly=self.hourly_price, daily=self.daily_price, weekly=self.weekly_price)
        if self.is_rented == True:
            return car_str + ", Rented until: {rent_end_time}, Rented By: {renter_id}".format(rent_end_time=self.rent_end_time, renter_id=self.renter_id)
        else :
            return car_str
    
class Customer:
    id = 0
    name = ''
    userName = ''
    password = ''

    def __init__(self, id, name, userName, password):
        self.id = id
        self.name = name
        self.userName = userName
        self.password = password
    
    def verifyLogin(self, password):
        return password == self.password


class CarRentalStore:
    RENT_TYPES = {
        "Hourly": 1,
        "Daily": 2,
        "Weekly": 3
    }

    customers = []
    cars = []

    def __init__(self, cars = [], customers = []):
        self.customers = customers
        self.cars = cars

    def addCustomer(self, id, name, userName, password):
        customer = Customer(id, name, userName, password)
        self.customers.append(customer)
    
    def addCar(self, id, make, model, hourly_price):
        car = Car(id, make, model, hourly_price)
        self.cars.append(car)

    def getAvailableCars(self):
        total_available = 0
        for car in self.cars:
            if car.is_rented == False:
                total_available+=1
                print(car)
        print("Total Cars Available: " + str(total_available) )

    def rentCar(self, car_id, customer_id, rent_type_id, rent_time_amount):
        unrented_cars = list(filter(lambda car: car.is_rented == False, self.cars))
        if len(unrented_cars) == 0:
            print('No cars available for rent')

        is_car_available = False
        car_found = False
        for i in range(len(self.cars)):
            car = self.cars[i]
            if car.id == car_id:
                car_found = True
                if car.is_rented == False:
                    is_car_available = True
                    car.is_rented = True

                    car.renter_id = customer_id
                    car.rent_type_id = rent_type_id
                    car.rent_start_time = datetime.now()

                    if rent_type_id == self.RENT_TYPES['Hourly']:
                        car.rent_end_time = car.rent_start_time + timedelta(hours=rent_time_amount)
                    elif rent_type_id == self.RENT_TYPES['Daily']:
                        car.rent_end_time = car.rent_start_time + timedelta(days=rent_time_amount)
                    elif rent_type_id == self.RENT_TYPES['Weekly']:
                        car.rent_end_time = car.rent_start_time + timedelta(days=rent_time_amount*7)
                    self.cars[i] = car
        
        if car_found == False:
            print('Car not found')
        elif is_car_available == False:
            print('Car with specified make and model has already been rented.')
        else:
            print('Car with id {id} rented successfully to user {customer_id}'.format(id=car_id, customer_id=customer_id))
    
    def returnCar(self, car_id, customer_id):
        car_found = False
        car_index = 0

        for i in range(len(self.cars)):
            if self.cars[i].id == car_id and self.cars[i].renter_id == customer_id:
                car_index = i
                car_found = True
        
        if not car_found:
            print('Car not found')
        else:
            time_rented = self.cars[car_index].rent_end_time - self.cars[car_index].rent_start_time
            time_rented_seconds = time_rented.total_seconds()
            if self.cars[car_index].rent_type_id == self.RENT_TYPES['Hourly']:
                print("Bill: $" + str(divmod(time_rented_seconds, 3600)[0] * self.cars[car_index].hourly_price))
            elif self.cars[car_index].rent_type_id == self.RENT_TYPES['Daily']:
                print("Bill: $" + str(divmod(time_rented_seconds, 86400)[0] * self.cars[car_index].daily_price))
            elif self.cars[car_index].rent_type_id == self.RENT_TYPES['Weekly']:
                print("Bill: $" + str( (divmod(time_rented_seconds, 86400)[0] / 7) * self.cars[car_index].weekly))

            self.cars[car_index].rent_start_time = None
            self.cars[car_index].rent_end_time = None
            self.cars[car_index].rent_type_id = 0
            self.cars[car_index].renter_id = None
            self.cars[car_index].is_rented = False
