import datetime

class Customer:
    """Class that contains all the details of a customer
    """
    def __init__(self, Name: str, CheckIn: datetime.date, CheckOut: datetime.date, RoomID: int, BookingType: int, PricePerNight: float = 0.0, People: int = 0, CustomerID:int = -1, Comments:str = " ", NumberOfStayNights:int = 1, TotalPrice:float = 0.0):
        """
        :param Name [string]: The name of the customer
        :param CheckIn [datetime object]: The date of the check in
        :param CheckOut [datetime object]: The date of the check out
        :param RoomID [int]: The ID of the room the customer is staying in
        :param BookingType [int]: The ID of the entity responsible for the booking
        :param CustomerID [int, optional]: The CustomerID as it appears in the database, defaults to 0
        :param PricePerNight [float, optional]: The price the customer is paying per night, defaults to 0.0
        :param People [int, optional]: The number of people staying in the room, defaults to 0
        """
        self.CustomerID = CustomerID
        self.Name = Name.lower()
        self.People = People
        self.CheckIn = CheckIn
        self.CheckOut = CheckOut
        self.PricePerNight = PricePerNight
        self.RoomID = RoomID
        self.BookingType = BookingType
        self.Comments = Comments
        self.NumberOfStayNights = NumberOfStayNights  # delta.days - 1
        self.TotalPrice = TotalPrice  # (delta.days - 1) * PricePerNight
        
    def GetSQLFormatedDataForInsertion(self):
        return [self.Name.lower(),
                self.People,
                self.CheckIn,
                self.CheckOut,
                self.PricePerNight,
                self.RoomID,
                self.BookingType,
                self.Comments,
                self.NumberOfStayNights,
                self.TotalPrice]
    
    def GetDictFormatedData(self):
        return {
            'customer_name': self.Name.lower(),
            'number_of_people': self.People,
            'check_in': self.CheckIn.strftime('%Y-%m-%d'),
            'check_out': self.CheckOut.strftime('%Y-%m-%d'),
            'price_per_night': self.PricePerNight,
            'room_id': self.RoomID,
            'booking_type': self.BookingType,
            'comment': self.Comments,
            'stay_days_number': self.NumberOfStayNights
        }
    
    def __str__(self):
        string = f"""Customer Name: {self.Name}
        Customer ID: {self.CustomerID}
        Number of people: {self.People}
        Check in date:  {self.CheckIn}
        Check out date: {self.CheckOut}
        Number of nights: {self.NumberOfStayNights}
        Price per night: {self.PricePerNight}
        Total price: {self.TotalPrice}
        Room ID: {self.RoomID}
        Booking Type: {self.BookingType}
        
        Comments: {self.Comments}"""
        return string
    
    def __eq__(self, other):
        if (isinstance(other, Customer)):
            return (self.Name == other.Name and self.People == other.People and self.CheckIn == other.CheckIn and self.CheckOut == other.CheckOut and self.PricePerNight == other.PricePerNight and self.RoomID == other.RoomID and self.BookingType == other.BookingType and self.Comments == other.Comments)
        return False