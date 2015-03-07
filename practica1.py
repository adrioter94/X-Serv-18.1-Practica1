#!/usr/bin/python
#-*- coding: utf-8 -*-


import webapp
import urllib


class contentApp (webapp.webApp):
    # Declare and initialize content
    urls_Acotadas = {}
    sec_urls = {}
    secuencia = -1

    def parse(self, request):

        recurso = request.split(' ', 2)[1]
        metodo = request.split(' ', 2)[0]

        if metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[1]
            cuerpo = cuerpo.split("=")[1].replace("+", " ")
        elif metodo == "GET":
            cuerpo = ""

        return (metodo, recurso, cuerpo)

    def process(self, resourceName):

        (metodo, recurso, cuerpo) = resourceName
        formulario = '<form action="" method="POST">'
        formulario += 'Acortar url: <input type="text" name="valor">'
        formulario += '<input type="submit" value="Enviar">'
        formulario += '</form>'

        if metodo == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body>" + formulario\
                           + "<p>" + str(self.urls_Acotadas)\
                           + "</p></body></html>"
            else:
                recurso = int(recurso[1:])
                if recurso in self.sec_urls:
                    httpCode = "300 Redirect"
                    htmlBody = "<html><body><meta http-equiv='refresh'"\
                               + "content='1 url="\
                               + self.sec_urls[recurso] + "'>"\
                               + "</p>" + "</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body>"\
                               + "Error: Recurso no disponible"\
                               + "</body></html>"

        elif metodo == "POST":

            if cuerpo == "":
                httpCode = "404 Not Found"
                htmlBody = "<html><body>"\
                           + "Error: no se introdujo ninguna url"\
                           + "</body></html>"
                return(httpCode, htmlBody)
            elif cuerpo.find("http") == -1:
                cuerpo = "http://" + cuerpo
            else:
                cuerpo = cuerpo.split("%3A%2F%2F")[0]\
                    + "://" + cuerpo.split("%3A%2F%2F")[1]

            if cuerpo in self.urls_Acotadas:
                secuencia = self.urls_Acotadas[cuerpo]
            else:
                self.secuencia = self.secuencia + 1
                secuencia = self.secuencia

            self.urls_Acotadas[cuerpo] = secuencia
            self.sec_urls[secuencia] = cuerpo
            httpCode = "200 OK"
            htmlBody = "<html><body>"\
                       + "<a href=" + cuerpo + ">" + cuerpo + "</href>"\
                       + "<p><a href=" + str(secuencia) + ">" + str(secuencia)\
                       + "</href></body></html>"

        else:

            httpCode = "404 Not Found"
            htmlBody = "<html><body>Metodo no soportado</body></html>"

        return (httpCode, htmlBody)


if __name__ == "__main__":
    try:
        testWebApp = contentApp("localhost", 1234)
    except KeyboardInterrupt:
        print ""
        print "Finalizando aplicación"
