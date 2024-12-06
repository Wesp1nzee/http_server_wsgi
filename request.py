from urllib.parse import parse_qs, urlparse
from typing import Dict, Optional


class HTTPRequest:
    """
    Класс для представления и обработки HTTP-запроса.
    """
    def __init__(self, raw_request: str):
        """
        Парсит HTTP-запрос из сырого текста.

        :param raw_request: Строка, содержащая полный HTTP-запрос.
        """
        self.raw_request = raw_request
        self.method: str = ""
        self.path: str = ""
        self.query_params: Dict[str, str] = {}
        self.headers: Dict[str, str] = {}
        self.body: Optional[str] = None

        self._parse_request()

    def _parse_request(self):
        """
        Основной метод для парсинга запроса.
        """
        lines = self.raw_request.split("\r\n")
        request_line = lines[0]  
        self.method, full_path, _ = request_line.split(" ")

        
        parsed_url = urlparse(full_path)
        self.path = parsed_url.path
        self.query_params = parse_qs(parsed_url.query)

    
        headers = {}
        body_index = 0
        for i, line in enumerate(lines[1:], start=1):
            if line == "":
                body_index = i
                break
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        self.headers = headers

        self.body = "\r\n".join(lines[body_index + 1:]) if body_index < len(lines) - 1 else None
