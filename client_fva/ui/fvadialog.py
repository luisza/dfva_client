import time
from base64 import b64decode

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QTableWidgetItem

from client_fva import signals
from client_fva.fva_speaker import FVA_client
from client_fva.ui.fvadialogui import Ui_FVADialog
from client_fva.user_settings import UserSettings
import logging
logger = logging.getLogger('dfva_client')


class Timer(QRunnable):
    def __init__(self, fvaspeaker):
        self.fva_speaker = fvaspeaker
        QRunnable.__init__(self)

    @pyqtSlot()
    def run(self):
        while not self.fva_speaker.operation_finished:
            time.sleep(1)
            self.fva_speaker.on_timer()


class FVASpeakerClient(Ui_FVADialog):
    rejected = False
    operation_finished = False

    CONNECTING = 0
    CONNECTED = 1
    ERROR = 2

    def __init__(self, dialog, slot, identification):
        Ui_FVADialog.__init__(self)
        self.status_widget = QTableWidgetItem()
        self.status_widget.setIcon(QtGui.QIcon(":/images/sign.png"))

        self.dialog = dialog
        self.setupUi(dialog)
        self.cancel.clicked.connect(self.closeEvent)
        self.submit.clicked.connect(self.send_code)
        self.timeout = 0
        self.settings = UserSettings.getInstance()
        self.client = FVA_client(settings=self.settings,
                                 slot=slot,
                                 identification=identification,
                                 daemon=self.settings.start_fva_bccr_client,
                                 notifier=self
                                 )


        self.client.start()
        signals.connect('fva_speaker', self.request_pin_code)
        self.threadpool = QThreadPool()
        self.timer = None
        self.obj = None

    def closeEvent(self, event):
        logger.info("Reject fva speaker dialog")
        self.rejected = True
        self.operation_finished = True
        self.dialog.hide()
        if event is not None:
            self.notify()

    def close(self):
        self.closeEvent(None)
        self.client.close()
        self.client.kill()

    def send_code(self, event):
        logger.info("Signing fva speaker dialog")
        self.rejected = False
        self.operation_finished = True
        self.dialog.hide()
        self.notify()

    def notify(self):
        self.obj.response['pin'] = self.pin.text()
        self.obj.response['code'] = self.code.text()
        self.obj.response['rejected'] = self.rejected
        signals.receive(self.obj, notify=True)

    def request_pin_code(self, sender, obj):
        logger.info("Request fva speaker dialog %r" %
                    obj.data['M'][0]['A'][0]['c'])
        #obj = kw['obj']
        self.obj = obj
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
        self.timer = Timer(self)
        self.threadpool.start(self.timer)

    def on_timer(self):
        self.timeout -= 1
        self.displaytimeout.display("%d:%02d" % (
            self.timeout / 60, self.timeout % 60))
        if self.timeout == 0:
            self.rejected = True
            self.operation_finished = True
            self.dialog.hide()
            self.notify()

    def change_fva_status(self, status):
        if status == self.CONNECTING:
            self.status_widget.setIcon(QtGui.QIcon(":/images/connecting.png"))
            self.status_widget.setToolTip('Conectando al servicio de firmado')
        elif status == self.CONNECTED:
            self.status_widget.setIcon(QtGui.QIcon(":/images/connected.png"))
            self.status_widget.setToolTip('Conectado al servicio de firmado')
        elif status == self.ERROR:
            self.status_widget.setIcon(QtGui.QIcon(":/images/error.png"))
            self.status_widget.setToolTip("Error al conectar con el servicio de firmado")

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
