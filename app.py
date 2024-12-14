from server import WSGIServer
from request import HTTPRequest
from response import HTTPResponse
from router import Router

router = Router()  

@router.route("/", "GET")
def index_handler(request: HTTPRequest) -> HTTPResponse:
    """
    Обработчик для главной страницы.
    """
    return HTTPResponse(
        status="200 OK",
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="Hello, World!".encode("utf-8")
    )

@router.route("/about", "GET")
def about_handler(request: HTTPRequest) -> HTTPResponse:
    """
    Обработчик для страницы "О нас".
    """
    return HTTPResponse(
        status="200 OK",
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="About Us".encode("utf-8")
    )

@router.route("/hello", "GET")
def hello_handler(request: HTTPRequest) -> HTTPResponse:
    """
    Обработчик для страницы "Привет".
    """
    return HTTPResponse(
        status="200 OK",
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="Hello there!".encode("utf-8")
    )


if __name__ == "__main__":
    server = WSGIServer(host="127.0.0.1", port=8080, app=router) 
    server.run()