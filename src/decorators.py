from client_fva import signals
import logging
import pkcs11

from client_fva.exception import PinNotProvided

logger = logging.getLogger()


def decore_pkcs11(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        count = 0
        try_again = True
        dev = None
        slot = kwargs['slot'] if 'slot' in kwargs else None
        while try_again and count < 3:
            try:
                dev = func(*args, **kwargs)
                try_again = False
            except pkcs11.exceptions.PinLocked as e:
                signals.send('notify', signals.SignalObject(signals.NOTIFTY_ERROR, {
                    'message': "Tarjeta bloqueada, por favor contacte con su proveedor para desbloquearla"}))
                logger.error("Tarjeta bloqueada, por favor contacte con su proveedor para desbloquearla "+str(instance.serial))
                try_again = False
            except pkcs11.exceptions.TokenNotRecognised as e:
                signals.send('notify', signals.SignalObject(signals.NOTIFTY_ERROR,
                                                            {'message': "No se puede obtener la identificación de la "
                                                                        "persona, posiblemente porque la tarjeta está "
                                                                        "mal conectada"}))
                logger.error("Tarjeta no detectada %r" % (e,))
                try_again = False
            except pkcs11.exceptions.PinIncorrect as e:
                count += 1
                logger.info("Pin incorrecto para el slot %s  intento %d"%(str(slot), count))
                obj = signals.SignalObject(signals.NOTIFTY_ERROR, {
                    'message': "Pin incorrecto, recuerde después de 3 intentos su tarjeta puede bloquearse, este es el intento %d"%(count)})
                signals.send('notify', obj)
                signals.receive(obj)
                try_again = True
            except PinNotProvided as e:
                signals.send('notify', signals.SignalObject(signals.NOTIFTY_ERROR, {
                    'message': "No se ha logrado identificar el PIN correcto con ninguno de los mecanismos establecidos"}))
                logger.error("Pin no provisto, el sistema no identificó un pin adecuado")
                try_again = True
                count += 1
            except pkcs11.exceptions.DataInvalid as e:
                signals.send('notify', signals.SignalObject(
                    signals.NOTIFTY_ERROR,
                    {'message': "No se ha logrado firmar, posiblemente porque el mecanismo usado en la aplicación no está disponible en su tarjeta"}))
                logger.error("Error al firmar documento %r" % (e,))
                try_again = False

        if count == 3:
            signals.send('notify', signals.SignalObject(signals.NOTIFTY_ERROR, {
                'message': "Se ha excedido el número de intentos, puede que su tarjeta haya sido bloqueada"}))

        return dev

    return wrapper
