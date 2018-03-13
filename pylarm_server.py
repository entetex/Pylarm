#!/usr/bin/env python3
import socket
import threading


# This class handles the opened connections.
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket

    def run(self):
        print("Connection from : ", clientAddress, " at ", get_time())
        while True:
            data = self.csocket.recv(1024)
            print("from client", data)
            retData = get_bin_info(data)
            if len(retData) >= 1:
                self.csocket.send(retData)
            break


if __name__ == "__main__":

    from pygame import mixer
    from datetime import datetime
    import pylarm_config

    # Method to start the alarm
    def start_alarm():
        mixer.init()
        mixer.music.load(pylarm_config.musicfile)
        mixer.music.play(-1)
        set_busy(True)
        return

    # Method to stop the alarm
    def stop_alarm():
        mixer.music.stop()
        mixer.quit()
        set_busy(False)
        return

    # Method to edit the status of the alarm
    def set_busy(bool):
        global engaged
        engaged = bool
        return

    # Method to request the status of the alarm
    def get_busy():
        global engaged
        return engaged

    # Method to check is an alarm initiation falls between allowed times
    def try_time():
        nu = datetime.now()
        dag = nu.weekday()
        uur = nu.hour
        if (pylarm_config.dagAan <= dag <= pylarm_config.dagUit and
                pylarm_config.tijdAan <= uur <= pylarm_config.tijdUit):
            return True
        else:
            return False

    # Method to get the current date and time
    def get_time():
        nu = datetime.now()
        retStr = str(nu)
        return retStr

    # Method to check the commands and to initiate appropriate actions.
    # The method returns binary data, to send back to the client.
    def get_bin_info(datastream):
        # At first the token is checked.
        if datastream[-(len(pylarm_config.token)):] == pylarm_config.token:
            # If the token was correct, the token is removed from the command,
            # so that only the action remains.
            data = datastream[:-(len(pylarm_config.token))]
            if data == b'info':
                # Info returns the current state of the alarm.
                if get_busy():
                    return_bs = b'Alarm is engaged'
                else:
                    return_bs = b'Alarm is not engaged'
            elif data == b'alarm':
                # Alarm tries to initiate the alarm.
                if get_busy():
                    # The first check is to see if the alarm is already
                    # playing.
                    return_bs = b'Alarm is already engaged!'
                else:
                    # The second check is to see if the alarm is allowed
                    # to be initiated.
                    if try_time():
                        # If all is well, the alarm is started.
                        start_alarm()
                        return_bs = b'The alarm is engaged!'
                    else:
                        # If the initiation is tried in a moment that falls
                        # out of the allowed configuration, an appropriate
                        # message is sent back to the client.
                        return_bs = (b'The alarm could not be started as it '
                                     b'falls out of the configured hours!')

            elif data == b'stop':
                # stop cancels the alarm if it is engaged.
                if not get_busy():
                    # If the alarm is not playing, it cannot be canceled.
                    return_bs = b'Alarm is not engaged'
                else:
                    # If the alarm was playing, it is stopped.
                    stop_alarm()
                    return_bs = b'The alarm has been disengaged!'
            else:
                # If no appropriate acttion was sent, an error message is
                # sent back.
                return_bs = b'ERROR Incorrect action'
        # If no correct token was provided, an empty message is sent.
        else:
            return_bs = b''
        return return_bs

    # Variables
    engaged = False
    host = pylarm_config.host
    port = pylarm_config.port

    # Prepare socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    print("Pylarm server initiated.")
    while True:
        # Await connections
        server.listen(1)
        # Accept connections
        clientsock, clientAddress = server.accept()
        # Spawn a thread for a new connection
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
