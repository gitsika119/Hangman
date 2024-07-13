
import mysql.connector
import sys

def hangman():
    stages =['''
        +---+
         |  |
         O  |
        /|\ |
        / \ |
            |
    =========
    ''', '''
        +---+
         |  |
         O  |
        /|\ |
        /   |
            |
    =========
    ''', '''
        +---+
         |  |
         O  |
        /|\ |
            |
            |
    =========
    ''', '''
        +---+
         |  |
         O  |
        /|  |
            |
            |
    =========''', '''
        +---+
         |  |
         O  |
         |  |
            |
            |
    =========
    ''', '''
        +---+
         |  |
         O  |
            |
            |
            |
    =========
    ''', '''
        +---+
          | |
            |
            |
            |
            |
    =========
    ''']
    
    print()
    print("*"*30,"Welcome to Hangman","*"*30)
    print()
    print("Select a theme")
    print("1 => anime")
    print("2 => film industry")
    print("3 => sports")
    print("4 => singers")
    print("5 => countries")
    print()
    
    b=(input("Enter theme number: "))
    if b=='1':
        b='anime'
        l=['naruto','luffy','ichigo','asta','goku','gintoki','itadori','deku','tanjiro','eren jaeger']
    elif b=='2':
        b='film industry'
        l=['leonardo dicaprio','salman khan','conjuring','american psycho','hrithik roshan','katrina kaif','sidharth malhotra','sholay','emma watson','student of the year']
    elif b=='3':
        b='sports'
        l=['basketball','football','cricket','usain bolt','hockey','ronaldo','messi','lebron james','stephen curry','virat kohli']
    elif b=='4':
        b='singers'
        l=['zayn malik','ariana grande','the weeknd','arijit singh','atif aslam','the neighbourhood','my chemical romance','kendrick lamar','eminem','kid cudi']
    elif b=='5':
        b='countries'
        l=['india','pakistan','russia','china','japan','canada','dubai','nepal','germany','nigeria']
    else:
        print("Invalid entry")
        game()
 
    ch=0
    while True:
        for i in l:
            display = []
            for _ in i:
                if _ != " ":
                    display += "_"
                else:
                    display +=" "
            lives = 6
            print()
            print("Guess the word:- ", end=" ")
            print(f"{' '.join(display)}")
            print(f"Lives: {lives}")
            print()
            while lives>0:
                    guess = input("Guess a Letter: ").lower()
                    if not (guess in i):
                            lives -= 1
                    index = 0
                    for c in i:
                        if c == guess:
                                display[index] = guess
                        index += 1
                    print(f"{' '.join(display)}")
                    print(f"Lives: {lives}")
                    print(stages[lives-1])
                    if "_" not in display:
                            print("You Win")
                            ch=ch+1
                            if ch==10:
                                mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
                                mycur=mydb.cursor()
                                sql="insert into stats values(%s,%s,%s)"
                                mycur.execute(sql,(z,b,ch))
                                mydb.commit()
                                print()
                                print("Theme over, you win!")
                                print()
                                hs()
                                game()
                                sys.exit()
                            break
                    if lives == 0:
                        while True:
                            mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
                            mycur=mydb.cursor()
                            sql="insert into stats values(%s,%s,%s)"
                            mycur.execute(sql,(z,b,ch))
                            mydb.commit()
                            print("You Lose")
                            print(f"The word was: {i}")
                            print("Game over")
                            print()
                            hs()
                            game()
                            sys.exit()
                        
def hs():                            
    mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
    mycur=mydb.cursor()                            
    sql="select max(correct_guesses)from stats"
    mycur.execute(sql,)
    x=mycur.fetchall()
    mydb.commit()
    for i in x:
        for j in i:
            y=j
    sql="select correct_guesses,gamertag,theme from stats where correct_guesses=%s"
    mycur.execute(sql,(y,))
    k=mycur.fetchall()
    mydb.commit()
    l=[]
    for i in k:
        for j in i:
            l.append(j)
    m=0
    n=1
    o=2
    while True:
        try:
            print("Current high score => ",l[m])
            print("By => " ,l[n])
            print("With theme => ",l[o])
            print()
            m=m+3
            n=n+3
            o=o+3
        except:
            break

def game():
    print()
    print("CLICK A TO CONTINUE")
    print("CLICK B TO LEAVE")
    print()
    i=input("Enter choice: ")
    while True:
        if i=="A" or i=="a":
            hangman()
        elif i=='B'or i=="b":
            print()
            print("Leaving...")
            break
        else:
            print("Invalid entry")
            break  
    
def log():
    mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
    mycur=mydb.cursor(buffered=True)
    global z
    z=input("Enter gamertag: ")
    sql="select player_name from login where gamertag=%s"
    mycur.execute(sql,(z,))
    r=(mycur.fetchone())
    if r=='None' or r==('None',)or r==None:
        print("Gamertag doesn't exist")
        print()
        print("Click A to try login again")
        print("Click B to sign up")
        print("Click X to leave")
        print()
        a=input("Enter choice: ")
        if a=='b' or a=='B':
            sign()
        elif a=='A' or a=='a':
            z=input("Enter gamertag: ")
            sql="select player_name from login where gamertag=%s"
            mycur.execute(sql,(z,))
            r=(mycur.fetchone())
            if r=='None' or r==('None',)or r==None:
                print("Gamertag doesn't exist")
                print("Redirecting to sign up...")
                sign()
        else:
            print("Leaving...")
    else:
        sql="select phoneNO from userdet where gamertag=%s"
        mycur.execute(sql,(z,))
        re=(mycur.fetchone())
        sql="select emailID from userdet where gamertag=%s"
        mycur.execute(sql,(z,))
        res=(mycur.fetchone())
        sql="insert into userdet values(%s,%s,%s)"
        mycur.execute(sql,(str(z),str(res),str(re)))
        mydb.commit()
        mydb.close()
        print()
        print("Added login info")
    
def sign():
    mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
    mycur=mydb.cursor()
    global z
    print()
    y=input("Enter player name: ")
    z=input("Enter gamertag: ")
    a=input("Enter phone number: ")
    b=input("Enter email id: ")
    print()
    try:
        sql="insert into login values(%s,%s)"
        mycur.execute(sql,(y,z))
        mydb.commit()
        print("Added login info")
    except:
        print("Gamertag in use, pick another")
        print()
        while True:
            try:
                z=input("Enter gamertag: ")
                sql="insert into login values(%s,%s)"
                mycur.execute(sql,(y,z))
                mydb.commit()
                print("Added login info")
            except:
                print("Gamertag in use, pick another")
            else:
                break
    sql="insert into userdet values(%s,%s,%s)"
    mycur.execute(sql,(z,b,a))
    mydb.commit()
    print("Added user data")

def update():
    mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
    mycur=mydb.cursor()
    x=input("Enter gamertag to change phone number: ")
    y=input("Enter new phone number: ")
    try:
        sql="update userdet set phoneNO=%s where gamertag=%s"
        mycur.execute(sql,(y,x))
        mydb.commit()
        print("Updated phone number")
        print()
    except:
        print("Invalid Entry")
        print("Redirecting")
        print()

def delete():
    mydb=mysql.connector.connect(host="localhost",user="root",password="giti",database="hangman")
    mycur=mydb.cursor()
    x=input("Enter gamertag you want to delete: ")
    y=input("Are you sure you want to delete all stats <y/n>: ")
    try:
        if y=="Y" or y=="y":
            sql="delete from login where gamertag=%s"
            mycur.execute(sql,(x,))
            sql="delete from userdet where gamertag=%s"
            mycur.execute(sql,(x,))
            sql="delete from stats where gamertag=%s"
            mycur.execute(sql,(x,))
            mydb.commit()
            print("Deleted all records")
            print()
        elif y=="N"or y=="n":
            print("Redirecting...")
        else:
            print("Redirecting...")
    except:
        print("Invalid Entry")
        print("Redirecting")
        print()

print("*"*30,"LOGIN/SIGN UP","*"*30)
print()
print("CLICK A TO LOGIN")
print("CLICK B TO SIGN UP")
print("CLICK Y TO UPDATE PHONE NO.")
print("CLICK Z TO DELETE USER")
print("CLICK X TO LEAVE")
print()
x=input("Enter option:")
if x.upper()=="A":
    log()
    game()
elif x.upper()=="B":
    sign()
    game()
elif x.upper()=="Y":
    update()
    print("CLICK A TO LOGIN")
    print("CLICK B TO SIGN UP")
    print("CLICK X TO LEAVE")
    x=input("Enter option:")
    if x.upper()=="A":
        log()
        game()
    elif x.upper()=="B":
        sign()
        game()
    elif x.upper()=="X":
        print()
        print("Leaving...")
elif x.upper()=="Z":
    delete()
    print("CLICK A TO LOGIN")
    print("CLICK B TO SIGN UP")
    print("CLICK X TO LEAVE")
    x=input("Enter option:")
    if x.upper()=="A":
        log()
        game()
    elif x.upper()=="B":
        sign()
        game()
    elif x.upper()=="X":
        print()
        print("Leaving...")
elif x.upper()=="X":
    print()
    print("Leaving...")