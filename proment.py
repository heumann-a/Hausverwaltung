
import logging

from proment.gui.main_gui import UI_MainWindow
from proment.logger import UniversalLogger


def main():
    UniversalLogger('Hausverwaltung', logging.DEBUG)
    app =  UI_MainWindow('Hausverwaltung', 'net.heumann.hausverwaltung')
    app.main_loop()

if __name__ == '__main__':
    main()