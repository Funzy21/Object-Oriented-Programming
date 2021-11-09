from abc import ABC, abstractmethod

class Account(ABC):
    @abstractmethod
    def __init__(self, n):
        self.n = n
    #Returns the accoutn number for transfer purposes
    def accountNum(self):
        pass
    def accountBalance(self):
        pass
    def accountDetails(self):
        pass    

class Payroll(Account):
    def __init__(self, name:str, age:int, gender:chr, accountID:int, balance:int):
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__accountID = accountID
        self.__balanceRecord = []
        self.balance = balance
        self.status = "Inactive"
    def accountNum(self):
        return self.__accountID
    def accountBalance(self):
        return self.balance
    def withdraw(self, ammount):
        if(ammount > self.balance):
            return "Insufficient balance"
        else:
            self.balance -= ammount
            self.__balanceRecord.append("Withdrawn ammount: -" + str(ammount))
            return str(ammount) + " Septims successfully withdrawn from account"
    def showRecord(self):
        return self.__balanceRecord
    def accountDetails(self):
        r:str = "Name: " + str(self.__name) + "\n" + "Type: Payroll" + "\n" + "Status: " + str(self.status) + "\n" + "Balance: " + str(self.balance) + "\n"
        return r
    #Prints the 5 most recent transactions
    def balanceReport(self):
        size = len(self.__balanceRecord)
        if(size == 0):
            print("No recent account activity found")
        else:
            print("Account: " + str(self.accountNum()) + " recent banking activity: \n")
            if(size < 4):
                for i in range(0, size):
                    print(self.__balanceRecord[i])
            else:
                for i in range((size-5), size):
                    print(self.__balanceRecord[i])
        print("\nCurrent balance: " + str(self.balance) + "\n")
        print("\n")
        return
            

class Credit(Account):
    def __init__(self, name:str, age:int, gender:chr, accountID:int):
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__accountID = accountID
        self.__balanceRecord = []
        self.status = "Inactive"
        self.balance = 0
        self.interest = 11
        self.creditLimit = 100000
    def accountNum(self):
        return self.__accountID
    def withdraw(self, ammount):
        temp = self.balance
        temp += ammount
        if(temp > self.creditLimit):
            return "Ammount exceeds this account's credit limit"
        else:
            self.balance += ammount
            self.__balanceRecord.append("Withdrawn ammount: +" + str(ammount))
            return str(ammount) + " Septims successfully withdrawn from account"
    def deposit(self, ammount):
        self.balance -= ammount
        self.__balanceRecord
        self.__balanceRecord.append("Deposit: -" + str(ammount))
        return str(ammount) + " Septims successfully deposited to account"
    def accountDetails(self):
        r:str = "Name: " + str(self.__name) + "\n" + "Type: Credit" + "\n" + "Status: " + str(self.status) + "\n" + "Balance: " + str(self.balance) + "\n"
        return r
    def showRecord(self):
        return self.__balanceRecord        
    def transfer(self, account:Account, ammount):
        if(ammount > self.creditLimit):
            return "Transfer unsuccessful. Balance exceeds this account's credit limit"
        else:
            self.balance += ammount
            if(isinstance(account, Credit) == True):
                account.balance -= ammount
            else:
                account.balance += ammount
            account.showRecord().append("Amount received from " + str(self.accountNum()) + ": +" + str(ammount))
            self.__balanceRecord.append("Transfer to account " + str(account.accountNum()) + ": +" + str(ammount))
            return "Transfer successful"
    def accountChanges(self):
        self.balance += (self.balance * self.interest)
        if(self.balance > self.creditLimit):
            self.status = "Inactive"
        return
    def balanceReport(self):
        size = len(self.__balanceRecord)
        if(size == 0):
            print("No recent account activity found")
        else:
            print("Account: " + str(self.accountNum()) + " recent banking activity: \n")
            if(size < 4):
                for i in range(0, size):
                    print(self.__balanceRecord[i])
            else:
                for i in range((size-5), size):
                    print(self.__balanceRecord[i])
        print("\nCurrent balance: " + str(self.balance) + "\n")
        return

class Debit(Account):
    def __init__(self, name:str, age:int, gender:chr, accountID:int, balance:int):
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__accountID = accountID
        self.__balanceRecord = []    
        self.balance = balance
        self.maintaining = 100
        self.status = "Inactive"
        self.interest = 2
    def accountNum(self):
        return self.__accountID   
    def accountBalance(self):
        return self.balance
    def withdraw(self, ammount):
        if(ammount > self.balance):
            return "Insufficient balance"
        else:
            #If account balance is less than maintaining balance, it becomes inactive
            if(self.balance< self.maintaining):
                self.status = "Inactive"
            self.balance-= ammount
            self.__balanceRecord.append("Withdrawn ammount: -" + str(ammount))
            return str(ammount) + " Septims successfully withdrawn from account"
    def deposit(self, ammount):
        self.balance+= ammount
        self.__balanceRecord.append("Deposit: +" + str(ammount))
        return str(ammount) + " Septims successfully deposited to account"
    def accountDetails(self):
        r:str = "Name: " + self.__name + "\n" + "Type: Debit" + "\n" + "Status: " + self.status + "\n" + "Balance: " + str(self.balance) + "\n"
        return r    
    def showRecord(self):
        return self.__balanceRecord        
    def transfer(self, account:Account, ammount):
        if(self.accountBalance() < self.maintaining):
            return "Insufficient balance"
        else:
            if(isinstance(account, Credit) == True):
                account.balance -= ammount
            else:
                account.balance += ammount
            self.balance -= ammount
            account.showRecord().append("Amount received from " + str(self.accountNum()) + ": +" + str(ammount))
            self.__balanceRecord.append("Transfer to account " + str(account.accountNum()) + ": -" + str(ammount))
            return "Transfer successful"
    def accountChanges(self):
        self.balance += (self.balance * self.interest)
        if(self.balance < self.maintaining):
            self.status = "Inactive" 
        return
    def balanceReport(self):
        size = len(self.__balanceRecord)
        if(size == 0):
            print("No recent account activity found")
        else:
            print("Account: " + str(self.accountNum()) + " recent banking activity: \n")
            if(size < 4):
                for i in range(0, size):
                    print(self.__balanceRecord[i])
            else:
                for i in range((size-5), size):
                    print(self.__balanceRecord[i])
        print("\nCurrent balance: " + str(self.balance) + "\n")
        return

class Bank:
    def __init__(self, name, database):
        self.__name = name
        self.__database = database
    #Activated accounts are stored into the bank's database for future reference
    def activate(self, account:Account) -> str:
        if(isinstance(account, Debit)):
            if(account.accountBalance() < account.maintaining):
                return "Sorry, your initial deposit is below the maintaining balance. Account cannot be activated"
            else:
                if(self.isActivated(account) == True):
                    return "Account is already activated, please try again"
                else:
                    self.__database.append(account)
                    account.status = "Active"
                    return "Account succesfully activated"
        else:
            self.__database.append(account)
            account.status = "Active"
            return "Account succesfully activated"
                    
    def deactivate(self, account:Account) -> str:
        list = self.__database
        if(self.isActivated(account) == True):
            for item in list:
                if(account == item):
                    account.status = "Inactive"
                    break
            return "Account successfully deactivated" 
        else:
            return "Account is not activated"
    #Checks if an account is already activated
    def isActivated(self, account:Account) -> bool:
        list = self.__database
        for i in range(0, len(list)):
            if(account == list[i] and account.status == "Active"):
                return True
            else:
                return False

#Instantiation
bank1:Bank = Bank("Cyrodiil Imperial Bank", [])
account1:Account = Debit("Dovahkiin", 35, "M", 177013, 3000)
account2:Account = Payroll("Alduin", 20000, "M", 420690, 5000)
account3:Account = Credit("Paarthurnax", 20000, "M", 314536)

#Activating the accounts
bank1.activate(account1)
bank1.activate(account2)
bank1.activate(account3)


print(account1.accountDetails())
print(account2.accountDetails())
print(account3.accountDetails())

#Test transactions
account1.withdraw(2000)
account1.deposit(5000)
account1.transfer(account2, 1000)

#Checking to see if the transactions update both accounts
account1.balanceReport()
account2.balanceReport()

