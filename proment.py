
from proment.gui.main_gui import UI_MainWindow


def main():
    app =  UI_MainWindow('Hausverwaltung', 'net.heumann.hausverwaltung')
    app.main_loop()

if __name__ == '__main__':
    main()