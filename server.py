import socket
from typing import Tuple
from router import Router
from request import HTTPRequest
from response import HTTPResponse

class WSGIServer:
    """
    Класс WSGI-сервера для обработки HTTP-запросов.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 8080, app: Router = None):
        """
        Инициализация WSGI-сервера.

        :param host: Хост для привязки сервера.
        :param port: Порт для привязки сервера.
        :param app: WSGI-приложение, которое будет обрабатывать запросы.
        """
        self.host = host
        self.port = port
        self.router = app  

    def run(self):
        """
        Запускает сервер и начинает прослушивание подключений.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер запущен на {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    self.handle_request(client_socket)

    def handle_request(self, client_socket: socket.socket):
        """
        Обрабатывает входящий HTTP-запрос.
        """
        request_data = client_socket.recv(1024).decode("utf-8")
        if not request_data:
            return

 
        request = HTTPRequest(request_data)

        normalized_path = request.path.strip("/") 
        print(f"Получен запрос: {request.method} /{normalized_path}") 

        try:

            handler = self.router.resolve(normalized_path, request.method)
            response = handler(request)  
            self.send_response(client_socket, "200 OK", [("Content-Type", "text/plain; charset=utf-8")], response.body)
        except KeyError:
            print(f"Ошибка: {request.method} /{normalized_path} не найден.") 
            self.send_response(client_socket, "404 Not Found", [("Content-Type", "text/plain")], b"Page Not Found")


    def build_environ(self, request: HTTPRequest) -> dict:
        """
        Создает WSGI-окружение из объекта HTTP-запроса.
        """
        environ = {
            "REQUEST_METHOD": request.method,
            "PATH_INFO": request.path,
            "QUERY_STRING": request.query_params,
            "SERVER_NAME": self.host,
            "SERVER_PORT": str(self.port),
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": request.body.encode("utf-8") if request.body else b"",
            "wsgi.errors": None,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }

        for key, value in request.headers.items():
            environ[f"HTTP_{key.upper().replace('-', '_')}"] = value

        return environ
    
    def send_response(self, client_socket: socket.socket, status: str, headers: list[Tuple[str, str]], body: str):
        """
        Отправляет HTTP-ответ клиенту.
        """
        response = HTTPResponse(status=status, headers=dict(headers), body=body)
        client_socket.sendall(response.to_bytes())