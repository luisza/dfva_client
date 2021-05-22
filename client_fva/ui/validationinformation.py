from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

from .validationinformationui import Ui_Dialog


class ValidationInformation(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, widget, main_app):
        super().__init__(widget)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.signer_count = 0
        self.signers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.signers.setRowCount(0)
        # set column count
        self.signers.setColumnCount(6)
        self.signers.setHorizontalHeaderItem(0, QTableWidgetItem("Identificación"))
        self.signers.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.signers.setHorizontalHeaderItem(2, QTableWidgetItem("Fecha de Firma"))
        self.signers.setHorizontalHeaderItem(3, QTableWidgetItem("Autoría"))
        self.signers.setHorizontalHeaderItem(4, QTableWidgetItem("Válida"))
        self.signers.setHorizontalHeaderItem(5, QTableWidgetItem("Avanzada"))

        self.error_table_count = 0
        self.errortable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.errortable.setRowCount(0)
        self.errortable.setColumnCount(3)
        self.errortable.setHorizontalHeaderItem(0, QTableWidgetItem("Identificación"))
        self.errortable.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.errortable.setHorizontalHeaderItem(2, QTableWidgetItem("Descripción"))

    def add_error_to_table(self, identification,name, description):
        self.errortable.insertRow(self.errortable.rowCount())
        self.errortable.setItem(self.signer_count, 0, QTableWidgetItem(identification))
        self.errortable.setItem(self.signer_count, 1, QTableWidgetItem(name))
        self.errortable.setItem(self.signer_count, 2, QTableWidgetItem(description))
        self.error_table_count += 1
        self.errortable.resizeColumnsToContents()

    def add_signer(self, data):
        # {'es_valida': True, 'es_avanzada': True, 'error': False, 'detalle_de_error': '',
        # 'garantia_de_integridad_y_autenticidad': True,
        # 'garantia_de_validez_tiempo': [0, 'Tiene Garantía'],
        # 'detalle': {'integridad': {'estado': False, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        # 'jerarquia_de_confianza': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        # 'vigencia': {'estado': False, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        # 'tipo_de_certificado': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        # 'revocacion': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        # 'fecha_de_firma': {'estado': False, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1, 'fecha_de_estama': '2021-05-20T00:00:00Z'}},
        # 'autoria_del_firmante': {'nombre': 'Joan Lucas Arce', 'identificacion': '0408880888', 'tiene_autoria': True}}

        if 'autoria_del_firmante' not in data:
            return
        if 'detalle' not in data and 'fecha_de_firma' not in data['detalle'] and 'fecha_de_estama' not in data['detalle']['fecha_de_firma']:
            return

        autoria_icon = ':/images/error.png'
        valida_icon = ':/images/error.png'
        avanzada_icon = ':/images/error.png'

        identification = data['autoria_del_firmante']['identificacion']
        name = data['autoria_del_firmante']['nombre']
        date = data['detalle']['fecha_de_firma']['fecha_de_estama']

        if data['autoria_del_firmante']['tiene_autoria']:
            autoria_icon = ':/images/connected.png'
        if 'es_valida' in data and data['es_valida']:
            valida_icon = ':/images/connected.png'
        if 'es_avanzada' in data and data['es_avanzada']:
            avanzada_icon = ':/images/connected.png'

        autoria = QTableWidgetItem()
        autoria.setIcon(QtGui.QIcon(autoria_icon))
        valida = QTableWidgetItem()
        valida.setIcon(QtGui.QIcon(valida_icon))
        avanzada = QTableWidgetItem()
        avanzada.setIcon(QtGui.QIcon(avanzada_icon))

        self.signers.insertRow(self.signers.rowCount())
        self.signers.setItem(self.signer_count, 0, QTableWidgetItem(identification))
        self.signers.setItem(self.signer_count, 1, QTableWidgetItem(name))
        self.signers.setItem(self.signer_count, 2, QTableWidgetItem(date))

        self.signers.setItem(self.signer_count, 3, autoria)
        self.signers.setItem(self.signer_count, 4, valida)
        self.signers.setItem(self.signer_count, 5, avanzada)
        self.signer_count += 1
        self.signers.resizeColumnsToContents()

        if 'error' in data and data['error']:
            self.add_error_to_table(identification, name, data['detalle_de_error'])


    def add_errors(self, data):
        if data:
            self.errorlabel.setText(data)
        else:
            self.errorlabel.setText("")

    def add_resumen(self, data):
        # {'garantia_de_integridad_y_autenticidad': True, 'garantia_validez_en_el_tiempo': True, 'resultado_de_validacion': 0}
        if 'garantia_de_integridad_y_autenticidad' in data:
            self.set_status_resumen_icon(self.gintegridad, data['garantia_de_integridad_y_autenticidad'])
        else:
            self.set_status_resumen_icon(self.gintegridad, False)

        if 'garantia_validez_en_el_tiempo' in data:
            self.set_status_resumen_icon(self.vtiempo, data['garantia_validez_en_el_tiempo'])
        else:
            self.set_status_resumen_icon(self.vtiempo, False)

        #if 'resumen' in data:
        #    for signer_resumen in data['resumen']:
                # {'firmante': 'Luis Madrigal Viquez', 'identificacion': '0208880888', 'garantia_de_integridad_y_autenticidad': True, 'garantia_validez_en_el_tiempo': True, 'resultado': 0, 'fecha_estampa_de_tiempo': '2021-05-20T23:30:16Z', 'tipo_identificacion': 0, 'tiene_fecha_estampa_de_tiempo': True}


    def set_status_resumen_icon(self, icon, status):
        if status:
            icon.setStyleSheet("image: url(:/images/connected.png);")
        else:
            icon.setStyleSheet("image: url(:/images/error.png);")

    def set_status_icon(self, code):

        if code == 0:
            self.statusicon.setStyleSheet("image: url(:/images/connected.png);")
        else:
            self.statusicon.setStyleSheet("image: url(:/images/error.png);")