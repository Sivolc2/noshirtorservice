def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["<html><body><h1 style>Hello, there!</h1></body></html>"]

