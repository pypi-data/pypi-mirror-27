import sys
import errno
import socket
import logging
import threading

logger = logging.getLogger(__name__)


class Heartbeat(object):

    def __init__(self, connection, on_error=None, rejects=None):
        self._connection = connection
        self._on_error = on_error
        self._rejects = rejects
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

    def _run(self):
        while not self._stop.wait(1):
            if self._rejects:
                self._rejects.send_pending()
            try:
                try:
                    self._connection.send_heartbeat()
                except socket.error as e:
                    if e.errno != errno.EINTR:
                        raise
            except socket.timeout:
                pass
            except Exception as e:
                logger.error(e)
                if self._on_error:
                    self._on_error(sys.exc_info())
                break
