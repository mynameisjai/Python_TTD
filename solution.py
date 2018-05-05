'''
Created on 22-Mar-2018

@author: jayasakthiram
'''
from com.project.temple_classes import Hundi, Database, Priveleges, Specialdharshan, Sevas, Accomodation, Address, Devotee, Trustee
import sys, re
bill_topics_list = ['Booking Id', 'Booking Date', 'Booking For', 'Seats Booked', 'Total cost', 'Booked on']
trust_dict = {1:'BIRRD Trust', 2:'Sri Venkateswara Pranadana Trust', 3:'Sri Venkateswara Vidyadana Trust', 4:'Sri Venkateshwara Sarva Sreyas Trust'}
dharshan_object = Specialdharshan()
accmo_object = Accomodation()
trust_object = Trustee()

#Function to validate Login
def signin(admin=None, idtype=None):
    try:
        username = input('\tUsername : ')
        password = input('\tPassword : ')
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        if(admin == None):
            if(idtype == None):
                cur.execute("select firstName,username from person where username=(:0) and password =(:1) and idtype != 'ADMIN'", (username, password))
            else:
                cur.execute("select firstName,username from person where username=(:0) and password =(:1) and idtype=(:2)", (username, password, idtype))
        else:
            cur.execute('select firstName,username from person where username=(:0) and password =(:1) and idtype=(:2)', (username, password, 'ADMIN'))
        row = cur.fetchone()
        if row == None:
            print ('\n\tInvalid username/password')
            return False
        else:
            print ("\n\tWelcome ", row[0], "\n")
            return row[1]
        db.close(True)   
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()
    
#function used to validate each columns specified
def validate(string_to_validate, fname=None, lname=None, phone=None, email=None, user=None, passw=None):
    try:
        if fname == True or lname == True:
            if str(string_to_validate).isalpha():
                return True
            else:
                return False
        elif phone == True:
            db = Database('system', 'SysOracle')
            cur = db.get_cursor()
            if str(string_to_validate).isdigit() and len(string_to_validate) == 10:
                cur.execute("select mobileNumber from person where mobileNumber =:param", {'param':string_to_validate})
                result = cur.fetchall()
                db.close(True)
                if result == []:
                    return True
                else:
                    print("\tPhone  Already exists", file=sys.stderr)
                    return False
            else:
                return False
        elif email == True:
            db = Database('system', 'SysOracle')
            cur = db.get_cursor()
            if re.search(r"^([a-z0-9_\.-]+)@([\da-z-]+)\.([a-z\.]{2,6})$", string_to_validate):
                cur.execute("select emailId from person where emailId=:param", {'param':string_to_validate})
                result = cur.fetchall()
                db.close(True)
                if result == []:
                    
                    return True
                else:
                    print("\tEmail Id Already exists", file=sys.stderr)
                    return False
            else:
                return False
        elif user == True:
            if re.search(r"^[a-z0-9_-]{4,10}$", string_to_validate):
                db = Database('system', 'SysOracle')
                cur = db.get_cursor()
                cur.execute("select username from person where username=:param", {'param':string_to_validate})
                result = cur.fetchall()
                db.close(True)
                if result == []:
                    return True
                else:
                    print("\tUsername Already exists", file=sys.stderr)
                    return False
            else:
                return False
    
        elif passw == True:
            if re.search(r"^[A-Za-z0-9@!#$%^&*()?><\._-]{6,18}$", string_to_validate):
                return True
            else:
                return False
    
        else:
            return False
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def signup(personType=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        print("\n\tWelcome to TTD- User Registration:-\n\tFill the Below details...\n")
        if(personType.lower() == 'devotee'):
            person_object = Devotee()
        else:
            person_object = Trustee()
        test_choice = 1
        while test_choice == 1:
            first_name = input("\tFirst Name: ")
            if validate(first_name, fname=True) == True:
                person_object.set_firstname(first_name)
                test_choice = 0
            else:
                print("\n\tIN valid First name entered\n\tFirst name only contains alphabets or cannot be blank\n")    
        test_choice = 1
        while test_choice == 1:
            last_name = input("\tLast Name: ")
            if validate(last_name, lname=True) == True:
                person_object.set_lastname(last_name)
                test_choice = 0
            else:
                print("\n\tIN valid Last name entered\n\tLast name only contains alphabets or cannot be blank\n")    
    
        test_choice = 1
        while test_choice == 1:
            phone = input("\tMobile number (+91): ")
            if validate(phone, phone=True) == True:
                person_object.set_phonenumber(phone)
                test_choice = 0
            else:
                print("\n\tIN valid Phone number entered\n\tPhone number only contains  Digits with 10 digit length or cannot be blank\n")    
        
        test_choice = 1
        while test_choice == 1:
            emails = input("\tEmail Id: ")
            if validate(emails, email=True) == True:
                person_object.set_email(emails)
                test_choice = 0
            else:
                print("\n\tIN valid Email entered or Email id already registered or cannot be blank\n")    
    
        test_choice = 1
        while test_choice == 1:
            username = input("\tEnter Username for the Account: ")
            if validate(username, user=True) == True:
                person_object.set_username(username)
                test_choice = 0
            else:
                print("\n\tIn valid Username (Length of [4-16] and only [ _ , - ] special character is allowed)or Username already exists..")    
    
        test_choice = 1
        while test_choice == 1:
            password = input("\tEnter Password for the Account: ")
            if validate(password, passw=True) == True:
                person_object.set_password(password)
                test_choice = 0
            else:
                print("\n\tIn valid Password..\n\t\t1. Password must be of length (6-18) and only [ _ - ! @ # $ % ^ & * ( ) < > ? ] special character is allowed is allowed\n\t")    
    
        person_object.set_personid(get_personid())
        person_object.set_person_type(personType.lower())
        cur.execute("""insert into person values(:0,:1,:2,:3,:4,:5,:6,:7)""", (person_object.get_personid(), person_object.get_firstname(), person_object.get_lastname(), person_object.get_email(), person_object.get_phonenumber(), person_object.get_person_type(), person_object.get_username(), person_object.get_password()))
    
        db.close(True)
        address(person_object.get_personid())
        print("\n\t\tDon't share your Username and password to others. \n\t\tOur management is not responsible for it.\n")
        print("\n\t~~~~ ACCOUNT CREATED ~~~~\n\n")
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def address(personId=None, privilege=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        print("\n\tTTD management requires your Address for communication. So please fill your address details.\n")
        address_object = Address()
        address_object.set_line_1(input("\tAddress line1: "))
        address_object.set_line_2(input("\tAddress line2: "))
        address_object.set_city(input("\tCity: "))
        address_object.set_state(input("\tState: "))
        address_object.set_personid(personId)
        choice_exit = 1
        while choice_exit == 1:
            pincode = address_object.validatepincode(int(input("\tPincode: ")))
            if(pincode == None):
                print("Enter a Valid Pincode..", file=sys.stderr)
            else:
                address_object.set_pincode(pincode)
                choice_exit = 0
        if(privilege == None):
            cur.execute("insert into personAddress values (:0,:1)", (address_object.get_personid(), address_object.__repr__()))
        else:
            cur.execute("insert into ladduDelivery  values (:0,:1,to_date(sysdate,'dd-mm-yyyy'))", (address_object.get_personid(), address_object.__repr__()))
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

#function to get today's date
def get_date():
    db = Database('system', 'SysOracle')
    cur = db.get_cursor()
    cur.execute('select sysdate from dual')
    ddate = cur.fetchone()[0]
    db.close(True)
    return ddate

#function to generate booking Id
def get_booking_id_gen():
    
    db = Database('system', 'SysOracle')
    cursor = db.get_cursor()
    cursor.execute('select booking_no_gen.nextval from dual')
    bk_id = cursor.fetchone()[0]
    db.close(True)
    return bk_id

#function to generate Person Id
def get_personid():
    db = Database('system', 'SysOracle')
    cur = db.get_cursor()
    cur.execute('select user_id_gen.nextval from dual')
    cust_id = cur.fetchone()[0]
    db.close(True)
    return cust_id


def main_menu():  
    try:
        choice_exit=1
        while choice_exit == 1:
            print("\n\t\tWelcome to TTD Online services\n\n\t1. Admin Login\t\t\t2. Hundi\n\t3. Sevas Booking\t\t4. Darshan Entry Booking\n\t5. Accomadation\t\t\t6. Trusts donation\n\t7. Privileges Available\t\t8. Today's News and events\n\n\t\t\t\t9. QUIT")
            user_input = int(input("\n\tEnter your choice: "))
            if user_input == 1:
                print("""\n\tAdmin Login\n""")
                result = signin(admin=True)
                if result != False:
                    checker = 1
                    while checker == 1:
                        db = Database('system', 'SysOracle')
                        cur = db.get_cursor()
                        print("\t1. Update Schedules \n\t2. Delete old records\n\t3. Hundi collection\n\t4. Trust's amount collections\n\t5. Date codes Generation\n\t6. Logout\n")
                        user_input = int(input("\n\tEnter your choice: "))
                        if(user_input == 1):
                            cur.execute("""select * from schedule where dateToDisplay=to_date(:param,'dd-mon-yy') """, {'param':get_date()})
                            cur.fetchone()
                            if(cur.rowcount == 0):
                                print("\n\tAdmin! Todays News need to be updated first..")
                                end = 1
                                news_dict = {}
                                while(end == 1):
                                    timing = input("Enter time: ")
                                    news = input("Enter news: ")
                                    news_dict.update({timing:news})
                                    end = int(input("Enter \n\t'1' to continue\n\t'0' to end : "))
                                for key, value in news_dict.items():
                                    cur.execute("""insert into schedule values(:0,:1,to_date(:3,'dd-mon-yy'))""", (key, value, get_date()))
                                db.close(True)
                                update_schedule()
                            else:
                                db = Database('system', 'SysOracle')
                                cur = db.get_cursor()
                                cur.execute("""select to_char(max(dateToDisplay),'dd/mm/yyyy') from  schedule""")
                                result = cur.fetchone()
                                print("\tLast updated Date: ", result[0])
                                update_schedule()
                                db.close(True)
                        elif(user_input == 2):
                            print("\n\tWelcome Admin to the Trash..\n")
                            db = Database('system', 'SysOracle')
                            cur = db.get_cursor()
                            
                            cur.execute("""
                            select count(*) from dates_codes where dateavail in (select dateavail from dates_codes where (to_date(dateAvail)- to_date(sysdate)) < 0)
                            """)
                            rows = cur.fetchall()[0]
                            print("\t(", rows[0], ") days of old records found..\n")
                            if int(rows[0]) != 0:
                                delete_choice = int(input("\tAre you sure you want to delete these records ?\n\t1. Accept\n\t2. Decline\n\tYour choice: "))
                                if(delete_choice == 1):
                                    cur.execute("delete from dates_codes where dateavail in (select dateavail from dates_codes where (to_date(dateAvail) - to_date(sysdate)) < 0)")
                                    cur.execute("delete from status_user_prvlg where to_date(expirydate) < to_date(sysdate) or status = 'no'")
                                    db.close(True)
                                    print("\n\tDeleted old records..")
                                    print("\n\tRedirected to sub menu..\n")
                                else:
                                    print("\tRedirected to sub menu..\n")
                            else:
                                print("\tRedirected to sub menu..\n")
                        elif(user_input == 3):
                            print("\n\tWelcome to Hundi collections admin!\n")
                            db = Database('system', 'SysOracle')
                            cur = db.get_cursor()
                            cur.execute("select sum(amount) from hundi")
                            result = cur.fetchall()[0]
                            if(result[0] == None):
                                print("\n\tNo data found (means hundi yet to be filled)\n\n\tRedirected to sub menu....\n")
                            else:
                                cur.execute("select to_char(min(RECEIVED_ON),'dd/mm/yyyy') from hundi")
                                from_date = cur.fetchall()[0]
                                print("\t\tHundi Last updated on: ", *from_date, "\n")
                                print("\t\tReceived amount: Rs ", *result, "\n")
                                user_choice = int(input("\tWant to clear Hundi data?\n\t1.yes\t2.no\n\tYour choice: "))
                                if user_choice == 1:
                                    cur.execute("""delete from hundi""")
                                    db.close(True)
                                    print("\n\tHundi details are wiped out..\n")
                                else:
                                    print("\tRedirected to sub menu....\n")
                        elif(user_input == 4):
                            print("\n\tWelcome Admin to Trust Logs\n")
                            display_topics = ['Trust Name', 'Total Receives Amount']
                            db = Database('system', 'SysOracle')
                            cur = db.get_cursor()
                            cur.execute("""select trustname,trustamountcollected from trust_details""")
                            result = cur.fetchall()
                            print("\n\n\tTrust & Revenue details:-\n")
                            
                            for each in result:
                                print(end='\t')
                                print(display_topics[0], ":", each[0], end='\n', sep='\t')
                                print(display_topics[1], ":", each[1], end='\n', sep='\t')
                                print("\n")
                            cur.execute("select sum(trustamountcollected) from trust_details")
                            print("\n\tTotal Revenue earned from Trust (in Rs.)", ":", cur.fetchone()[0], end='\n', sep='\t')
                            print("\n\n")
                            print("\n\tRedirected to sub menu..\n")
                            db.close(True)
                        elif user_input == 5:
                            db = Database('system', 'SysOracle')
                            cur = db.get_cursor()
                            cur.execute("""
                            select count(*),to_char(max(dateavail),'dd-mon-yy') from dates_codes where dateavail in (select dateavail from dates_codes where (sysdate-to_date(dateAvail)) < 0)
                            """)
                            result = cur.fetchall()
                            count_avail = result[0][0]
                            max_date_avail = result[0][1]
                            if(count_avail < 7):
                                user_choice = int(input("\n\tAre you sure you want to generate date codes and data?\n\t1. Yes\t2. No\n\t:-"))
                                if(user_choice == 1):
                                    creation_panel(max_date_avail)
                                else:
                                    print("\n\tLets do this next time..\n\tRedirecting to submenu...\n")
                            else:
                                print("\n\tData available till: ", max_date_avail)
                                print("\n\tEnough Date codes and data available\n\n\tNo need to generate..\n\tRedirecting to submenu...\n\n")
                            db.close(True)
                        elif(user_input == 6):
                            checker = 0
                        else:
                            print("Enter only Available options (1-5): ")
                else:
                    print("\n\tRedirected to main menu..\n")       
            elif user_input == 2:
                print("\tAmount offered to Hundi is towards TTD Srivari Hundi,Tirumala.\n\tNo privileges would be provided for hundi offerings.")
                
                object_hundi = Hundi()
                object_hundi.set_hundi_amount(int(input("\nEnter Amount(In Rs.): ")))
                object_hundi.set_devotee_name(input("\tEnter name:"))
                object_hundi.set_devotee_mobile(int(input("\tEnter mobile number (+91):")))
                object_hundi.set_on_occasion_of(input("\tEnter On occasion of:"))
                db = Database('system', 'SysOracle')
                cur = db.get_cursor()
                cur.execute("""insert into hundi values(:0,:1,:2,:3,:4)""", (object_hundi.get_devotee_name(), object_hundi.get_devotee_mobile(), object_hundi.get_hundi_amount(), get_date(), object_hundi.get_on_occasion_of()))
                db.close(True)
                checker = 1
                while(checker == 1):
                    hundi_continue = int(input("Enter 1. continue \n      2. Exit\nEnter your choice: "))
                    if hundi_continue == 1:
                        print("Welcome again ", object_hundi.get_devotee_name())
                        object_hundi.set_hundi_amount(int(input("Enter Amount(In Rs.): ")))
                        object_hundi.set_on_occasion_of(input("\tEnter On occasion of:"))
                        db = Database('system', 'SysOracle')
                        cur = db.get_cursor()
                        cur.execute("""insert into hundi values(:0,:1,:2,:3,:4)""", (object_hundi.get_devotee_name(), object_hundi.get_devotee_mobile(), object_hundi.get_hundi_amount(), get_date(), object_hundi.get_on_occasion_of()))
                        db.close(True)
                
                    elif hundi_continue == 2:
                        print("""\n Govindha!! \tGovindha!!\n""")
                        checker = 0
                    else:
                        print("Please Enter (1-2) only..", file=sys.stderr)
                
            elif user_input == 3:
                db = Database('system', 'SysOracle')
                cur = db.get_cursor()
                print("\tWelcome to Seva Online portal..\n")
                print("\n\tYou can book for Seva well in advance through Seva online service.\n")
                username = signin()
                if(username != False):
                    seva(username=username)
                else:
                    print("\n\tRedirected to Main menu...\n")
                db.close(True)
            
                        
                
            elif user_input == 4:  # SPECIAL DHARSHAN BOOKING BLOCK COMPLETE
                call_flag = 0
                print("\n\tA pilgrim can avail the darshan of Lord Sri Venkateswara, Tirumala by booking 'Special Entry Darshan' tickets well-in advance through this portal.\n\n\t Select from Availble Dates...")
    
                login_choice = int(input("\tWelcome to Special dharshan Online booking portal..\n\tEnter \n\t1. Existing User\t2. New User\n\t:- "))
                if(login_choice == 1):
                    username = signin(idtype='devotee')
                    if(username != False):
                        call_flag = 1
                elif login_choice == 2:
                    signup(personType="devotee")
                    username = signin(idtype='devotee')
                    if(username != False):
                        call_flag = 1
                        
                if call_flag == 1:
                    special_dharshan(username_person=username) 
                    if dharshan_object.get_total_cost() != None:
                        if dharshan_object.get_total_cost() >= 5000:
                            print("\n\tDear User,\n\t\tAs you have reserved Special Entry Dharshan for over Rs.5000 in our online portal you are eligible for certain Privileges.\n\t\tDo you accept this privileges ?\n")
                            privilege_method(person_id=dharshan_object.get_personid())
                else:
                    print("\n\t\tRedirecting to Main menu...")
            elif user_input == 5:  # Accomodation BOOKING BLOCK COMPLETE
                call_flag = 0
                
                print("\t'Accomodation' allows you to book an Accommodation either in Tirumala or Tirupati well in advance.\n")
                login_choice = int(input("\tWelcome to Room Accommodation  Online booking portal..\n\tEnter \n\t1. Existing User\t2. New User\n\t:- "))
                if(login_choice == 1):
                    username = signin(idtype='devotee')
                    if(username != False):
                        call_flag = 1
                elif login_choice == 2:
                    signup(personType="devotee")
                    username = signin(idtype="devotee")
                    if(username != False):
                        call_flag = 1
                if call_flag == 1:
                    accomodation(username_person=username)
                    if accmo_object.get_room_pay() != None:
                        if accmo_object.get_room_pay() >= 5000:
                            print("\n\tDear User,\n\t\tAs you have Booked rooms for over Rs.5000 in our online Accomodation portal andso you are eligible for certain Privileges.\n\t\tDo you accept this privileges ?\n")
                            privilege_method(person_id=accmo_object.get_personid())                
                else:
                    print("\n\t\tRedirecting to Main menu...")
                
            elif user_input == 6:  # Trust donation is complete
                call_flag = 0
    
                print("\t\tMinimum amount to be deposited in a Trust: 5000 Rs")
                login_choice = int(input("\n\tWelcome to trustee Donation portal..\n\n\tPlease Enter \n\n\t1. Existing User\t2. New User\n\t:- "))
                if(login_choice == 1):
                    username = signin(idtype='trustee')
                    if(username != False):
                        call_flag = 1
                elif login_choice == 2:
                    signup(personType="trustee")
                    username = signin(idtype='trustee')
                    if(username != False):
                        call_flag = 1
                if call_flag == 1:
                    amount_to_donate = int(input("\n\tEnter amount to be donated : Rs. "))
                    if(amount_to_donate >= 5000):
                        donate_amount_check(amount_to_donate, username=username)
                    else:
                        print("\n\tSorry your denomination is less than required..\n")
                        print("\t\tRedirected to main menu..")
            elif user_input == 7:
                print("\n\t\tWelcome to privileges..\n")
                db = Database('system', 'SysOracle')
                cur = db.get_cursor()
                username = signin()
                id_list = []
                privilege_object = Priveleges()
                if(username != False):
                    cur.execute("""select userId from person where username=:param""", {'param':username})
                    user_id = cur.fetchone()[0]
                    privilege_object.set_personid(user_id)
                    cur.execute("""select  * from privilege_details where privilegeid in (select privilegeid from status_user_prvlg where userid=:param and to_number(expirydate-sysdate) >0 and status='yes')""", {'param':privilege_object.get_personid()})
                    prvlg_level = cur.fetchall()
                    if(prvlg_level != []):
                        counter = 1;
                        for each in prvlg_level:
                            cur.execute("""select to_char(expirydate,'dd-mm-yyyy') from status_user_prvlg where privilegeid=:param""", {'param':each[0]})
                            result = cur.fetchone()[0]
                            print("\n")
                            id_list.append(counter)
                            print("\t\tPrivilege Code", ':', counter, sep='\t', end="\t")
                            print("\tPrvilege Level", ':', each[1], sep='\t')
                            print("\t\tSeva pack", ':', each[2], sep='\t', end="\t")
                            print("\tSmall Laddu", ':', each[3], sep='\t')
                            print("\t\tBig laddu", ':', each[4], sep='\t', end="\t")
                            print("\tAccomodation", ':', each[5], sep='\t')
                            print("\t\tValidity Days", ':', each[6], sep='\t', end="\t")
                            print("\tExpiry On", ':', result, sep='\t')
                            counter += 1
                            print("\n\n")
                        exit_choice = int(input("\tDo you want to Use your Privilege 1. now or 2. later\n\tYour choice:- "))
                        if(exit_choice == 1):
                            user_input = int(input("Enter Privilege Code to confirm: "))
                            if user_input not in id_list:
                                
                                print("\t\tEnter Only Available privileges...", file=sys.stderr)
                                print("\t\tRedirected to main menu...\n")
                            else:
                                privilege_object.set_privilege_id(prvlg_level[user_input - 1][0])
                                if (prvlg_level[user_input - 1][1]) == 'Bronze' or (prvlg_level[user_input - 1][1]) == 'Silver':
                                    print("\n\tYou are eligible to book tickets for Sevas\n\tMaximum '2' seats can be booked from seva\n")
                                    seva(privilege=privilege_object.get_privilege_id(), username=username)
                                    
                                else:
                                    # accomodation redirect
                                    print("\n\tYou are up to use a highly privileged coupon..\n\tYou got 2 options to choose:-\n\t\t 1. Seva Booking\n\t\t2. Accomodation Booking\n")
                                    book_choice = int(input("\t\tYour Choice:- "))
                                    if(book_choice == 1):
                                        seva(privilege=privilege_object.get_privilege_id(), username=username)
                                    elif book_choice == 2:
                                        
                                        accomodation(username_person=privilege_object.get_personid(), privilege=privilege_object.get_privilege_id())
                            db.close(True)
                        else:
                            print("Redirected to main menu")
                    else:
                        print("\tSorry No privilege Available at the moment..\n\n\t\tRedirected to Main menu...\n")
                
                    
                
            elif user_input == 8:  # Schedules Visit is complete
                db = Database('system', 'SysOracle')
                cur = db.get_cursor()
                cur.execute("select timing,schedule from schedule where dateToDisplay=to_date(:param,'dd-mon-yy') ", {'param':get_date()})
                result = cur.fetchall()
                
                if result == []:
                    print("\n\tToday's Schedule is not yet updated\n\tSorry for the Inconvenience.\n")
                else:
                    print("\n")
                    print("\t\t\tTimings\t", "-", "Schedule", sep='\t')
                    
                    for each in result:
                        print("\t", each[0], "-", each[1], sep='\t')
                    db.close(True)
                user_choice = int(input("\n\tEnter\n\t1. Back to main menu\t2. Exit application\n\t:-"))
                if(user_choice == 1):
                    print("\n\tRedirected to main menu...")
                elif user_choice == 2:
                    choice_exit=0
                    
                else:
                    print("\tEntered wrong input", file=sys.stderr)
                    print("\n\tRedirected to main menu...")
            elif user_input == 9:
                choice_exit=0
                
            else:
                print("Please Enter in (1-9) only..", file=sys.stderr)
    
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()


def special_dharshan(privileged=None, username_person=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        cur.execute("""select userId from person where username=:param""", {'param':username_person})
        user_id = cur.fetchone()
        dharshan_object.set_personid(user_id[0])
        cur.execute(""" select dateCode,to_char(dateAvail,'dd-mm-yyyy') from dates_Codes where (to_date(dateAvail)-to_date(sysdate))>=0 and (to_date(dateAvail)-to_date(sysdate))<=7 order by dateCode""")
        dharshan_list = cur.fetchall()
        keys_list = []
        print("\n\t\tCode   ", "  Value\n")
        for key, value in dharshan_list:
            keys_list.append(key)
            print("\t\t", key, "\t", value, "\n")
        checker1 = 1
        while checker1 == 1:
            user_input = int(input("\tEnter the respective Date Code: "))
            if((user_input not in keys_list)):
                print("Select only the respective keys above...", file=sys.stderr)
            else:
                cur.execute("""select to_char(dateAvail,'dd-mon-yyyy') from dates_codes where dateCode=:param and (to_date(dateAvail)-to_date(sysdate))>=0 and (to_date(dateAvail)-to_date(sysdate))<=7""", {'param':user_input})
                dharshan_object.set_booking_date(cur.fetchone()[0])
                cur.execute("""select seatsAvailable from dharshan where dateOfDharshan=to_date(:param ,'dd-mon-yy')  and seatsAvailable>0""", {'param':dharshan_object.get_booking_date()})
                seats_available = cur.fetchone()[0]
                checker2 = 1
                while checker2 == 1:
                    print("Seats Available on the (", dharshan_object.get_booking_date(), ")", ":", seats_available)
                    print("\t\t\tPrice per seat :", dharshan_object.get_price_per_seat())
                    select_seats = (int(input("Enter required seats (min: 1, max: 30) : ")))
                    limit_to_book = 30
                    if(select_seats > seats_available or select_seats > limit_to_book):
                        print("Maximum Ticket limit exceeds...", file=sys.stderr)
                        
                    else:
                        dharshan_object.set_total_cost(dharshan_object.get_price_per_seat() * (select_seats))
                        dharshan_object.set_seats_quantity(select_seats)
                        dharshan_object.set_booking_id(get_booking_id_gen())
                        dharshan_object.set_booked_on(get_date())
                        cur.execute("update dharshan set seatsAvailable=seatsAvailable-:param1 where dateOfDharshan=:param2", {'param1':select_seats, 'param2':dharshan_object.get_booking_date()})
                        cur.execute("""insert into booking_details values(:0,:1,:2,:3,:4,:5,to_char(:6,'dd-mon-yyyy'))""", (dharshan_object.get_booking_id(), dharshan_object.get_booking_date(), 'Special Entry Dharshan', dharshan_object.get_seats_quantity(), dharshan_object.get_personid() , dharshan_object.get_total_cost(), dharshan_object.get_booked_on()))
                        cur.execute("select bookingId,bookingDate,bookingFor,seatsBooked,totalCost,to_char(bookedOn,'dd/mm/yyyy') from booking_details where bookingId=:param", {'param':dharshan_object.get_booking_id()})
                        result = cur.fetchall()[0]
                        print("\n\n\t\t\tSpecial Dharshan Booking details\n")
                        
                        counter = 0;
                        for each in result:
                            print("\t\t", bill_topics_list[counter], ":", each, end='\n', sep='\t')
                            counter += 1
                        checker2 = 0
                checker1 = 0
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def accomodation(username_person=None, privilege=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        if privilege == None:
            cur.execute("""select userId from person where username=:param""", {'param':username_person})
            user_id = cur.fetchone()
            accmo_object.set_personid(user_id[0])
        else:
            accmo_object.set_personid(username_person)
        checker = 1
        codes_list = []
        while checker == 1:
            print("\t\tAvailble Dates below...")
            result = cur.execute(""" select dateCode,to_char(dateAvail,'dd-mm-yyyy') from dates_Codes where (to_date(dateAvail)-to_date(sysdate))>0 and (to_date(dateAvail)-to_date(sysdate))<=7 order by dateCode""")
            print("\n\t\tCode   ", "  Value (dd-mm-yyyy)\n")
            for key, value in result:
                codes_list.append(key)
                print("\t\t", key, "\t", value, "\n")
    
            user_input = int(input("Enter the respective date code: "))
            if((user_input not in codes_list)):
                print("Select only the respective keys above...", file=sys.stderr)
            else:
                cur.execute("""select to_char(dateAvail,'dd-mon-yyyy') from dates_Codes where dateCode=:param and (to_date(dateAvail)-to_date(sysdate))>=0 and (to_date(dateAvail)-to_date(sysdate))<=7""", {'param':user_input})
                accmo_object.set_booking_date(cur.fetchone()[0])
                print("\n")
                checker2 = 1
                while checker2 == 1:
                    if privilege == None:
                        cur.execute("""select * from rooms_data where roomId in (select roomId from rooms_available where availabledate = to_date(:param ,'dd-mon-yy')) and privileged='no'""", {'param':accmo_object.get_booking_date()})
                        limit_to_book = 6
                    else:
                        cur.execute("""select * from rooms_data where roomId in (select roomId from rooms_available where availabledate = to_date(:param ,'dd-mon-yy')) and privileged='yes'""", {'param':accmo_object.get_booking_date()})
                        limit_to_book = 2
                    result = cur.fetchone();
                    roomid = []
                    while (result != None):
                        print("Room Id\t", ":", result[0], sep="\t")
                        roomid.append(result[0])
                        print("Hotel Name", ":", result[1], sep="\t")
                        print("Location", ":", result[2], sep="\t")
                        print("Price per Room", ":", result[3], sep="\t")
                        print("\n")
                        result = cur.fetchone()
                    
                    user_input = int(input("Enter Room Id :"))
                    if user_input not in roomid:
                        print("\t\tEntered wrong Room Id\n", file=sys.stderr)
                        
                    else:
                        print("Enter from Time slot below..\n\t1: (00:00 to 05:59 hrs)\n\t2: (06:00 to 11:59 hrs)\n\t3: (12:00 to 17:59 hrs)\n\t4: (18:00 to 23:59 hrs)\n\n")
                        accmo_object.set_room_id(user_input)
                        cur.execute("""select roomsAvailable from rooms_available where roomId=:param1 and availabledate=:param2""", {'param1':accmo_object.get_room_id(), 'param2':accmo_object.get_booking_date()})
                        result = cur.fetchone();
                        seats_result = []
                        while (result != None):
                            seats_result.append(result[0])
                            result = cur.fetchone()
                        counter = 0
                        null_counter_list = []
                        counter_value = []
                        print("Time slot", ":", "Seats Available", sep="\t")
                        for each in seats_result:
                            counter += 1
                            print(end="\t")
                            if each == 0:
                                null_counter_list.append(counter)
                            counter_value.append(each)
                            print(counter, ":", each, sep="\t")
                        if len(null_counter_list) < 4:
                            time_slot_input = int(input("Enter time slots satisfies your conditions: "))
                            accmo_object.set_time_slot(time_slot_input)
                            if(time_slot_input not in null_counter_list and time_slot_input >= 1 and time_slot_input <= 4):
                                per_room_cost = cur.execute("""select perRoomCost from rooms_data where roomId=:param""", {'param':accmo_object.get_room_id()})
                                accmo_object.set_per_room_cost(int(*list(per_room_cost)[0]))
                                print("\t\tPer Room cost in selected hotel :", accmo_object.get_per_room_cost())
                                print("\n\t\tMinimum room :  1\n\t\tMaximum rooms: ", limit_to_book, "\n")
                                user_input = int(input("\n\tEnter required rooms: "))
                                if user_input <= limit_to_book and (counter_value[time_slot_input - 1] - user_input) >= 0 and user_input > 0:
                                    accmo_object.set_seats_quantity(user_input)
                                    accmo_object.set_booked_on(get_date())
                                    accmo_object.set_booking_id(get_booking_id_gen())
                                    result = cur.execute("""select roomDescription,location from rooms_data where roomId=:param""", {'param':accmo_object.get_room_id()})
                                    for each in list(result):
                                        accmo_object.set_room_description(each[0])
                                        accmo_object.set_room_location(each[1])
                                        accmo_object.set_room_pay(accmo_object.get_per_room_cost() * accmo_object.get_seats_quantity())
                                    cur.execute("""insert into booking_details values(:0,:1,:2,:3,:4,:5,to_char(:6,'dd-mon-yyyy'))""", (accmo_object.get_booking_id(), accmo_object.get_booking_date(), accmo_object.get_room_description() + " , " + accmo_object.get_room_location(), accmo_object.get_seats_quantity(), accmo_object.get_personid(), accmo_object.get_room_pay(), accmo_object.get_booked_on()))
                                    cur.execute("select bookingId,bookingDate,bookingFor,seatsBooked,totalCost,to_char(bookedOn,'dd/mm/yyyy') from booking_details where bookingId=:param", {'param':accmo_object.get_booking_id()})
                                    result = cur.fetchall()[0]        
                                    cur.execute("""update rooms_available set roomsAvailable = roomsAvailable - :param1  where roomId=:param2 and timeSlot=:param3 and availabledate= :param4""", {'param1':accmo_object.get_seats_quantity(), 'param2':accmo_object.get_room_id(), 'param3':accmo_object.get_time_slot(), 'param4':accmo_object.get_booking_date()})
                                    print("\n\n\t\t\tAccomodation Booking details\n")
                                    counter = 0;
                                    for each in result:
                                        if counter != 4 and privilege != None:
                                            print("\t\t", bill_topics_list[counter], ":", each, end='\n', sep='\t')
                                        elif privilege == None:
                                            print("\t\t", bill_topics_list[counter], ":", each, end='\n', sep='\t')
                                        counter += 1    
                                    print("\t\t\tTime Slot", ":", accmo_object.get_time_slot(), "\n\n", sep='\t')
                                    if(privilege != None):
                                        laddu(personid=accmo_object.get_personid(), privilegeid=privilege)
                                    checker2 = 0
                                else:
                                    print("\n\t\tInvalid Request more rooms were requested than available", file=sys.stderr)
                                    accmo_object.set_room_pay(0)
                                    print("\n\t\tRedirected to Main menu..")
                                    checker2 = 0
                                checker = 0
                            else:
                                print("\t\tInvalid Request Due to :-\n\t1. Wrong timeslot selected with 0 rooms\n\t2. Wrong Timeslot typed\n", file=sys.stderr)
                                accmo_object.set_room_pay(0)
                                print("\t\tRedirected to Main menu..\n")
                                checker2 = 0
                            checker = 0
                        else:
                            print("\nSorry for the inconvenience no rooms available @ the respective hotel on the selected date\n")
                            accmo_object.set_room_pay(0)
                            checker2 = 0
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()
    
def trust_donation(username_person, trust_name, cost):
    db = Database('system', 'SysOracle')
    cur = db.get_cursor()
    cur.execute("""select userId from person where username=:param""", {'param':username_person})
    user_id = cur.fetchone()
    trust_object.set_personid(user_id[0])
    trust_object.set_date_donated(get_date())
    trust_object.set_donated_amount(cost)
    trust_object.set_trust_name(trust_name)
    cur.execute("""select trustId from trust_details where trustName=:param""", {'param':trust_object.get_trust_name()})
    trust_id = cur.fetchone()[0]
    cur.execute("""insert into trustee values(:0,:1,:2,:3)""", (trust_object.get_personid(), trust_object.get_donated_amount(), trust_id, trust_object.get_date_donated()))
    cur.execute("update trust_details set trustAmountCollected = trustAmountCollected + :0 where trustId = :1", (trust_object.get_donated_amount(), trust_id))
    db.close(True)
    
def donate_amount_check(amount_to_donate, username):

    if(amount_to_donate > 5000 and amount_to_donate < 10000):
        trust_name_trust = trust_dict.get(1)
        privilege_trust = 'Bronze'
        
    elif(amount_to_donate > 10000 and amount_to_donate < 100000):
        trust_name_trust = trust_dict.get(2)
        privilege_trust = 'Silver'

        
    elif(amount_to_donate > 100000 and amount_to_donate < 1000000):
        trust_name_trust = trust_dict.get(3)
        privilege_trust = 'Gold'

        
    elif(amount_to_donate > 1000000 and amount_to_donate < 10000000):
        trust_name_trust = trust_dict.get(4)
        privilege_trust = 'Diamond'

       
        
    elif(amount_to_donate > 10000000):
        trust_name_trust = trust_dict.get(5)
        privilege_trust = 'Platinum'

       
    trust_donation(username_person=username, trust_name=trust_name_trust, cost=amount_to_donate)
    print("\tYour amount is eligible to be donated", ':', trust_name_trust, sep='\t')
    print("\n\tDear User,\n\t\tThanks for donating in our online portal and you are eligible for certain Privileges.\n\t\tDo you accept this privileges ?\n")
    privilege_method(person_id=trust_object.get_personid(), privilege=privilege_trust)

def privilege_method(privilege=None, person_id=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        prvlg_label = ['Privilege Id\t', 'Privilege Level  ', 'Seva Pack\t   ', 'Small Laddu Pack ', 'Big Laddu Pack   ', 'Accomodation Pack', 'Validity days    ']
        prvlg_dict = {}
        prvlg_object = Priveleges()
        prvlg_object.set_personid(person_id)
        if(privilege == None):
            cur.execute("""select privilegeid, privilegename,sevapack,smallladdu,bigladdu,accomodationpack,validity from privilege_details where privilegeName=:param""", {'param':'Bronze'})
        else:
            cur.execute("""select privilegeid, privilegename,sevapack,smallladdu,bigladdu,accomodationpack,validity from privilege_details where privilegeName=:param""", {'param':privilege})
        result = cur.fetchall()[0]
        prvlg_object.set_privilege_id(result[0])
        prvlg_object.set_privilege_name(result[1])
        prvlg_object.set_privilege_validity_days(result[6])
        prvlg_object.set_privilege_status("yes")
        counter = 0
        for each in result:
            prvlg_dict.update({prvlg_label[counter]:each})
            counter += 1
        prvlg_label.remove('Privilege Id\t')
        
        for each in prvlg_label:
            print("\t\t", each, ':', prvlg_dict.get(each), sep='\t')
        cur.execute("select to_char((sysdate + (:param)),'dd-mon-yyyy') from dual" , {'param':prvlg_object.get_privilege_validity_days()})
        prvlg_object.set_privilege_expiry_date(cur.fetchall()[0][0])
        user_choice = int(input("\n\t\t1.Accept offer\n\t\t2.Decline offer\n\t\t:- "))
        if user_choice == 1:
            cur.execute("""insert into status_user_prvlg values(:0,:1,:2,:3)""", (prvlg_object.get_personid(), prvlg_object.get_privilege_id(), prvlg_object.get_privilege_status() , prvlg_object.get_privilege_expiry_date()))
            print("\n\t\tThanks for Accepting the privilege...\n\t\t\tGovindha.... \t Govindha...\n\n")
        else:
            print("\n\n")
            print("\t\t\tThanks for using our services...\n\t\t\tGovindha.... \t Govindha...\n\n")
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def seva(username, privilege=None):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        seva_object = Sevas()
        cur.execute("""select userId from person where username=:param""", {'param':username})
        user_id = cur.fetchone()
        seva_object.set_personid(user_id[0])
        cur.execute("""select  privilegeid,privilegename from privilege_details where privilegeid = (select min(privilegeid) from status_user_prvlg where userid=:param and to_number(expirydate-sysdate) >0 and status='yes')""", {'param':seva_object.get_personid()})
        prvlg_id = cur.fetchone()
        
        if(prvlg_id != None):
            if(privilege == None):
                seva_object.set_privileage_id(prvlg_id[0])
            else:
                seva_object.set_privileage_id(privilege)
            seva_dicts = {1:'Visesha Pooja', 2:'Kalyanotsavam', 3:'Vasanthotsavam', 4:'Unjal Seva', 5:'Sahasra Deepalankara Seva', 6:'Arjitha Brahmotsavam'}
            print("\tSelect a Seva from below..\n")
            print("\n\tCode\t Sevas List\n")
            for key, value in seva_dicts.items():
                print("\t", key, "\t", value)
            choice_exit = 1
            while choice_exit == 1:
                user_input = int(input("\nEnter Seva Code: "))
                if user_input >= 1 and user_input <= 6:
                    choice_exit = 0
                else:
                    print("Select only available sevas (1-6)", file=sys.stderr)
            seva_object.set_seva_name(seva_dicts.get(user_input))
            print("\n\tSelected Seva: ", seva_object.get_seva_name())
            result = cur.execute("select sevaNo from sevas where sevaName=:param", {'param':seva_object.get_seva_name()})
            seva_object.set_seva_no(*list(result)[0])
            result = cur.execute("""
                select dateCode,to_char(dateAvail,'dd-mm-yyyy') from dates_codes 
                where dateAvail in (select dateAvail from sevas_on_dates 
                where sevaNo = (select sevaNo from sevas where sevaName=:param)) 
                and to_number(dateavail- sysdate) >0 and to_number(dateavail- sysdate) <=7 order by dateCode""",
                {'param':seva_object.get_seva_name()})
            print("\n\tCode\tAvailable_Date")
            codes_list = []
            for key, value in result:
                codes_list.append(key)
                print("\t\t", key, "\t", value, "\n")
            choice_exit = 1
            while choice_exit == 1:
                user_input = int(input("\nEnter respective Date Code:"))
                if user_input not in codes_list:
                    print("Enter only availble date Codes", file=sys.stderr)
                else:
                    choice_exit = 0
            result = cur.execute("""select to_char(dateAvail,'dd-mon-yyyy') from dates_codes where dateCode=:param and to_number(dateavail- sysdate) >0 and to_number(dateavail- sysdate) <=7""", {'param':user_input})
            seva_object.set_booking_date(*list(result)[0])
            cur.execute("""select seatsAvailable from sevas_on_dates where sevaNo=:0 and dateAvail=(to_date(:1,'dd-mon-yy'))""", (seva_object.get_seva_no(), seva_object.get_booking_date()))
            result = cur.fetchall()[0]
            seva_object.set_seva_seats(result[0])
            print("Available seats for ", seva_object.get_seva_name(), " seva on (", seva_object.get_booking_date(), ")\n\t\tSeats: ", seva_object.get_seva_seats())
            user_input = int(input("\tEnter seat Qty (min:1 , max:2 ): "))
            limit_seat = 2
            if(user_input <= limit_seat):
                seva_object.set_seats_quantity(user_input)
                seva_object.set_booked_on(get_date())
                seva_object.set_booking_id(get_booking_id_gen())
                cur.execute("""update sevas_on_dates set seatsAvailable=(seatsAvailable-(:param1)) where sevaNo=:param2 and dateAvail=(to_date(:param3,'dd-mon-yy'))""", {'param1':seva_object.get_seats_quantity(), 'param2':seva_object.get_seva_no(), 'param3':seva_object.get_booking_date()})
                cur.execute("""insert into booking_details values(:0,:1,:2,:3,:4,:5,:6)""", (seva_object.get_booking_id(), seva_object.get_booking_date(), seva_object.get_seva_name(), seva_object.get_seats_quantity(), seva_object.get_personid(), None, seva_object.get_booked_on()))
                cur.execute("select bookingId,bookingDate,bookingFor,seatsBooked,totalCost,to_char(bookedOn,'dd/mm/yyyy') from booking_details where bookingId=:param", {'param':seva_object.get_booking_id()})
                result = cur.fetchall()[0]
                print("\n\n\tYour Booking details:-\n")
                counter = 0;
                for each in result:
                    if counter != 4:
                        print(bill_topics_list[counter], ":", each, end='\n', sep='\t')
                    counter += 1
                print("\n\tThanks for using our services...\n\tGovindha..\tGovindha..\n")
                laddu(personid=seva_object.get_personid(), privilegeid=seva_object.get_privileage_id())
                
            else:
                print("\n\tExceeds Maximum seats..", file=sys.stderr)
                print("\n\tRedirected to main menu...\n")
        else:
            print("\n\t\tNo privileges Availble to book Sevas in advance", file=sys.stderr)
            print("\n\tRedirected to main menu...\n")
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def laddu(personid, privilegeid):
    try:
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        print("\n\tTirupati Prasadam (Laddu pack) will be sent to your address by postage")
        cur.execute("select address from personAddress where userid=:param", {'param':personid})
        address_to_mail = cur.fetchall()
        print("\n\tRegistered Address:\n", address_to_mail[0][0])
        print("\n\tWill be sent to\n\t1.Registered Address\t2.Alternative Address")
        user_prefer = int(input("\n\tYour choice: "))
        if(user_prefer == 2):
            print("\tEnter an Alternative address:")
            address(personid, privilege=True)
            print("\tRespective Laddu pack will be sent to your Alternative Address")
        else:
            cur.execute("insert into ladduDelivery  values (:0,:1,to_date(sysdate,'dd-mm-yyyy'))", (personid, address_to_mail[0][0]))
            print("\tRespective Laddu pack will be sent to your Registered Address")
        cur.execute("""
            update status_user_prvlg set status='no' where userId=:param1 and privilegeId =:param2 and status =:param3
            """, {'param1':personid, 'param2':privilegeid, 'param3':'yes'})
        db.close(True)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

def update_schedule():
    try:
        print("\n\tToday's Events are updated..\n\t1. Delete events\n\t2. Add Next day's Events\n\t3. Sub menu\n")
        user_choice = int(input("Enter your choice: "))
        if(user_choice == 1):
            db = Database('system', 'SysOracle')
            cur = db.get_cursor()
            second_choice = int(input("\n\t1. Today's event\n\t2. Random Event\n\tEnter your choice: "))
            if(second_choice == 1):
                cur.execute("delete from schedule where dateToDisplay=to_date(:param,'dd-mm-yy') ", {'param':get_date()})
                print("\n\tSuccessfully deleted Today's data\n")
                db.close(True)
            elif second_choice == 2:
                select_date = input("\tEnter date to delete (dd-mm-yyyy): ")
                cur.execute("select * from schedule where dateToDisplay=to_date(:param,'dd-mm-yy') ", {'param':select_date})
                exists = cur.fetchone()
                if exists != None:
                    cur.execute("delete from schedule where dateToDisplay=to_date(:param,'dd-mm-yy') ", {'param':select_date})
                    print("\n\tSuccessfully deleted data on (", select_date, ")\n")
                else:
                    print("\n\tNo such record found on (", select_date, ")\n")
                db.close(True)
            
        elif(user_choice == 2):
            db = Database('system', 'SysOracle')
            cur = db.get_cursor()
            cur.execute(""" select dateCode,to_char(dateAvail,'dd-mm-yyyy') from dates_Codes where (to_date(dateAvail)-sysdate)>0 and (to_date(dateAvail)-sysdate)<=7 and dateavail not in (select dateToDisplay from schedule) order by dateAvail""")
            date_list = cur.fetchall()
            if date_list != []:
                keys_list = []
                print("\n\t\tCode   ", "  Value\n")
                for key, value in date_list:
                    keys_list.append(key)
                    print("\t\t", key, "\t", value, "\n")
                checker1 = 1
                while checker1 == 1:
                    user_input = int(input("\tEnter the respective Date Code: "))
                    if((user_input not in keys_list)):
                        print("Select only the respective keys above...", file=sys.stderr)
                    else:
                        cur.execute("""select to_char(dateAvail,'dd-mon-yyyy') from dates_codes where dateCode=:param and (to_date(dateAvail)-sysdate)>0 and (to_date(dateAvail)-sysdate)<=7""", {'param':user_input})
                        select_date = cur.fetchone()[0]
                        end = 1
                        news_dict = {}
                        while(end == 1):
                            timing = input("Enter time: ")
                            news = input("Enter news: ")
                            news_dict.update({timing:news})
                            end = int(input("Enter \n\t'1' to continue\n\t'0' to end : "))
                        for key, value in news_dict.items():
                            cur.execute("""insert into schedule values(:0,:1,to_date(:3,'dd-mon-yy'))""", (key, value, select_date))
                        checker1 = 0
                        print("\n\t\tUpdated Schedule on (", select_date, ")...\n")
            else:
                print("\n\tAll enabled dates are updated..\n\tRedirected to Sub menu...\n")
            db.close(True) 
        else:
            print("\tRedirected to Sub menu...\n")
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()
    
def creation_panel(max_date_avail):
    try:
        if (max_date_avail == None):
            max_date_avail = get_date()
            start_range = 0
        else:
            start_range = 1
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        cur.execute("drop sequence date_code_gen")
        print("\n\tSuccessfully dropped old Sequence..\n", file=sys.stderr)
        cur.execute("""create sequence date_code_gen
                        start with 1
                        maxvalue 999
                        increment by 1
                        nocycle""")
        db.close(True)
        print("\n\tSuccessfully created new Sequence..\n", file=sys.stderr)
        
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        for date in range(0, 181):
            cur.execute("insert into dates_codes values (date_code_gen.nextval,to_date(:param1)+:param2)", {'param1':max_date_avail, 'param2':date})
        db.close(True)
        print("\n\tInserted Date Codes\n", file=sys.stderr)
        
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        for date in range(start_range, 181):
            cur.execute("""insert into dharshan values(to_date(:param1)+:param2,500)""", {'param1':max_date_avail, 'param2':date})
        db.close(True)
        print("\n\tInserted Special entry dharshan's data\n", file=sys.stderr)
    
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        cur.execute("select sevaNo from sevas")
        result = cur.fetchall()
        seva_seats = 25
        for date in range(start_range, 181):
            for each in result:
                cur.execute("""
                insert into sevas_on_dates values(to_date(:param1)+:param2,:param3,:param4)
                """, {'param1':max_date_avail, 'param2':date, 'param3':each[0], 'param4':seva_seats})
        db.close(True)
        print("\n\tInserted Seva's data\n", file=sys.stderr)
        db = Database('system', 'SysOracle')
        cur = db.get_cursor()
        cur.execute("select roomId from rooms_data")
        result = cur.fetchall()
        time_slot_rooms_dict = {1:15, 2:15, 3:30, 4:50}
        for date in range(start_range, 181):
            for each in result:
                for key, value in time_slot_rooms_dict.items():
                    cur.execute("insert into rooms_available values(to_date(:param1)+:param2,:param3,:param4,:param5)", {'param1':max_date_avail, 'param2':date, 'param3':each[0], 'param4':key, 'param5':value}) 
        db.close(True)
        print("\n\tInserted Accomodation's data\n", file=sys.stderr)
    except Exception as e:
        print ('#' * 30)
        print('Error Message:', e)
        print('Please Try again')
        print ('#' * 30)
        main_menu()

if __name__ == '__main__':
    main_menu()
    print("\n\tThanks you for using our services...\n\tCopyright 2016. Tirumala  Tirupati Devasthanams - All rights reserved\n")

    
