from PyQt6.QtWidgets import *
from gui import *
import sys, csv, os.path, random
class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        '''
        sets up the gui interface
        '''
        super().__init__()
        self.setupUi(self)

        self.ButtonSubmit.clicked.connect(lambda: self.submit())
        self.calendarWidget.hide()
        self.labelDOB.setHidden(True)
        self.calendarWidget.setGridVisible(True)
        self.labelName.setHidden(True)
        self.lineName.setHidden(True)
        self.labelDiscritption.setHidden(True)
        self.ButtonSaveData.setHidden(True)
        self.ButtonVote.setHidden(True)
        self.ButtonExit.setHidden(True)

        self.labelID.setHidden(True)
    def submit(self)-> None:
        '''
        checks which radio button is checked and takes the user to the correct interface and function
        '''
        if self.ButtonCheckin.isChecked() or self.ButtonRestart.isChecked():
            #checks if the user clicked to check in then takes them to the check in function
            self.checkin()
        elif self.ButtonSaveData.isChecked():
            #checks if the user imputed a name and DOB using exception handling, then takes them to the vote function
            try:
                self.Name = self.lineName.text()
                self.DOB = self.calendarWidget.selectedDate()
                if self.Name == '' or self.DOB == '':
                    raise Exception()
                self.vote()
            except:
                self.labelDiscritption.setText(f'Please enter a name and date of birth')
        elif self.ButtonVote.isChecked():
            #checks to see if the users imput their info and then takes them to the save function
            try:
                self.Canidate = self.lineName.text()
                if self.Canidate == '':
                    raise Exception()
                self.save()
            except:
                self.labelDiscritption.setText(f'Please enter a Canidate')

        elif self.ButtonExit.isChecked():
            #allows the user to exit the voting screen
            sys.exit(0)

    def checkin(self)-> None:
        '''
        allows users to imput their name and DOB
        '''
        self.ID = self.generateID()
        self.labelDOB.setHidden(False)
        self.calendarWidget.show()
        self.labelName.setHidden(False)
        self.labelName.setText('Name (First, Last)')
        self.lineName.setHidden(False)
        self.lineName.setText('')
        self.labelDiscritption.setHidden(False)
        self.labelDiscritption.setText('Please either enter your information to vote')
        self.ButtonCheckin.setHidden(True)
        self.ButtonVote.setHidden(True)
        self.ButtonSaveData.setHidden(False)
        self.labelID.setHidden(False)
        self.labelID.setText(f'Your ID: {self.ID}')
        if self.ButtonRestart.isChecked():
            self.ButtonSaveData.setChecked(True)
    def save(self)-> None:
        '''
        saves the users name and DOB into a csv and
        '''
        with open('voter_info.csv', 'a', newline='') as csvfile:
            file_is_empty = os.stat('voter_info.csv').st_size == 0
            fieldnames = ['Voter ID', 'Name', 'DOB', 'Canidate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if file_is_empty:
                writer.writeheader()
            content = csv.writer(csvfile)
            data = [self.ID, self.Name, self.DOB, self.Canidate]
            content.writerow(data)
        with open('voter_info.csv', 'r') as inputFile:
            try:
                for line in inputFile:
                    line = line.rstrip().split(',')
                    if line[2] == self.ID:
                        raise Exception

                self.labelDiscritption.setText(f'Thank you {self.Name}, your vote has been counted. Please exit the screen now.')
                self.ButtonVote.setHidden(True)
                self.labelName.setHidden(True)
                self.lineName.setHidden(True)
                self.ButtonRestart.setHidden(True)
                self.ButtonExit.setHidden(False)
                self.labelDOB.setHidden(True)


                self.calendarWidget.hide()
            except:
                self.ID = self.generateID()



    def vote(self)-> None:
        '''
        Sets up the screen for the user to imput their candidate choice
        '''
        self.labelDiscritption.setText(f'Hello {self.Name}, please enter your canidate')
        self.labelName.setText('Candiate Name')
        self.lineName.setText('')
        self.ButtonSaveData.setHidden(True)

        self.labelDOB.setHidden(True)
        self.ButtonVote.setHidden(False)
        self.calendarWidget.hide()

        self.labelID.setHidden(True)
        if self.ButtonSaveData.isChecked():
            self.ButtonVote.setChecked(True)

    def generateID(self)-> str:
        '''
        Generates a random 3 char long str as a unique id
        '''
        characters = "abcdefghijklmnopqrstuvwxyz123456789"
        chosenLetter = random.sample(characters, 3)
        password = "".join(chosenLetter)
        return password

