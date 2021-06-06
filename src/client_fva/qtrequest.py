import humanize
from PyQt5.QtCore import QUrl, QMutex, QEventLoop, QJsonDocument, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QApplication, QLabel
import json
import io


class Respponse:
    def __init__(self, loop):
        self.loop = loop
        self.filedata = io.BytesIO()

    def json(self):
        if self.loop.exec_() == 0:
            self.filedata.seek(0)
            dev = json.load(self.filedata)
            return dev
        return {'status': 1, 'status_text': 'Error de comunicación'}

    def setData(self, data):
        self.filedata.write(data)

    def set_ready(self):
        self.loop.quit()


class RequestWidget(QObject):

    def __init__(self, controller):
        super(RequestWidget, self).__init__()
        self.httpRequestAborted = False
        self.downloadfile = None
        self.processBar = controller.statusBarManager

    def httpFinished(self):
        if self.httpRequestAborted or self._reply.error():
            pass # show message
        self.response.set_ready()
        self._reply.deleteLater()
        del self._reply
        self.processBar.text.emit("Operación finalizada")
        #self.processBar.hide.emit()

    def httpReadyRead(self):
        self.response.setData(self._reply.readAll())

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if totalBytes != -1:
            self.processBar.text.emit('Procesando %s of %s' % (humanize.naturalsize(bytesRead), humanize.naturalsize(totalBytes)))
        else:
            self.processBar.text.emit('Procesando %s' % humanize.naturalsize(bytesRead))

    def get(self, url, **kwargs):
        self.processBar.show.emit()
        self.processBar.value.emit(0)
        self.qnam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        extradata = None
        if 'json' in kwargs:
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            jdoc = QJsonDocument(kwargs['json'])
            extradata = jdoc.toJson()

        if 'headers' in kwargs:
            for key, value in kwargs['headers'].items():
                request.setRawHeader(key.encode(), value.encode())
        self.loop = QEventLoop()
        self._reply = self.qnam.sendCustomRequest(request, 'GET'.encode(), extradata)
        self.response = Respponse(self.loop)
        self._reply.finished.connect(self.httpFinished)
        self._reply.readyRead.connect(self.httpReadyRead)
        self._reply.downloadProgress.connect(self.updateDataReadProgress)

        return self.response

    def post(self, url, **kwargs):
        self.processBar.show.emit()
        self.processBar.value.emit(0)
        self.qnam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        extradata = None
        if 'json' in kwargs:
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            jdoc = QJsonDocument(kwargs['json'])
            extradata = jdoc.toJson()
        if 'headers' in kwargs:
            for key, value in kwargs['headers'].items():
                request.setRawHeader(key.encode(), value.encode())

        self._reply = self.qnam.sendCustomRequest(request, 'POST'.encode(), extradata)
        self.loop = QEventLoop()
        self.response = Respponse(self.loop)
        self._reply.finished.connect(self.httpFinished)
        self._reply.readyRead.connect(self.httpReadyRead)
        self._reply.uploadProgress.connect(self.updateDataReadProgress)
        return self.response

    def delete(self, url, **kwargs):
        self.processBar.show.emit()
        self.processBar.value.emit(0)
        self.qnam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        if 'headers' in kwargs:
            for key, value in kwargs['headers'].items():
                request.setRawHeader(key.encode(), value.encode());
        self._reply = self.qnam.deleteResource(request)
        self.response = Respponse(self._reply)
        self._reply.finished.connect(self.httpFinished)
        self._reply.readyRead.connect(self.httpReadyRead)
        self._reply.downloadProgress.connect(self.updateDataReadProgress)
        return self.response

    def hide(self):
        self.processBar.hide.emit()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = RequestWidget()
    URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
    w.get(URL)
    sys.exit(app.exec_())