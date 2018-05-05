'''
Created on 22-Mar-2018

@author: jayasakthiram
'''
import cx_Oracle,sys
class Database(object):
    def __init__(self, username, password):
        self.__connection = cx_Oracle.connect(username + '/' + password)
        self.__cursor = self.__connection.cursor()


    def get_connection(self):
        return self.__connection


    def get_cursor(self):
        return self.__cursor

    
    def close(self, save=False):
        if save:
            self.__connection.commit()
        self.__cursor.close()
        self.__connection.close()
class Person(object):
    def __init__(self, personid=None, firstname=None, lastname=None, email=None, phonenumber=None, address=None, personType=None, username=None, password=None):
        self.__personid = personid
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__phonenumber = phonenumber
        self.__address = address
        self.__personType = personType
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username


    def get_password(self):
        return self.__password


    def set_username(self, value):
        self.__username = value


    def set_password(self, value):
        self.__password = value


    def get_person_type(self):
        return self.__personType


    def set_person_type(self, value):
        self.__personType = value



    def get_personid(self):
        return self.__personid


    def set_personid(self, value):
        self.__personid = value


    def get_email(self):
        return self.__email


    def get_phonenumber(self):
        return self.__phonenumber


    def set_email(self, value):
        self.__email = value


    def set_phonenumber(self, value):
        self.__phonenumber = value


    def get_firstname(self):
        return self.__firstname


    def get_lastname(self):
        return self.__lastname


    def get_address(self):
        return self.__address


    def set_firstname(self, value):
        self.__firstname = value


    def set_lastname(self, value):
        self.__lastname = value


    def set_address(self, value):
        self.__address = value
        
    
    def getdict(self):
        return dict([('firstname', self.get_firstname()), ('lastname', self.get_lastname()),
                     ('email', self.get_email()), ('phonenumber', self.get_phonenumber()),
                     ('address', self.get_address()), ('customerid', self.get_customerid())])
    def __repr__(self):
        return 'Customer Id : {customerid}\nFirst Name : {firstname}\nLast Name : {lastname}\nEmail Id : {email}\nPhone no. : {phonenumber}\nAddress : \n{address}'.format(**self.getdict())
class Booking(Person):
        def __init__(self, personid=None, bookingId=None, bookingDate=None, devoteeId=None, seatsQuantity=None, bookedOn=None):
            Person.__init__(self,
                personid)
            self.__bookingId = bookingId
            self.__bookingDate = bookingDate
            self.__devoteeId = devoteeId
            self.__seatsQuantity = seatsQuantity
            self.__bookedOn = bookedOn

        def get_booking_id(self):
            return self.__bookingId


        def get_booking_date(self):
            return self.__bookingDate


        def get_devotee_id(self):
            return self.__devoteeId


        def get_seats_quantity(self):
            return self.__seatsQuantity


        def get_booked_on(self):
            return self.__bookedOn


        def set_booking_id(self, value):
            self.__bookingId = value


        def set_booking_date(self, value):
            self.__bookingDate = value


        def set_devotee_id(self, value):
            self.__devoteeId = value


        def set_seats_quantity(self, value):
            self.__seatsQuantity = value


        def set_booked_on(self, value):
            self.__bookedOn = value
class Specialdharshan(Booking):

        def __init__(self, bookingId=None, bookingDate=None, devoteeId=None, seatsQuantity=None, bookedOn=None, totalCost=None, pricePerSeat=300):
            Booking.__init__(self,
                bookingId, bookingDate, devoteeId, seatsQuantity, bookedOn)
            self.__pricePerSeat = pricePerSeat
            self.__totalCost = totalCost
        
        def get_total_cost(self):
            return self.__totalCost


        def set_total_cost(self, value):
            self.__totalCost = value


        def get_price_per_seat(self):
            return self.__pricePerSeat


        def set_price_per_seat(self, value):
            self.__pricePerSeat = value
class Sevas(Booking):

    def __init__(self, bookingId=None, bookingDate=None, devoteeId=None, seatsQuantity=None, bookedOn=None, sevaName=None, privileageId=None, sevaNo=None, sevaSeats=None):
        Booking.__init__(self,
            bookingId, bookingDate, devoteeId, seatsQuantity, bookedOn)
        self.__sevaName = sevaName
        self.__privileageId = privileageId
        self.__sevaNo = sevaNo
        self.__sevaSeats = sevaSeats

    def get_seva_seats(self):
        return self.__sevaSeats


    def set_seva_seats(self, value):
        self.__sevaSeats = value


    def get_seva_no(self):
        return self.__sevaNo


    def set_seva_no(self, value):
        self.__sevaNo = value


    def get_seva_name(self):
        return self.__sevaName


    def get_privileage_id(self):
        return self.__privileageId


    def set_seva_name(self, value):
        self.__sevaName = value


    def set_privileage_id(self, value):
        self.__privileageId = value
class Accomodation(Booking):

    def __init__(self, bookingId=None, bookingDate=None, devoteeId=None, seatsQuantity=None, bookedOn=None, roomId=None, roomDescription=None, roomLocation=None, perRoomCost=None, roomPay=None, timeSlot=None):
        Booking.__init__(self,
            bookingId, bookingDate, devoteeId, seatsQuantity, bookedOn)
        self.__roomId = roomId
        self.__roomDescription = roomDescription
        self.__roomLocation = roomLocation
        self.__perRoomCost = perRoomCost
        self.__roomPay = roomPay
        self.__timeSlot = timeSlot

    def get_time_slot(self):
        return self.__timeSlot


    def set_time_slot(self, value):
        self.__timeSlot = value

        
    def get_room_id(self):
        return self.__roomId


    def get_room_description(self):
        return self.__roomDescription


    def get_room_location(self):
        return self.__roomLocation


    def get_per_room_cost(self):
        return self.__perRoomCost


    def get_room_pay(self):
        return self.__roomPay


    def set_room_id(self, value):
        self.__roomId = value


    def set_room_description(self, value):
        self.__roomDescription = value


    def set_room_location(self, value):
        self.__roomLocation = value


    def set_per_room_cost(self, value):
        self.__perRoomCost = value


    def set_room_pay(self, value):
        self.__roomPay = value
class Hundi(object):

    def __init__(self, hundi_amount=None, devotee_name=None, devotee_mobile=None, on_occasion_of=None):
        self.__hundi_amount = hundi_amount
        self.__devotee_name = devotee_name
        self.__devotee_mobile = devotee_mobile
        self.__on_occasion_of = on_occasion_of

    def get_hundi_amount(self):
        return self.__hundi_amount


    def get_devotee_name(self):
        return self.__devotee_name


    def get_devotee_mobile(self):
        return self.__devotee_mobile


    def get_on_occasion_of(self):
        return self.__on_occasion_of


    def set_hundi_amount(self, value):
        self.__hundi_amount = value


    def set_devotee_name(self, value):
        self.__devotee_name = value


    def set_devotee_mobile(self, value):
        self.__devotee_mobile = value


    def set_on_occasion_of(self, value):
        self.__on_occasion_of = value
class Address(Person):
    @staticmethod
    def validatepincode(pincode):
        if pincode == None:
            return None
        elif type(pincode) != int or len(str(pincode)) != 6:
            print('pincode must be an integer with length 6',file=sys.stderr)
        else:
            return pincode
    def __init__(self, personid=None, line1=None, line2=None, city=None, state=None, pincode=None):
        Person.__init__(self, personid)
        self.__line1 = line1
        self.__line2 = line2
        self.__city = city
        self.__state = state
        self.__pincode = pincode
    def get_line_1(self):
        return self.__line1


    def get_line_2(self):
        return self.__line2


    def get_city(self):
        return self.__city


    def get_state(self):
        return self.__state


    def get_pincode(self):
        return self.__pincode


    def set_line_1(self, value):
        self.__line1 = value


    def set_line_2(self, value):
        self.__line2 = value


    def set_city(self, value):
        self.__city = value


    def set_state(self, value):
        self.__state = value


    def set_pincode(self, value):
        self.__pincode = value

    
    def getdict(self):
        return dict([('line1', self.get_line_1()), ('line2', self.get_line_2()),
                     ('city', self.get_city()), ('state', self.get_state()),
                     ('pincode', self.get_pincode())])

    
    def __repr__(self):
        return '''\t{line1}, \n\t{line2}, \n\t{city}, \n\t{state} - {pincode}.'''.format(**self.getdict())
class Devotee(Person):

    def __init__(self, personid=None, firstname=None, lastname=None, email=None, phonenumber=None, address=None, personType=None, username=None, password=None, serviceUsed=None, dateUsed=None, costPurchased=None):
        Person.__init__(self,
            personid, firstname, lastname, email, phonenumber, address, personType, username, password)
        self.__serviceUsed = serviceUsed
        self.__dateUsed = dateUsed
        self.__costPurchased = costPurchased

    def get_service_used(self):
        return self.__serviceUsed


    def get_date_used(self):
        return self.__dateUsed


    def get_cost_purchased(self):
        return self.__costPurchased


    def set_service_used(self, value):
        self.__serviceUsed = value


    def set_date_used(self, value):
        self.__dateUsed = value


    def set_cost_purchased(self, value):
        self.__costPurchased = value
class Trustee(Person):

    def __init__(self, personid=None, firstname=None, lastname=None, email=None, phonenumber=None, address=None, personType=None, username=None, password=None, donatedAmount=None, trustName=None, privileageId=None, dateDonated=None):
        Person.__init__(self,
            personid, firstname, lastname, email, phonenumber, address, personType, username, password)
        self.__donatedAmount = donatedAmount
        self.__trustName = trustName
        self.__privileageId = privileageId
        self.__dateDonated = dateDonated

    def get_date_donated(self):
        return self.__dateDonated


    def set_date_donated(self, value):
        self.__dateDonated = value

    
    def get_donated_amount(self):
        return self.__donatedAmount


    def get_trust_name(self):
        return self.__trustName


    def get_privileage_id(self):
        return self.__privileageId


    def set_donated_amount(self, value):
        self.__donatedAmount = value


    def set_trust_name(self, value):
        self.__trustName = value


    def set_privileage_id(self, value):
        self.__privileageId = value
class Priveleges(Person):

    def __init__(self, personid=None, firstname=None, privilege_id=None, privilege_name=None, privilege_validity_days=None, privilege_expiry_date=None, privilege_status=None):
        Person.__init__(self,
            personid, firstname)
        self.__privilege_id = privilege_id
        self.__privilege_name = privilege_name
        self.__privilege_validity_days = privilege_validity_days
        self.__privilege_expiry_date = privilege_expiry_date
        self.__privilege_status = privilege_status

    def get_privilege_id(self):
        return self.__privilege_id


    def get_privilege_name(self):
        return self.__privilege_name


    def get_privilege_validity_days(self):
        return self.__privilege_validity_days


    def get_privilege_expiry_date(self):
        return self.__privilege_expiry_date


    def get_privilege_status(self):
        return self.__privilege_status


    def set_privilege_id(self, value):
        self.__privilege_id = value


    def set_privilege_name(self, value):
        self.__privilege_name = value


    def set_privilege_validity_days(self, value):
        self.__privilege_validity_days = value


    def set_privilege_expiry_date(self, value):
        self.__privilege_expiry_date = value


    def set_privilege_status(self, value):
        self.__privilege_status = value
