
from client_fva.fva_speaker import FVA_client
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from base64 import b64decode
from client_fva.user_settings import UserSettings
from client_fva.ui.fvadialogui import Ui_FVADialog


class FVASpeakerClient(Ui_FVADialog):
    rejected = False
    operation_finished = False

    def __init__(self, dialog, slot):
        Ui_FVADialog.__init__(self)
        self.dialog = dialog
        self.setupUi(dialog)
        self.cancel.clicked.connect(self.closeEvent)
        self.submit.clicked.connect(self.send_code)
        self.timeout = 0
        self.settings = UserSettings()
        self.client = FVA_client(settings=self.settings, slot=slot)
        self.client.daemon = True
        self.client.start()
        self.client.signal.connect(self.request_pin_code)

    def closeEvent(self, event):
        print("Closing")
        self.rejected = True
        self.operation_finished = True
        self.dialog.hide()

    def send_code(self, event):
        print("Signing")
        self.rejected = False
        self.operation_finished = True
        self.dialog.hide()

    def request_pin_code(self, sender, **kw):
        obj = kw['obj']

        self.pin.setText('')
        self.code.setText('')

        self.requesting.setText(obj.data['M'][0]['A'][0]['d'])
        self.information.setText(obj.data['M'][0]['A'][0]['c'])
        self.operation_finished = False
        img = QtGui.QImage.fromData(b64decode(obj.data['M'][0]['A'][0]['e']))
        pixmap = QtGui.QPixmap.fromImage(img)
        self.image.setPixmap(pixmap)
        self.dialog.show()
        self.timeout = int(obj.data['M'][0]['A'][0]['f'])
        while not self.operation_finished:
            time.sleep(1)
            self.on_timer()
        obj.response['pin'] = self.pin.text()
        obj.response['code'] = self.code.text()
        obj.response['rejected'] = self.rejected
        return obj

    def on_timer(self):
        self.timeout -= 1
        self.displaytimeout.display("%d:%02d" % (
            self.timeout / 60, self.timeout % 60))
        if self.timeout == 0:
            self.rejected = True
            self.operation_finished = True
            self.dialog.hide()


def run():
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FVADialog = QtWidgets.QDialog()
    ui = FVASpeakerClient(FVADialog)
    # ui.setupUi(FVADialog)
    # FVADialog.show()
    sys.exit(app.exec_())
