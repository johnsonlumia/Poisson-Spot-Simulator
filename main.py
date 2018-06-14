#
#  PHYS 129 final project
#  Poisson's Spot
#  main program
#
#  May 23, 2018 created by Renjie Zhu
#

import sys
from gui import Gui
from info import Info
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

main_window = Gui(title='Poisson\'s Spot')
main_window.start()
info = Info(title=main_window.INFO_TITLE)
info.info_window(main_window.POISSON_MESSAGE)

sys.exit(app.exec_())
