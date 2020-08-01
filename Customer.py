
class Customer:
    """Class that contains all the details of a customer
    """
    def __init__(self, Name, CheckIn, CheckOut, RoomID, CustomerID=0, PricePerNight=0.0, People=0,):
        """
        :param Name [string]: The name of the customer
        :param CheckIn [datetime object]: The date of the check in
        :param CheckOut [datetime object]: The date of the check out
        :param RoomID [int]: The ID of the room the customer is staying in
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
        delta = CheckOut - CheckIn
        self.NumberOfStayDays = delta.days
        
    def GetSQLFormatedDataForInsertion(self):
        return [self.Name, self.People, self.CheckIn, self.CheckOut, self.PricePerNight, self.RoomID]
    
    def __str__(self):
        string = f"""Customer Name: {self.Name}
        Customer ID: {self.CustomerID}
        Number of people: {self.People}
        Check in date:  {self.CheckIn}
        Check out date: {self.CheckOut}
        Price per night: {self.PricePerNight}
        Room ID: {self.RoomID}"""
        return string