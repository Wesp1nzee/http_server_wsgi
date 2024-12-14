from typing import Callable

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path: str, method: str, handler: Callable):
        """
        Добавляет маршрут в маршрутизатор. Убирает ведущие и завершающие слэши из пути.
        """
        path = path.strip("/")  
        if path not in self.routes:
            self.routes[path] = {}
        if method not in self.routes[path]:  
            self.routes[path][method] = handler
            print(f"Маршрут {method} /{path} зарегистрирован.")
        else:
            print(f"Маршрут {method} /{path} уже существует.")

    def resolve(self, path: str, method: str) -> Callable:
        """
        Находит обработчик для заданного маршрута и метода.
        """
        path = path.strip("/")  
        try:
            return self.routes[path][method]
        except KeyError:
            raise KeyError(f"Маршрут {method} /{path} не найден.")


    def route(self, path: str, method: str = "GET"):
        """
        Декоратор для регистрации маршрутов.
        """
        path = path.strip("/") 
        def decorator(handler: Callable):
            self.add_route(path, method, handler)
            return handler
        return decorator

