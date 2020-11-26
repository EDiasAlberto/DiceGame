#These are libraries that are used later.
import tkinter #This is used for the GUI
from tkinter import messagebox #This is used to show alerts after rounds and for incorrect logins.
import random #This is used to generate pseudo-random dice values.

#---------------------Global variables---------------------


helv36 = ("Helvetica", 36)
helv24 = ("Helvetica", 24)
helv12 = ("Helvetica", 12)

helv36Bold = ("Helvetica", 36, "bold")
helv24Bold = ("Helvetica", 24, "bold")
helv12Bold = ("Helvetica", 12, "bold")

plrList = [] #Just a list to hold both player objects.

#--------------Class to represent each player--------------
class Player:
    def __init__(self, username):
        self.username = username
        self.score    = 0

    # Function to roll a die and generate a random value for all three.
    def rollADie(self, die):
        die1Value = die.roll()
        die2Value = die.roll()
        turnTotal = die1Value + die2Value
        
        #If the user rolls a double, they get to roll a third die.
        #The third die is rolled in the roundGameLogic function.
        if die1Value == die2Value:
            self.score+= die1Value + die2Value
            condition = "double"
            
        #If the total is even, then the user's score increases by 10
        elif turnTotal%2==0:
            self.score+=turnTotal + 10
            condition = "even"
            
        #If the total is odd, then the user loses 3 points and the score becomes 0, or the score, whichever is larger
        #in order to prevent the user's score dropping below 0.
        else:
            self.score=max(self.score+turnTotal - 3, 0)
            condition = "odd"
            
        return die1Value, die2Value, condition

#------------Class to represent each of the dice------------
class Die:
    def __init__(self):
        self.values = [1, 2, 3, 4, 5, 6]
    
    def roll(self):
        return random.choice(self.values)
    

#---------Function that contains the main program.----------
def main():
    #Defines some global variables so I can destroy the widgets later.
    global mainWindow, btn1
    #Creates a main window for the user to access the main program.
    mainWindow = tkinter.Tk()
    mainWindow.geometry("900x600")
    mainWindow.title("Dice Game")
    #Configures all rows and columns to allow me to fill the rows.
    for x in range(3):
        mainWindow.rowconfigure(x, weight=1)
    for x in range(2):
        mainWindow.columnconfigure(x, weight=1)
    #Creates the text and buttons on the window.
    label1 = tkinter.Label(mainWindow, text="Welcome to the Dice Game!", fg="blue", font = helv36)
    label1.grid(row=0, columnspan=2)
    btn1 = tkinter.Button(mainWindow, command = lambda : verifyPlr(1), text="Enter", fg="white", bg="green", font = helv24Bold)
    btn1.grid(row=1, columnspan=2, sticky="NSEW")
    btn2 = tkinter.Button(mainWindow, command = mainWindow.destroy, text = "Exit", fg = "white", bg = "red", font = helv24Bold)
    btn2.grid(row=2, columnspan=2)
    #Begins the program's main loop.
    mainWindow.mainloop()

#----Function to allow both players to verify themselves.----
def verifyPlr(plrNum, flag=False):
    #Again, defining global variable in order to allow me to re-use them.
    global mainWindow, btn1, unEntry, lbl1, lbl2, pwdEntry, sbmtBtn, exitBtn
    #Removes all buttons and labels from the window.
    mainWindow.destroy()
    #This resizes the main window and adds another 2 rows for more widgets.
    mainWindow = tkinter.Tk()
    mainWindow.title("Dice Game")
    mainWindow.geometry("450x300")
    for x in range(5):
        mainWindow.rowconfigure(x, weight=1)
    for x in range(2):
        mainWindow.columnconfigure(x, weight=1)
    #This creates the labels and buttons for the window.
    btn1=tkinter.Label(mainWindow, text = f"Player {plrNum}, Please enter your login details: ", fg="blue", font=helv12Bold)
    lbl1 = tkinter.Label(mainWindow, text="Username", fg="black", font=helv12)
    lbl2 = tkinter.Label(mainWindow, text="Password", fg="black", font=helv12)
    unEntry = tkinter.Entry(mainWindow)
    pwdEntry = tkinter.Entry(mainWindow, show="*")
    sbmtBtn = tkinter.Button(mainWindow, text="Submit", bg="green", fg="white", font=helv12Bold, command= lambda: checkUsrInfo(unEntry.get(), pwdEntry.get()))
    exitBtn = tkinter.Button(mainWindow, text="Cancel", bg="red", fg="white", font=helv12Bold, command=mainWindow.destroy)
    #This allows the user to press "Enter" rather than clicking the button
    mainWindow.bind('<Return>', lambda event=None: sbmtBtn.invoke() )
    #This outputs all the widgets and adds them to the window.
    btn1.grid(row=0, columnspan=2)
    lbl1.grid(row=1, column=0)
    unEntry.grid(row=1, column=1, sticky="W")
    lbl2.grid(row=2, column=0)
    pwdEntry.grid(row=2, column=1, sticky="W")
    sbmtBtn.grid(row=3, column=0, sticky="NSEW")
    exitBtn.grid(row=3, column=1, sticky="NSEW")

#---This function is the logic behind the user verification.---
def checkUsrInfo(username, password):
    flag = False
    #This checks if the user's details are in the users.txt file.
    with open("users.txt") as file1:
        for line in file1:
            txtUsername, txtPassword = line.strip().split(",")
            if txtUsername == username and txtPassword == password:
                #This statement is used to ensure that only two players are verified
                if len(plrList)<1:
                    plrList.append(Player(username))
                    flag = True
                    verifyPlr(2, True)
                    #After finding the correct user's details, it exits the loop for efficiency and then
                    #sets flag to True to prevent the error message displaying.
                    #Then, it goes back to the screen that allows players to enter details, for player 2.
                    break
                else:
                    #This is slightly different code that is used when the second player is logging in.
                    plrList.append(Player(username))
                    flag = True
                    #Instead of going back to the verification window for player 2 again, it instead advances to the actual game.
                    roundGame(1, Die())
                    break
        if not flag:
            messagebox.showinfo(title = "Error!", message = "Invalid login details!")

#-----Function to be run to handle each round of the game-----
def roundGame(roundNum, die, plrNum=1, flag=False):
    global rollBtn, die1ValLbl, die2ValLbl, roundLbl, die1Lbl, die2Lbl, plrLbl, rollBtn
    #First I remove all the widgets from the old screen.
    btn1.destroy()
    lbl1.destroy()
    lbl2.destroy()
    sbmtBtn.destroy()
    exitBtn.destroy()
    unEntry.destroy()
    pwdEntry.destroy()
    #This is used to remove the old dice values from previous rounds when new rounds begin.
    if flag:
        die1ValLbl["text"] = ""
        die2ValLbl["text"] = ""
    if roundNum==6:
        endGame(die)
    else:
        #Then I define variables that hold all the new widgets for the round begin screen.
        roundLbl = tkinter.Label(mainWindow, text=f"Round: {roundNum}", font=helv24Bold)
        die1Lbl = tkinter.Label(mainWindow, text="Die 1: ", font=helv12)
        die2Lbl = tkinter.Label(mainWindow, text="Die 2: ", font=helv12)
        plrLbl = tkinter.Label(mainWindow, text=f"Player: {plrList[plrNum-1].username}", font=helv12)
        rollBtn = tkinter.Button(mainWindow, text="ROLL", fg="white", bg="green", font=helv12Bold, command=lambda: roundGameLogic(plrList[plrNum-1], die, roundNum, plrNum))
        #Then I display all the widgets in an organised grid.
        roundLbl.grid(row=0, columnspan=2)
        die1Lbl.grid(row=1, column=0)
        die2Lbl.grid(row=2, column=0)
        plrLbl.grid(row=3, columnspan=2)
        rollBtn.grid(row=4, columnspan=2, sticky="EW")

#--Function to handle the background actions during each round--
def roundGameLogic(plr, die, roundNum, plrNum):
    #First I remove the button from the previous screen so I can change its text and function
    global rollBtn, die1ValLbl, die2ValLbl
    rollBtn.destroy()
    #Then I generate the values for both die and check for any special conditions in the results such as the result is even or odd or the dice are doubles.
    die1Value, die2Value, condition = plr.rollADie(die)
    #Then I create a text widget that will show the values of both of the dice.
    die1ValLbl = tkinter.Label(mainWindow, text=die1Value, font=helv12)
    die2ValLbl = tkinter.Label(mainWindow, text=die2Value, font=helv12)
    #This is just used to ensure the program does not attempt to play with a third player or that it continues on "Round 1" forever.
    if plrNum==2:
        plrNum=0
        roundNum+=1
    #This means that the roll button is changed to "NEXT ROUND" after the player has rolled, apart from Player 2's turn on round 6
    #where the button shows "FINISH"
    if roundNum==6:
        rollBtn = tkinter.Button(mainWindow, text="FINISH", fg="white", bg="green", font=helv12Bold, command=lambda: roundGame(roundNum, die, plrNum+1, flag=True))
    else:
        rollBtn = tkinter.Button(mainWindow, text="NEXT ROUND", fg="white", bg="green", font=helv12Bold, command=lambda: roundGame(roundNum, die, plrNum+1, flag=True))
    #This then just prints all the widgets made earlier.
    die1ValLbl.grid(row=1, column=1)
    die2ValLbl.grid(row=2, column=1)
    rollBtn.grid(row=4, columnspan=2, sticky="EW")
    #This updates the window so that all the widgets are correctly shown.
    mainWindow.update()
    #This then creates a popup window that shows the player's current total as well as an explanation for any special 
    #conditions.
    if condition == "double":
        die3Val = die.roll()
        plr.score+=die3Val
        messagebox.showinfo(title="Round Total", message=f"The dice are doubles.\nA third die has been rolled.\nDie 3: {die3Val}\n{plr.username}'s Total: {plr.score}")
    elif condition=="even":
        messagebox.showinfo(title="Round Total", message=f"The dice total is even.\n10 extra points have been added.\n{plr.username}'s Total: {plr.score}")
    else:
        messagebox.showinfo(title="Round Total", message=f"The dice total is odd.\n3 points have been removed.\n{plr.username}'s Total: {plr.score}")
    
#---------Carries out the end of game score evaluations--------
def endGame(die):
    #This first defines some variables to be used later.
    global roundNum
    pl1 = plrList[0]
    pl2 = plrList[1]
    #This ensures that the game only runs the draw function whilst players have identical scores.
    if pl1.score==pl2.score:
        messagebox.showinfo(title="Both players have identical scores.", message="The game will now auto-roll one die each until one wins.")
        roundNum = 1
        drawMechanic(die, pl1, pl2, mainWindow)
    #If the player's scores are not equal, then the game will continue to the score evaluation screen.
    else:
        gameOver(pl1, pl2)
    
#-----Logic for when both players have identical scores.-----
def drawMechanic(die, pl1, pl2, mainWindow):
    global roundNum
    #Generates a new window each time it rolls for the players until the scores are different.
    mainWindow.destroy()
    mainWindow = tkinter.Tk()
    mainWindow.title("Dice Game")
    mainWindow.geometry("450x300")
    for x in range(5):
        mainWindow.rowconfigure(x, weight=1)
    for x in range(2):
        mainWindow.columnconfigure(x, weight=1)
    #Adds a random die value to each of their scores.
    for plr in plrList:
        dieValue = die.roll()
        plr.score+=dieValue
    #Outputs the number of rolls made as well as the current score for both players.
    roundCounter = tkinter.Label(mainWindow, text=f"Roll Number: {roundNum}", fg="blue", font=helv12Bold)
    plr1Lbl = tkinter.Label(mainWindow, text=f"{pl1.username}'s Score: {pl1.score}")
    plr2Lbl = tkinter.Label(mainWindow, text=f"{pl2.username}'s Score: {pl2.score}")
    roundCounter.grid(row=0, columnspan=2)
    plr1Lbl.grid(row=1, columnspan=2)
    plr2Lbl.grid(row=2, columnspan=2)
    #This checks if the players' scores are still identical and if so, runs the function again.
    if pl1.score==pl2.score:
        roundNum+=1
        mainWindow.after(2000, lambda: drawMechanic(die, pl1, pl2, mainWindow))
    #Otherwise, it just adds a button so the players can advance onto the Game End screen.
    else:
        advanceBtn = tkinter.Button(mainWindow, text="NEXT", fg="white", bg="green", font=helv12Bold, command=lambda: endGame(die))
        advanceBtn.grid(row=3, columnspan=2)

#-----Function to save player data and show winners.-----     
def gameOver(pl1, pl2):
    global endGameWindow, titleLabel, totalLabel, pl1TotalLabel, pl2TotalLabel, winnerLabel, loserLabel, leaderBtn, exitBtn
    #This first removes the old windows and creates a new one to show the player scores.
    mainWindow.destroy()
    endGameWindow = tkinter.Tk()
    endGameWindow.title("Dice Game")
    endGameWindow.geometry("400x300")
    for num in range(7):
        endGameWindow.rowconfigure(num, weight=1)
    for num in range(2):
        endGameWindow.columnconfigure(num, weight=1)
    
    #This then creates variables to store the winner and loser of the game.
    if pl1.score > pl2.score:
        winner = pl1
        loser = pl2
    else:
        winner = pl2
        loser = pl1
    
    with open("winners.txt", "a") as winnerFile:
        winnerFile.write(f"{winner.username}, {winner.score}\n")

    #This then creates widgets that show all information such as winner and loser as well as each person's score.
    #It also creates two buttons to allow players to either exit the game or view the leaderboard.
    titleLabel = tkinter.Label(endGameWindow, text="Game Over!", fg="blue", font=helv24Bold)
    totalLabel = tkinter.Label(endGameWindow, text="Totals: ", fg="blue", font=helv24Bold)
    pl1TotalLabel = tkinter.Label(endGameWindow, text=f"{pl1.username} : {pl1.score}", font=helv12)
    pl2TotalLabel = tkinter.Label(endGameWindow, text=f"{pl2.username} : {pl2.score}", font=helv12)
    winnerLabel = tkinter.Label(endGameWindow, text=f"Congratulations, {winner.username}", font=helv12)
    loserLabel = tkinter.Label(endGameWindow, text=f"Unlucky, {loser.username}", font=helv12)
    leaderBtn = tkinter.Button(endGameWindow, text="View Leaderboard", fg="white", bg="green", font=helv12Bold, command=leader)
    exitBtn = tkinter.Button(endGameWindow, text="Exit", fg="white", bg="red", font=helv12Bold, command=endGameWindow.destroy)

    #This then just displayes the widgets in a grid.
    titleLabel.grid(row=0, columnspan=2)
    totalLabel.grid(row=1, columnspan=2)
    pl1TotalLabel.grid(row=2, columnspan=2)
    pl2TotalLabel.grid(row=3, columnspan=2)
    winnerLabel.grid(row=4, columnspan=2)
    loserLabel.grid(row=5, columnspan=2)
    leaderBtn.grid(row=6, column=0, sticky="NSEW")
    exitBtn.grid(row=6, column=1, sticky="NSEW")
    endGameWindow.mainloop()

#-----Function to display the leaderboard of top 5 player scores.
def leader():
    #Here I just defined some global variables to ues later in the function.
    global endGameWindow, titleLabel, totalLabel, pl1TotalLabel, pl2TotalLabel, winnerLabel, loserLabel, leaderBtn, exitBtn
    playerScores = []
    plrCount     = 2

    #First I prepared the window to display the leaderboard by removing previous widgets.
    #Then I prepare an eighth row, as well as set the window title to "Leaderboard"
    titleLabel.destroy()
    totalLabel.destroy()
    pl1TotalLabel.destroy()
    pl2TotalLabel.destroy()
    winnerLabel.destroy()
    loserLabel.destroy()
    leaderBtn.destroy()
    exitBtn.destroy()
    endGameWindow.rowconfigure(8, weight=1)
    endGameWindow.title("Leaderboard")

    #Here I load in the top 5 scores into a 2D list.
    with open("winners.txt", "r") as winnersFile:
        for line in winnersFile:
            username, score = line.strip().split(",")
            playerScores.append([username, score])
    playerScores = sorted(playerScores, key = lambda x: x[1], reverse=True)[0:5]

    #Here I generate the title for the screen as well as the headers for the table and the exit button.
    titleLabel   = tkinter.Label(endGameWindow, text="Top 5 Scores: ", fg="blue", font=helv24Bold)
    headerLabel1 = tkinter.Label(endGameWindow, text="Player: ", font=helv12)
    headerLabel2 = tkinter.Label(endGameWindow, text="Score: ", font=helv12)
    exitBtn = tkinter.Button(endGameWindow, text="Exit", fg="white", bg="red", font=helv12Bold, command=endGameWindow.destroy)

    #Then I present the title and headers on the screen.
    titleLabel.grid(row=0, columnspan=2)
    headerLabel1.grid(row=1, column=0)
    headerLabel2.grid(row=1, column=1)

    #Then I show each of the players' scores on screen.
    for player in playerScores:
        tkinter.Label(endGameWindow, text=player[0], font=helv12).grid(row=plrCount, column=0)
        tkinter.Label(endGameWindow, text=player[1], font=helv12).grid(row=plrCount, column=1)
        plrCount+=1
    
    #Finally I show the exit button on screen.
    exitBtn.grid(row=8, columnspan=2, sticky="NSEW")
    
    
if __name__ == "__main__":
    main()

        