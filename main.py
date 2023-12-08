from logic import *

def main():
    '''
    code that initializes the GUI
    '''
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()
if __name__ == '__main__':
    main()
