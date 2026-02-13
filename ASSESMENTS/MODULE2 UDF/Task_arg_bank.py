account = {}
data_list = []


def getdata():
    global account

    stdacn = input("Enter your Account Number: ")
    stdhnm = input("Enter your Account holder name: ")
    stdty = input("Enter your Account Type: ")

    account = {
        "Account Number": stdacn,
        "Account Holder name": stdhnm,
        "Account Type": stdty,
        "Balance": 0
    }

    data_list.append(account)


def deposit():
    global account

    deamt = int(input("Enter amount to deposit: "))

    if deamt < 2000:
        print("Minimum deposit amount is 2000")
    else:
        account["Balance"] += deamt
        print("Deposit Successful")


def withdrawal():
    global account

    wdamt = int(input("Enter the amount to withdraw: "))

    if wdamt < 2000:
        print("Minimum withdrawal amount is 2000")
    elif wdamt > account["Balance"]:
        print("Insufficient Balance")
    else:
        account["Balance"] -= wdamt
        print("Successfully Withdrawn")


def statement():
    global account

    print("\n--- Account Statement ---")
    print("Account Number:", account["Account Number"])
    print("Account Holder name:", account["Account Holder name"])
    print("Account Type:", account["Account Type"])
    print("Total Balance:", account["Balance"])

print("Account Details:")
getdata()

deposit()
withdrawal()
statement()



