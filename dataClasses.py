class ticket:
    def __init__(self,ticketNumber, batchNumber, destination, date, price, machineId,type):
        self.ticketNumber=ticketNumber
        self.batchNumber = batchNumber
        self.destination = destination
        self.date = date
        self.price = price
        self.machineId = machineId
        self.type = type


class batch:
    def __init__(self, batchNumber, machineId, startDate, endDate, numberOfTickets,numberOfCivilTickets,numberOfMilTickets, closingTotal):
        self.batchNumber = batchNumber
        self.machineId = machineId
        self.startDate = startDate
        self.endDate = endDate
        self.numberOfTickets = numberOfTickets
        self.numberOfCivilTickets = numberOfCivilTickets
        self.numberOfMilTickets = numberOfMilTickets

        self.closingTotal = closingTotal


class machine:

    def __init__(self, machineId, destination,militaryPrice,civilianPrice):

         self.machineId = machineId
         self.destination = destination
         self.militaryPrice=militaryPrice
         self.civilianPrice = civilianPrice

class myUSB:

    def __init__(self, vendorId, productId,securityLevel,userId,bus,device,iSerialNumber):

         self.vendorId = vendorId
         self.productId = productId
         self.securityLevel=securityLevel
         self.userId = userId
         self.bus = bus
         self.device=device
         self.iSerialNumber=iSerialNumber