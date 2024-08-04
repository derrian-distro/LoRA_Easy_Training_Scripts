from PySide6.QtCore import QUrlQuery, QUrl, QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json

from functools import wraps

# Wrap failed network reply with additional error message
def default_error(message = ""):
    def print_error(reply: QNetworkReply):
        print(message)
        print("Server reply: ")
        print(reply.errorString())
    return print_error


class NetworkManager(object):
    _instance = None
    _url = None
    _network_manager = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkManager, cls).__new__(cls)
            cls._network_manager = QNetworkAccessManager()
            cls._url = "http://localhost:8000"
        return cls._instance

    def set_backend_url(self, url: str):
        self._url = url

    def query(self, route: str, data: dict, on_success, on_failure = None):
        url = QUrl(self._url)
        url.setPath(route)
        query = QUrlQuery()
        for key, value in data.items():
            query.addQueryItem(key, value)
        url.setQuery(query)
        request = QNetworkRequest(url)
        reply = self._network_manager.get(request)
        on_failure = on_failure or default_error("Query failed: " + route)
        reply.finished.connect(lambda: self.handle_response(reply, on_success, on_failure))


    def handle_response(self, reply: QNetworkReply, on_success, on_failure):
        if reply.error() == QNetworkReply.NoError:
            response_data = json.loads(reply.readAll().data())
            on_success(response_data)
        else:
            on_failure(reply)
        reply.deleteLater()


    def debounce(timeout: float):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapper.timer.stop()
                wrapper.timer.setInterval(timeout)
                wrapper.timer.setSingleShot(True)
                wrapper.timer.timeout.connect(lambda: func(*args, **kwargs))
                wrapper.timer.start()
            wrapper.timer = QTimer()

            return wrapper
        return decorator