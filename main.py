import mysql.connector as mc

mydb = mc.connect(host='localhost', user='root', password='root', database='library1')


def addbook():
    bname = input("Enter Book Name(char) : ")
    bcode = input("Enter Book Code(char) : ")
    total = input("Total Books(int) : ")
    sub = input("Enter Subjects(char) : ")
    data = (bname, bcode, total, sub)
    sql = 'insert into books values(%s,%s,%s,%s)'
    c = mydb.cursor()

    c.execute("select bcode from books")
    check = c.fetchall()
    if len(check) == 0:
        c.execute(sql, data)
        mydb.commit()
        print("..........................")
        print("Data Entered Succesfully..")
    else:
        list1 = []
        for i in check:
            list1.append(i[0])
        if bcode not in list1:
            c.execute(sql, data)
            mydb.commit()
            print("..........................")
            print("Data Entered Succesfully..")
            main()
        else:
            print("Book Already exist.....")
            print('.................................')
            main()

    main()


def issueb():
    name = input("Enter Name(char) : ")
    rno = input("Enter RollNO(char) : ")
    code = input("Enter Book Code(char) : ")
    date = input("Enter Date Of Issue(yyyy-mm-dd) : ")
    data = (name, rno, code, date)
    sql = 'insert into issue values(%s,%s,%s,%s)'
    c = mydb.cursor()
    c.execute("select bcode from books")
    check = c.fetchall()
    if len(check) == 0:
        print("Book Not Exist....")
        main()
    else:
        list1 = []
        for i in check:
            list1.append(i[0])
        if code in list1:
            c.execute("select total from books where bcode=%s", (code,))
            result = c.fetchone()
            if result[0] > 0:
                c.execute(sql, data)
                mydb.commit()
                print("..........................")
                print("Book Issued to : ", name, " .")
                print('.................................')
                bookup(code, -1)
            else:
                print(code, ' Book Count is 0', " / book not issued")
                print('.................................')
                main()
        else:
            print("Book Not Exist.....")
            print('.................................')
            main()
    main()


def submitb():
    name = input("Enter Name(char) : ")
    rno = input("Enter RollNO(char) : ")
    code = input("Enter Book Code(char) : ")
    date = input("Enter Date Of Submit(yyyy-mm-dd) : ")
    data = (name, rno, code, date)
    sql = 'insert into submit values(%s,%s,%s,%s)'
    c = mydb.cursor()
    d1 = (rno, code)
    result1 = c.execute("select name from issue where regno= %s and bcode= %s ", d1)
    a = c.fetchall()
    c.execute("select idate from issue where regno= %s and bcode= %s", d1)
    b = c.fetchall()
    result2 = c.execute("select datediff(%s,%s)", (date, b[0][0]))
    a1 = c.fetchall()
    finedate = 60
    if len(a) > 0:
        c.execute(sql, data)
        mydb.commit()
        print("..........................")
        print("Book Submitted from ", name, " .")
        print('.................................')

        id = b[0][0]
        dd = a1[0][0]
        ff = int(dd) - finedate
        if ff > 0:
            fa = str(ff * 2)
            payment = "no"
        else:
            fa = "0"
            payment = "yes"
        c.execute("insert into fine values (%s,%s,%s,%s,%s,%s,%s,%s)", (code, name, rno, id, date, dd, fa, payment))
        bookup(code, 1)

    else:
        print(".................................")
        print("NO data in issued Books for ", name)
        print(".................................")
        main()


def bookup(code, u):
    sql = "select total from books where bcode= %s"
    data = (code,)
    c = mydb.cursor()
    c.execute(sql, data)

    myresult = c.fetchone()
    t = myresult[0] + u

    sql = "update books set total= %s where bcode= %s"
    data1 = (t, code)
    c.execute(sql, data1)
    mydb.commit()
    main()


def dbook():
    print("""============Delete Functions==============
    1.Delete Books
    2.Delete Issued Book Details
    3.Delete Submitted Book Details
    4.Delete Fine Table Details
    5.Return to Main Menu

    """)
    choice11 = input("Enter your Option : ")
    if choice11 == "1":
        ac = input("Enter Book Code : ")
        sql = "delete from books where bcode = %s"
        data = (ac,)
        c = mydb.cursor()
        c.execute(sql, data)
        print("Data Deleted From Book Table........")
        print("--------------------------------------")
        mydb.commit()
        dbook()
    elif choice11 == "2":
        regno = input("Enter Registeration number : ")
        bcode = input("Enter Book Code : ")
        sql = "delete from issue where regno= %s and bcode= %s"
        data = (regno, bcode)
        c = mydb.cursor()
        c.execute(sql, data)
        print("Data Deleted from Issue Table.......")
        print("-------------------------------------")
        mydb.commit()
        dbook()
    elif choice11 == "3":
        regno = input("Enter Registeration number : ")
        bcode = input("Enter Book Code : ")
        sql = "delete from submit where regno= %s and bcode= %s"
        data = (regno, bcode)
        c = mydb.cursor()
        c.execute(sql, data)
        print("Data Deleted from Submit Table.......")
        print("-------------------------------------")
        mydb.commit()
        dbook()
    elif choice11 == "4":
        regno = input("Enter Registeration number : ")
        bcode = input("Enter Book Code            : ")
        sql = "delete from fine where regno= %s and bcode= %s"
        data = (regno, bcode)
        c = mydb.cursor()
        c.execute(sql, data)
        print("Data Deleted from Fine Table.......")
        print("-------------------------------------")
        mydb.commit()
        dbook()
    elif choice11 == "5":
        main()
    dbook()


def dispbook():
    sql = "select * from books"
    c = mydb.cursor()
    c.execute(sql)
    myresult = c.fetchall()
    for i in myresult:
        print("Book Name : ", i[0])
        print("Book Code : ", i[1])
        print("Total     : ", i[2])
        print("..........................")
    main()


def dispissue():
    sql = "select * from issue"
    c = mydb.cursor()
    c.execute(sql)
    myresult = c.fetchall()
    for i in myresult:
        print("Book Name   : ", i[0])
        print("Regno       : ", i[1])
        print("Bcode       : ", i[2])
        print("Issued Date : ", i[3])
        print(".........................")
    main()


def dispsubmit():
    sql = "select * from submit"
    c = mydb.cursor()
    c.execute(sql)
    myresult = c.fetchall()
    for i in myresult:
        print("Book Name      : ", i[0])
        print("Regno          : ", i[1])
        print("Bcode          : ", i[2])
        print("Submitted Date : ", i[3])
        print(".........................")
    main()


def dispfine():
    sql = "select * from fine"
    c = mydb.cursor()
    c.execute(sql)
    myresult = c.fetchall()
    for i in myresult:
        print("Book Code             : ", i[0])
        print("Student Name          : ", i[1])
        print("Register number       : ", i[2])
        print("Issued Date           : ", i[3])
        print("Submitted Date        : ", i[4])
        print("Date Difference       : ", i[5])
        print("fine Amount (>60days) : ", i[6])
        print("payment done          : ", i[7])

        print(".........................")
    main()


def search():
    print("""========== Search Box============

    1.Search Books
    2.Search Issued Details
    3.Search Submited Details
    4.Search Fine Details
    5.Back to Main Menu

    """)
    choice1 = input("Enter Your Search Function : ")
    print("..................................")
    if choice1 == "1":
        print("""========== Search Book============

        1.Search by Name
        2.Search by Book Code

        """)
        choice2 = input("Enter Your Choice : ")
        print("...........................")
        if choice2 == "1":
            sql = "select * from books where bname= %s"
            d = input("Enter the Book Name to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name : ", i[0])
                print("Book Code : ", i[1])
                print("Total     : ", i[2])
                print("Subject   : ", i[3])
                print("..........................")
            search()

        elif choice2 == "2":
            sql = "select * from books where bcode= %s"
            d = input("Enter the Book code to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name : ", i[0])
                print("Book Code : ", i[1])
                print("Total     : ", i[2])
                print("Subject   : ", i[3])
                print("..........................")
            search()
        else:
            search()
    elif choice1 == "2":
        print("""========== Issued Books details ============

        1.Search by Register number
        2.Search by Book Code

                """)
        choice3 = input("Enter Your Choice : ")
        print("...........................")
        if choice3 == "1":
            sql = "select * from issue where regno= %s"
            d = input("Enter the Registered Number to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name   : ", i[0])
                print("Book Regno  : ", i[1])
                print("Book Code   : ", i[2])
                print("Issued Date : ", i[3])
                print("..........................")
            search()
        elif choice3 == "2":
            sql = "select * from issue where bcode= %s"
            d = input("Enter the Book Code to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name   : ", i[0])
                print("Book Regno  : ", i[1])
                print("Book Code   : ", i[2])
                print("Issued Date : ", i[3])
                print("..........................")
            search()
        else:
            search()

    elif choice1 == "3":
        print("""========== Submitted Books details ============

        1.Search by Register number
        2.Search by Book Code

                        """)
        choice3 = input("Enter Your Choice : ")
        print("...........................")
        if choice3 == "1":
            sql = "select * from submit where regno= %s"
            d = input("Enter the Registered Number to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name      : ", i[0])
                print("Book Regno     : ", i[1])
                print("Book Code      : ", i[2])
                print("Submitted Date : ", i[3])
                print("..........................")

            search()
        elif choice3 == "2":
            sql = "select * from submit where bcode= %s"
            d = input("Enter the Book Code to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Name      : ", i[0])
                print("Book Regno     : ", i[1])
                print("Book Code      : ", i[2])
                print("submitted Date : ", i[3])
                print("..........................")
            search()
        else:
            search()
    elif choice1 == "4":
        print("""========== Fine details ============

        1.Search by Book Code
        2.Search by Register Number
        3.Paid List
        4.Unpaid List

         """)
        choice3 = input("Enter Your Choice : ")
        print("...........................")
        if choice3 == "1":
            sql = "select * from fine where bcode= %s"
            d = input("Enter the Book Code to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Code                : ", i[0])
                print("Book Name                : ", i[1])
                print("Book Regno               : ", i[2])
                print("Issued Date              : ", i[3])
                print("Submitted  Date          : ", i[4])
                print("No of Days Book Borrowed : ", i[5])
                print("Fine Amount              : ", i[6])
                print("Payment                  : ", i[7])
                print(".........................................")
            search()

        elif choice3 == "2":
            sql = "select * from fine where regno= %s"
            d = input("Enter the Register Number to be Searched : ")
            c = mydb.cursor()
            c.execute(sql, (d,))
            r1 = c.fetchall()
            for i in r1:
                print("Book Code                : ", i[0])
                print("Book Name                : ", i[1])
                print("Book Regno               : ", i[2])
                print("Issued Date              : ", i[3])
                print("Submitted  Date          : ", i[4])
                print("No of Days Book Borrowed : ", i[5])
                print("Fine Amount              : ", i[6])
                print("Payment                  : ", i[7])
                print(".........................................")
            search()

        elif choice3 == "3":
            sql = "select * from fine where payment= %s"
            c = mydb.cursor()
            c.execute(sql, ('yes',))
            r1 = c.fetchall()
            for i in r1:
                print("Book Code                : ", i[0])
                print("Book Name                : ", i[1])
                print("Book Regno               : ", i[2])
                print("Issued Date              : ", i[3])
                print("Submitted  Date          : ", i[4])
                print("No of Days Book Borrowed : ", i[5])
                print("Fine Amount              : ", i[6])
                print("Payment                  : ", i[7])
                print(".........................................")
            search()

        elif choice3 == "4":
            sql = "select * from fine where payment= %s"
            c = mydb.cursor()
            c.execute(sql, ("no",))
            r1 = c.fetchall()
            for i in r1:
                print("Book Code                : ", i[0])
                print("Book Name                : ", i[1])
                print("Book Regno               : ", i[2])
                print("Issued Date              : ", i[3])
                print("Submitted  Date          : ", i[4])
                print("No of Days Book Borrowed : ", i[5])
                print("Fine Amount              : ", i[6])
                print("Payment                  : ", i[7])
                print(".........................................")
            search()

        else:
            search()

    elif choice1 == "5":
        main()
    else:
        print("Invalid Input")
        search()
    main()


def incbook():
    code = input("Enter Book code : ")
    u = input("Count to be increased : ")
    sql = "select total from books where bcode= %s"
    data = (code,)
    c = mydb.cursor()
    c.execute(sql, data)

    myresult = c.fetchone()
    t = myresult[0] + int(u)

    sql = "update books set total= %s where bcode= %s"
    data1 = (t, code)
    c.execute(sql, data1)
    mydb.commit()
    main()


def decbook():
    code = input("Enter Book code : ")
    u = input("Count to be decreased : ")
    sql = "select total from books where bcode= %s"
    data = (code,)
    c = mydb.cursor()
    c.execute(sql, data)

    myresult = c.fetchone()
    t = myresult[0] - int(u)

    sql = "update books set total= %s where bcode= %s"
    data1 = (t, code)
    c.execute(sql, data1)
    mydb.commit()
    main()


def delbook():
    sql = "delete from books "
    c = mydb.cursor()
    c.execute(sql)
    mydb.commit()
    main()


def delissue():
    sql = "delete from issue "
    c = mydb.cursor()
    c.execute(sql)
    mydb.commit()
    main()
    main()


def delsubmit():
    sql = "delete from submit "
    c = mydb.cursor()
    c.execute(sql)
    mydb.commit()
    main()
    main()


def finepay():
    rno = input("Enter RollNO(char) : ")
    code = input("Enter Book Code(char) : ")
    pay = input("Have done payment(yes/no) : ")
    c = mydb.cursor()
    c.execute("update fine set payment=%s where regno=%s and bcode=%s", (pay, rno, code))
    print("payment done by ", rno, ': ', pay)
    mydb.commit()
    main()


def main():
    print("""....................  LIBRARY MANAGEMANT ..................... 

    1.Add Book
    2.Issue Book
    3.Submit Book
    4.Delete Options
    5.Search Options
    6.Display Book
    7.Display issued details
    8.Display Submitted details
    9.Display Fine Details
    10.Fine Payment

    """)

    choice = input("Enter Your Option : ")
    print('-------------------------------------------------------')
    if choice == "1":
        addbook()
    elif choice == "2":
        issueb()
    elif choice == "3":
        submitb()
    elif choice == "4":
        dbook()
    elif choice == "6":
        dispbook()
    elif choice == "5":
        search()
    elif choice == "7":
        dispissue()
    elif choice == "8":
        dispsubmit()
    elif choice == "9":
        dispfine()
    elif choice == "10":
        finepay()
    elif choice == "+":
        incbook()
    elif choice == "-":
        decbook()
    elif choice == ".":
        delbook()
    elif choice == "..":
        delissue()
    elif choice == "...":
        delsubmit()
    elif choice == "exit" or choice == "EXIT":
        print("------------------------Thank You----------------------")
        exit()

    else:
        print("wrong Choice")
        main()


def password():
    print("--------------------Library Management System---------------------")
    print("1.Admin login")
    print("2.Student Login")
    print()
    inp = input("Enter Login Type : ")
    if inp == '1':
        dictpass = {"suriya": "root", 'admin': 'admin'}
        '''import random
        ps = random.randint(0, 10)'''
        user = input("Enter Username : ")
        # print("Your Password is : ", ps)
        verify = input("Enter Password : ")
        if user in dictpass.keys():
            a = dictpass[user]
            if verify == a:
                main()
            else:
                print("Wrong Password Entered!!!")
                password()
        else:
            print("Wrong User Name Entered!!!")
            password()
    elif inp == '2':
        print("Not Yet Activated.........")
    else:
        password()


password()













