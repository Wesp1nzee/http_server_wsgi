from typing import Dict, Tuple


class HTTPResponse:
    """
    Класс для представления и формирования HTTP-ответа.
    """
    def __init__(self, status: str = "200 OK", headers: Dict[str, str] = None, body: str = ""):
        """
        Инициализация HTTP-ответа.

        :param status: Статус ответа (например, '200 OK').
        :param headers: Заголовки ответа (например, {'Content-Type': 'text/plain'}).
        :param body: Тело ответа.
        """
        self.status = status
        self.headers = headers
        self.body = body

    def set_header(self, name: str, value: str):
        """
        Устанавливает или обновляет заголовок.

        :param name: Имя заголовка.
        :param value: Значение заголовка.
        """
        self.headers[name] = value


    def to_bytes(self) -> bytes:
        """
        Преобразует HTTP-ответ в байты для отправки клиенту.
        """
        response_line = f"HTTP/1.1 {self.status}\r\n"
        headers = "".join([f"{key}: {value}\r\n" for key, value in self.headers.items()])
        blank_line = "\r\n"
        
        
        if isinstance(self.body, str):
            body = self.body.encode("utf-8")  
        else:
            body = self.body
        
        return (response_line + headers + blank_line).encode("utf-8") + body
