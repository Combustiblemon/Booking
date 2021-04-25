
class Customer:
    """Class that contains all the details of a customer
    """
    def __init__(self, Name, CheckIn, CheckOut, RoomID, BookingType, PricePerNight=0.0, People=0, CustomerID=-1, Comments=" ", NumberOfStayNights=1, TotalPrice=0.0):
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
        self.Name = Name
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
        return [self.Name, self.People, self.CheckIn, self.CheckOut, self.PricePerNight, self.RoomID, self.BookingType, self.Comments, self.NumberOfStayNights, self.TotalPrice]
    
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