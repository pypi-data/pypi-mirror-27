from string import Template
from PyQt5.QtCore import QObject, pyqtSignal


class Receiver:
    ''' Класс-получатель информации из сокета
    '''
    def __init__(self, sock):
        self.sock = sock
        self.is_alive = False

    def process_message(self, message):
        pass

    def server_message(self, message):
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = self.sock.get_msg()
            if data:
                try:
                    if data['action'] == 'msg'\
                         or data['action'] == 'broadcast':
                        self.process_message(data)
                    else:
                        # нужно очередь добалять!
                        pass
                except:
                    pass
            else:
                break

    def stop(self):
        self.is_alive = False

class GuiReciever(Receiver, QObject):
    gotData = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock):
        Receiver.__init__(self, sock)
        QObject.__init__(self)
        self.templates = {
            "to": Template("""<p><span style="color:purple;">
                                    PRIVATE $from#</span>
                                    $message</p>"""),
            "#all": Template("""<p><span style="color: #0048BA;">
                                        $from# </span>
                                        $message</p>"""),
        }

    def process_message(self, message):
        to = self.templates["#all"] \
                            if message["to"] == "#all" else self.templates["to"]
        self.gotData.emit(to.substitute(message))

    def poll(self):
        super().poll()
        self.finished.emit(0)
