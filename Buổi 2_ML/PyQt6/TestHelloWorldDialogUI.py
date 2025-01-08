from PyQt6.QtWidgets import QApplication, QDialog
from HelloWorldDialog import Ui_Dialog

app=QApplication([])
dialog=QDialog()
window = Ui_Dialog()
window.setupUi(dialog)
dialog.show()
app.exec()