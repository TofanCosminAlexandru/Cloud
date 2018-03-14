import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

data = json.load(open('movies.json'))
movieList = []
for i in data:
    movieList.append(i)


def getItemFromId(id):
    for i in movieList:
        if i['id'] == id:
            return i
    return -1


def idExist(id):
    for i in movieList:
        if i['id'] == id:
            return True
    return False


def getLastId():
    return len(movieList)


def deleteById(id):
    for i in movieList:
        if i['id'] == id:
            movieList.remove(i)
            return 1
    return -1

def writeInFile(fileName, dataj):
    with open(fileName + ".json", 'w') as outfile:
        json.dump(dataj, outfile, indent=4)

fileName = 'movies'

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if re.search(r'/movies/id=', self.path):
            path = self.path
            path = path.split("/")
            id = path[2].split("=")
            id = int(id[1])
            s = getItemFromId(id)
            if (s != -1):
                self.send_response(200, "OK")
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                s = json.dumps(s, indent=4)
                self.wfile.write(s.encode())
            else:
                self.send_error(404,
                                'Not Found - The requested resource could not be found but may be available in the '
                                'future. Subsequent requests by the client are permissible')
        elif re.search(r'/movies', self.path):
            self.send_response(200, "Ok")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            s = json.dumps(movieList, indent=4)
            self.wfile.write(s.encode())
        else:
            self.send_error(404, 'Not Found - The requested resource could not be found but may be available in the '
                                 'future. Subsequent requests by the client are permissible')

    def do_POST(self):
        path = self.path
        path = path.split("?")
        print(path)
        # params = ["id", "title", "year", "runtime", "genres", "director", "actors", "plot", "posterUrl"]
        if len(path) != 1 and (path[0] == '/movies' or path[0] == '/movies/'):
            param = path[1].split("&")
            data = {}
            data["id"] = int(getLastId()) + 1
            data["title"] = ''
            data["year"] = ''
            data["runtime"] = ''
            data["genres"] = ''
            data["director"] = ''
            data["actors"] = ''
            data["plot"] = ''
            data["posterUrl"] = ''

            for x in param:
                j = x.split("=")
                # if j[0] in params:
                data[j[0]] = str(j[1]).replace(r"%20", " ")
            print(data)
            movieList.append(data)

            self.send_response(201, 'CREATED')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            s = json.dumps(data, indent=4)
            self.wfile.write(s.encode())
            writeInFile(fileName, movieList)

        elif len(path) == 1 and (path[0] == '/movies' or path[0] == '/movies/'):
            data = {}
            data["id"] = int(getLastId()) + 1
            data["title"] = ''
            data["year"] = ''
            data["runtime"] = ''
            data["genres"] = ''
            data["director"] = ''
            data["actors"] = ''
            data["plot"] = ''
            data["posterUrl"] = ''
            print(data)
            movieList.append(data)

            self.send_response(201, 'CREATED')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            s = json.dumps(data, indent=4)
            self.wfile.write(s.encode())
            writeInFile(fileName, movieList)
        else:
            self.send_error(404,
                            'Not Found - The requested resource could not be found but may be available in the '
                            'future. Subsequent requests by the client are permissible')

    def do_PUT(self):
        path = self.path
        path = path.split("?")
        # params = ["id", "title", "year", "runtime", "genres", "director", "actors", "plot", "posterUrl"]
        print(path[0].split("/"))
        if len(path) != 1 and re.findall("/movies/id=", path[0]):
            id = int(path[0].split("=")[1])
            print(id)
            param = path[1].split("&")
            print(param)

            if idExist(id):
                for elem in movieList:
                    if elem["id"] == id:
                        for x in param:
                            j = x.split("=")
                            # if j[0] in params:
                            elem[j[0]] = str(j[1]).replace(r"%20", " ")
            else:
                data = {}
                data["id"] = id
                data["title"] = ''
                data["year"] = ''
                data["runtime"] = ''
                data["genres"] = ''
                data["director"] = ''
                data["actors"] = ''
                data["plot"] = ''
                data["posterUrl"] = ''

                for x in param:
                    j = x.split("=")
                    # if j[0] in params:
                    data[j[0]] = str(j[1]).replace(r"%20", " ")
                movieList.append(data)

            print(getItemFromId(id))
            self.send_response(201, 'CREATED')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("201 CREATED".encode())
            global fileName
            writeInFile(fileName, movieList)

        elif path[0].split("/")[1] == "movies" and len(path[0].split("/")) == 3 and path[0].split("/")[2] != "":
            param = path[0].split("/")[2]
            file_path = param + '.json'
            if os.path.exists(file_path):
                movieList.clear()
                data = json.load(open(file_path))
                for i in data:
                    movieList.append(i)
                self.send_response(200, 'OK')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("204 No Content".encode())
                fileName = param
                writeInFile(fileName, movieList)
            else:
                self.send_error(404,
                                'Not Found - The requested resource could not be found but may be available in the '
                                'future. Subsequent requests by the client are permissible')
            print(movieList)
        else:
            self.send_error(404,
                            'Not Found - The requested resource could not be found but may be available in the '
                            'future. Subsequent requests by the client are permissible')

    def do_DELETE(self):
        path = self.path
        path2 = path
        path = path.split("/")
        print(path)
        if path[1] == 'movies' and re.findall("id=", path2):
            id = path[2].split("=")[1]
            id = int(id)

            if idExist(id):
                print(id)
                a = deleteById(id)
                print(a)
                print(movieList)
                self.send_response(200, 'No Content')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("204 No Content".encode())
                writeInFile(fileName, movieList)
            else:
                self.send_error(404,
                                'Not Found - The requested resource could not be found but may be available in the '
                                'future. Subsequent requests by the client are permissible')
        elif path[1] == 'movies':
            print("delete all")
            movieList.clear()
            print(movieList)
            self.send_response(200, 'No Content')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("204 No Content".encode())
            writeInFile(fileName, movieList)
        else:
            self.send_error(404,
                            'Not Found - The requested resource could not be found but may be available in the '
                            'future. Subsequent requests by the client are permissible')


def run(server_class=HTTPServer, handler_class=Server, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
