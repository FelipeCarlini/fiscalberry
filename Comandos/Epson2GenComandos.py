# -*- coding: iso-8859-1 -*-
import string
import types
import logging
import ctypes
import unicodedata
from ctypes import (
    byref,
    c_int,
    c_char,
    c_char_p,
    c_long,
    c_short,
    c_float,
    create_string_buffer,
)
from Comandos.ComandoFiscalInterface import ComandoFiscalInterface
from Drivers.FiscalPrinterDriver import PrinterException
from ComandoInterface import formatText


class Epson2GenComandos(ComandoFiscalInterface):
    # el traductor puede ser: TraductorFiscal o TraductorReceipt
    # path al modulo de traductor que este comando necesita
    traductorModule = "Traductores.TraductorFiscal"
    DEFAULT_DRIVER = "Epson2Gen"
    AVAILABLE_MODELS = ["TM-T900"]

    docTypes = {
        "CUIT": 3,
        "CUIL": 2,
        "LIBRETA_ENROLAMIENTO": 7,
        "LIBRETA_CIVICA": 6,
        "DNI": 1,
        "PASAPORTE": 5,
        "CEDULA": 4,
        "SIN_CALIFICADOR": 0,
    }

    ivaTypes = {
        "RESPONSABLE_INSCRIPTO": 1,
        "EXENTO": 6,
        "NO_RESPONSABLE": 3,
        "CONSUMIDOR_FINAL": 5,
        "NO_CATEGORIZADO": 7,
        "RESPONSABLE_MONOTRIBUTO": 4,
        "MONOTRIBUTISTA_SOCIAL": 8,
    }

    comprobanteTypes = {
        "T": 1,
        "FB": 2,
        "FA": 2,
        "FC": 2,
        "FM": 2,
        "NCT": 3,
        "NCA": 3,
        "NCB": 3,
        "NCC": 3,
        "NCM": 3,
        "NDA": 4,
        "NDB": 4,
        "NDC": 4,
        "NDM": 4,
    }

    ivaPercentageIds = {
        "0.00": 0,
        "10.50": 4,
        "21.00": 5,
        "21.0": 5,
        "21": 5,
        21.0: 5,
        21: 5,
    }

    def runcommand(self, commando, *args):
        arg = None
        if args and args[0] is not None and len(args[0]):
            arg = args[0].split(",")
        if arg is None or len(arg) <= 10:
            ret = self.conector.driver.EpsonLibInterface[commando](*(arg or []))
        else:
            ret = None
        return ret

    def getcommand(self, commando, *args):
        str_version_max_len = 500
        str_version = create_string_buffer(b"\000" * str_version_max_len)
        int_major = c_int()
        int_minor = c_int()
        error = self.conector.driver.EpsonLibInterface.ConsultarVersionDll(
            str_version,
            c_int(str_version_max_len).value,
            byref(int_major),
            byref(int_minor),
        )
        print "Machinne Version        : ",
        print error
        print "String Machinne Version : ",
        print str_version.value
        print "Major Machinne Version  : ",
        print int_major.value
        print "Minor Machine Version   : ",
        print int_minor.value
        return {
            "Machinne Version": error,
            "String Machinne Version": str_version.value,
            "Major Machinne Version": int_major.value,
            "Minor Machine Version": int_minor.value,
        }

        # if arg == None:
        #   ret = self.conector.driver.EpsonLibInterface[commando]()
        # elif len(arg)==1:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0])
        # elif len(arg)==2:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1])
        # elif len(arg)==3:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2])
        # elif len(arg)==4:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3])
        # elif len(arg)==5:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4])
        # elif len(arg)==6:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4],arg[5])
        # elif len(arg)==7:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6])
        # elif len(arg)==8:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])
        # elif len(arg)==9:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8])
        # elif len(arg)==10:
        #   ret = self.conector.driver.EpsonLibInterface[commando](arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9])
        # else:
        #   ret = None
        # return ret

    def getState(self):
        data = self.conector.driver.EpsonLibInterface.getState()
        return data

    def getLastError(self):
        data = self.conector.driver.EpsonLibInterface.getLastError()
        return data

    def getFiscalStatus(self):
        data = self.conector.driver.EpsonLibInterface.getFiscalStatus()
        return data

    def getPrinterStatus(self):
        data = self.conector.driver.EpsonLibInterface.getPrinterStatus()
        return data

    def getReturnCode(self):
        data = self.conector.driver.EpsonLibInterface.getReturnCode()
        return data

    def getComPort(self):
        data = self.conector.driver.EpsonLibInterface.getComPort()
        return data

    def getBaudRate(self):
        data = self.conector.driver.EpsonLibInterface.getBaudRate()
        return data

    def getProtocolType(self):
        data = self.conector.driver.EpsonLibInterface.getProtocolType()
        return data

    def GetHTTPStatusCode(self):
        data = self.conector.driver.EpsonLibInterface.GetHTTPStatusCode()
        return data

    def SetSSLInsecureMode(self):
        data = self.conector.driver.EpsonLibInterface.SetSSLInsecureMode()
        return data

    def GetTimeOut(self):
        data = self.conector.driver.EpsonLibInterface.GetTimeOut()
        return data

    def GetResponseHeadersCount(self):
        data = self.conector.driver.EpsonLibInterface.GetResponseHeadersCount()
        return data

    def getExtraFieldCount(self):
        data = self.conector.driver.EpsonLibInterface.getRegetExtraFieldCountturnCode()
        return data

    def ComenzarLog(self):
        data = self.conector.driver.EpsonLibInterface.ComenzarLog()
        return data

    def ConsultarEstadoDeConexion(self):
        data = self.conector.driver.EpsonLibInterface.ConsultarEstadoDeConexion()
        return data

    def ConsultarVersionDll(self):
        str_version_max_len = 500
        str_version = create_string_buffer(b"\000" * str_version_max_len)
        int_major = c_int()
        int_minor = c_int()
        error = self.conector.driver.EpsonLibInterface.ConsultarVersionDll(
            str_version,
            c_int(str_version_max_len).value,
            byref(int_major),
            byref(int_minor),
        )
        return {
            "Machinne Version": error,
            "String Machinne Version": str_version.value,
            "Major Machinne Version": int_major.value,
            "Minor Machine Version": int_minor.value,
        }

    #   # get document number
    #   str_doc_number_max_len = 20
    #   str_doc_number = create_string_buffer( b'\000' * str_doc_number_max_len )
    #   error = Handle_HL.ConsultarNumeroComprobanteActual( str_doc_number, c_int(str_doc_number_max_len).value )
    #   print "Get Doc. Number Error : ",
    #   print error
    #   print "Doc Number            : ",
    #   print str_doc_number.value

    #   str_version_max_len = 500
    #   str_version = create_string_buffer( b'\000' * str_version_max_len )
    #   int_major = c_int()
    #   int_minor = c_int()
    #   error = Handle_HL.ConsultarVersionDll( str_version, c_int(str_version_max_len).value, byref(int_major), byref(int_minor) )
    #   print "Machinne Version        : ",
    #   print error
    #   print "String Machinne Version : ",
    #   print str_version.value
    #   print "Major Machinne Version  : ",
    #   print int_major.value
    #   print "Minor Machine Version   : ",
    #   print int_minor.value

    #   # get header #1
    #   str_header1_max_len = 100
    #   str_header1 = create_string_buffer( b'\000' * str_header1_max_len )
    #   error = Handle_HL.ConsultarEncabezado( c_int(1).value, str_header1, c_int(str_header1_max_len).value )
    #   print "Get Header Error      : ",
    #   print error
    #   print "Header #1 String      : ",
    #   print str_header1.value

    #   # get trailer #1
    #   str_trailer1_max_len = 100
    #   str_trailer1 = create_string_buffer( b'\000' * str_trailer1_max_len )
    #   error = Handle_HL.ConsultarCola( c_int(1).value, str_trailer1, c_int(str_trailer1_max_len).value )
    #   print "Get Trailer Error     : ",
    #   print error
    #   print "Trailer #1 String     : ",
    #   print str_trailer1.value

    #   # get datetime
    #   str_datetime_max_len = 100
    #   str_datetime = create_string_buffer( b'\000' * str_datetime_max_len )
    #   error = Handle_HL.ConsultarFechaHora( str_datetime, c_int(str_datetime_max_len).value )
    #   print "Get Date & Time Error : ",
    #   print error
    #   print "Date & Time           : ",
    #   print str_datetime.value

    #   # get subtotal gross amount
    #   str_subtotal_max_len = 20
    #   str_subtotal = create_string_buffer( b'\000' * str_subtotal_max_len )
    #   error = Handle_HL.ConsultarSubTotalBrutoComprobanteActual( str_subtotal, c_int(str_subtotal_max_len).value )
    #   print "Get Subtotal Gross    : ",
    #   print error
    #   print "Subtotal Gross Amount : ",
    #   print str_subtotal.value

    def getStatus(self, *args):
        return {self.conector.driver.ObtenerEstadoFiscal()}

    def setHeader(self, headerlist=[]):
        """Establecer encabezado"""
        print headerlist
        line = 1
        while line <= len(headerlist):
            texto = c_char_p(headerlist[line - 1]).value
            print "------------"
            print texto
            print "------------"
            self.conector.driver.EpsonLibInterface.EstablecerEncabezado(line, texto)
            line += 1
            pass
        # line = 0
        # for text in headerlist:
        #   self.conector.driver.EstablecerEncabezado(line, text)
        #  line += 1

    def setTrailer(self, trailer=[]):
        """Establecer pie"""
        line = 1
        while line <= len(trailer):
            texto = c_char_p(trailer[line - 1]).value
            self.conector.driver.EpsonLibInterface.EstablecerCola(line, texto)
            line += 1
            pass
        # line = 0
        # for text in trailer:
        #   self.conector.driver.EstablecerCola(line, text)
        #  line += 1

    def _sendCommand(self, commandNumber, parameters, skipStatusErrors=False):
        self.conector.sendCommand()

    def _setCustomerData(
        self, name=" ", address=" ", doc=" ", docType=" ", ivaType="T"
    ):
        # nombre, segunda línea nombre, primer segunda y tercera línea dirección, tipo de documento, número de documento y tipo de responsabilidad ante el IVA
        self.conector.driver.EpsonLibInterface.CargarDatosCliente(
            name,
            None,
            address,
            None,
            None,
            self.docTypes.get(docType),
            doc,
            self.ivaTypes.get(ivaTypes),
        )

    # Documentos no fiscales

    def openNonFiscalReceipt(self):
        """Abre documento no fiscal"""
        pass

    def printFiscalText(self, text):
        pass
        # self.conector.sendCommand( jdata )

    def printNonFiscalText(self, text):
        """Imprime texto fiscal. Si supera el límite de la linea se trunca."""
        pass
        # self.conector.sendCommand( jdata )

    def closeDocument(self, copias=0, email=None):
        """Cierra el documento que esté abierto"""
        self.conector.driver.EpsonLibInterface.CerrarComprobante()

    def cancelDocument(self):
        """Cancela el documento que esté abierto"""
        self.conector.driver.EpsonLibInterface.Cancelar()

    def imprimirAuditoria(self, desde, hasta):
        # desde & Hasta = Nros de Zeta o fechas, ambos pueden ser usados como intervalos de tiempo.
        self.conector.driver.ImprimirAuditoria(desde, hasta)

    def addItem(
        self,
        description,
        quantity,
        price,
        iva,
        itemNegative=False,
        discount=0,
        discountDescription="",
        discountNegative=False,
    ):
        """
        Agrega un item a la FC.
            @param description          Descripción del item. Puede ser un string o una lista.
                Si es una lista cada valor va en una línea.
            @param quantity             Cantidad
            @param price                Precio (incluye el iva si la FC es B o C, si es A no lo incluye)
            @param iva                  Porcentaje de iva
            @param itemNegative         Anulación del ítem.
            @param discount             Importe de descuento
            @param discountDescription  Descripción del descuento
            @param discountNegative     True->Resta de la FC
        """

        id_item = 200  # Agregar como ítem de venta.
        if itemNegative is True:
            id_item = 201
        if discountNegative is True:
            id_item = 206

        # id tipo de item, descripción, cantidad, porcentaje de IVA,
        # identificador II impuestos internos (0 = Ninguno), valor II, id_codigo (1 = Interno), valor del codigo, codigo_unidad_matrix, unidad de medida Unidad (7)
        ivaid = self.ivaPercentageIds.get("iva", 5)
        qty = str(quantity)
        ret = self.conector.driver.ImprimirItem(id_item, description, qty, price, ivaid)
        print("Imprimiendo item       : %s", ret)

    def addPayment(self, description, payment):
        """
        Agrega un pago a la FC.
            @param description  Descripción
            @param payment      Importe
        """
        print 200, 8, 1, str(payment), "None", description
        ret = self.conector.driver.EpsonLibInterface.CargarPago(
            200, 8, 1, str(payment), "None", description, "asd", "ga"
        )
        pass

        # self.conector.sendCommand( jdata )

    # Ticket fiscal (siempre es a consumidor final, no permite datos del cliente)

    def openTicket(self, comprobanteType="T"):
        """Abre documento fiscal
        str comprobanteType

        • 1 – Tique.
        • 2 – Tique factura A/B/C/M.
        • 3 – Tique nota de crédito, tique nota crédito A/B/C/M.
        • 4 – Tique nota de débito A/B/C/M.
        • 21 – Documento no fiscal homologado genérico.
        • 22 – Documento no fiscal homologado de uso interno.
        """
        numcomp = self.comprobanteTypes[comprobanteType]
        err = self.conector.driver.EpsonLibInterface.AbrirComprobante(numcomp)
        print err
        logging.getLogger().info("Abrio comprobante  : %s" % (err))

    def openBillTicket(self, type, name, address, doc, docType, ivaType):
        """
        Abre un ticket-factura
            @param  type        Tipo de Factura "A", "B", o "C"
            @param  name        Nombre del cliente
            @param  address     Domicilio
            @param  doc         Documento del cliente según docType
            @param  docType     Tipo de documento
            @param  ivaType     Tipo de IVA
        """

        comprobanteType = self.comprobanteTypes[type]
        self.conector.driver.EpsonLibInterface.AbrirComprobante(comprobanteType)

    def openBillCreditTicket(
        self, type, name, address, doc, docType, ivaType, reference="NC"
    ):
        """
        Abre un ticket-NC
            @param  type        Tipo de Factura "A", "B", o "C"
            @param  name        Nombre del cliente
            @param  address     Domicilio
            @param  doc         Documento del cliente según docType
            @param  docType     Tipo de documento
            @param  ivaType     Tipo de IVA
            @param  reference
        """
        comprobanteType = 3  # Tique Nota de crédito A/B/C/M

        self.conector.driver.EpsonLibInterface.AbrirComprobante(comprobanteType)

    def __cargarNumReferencia(self, numero):
        pass

    def openDebitNoteTicket(self, type, name, address, doc, docType, ivaType):
        """
        Abre una Nota de Débito
            @param  type        Tipo de Factura "A", "B", o "C"
            @param  name        Nombre del cliente
            @param  address     Domicilio
            @param  doc         Documento del cliente según docType
            @param  docType     Tipo de documento
            @param  ivaType     Tipo de IVA
            @param  reference
        """

        comprobanteType = 4  # Tique Nota de débito A/B/C/M

        self.conector.driver.EpsonLibInterface.AbrirComprobante(comprobanteType)

    def openRemit(self, name, address, doc, docType, ivaType):
        """
        Abre un remito
            @param  name        Nombre del cliente
            @param  address     Domicilio
            @param  doc         Documento del cliente según docType
            @param  docType     Tipo de documento
            @param  ivaType     Tipo de IVA
        """
        pass

    def openReceipt(self, name, address, doc, docType, ivaType, number):
        """
        Abre un recibo
            @param  name        Nombre del cliente
            @param  address     Domicilio
            @param  doc         Documento del cliente según docType
            @param  docType     Tipo de documento
            @param  ivaType     Tipo de IVA
            @param  number      Número de identificación del recibo (arbitrario)
        """
        pass

    def addRemitItem(self, description, quantity):
        """
        Agrega un item al remito
            @param description  Descripción
            @param quantity     Cantidad
        """
        pass

    def addReceiptDetail(self, descriptions, amount):
        """
        Agrega el detalle del recibo
            @param descriptions Lista de descripciones (lineas)
            @param amount       Importe total del recibo
        """
        pass

    def ImprimirAnticipoBonificacionEnvases(
        self, description, amount, iva, negative=False
    ):
        """
        Agrega un descuento general a la Factura o Ticket.
            @param description  Descripción
            @param amount       Importe (sin iva en FC A, sino con IVA)
            @param iva          Porcentaje de Iva
            @param negative     Si negative = True, se añadira el monto como descuento, sino, sera un recargo
        """
        pass

    def addAdditional(self, description, amount, iva, negative=False):
        """
        Agrega un descuento general a la Factura o Ticket.
            @param description  Descripción
            @param amount       Importe (sin iva en FC A, sino con IVA)
            @param iva          Porcentaje de Iva
            @param negative     Si negative = True, se añadira el monto como descuento, sino, sera un recargo
        """
        ivaid = self.ivaPercentageIds.get(iva)
        self.conector.driver.EpsonLibInterface.CargarAjuste(
            c_int(400).value, description, str(amount), c_int(ivaid).value, "asdads"
        )

    def setCodigoBarras(
        self, numero, tipoCodigo="CodigoTipoI2OF5", imprimeNumero="ImprimeNumerosCodigo"
    ):
        pass

    def start(self):
        self.conector.driver.start()

    def close(self):
        self.conector.driver.close()

    def getLastNumber(self, letter):
        """Obtiene el último número de FC"""
        # self.start()
        # self.cancelDocument()
        # retLenght = 20
        # ret = create_string_buffer( b'\000' * retLenght )
        # self.conector.driver.EpsonLibInterface.ConsultarNumeroComprobanteActual(ret, c_int(retLenght).value)
        if letter == "T":
            letter = "83"
        elif letter == "FA":
            letter = "81"
        elif letter == "FB":
            letter = "82"
        elif letter == "C":
            letter = "111"
        else:
            letter = "83"
        str_doc_number_max_len = 28
        str_doc_number = create_string_buffer(b"\000" * str_doc_number_max_len)
        test = self.conector.driver.EpsonLibInterface.ConsultarNumeroComprobanteUltimo(
            letter, str_doc_number, c_int(str_doc_number_max_len).value
        )

        # self.close()
        return str_doc_number.value

    def getLastCreditNoteNumber(self, letter):
        """Obtiene el último número de FC"""
        pass

    def getLastRemitNumber(self):
        """Obtiene el último número de Remtio"""
        pass

    def cancelAnyDocument(self):
        """Este comando no esta disponible en la 2da generación de impresoras, es necesaria su declaración por el uso del TraductorFiscal """
        return self.cancelDocument()

    def CargarLogo(self, path):
        """Este comando no esta disponible en la 2da generación de impresoras, es necesaria su declaración por el uso del TraductorFiscal """
        print path
        ret = self.conector.driver.EpsonLibInterface.CargarLogo(path)
        return ret

    def EliminarLogo(self):
        """Este comando no esta disponible en la 2da generación de impresoras, es necesaria su declaración por el uso del TraductorFiscal """
        ret = self.conector.driver.EpsonLibInterface.EliminarLogo()
        return ret

    def dailyClose(self, type):
        # self.start()

        # ver si conviene o no dejar alguna de estas opciones
        # alenta un poco mas el cierre x o Z
        # pero permitiria que ande siempre siempre, por si algo quedo trabado antes
        # self.cancel()
        # self.cancelAnyDocument()

        if type == "Z":
            ret = self.conector.driver.EpsonLibInterface.ImprimirCierreZ()
        else:
            ret = self.conector.driver.EpsonLibInterface.ImprimirCierreX()
        print "--------------"
        print "--------------"
        print "--------------"
        print ret
        print "--------------"
        print "--------------"
        print "--------------"
        # self.close()

        return ret

    def getWarnings(self):
        return []

    def openDrawer(self):
        pass
