from abc import ABC, abstractmethod

#Credits to GeeksForGeeks for some of the helper functions ^^

class Date:
    def __init__(self, month, day, year):
        self.__month = month
        self.__day = day
        self.__year = year
    def mdyFormat(self) -> str:
        return str(self.__month) + "/" + str(self.__day) + "/" + str(self.__year)
    #Checks for leap years
    def countLeapYears(self):
        years = self.__year
        if(self.__month <= 2):
            years -= 1
        return int(years/4) - int(years/100) + int(years/400)
    #Returns the difference in days between 2 dates
    def getDifference(self, dueDate):
        monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        n1 = dueDate.__year * 365 + dueDate.__day
        for i in range(0, dueDate.__month - 1):
            n1 += monthDays[i]
        n1 += dueDate.countLeapYears()
        n2 = self.__year * 365 + self.__day
        for i in range(0, self.__month - 1):
            n2 += monthDays[i]
        n2 += self.countLeapYears()
        return (n2 - n1)



class Page:
    def __init__(self, sectionHeader, body):
        self.__sectionHeader = sectionHeader
        self.__body = body

class BorrowableItem(ABC):
    @abstractmethod
    def uniqueItemId(self) -> int:
        pass
    @abstractmethod
    def commonName(self) -> str:
        pass



class Book(BorrowableItem):
    def __init__(self, bookId, title, author, publishDate, pages):
        self.__bookId = bookId
        self.__title = title
        self.__publishDate = publishDate
        self.__author = author
        self.__pages = pages
    def coverInfo(self) -> str:
        return "Title: " + self.__title + "\nAuthor: " + self.__author
    def uniqueItemId(self) -> int:
        return self.__bookId
    def commonName(self) -> str:
        return "Borrowed Item: " + self.__title + " by " + self.__author

class Periodical(BorrowableItem):
    def __init__(self, periodicalID, title, issue, pages):
        self.__periodicalID = periodicalID
        self.__title = title
        self.__issue = issue
        self.__pages = pages
    def uniqueItemId(self) -> str:
        return self.__periodicalID
    def commonName(self) -> str:
        return "Borrowed item: " + self.__title + ": " + self.__issue.mdyFormat()

class PC(BorrowableItem):
    def __init__(self, pcID):
        self.__pcID = pcID
    def uniqueItemId(self) -> str:
        return self.__pcID
    def commonName(self) -> str:
        return "Borrowed item: PC" + str(self.__pcID)


class LibraryCard:
    def __init__(self, idNumber, name, borrowedItems):
        self.__idNumber = idNumber
        self.__name = name
        self.__borrowedItems = borrowedItems
    def borrowItem(self, borrowable:BorrowableItem, date:Date):
        self.__borrowedItems[borrowable] = date
    def borrowerReport(self) -> str:
        r:str = self.__name + "\n"
        for borrowedItem in self.__borrowedItems:
            r = r + borrowedItem.commonName() + ", borrow date:" + self.__borrowedItems[borrowedItem].mdyFormat() + "\n"
        return r
    #Returns the date a borrowable item was borrowed
    def borrowDate(self, borrowable:BorrowableItem) -> Date:
        return self.__borrowedItems[borrowable]
    #Returns the days elapsed between the date when the item was borrowed and today
    def getElapsed(self, borrowable:BorrowableItem, today:Date) -> int:
        return today.getDifference(self.borrowDate(borrowable))

    def returnItem(self, borrowable:BorrowableItem):
        for key in self.__borrowedItems.keys():
            if(self.borrowDate(borrowable).mdyFormat() == self.__borrowedItems[key].mdyFormat()):
                self.__borrowedItems.pop(key)
                break
        return
    def penalty(self, borrowable:BorrowableItem ,today:Date) -> int:
        elapsed = self.getElapsed(borrowable, today)
        if(isinstance(borrowable, Book) == True):
            if(self.getElapsed(borrowable, today) > 7):
                return float(3.5 * elapsed)
        elif(isinstance(borrowable, Periodical)):
            if(self.getElapsed(borrowable, today) > 1):
                return float(3.5 * elapsed)
        elif(isinstance(borrowable, PC)):
            if(self.getElapsed(borrowable, today) > 0):
                return float(3.5 * elapsed)
        return 0

    def itemsDue(self, today:Date):
        list = []
        for key in dict.keys(self.__borrowedItems):
            elapsedDays = self.getElapsed(key, today)
            if(isinstance(key, Book) == True):
                if(elapsedDays >= 7):
                    list.append(key)
            elif(isinstance(key, Periodical) == True):
                if(elapsedDays >= 1):
                    list.append(key)
            elif(isinstance(key, PC) == True):
                list.append(key)
        return list
    #Identical to the previous function, except this returns the common names
    def printDue(self, today:Date):
        list = []
        for key in dict.keys(self.__borrowedItems):
            elapsedDays = self.getElapsed(key, today)
            if(isinstance(key, Book) == True):
                if(elapsedDays >= 7):
                    list.append(key.commonName())
            elif(isinstance(key, Periodical) == True):
                if(elapsedDays >= 1):
                    list.append(key.commonName())
            elif(isinstance(key, PC) == True):
                list.append(key.commonName())
        return list


    def totalPenalty(self, today:Date):
        list = self.itemsDue(today)
        penalty = 0
        for i in range(0,len(list)):
            penalty += self.penalty(list[i], today)
        return penalty


#Random testing grounds below

b:BorrowableItem = Book(10991,"Corpus Hermeticum", "Hermes Trismegistus", Date(9,1,1991), [])
#print(b.commonName()) 

p:BorrowableItem = Periodical(177013, "National Geographic", Date(4,6,2001), [])
#print(p.commonName())

pc:BorrowableItem = PC(69420)
#print(pc.commonName())

l:LibraryCard = LibraryCard(9982,"Dovahkiin",{})
l.borrowItem(b,Date(9,25,2021))
l.borrowItem(p,Date(9,27,2021))
l.borrowItem(pc,Date(9,30,2021))
print(l.borrowerReport())

today = Date(9,30,2021)
print(l.penalty(b,today))
l.itemsDue(today)
l.totalPenalty(today)

l.returnItem(b)

print(l.borrowerReport())
print(l.penalty(p,today))
l.itemsDue(today)
l.totalPenalty(today)

