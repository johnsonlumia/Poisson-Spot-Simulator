#
# PHYS 129 final project
# Poisson's Spot
# GUI
#
# June 6, 2018 modified by Renjie Zhu
# June 5, 2018 modified by Renjie Zhu
# May 23, 2018 created by Renjie Zhu
#

import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QErrorMessage,
    QMenuBar,
    QMessageBox,
)
from PyQt5.QtCore import (
    pyqtSlot,
)
from disk import Poisson


class Gui(QWidget):

    def __init__(self, left=300, top=300, width=450, height=140, title='New Window'):
        super().__init__()
        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.l_label = QLabel('Distance between disk and screen', self)
        self.d_label = QLabel('Diameter of disk', self)
        self.w_label = QLabel('Wavelength of incident light', self)

        self.l_unit = QLabel('mm', self)
        self.d_unit = QLabel('mm', self)
        self.w_unit = QLabel('nm', self)

        self.l_edit = QLineEdit('1000', self)
        self.d_edit = QLineEdit('2', self)
        self.w_edit = QLineEdit('600', self)

        self.l_value = 0
        self.d_value = 0
        self.w_value = 0

        self.reset_button = QPushButton('Reset', self)
        self.compute_button = QPushButton('Compute', self)

        self.error_dialog = QErrorMessage()
        self.ERROR_MESSAGE = "Make sure you give positive numbers.\nPlease try again."
        self.l_MESSAGE = """Please make sure that the distance between the screen 
and the disk is a hundred times larger than the diameter of the disk."""

        self.help_box = QMessageBox()
        self.FRESNEL_MESSAGE = """
For Fresnel diffraction (the diffraction that causes 
Poisson's Point to show), the parameters must satisfy. 
the following requirement.
\t\td^2              
\t\t-----  >~ 1,      
\t\tl * λ             
where
\td is the diameter of disk,
\tl is the distance between disk and screen, and
\tλ is the wavelength of incident light.
        
Please make sure your input meet this requirement!
"""

        self.INFO_TITLE = 'Information about Poisson\'s Spot:'
        self.POISSON_MESSAGE = """
This program is used to simulate the Poisson Spot with
parameters given by the user. Parameters include
1. distance between the disk and screen,
2. diameter of the disk,
3. wavelength of incident light.
The plot will be shown as a 400 by 400 grid image of the
Poisson Spot on a screen of 16mm by 16mm.

Please make sure that you give integers as input and 
follow the suggestions if you encounter any.
"""

        self.warning_box = QMessageBox()
        self.WARNING_MESSAGE = """
Due to both hardware and software limitations, the 
computation may take a rather long time to run. 
Please be patient if the program is not responding,
and expect it to run for about 10 minutes until you 
see the result.

The result will be saved to the program directory
as an eps file with parameters listed in the filename.
"""

        self.plot_info = """
Parameters: 
Distance between disk and screen: %d m
Diameter of disk: %d mm
Wavelength of incident light: %d nm
"""

    def main_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.reset_button.setToolTip('Reset the entries.')
        self.compute_button.setToolTip(
            'Compute the Poisson\'s Spot using parameters above.')
        self.compute_button.setDefault(True)

        self.l_label.move(10, 7)
        self.l_edit.move(260, 5)
        self.l_unit.move(420, 7)
        self.d_label.move(10, 42)
        self.d_edit.move(260, 40)
        self.d_unit.move(420, 42)
        self.w_label.move(10, 77)
        self.w_edit.move(260, 75)
        self.w_unit.move(420, 77)
        self.reset_button.move(200, 110)
        self.compute_button.move(310, 110)

        self.reset_button.clicked.connect(self.reset_on_click)
        self.compute_button.clicked.connect(self.compute_on_click)
        self.show()

    def fresnel_help_page(self):
        self.help_box.setWindowTitle(self.INFO_TITLE)
        self.help_box.setIcon(QMessageBox.Information)
        self.help_box.setText(self.FRESNEL_MESSAGE)
        self.help_box.show()

    def info_page(self):
        self.info_box.setWindowTitle(self.INFO_TITLE)
        self.info_box.setIcon(QMessageBox.Information)
        self.info_box.setText(self.POISSON_MESSAGE)
        self.info_box.show()

    def warning_page(self):
        self.warning_box.setWindowTitle('Warning!')
        self.warning_box.setIcon(QMessageBox.Warning)
        self.warning_box.setText(self.WARNING_MESSAGE)
        self.warning_box.setStandardButtons(self.warning_box.Cancel | self.warning_box.Ok)
        if self.warning_box.exec_() == self.warning_box.Ok:
            self.proceed_on_click()

    def start(self):
        self.main_window()

    @pyqtSlot(name='compute_on_click')
    def compute_on_click(self):
        try:
            l_value_temp = float(self.l_edit.text())
            if l_value_temp < 0:
                self.value_error_handling()
                self.l_edit.setText('1000')
                return
        except ValueError:
            self.value_error_handling()
            self.l_edit.setText('1000')
            return

        try:
            d_value_temp = float(self.d_edit.text())
            if d_value_temp < 0:
                self.value_error_handling()
                self.d_edit.setText('2')
                return
        except ValueError:
            self.value_error_handling()
            self.d_edit.setText('2')
            return

        try:
            w_value_temp = float(self.w_edit.text())
            if w_value_temp < 0:
                self.value_error_handling()
                self.w_edit.setText('600')
                return
        except ValueError:
            self.value_error_handling()
            self.w_edit.setText('600')
            return

        # Convert to SI Units
        # l_value_temp: input (mm) -> m
        l_value_temp = l_value_temp * 1e-3
        # d_value_temp: input (mm) -> m
        d_value_temp = d_value_temp * 1e-3
        # w_value_temp: input (nm) -> m
        w_value_temp = w_value_temp * 1e-9

        if d_value_temp > 0.01 * l_value_temp:
            self.value_error_handling(is_l_small=True)
            self.reset_input()
            return

        # Fresnel number requirement
        # d^2/(l*w) >~ 1
        # Ask for new inputs if this is requirement is not met
        # and inform them about this problem
        fresnel_num = (d_value_temp ** 2) / (l_value_temp * w_value_temp)
        if fresnel_num < 0.95:
            self.value_error_handling(is_fresnel=True)
            self.reset_input()
            return

        self.l_value = l_value_temp
        self.d_value = d_value_temp
        self.w_value = w_value_temp

        self.warning_page()

    @pyqtSlot(name='reset_on_click')
    def reset_on_click(self):
        self.reset_input()

    @pyqtSlot(name='proceed_on_click')
    def proceed_on_click(self):
        instance = Poisson(lamda=self.w_value, rad=(self.d_value / 2), L=self.l_value)
        matrix = instance.poiss()
        self.matrix_plotting(matrix)

    def reset_input(self):
        self.l_edit.setText('1000')
        self.d_edit.setText('2')
        self.w_edit.setText('600')

    def value_error_handling(self, is_fresnel=False, is_l_small=False):
        if is_fresnel:
            self.fresnel_help_page()
        elif is_l_small:
            self.error_dialog.setWindowTitle('ERROR!!!')
            self.error_dialog.showMessage(self.l_MESSAGE)
        else:
            # This part will be trigger if error is not specified.
            # Which means value errors in this case.
            self.error_dialog.setWindowTitle('ERROR!!!')
            self.error_dialog.showMessage(self.ERROR_MESSAGE)

    def matrix_plotting(self, matrix):
        f1, ax1 = plt.subplots()
        ax1.imshow(matrix, interpolation='none', cmap='gray')
        ax1.axis('off')
        ax1.set_title('The Simulation of Poisson Spot on the Screen of Side Length 16 mm')
        f1.text(0.5, 0, self.plot_info % (self.l_value, self.d_value * 1e3, self.w_value * 1e9),
                verticalalignment='baseline')
        f1.show()
        filename = 'poisson_spot_%d_%d_%d.eps' % (self.l_value, self.d_value * 1e3, self.w_value * 1e9)
        f1.savefig(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
