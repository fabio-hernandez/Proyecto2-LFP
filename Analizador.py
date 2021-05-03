from Gramatica import *
from tkinter import filedialog as FileDialog

class ListGram(object):
    def __init__(self):
        self.gramatica = []

    def cargar():
        # Abrir ventena de seleccion
        fichero = FileDialog.askopenfilename(title="Seleccione un archivo")
        file = open(fichero, 'r')
        contenedor = file.readlines()
        print(contenedor)

    def ExisteGramatica(self, AFD):
        for afd in self.gramatica:
            if afd.nombre == AFD:
                print('Existe una gramatica con ese nombre')
                return True
        return False

    def EsVacio(self):
        if len(self.gramatica) == 0:
            return True
        else:
            return False
    def EliminarAutomata(self, nombre):
        for afd in self.gramatica:
            if afd.nombre == nombre:
                self.gramatica.remove(afd)
                print('Se ha eliminado la gramatica')

    def insertar(self, AFD):
        if not self.ExisteGramatica(AFD.nombre):
            self.gramatica.append(AFD)
        else:
            '''Ya existe una gramatica'''

    def MostrarGramaticas(self):
        for afd in self.gramatica:
            print(afd.nombre)

    def CargarGramaticas(self, direccion):
        global EnCreacion
        automatas = open(direccion, 'r')
        noL = 0
        for linea in automatas.readlines():
            noL += 1
            linea = linea.replace('\n', '')

            if noL == 1:
                if not self.ExisteGramatica(linea):
                    EnCreacion = Gramatica(linea)
                    print(EnCreacion.nombre, 'creandose')
                else:
                    self.EliminarAutomata(linea)
                    EnCreacion = Gramatica(linea)
                    print(EnCreacion.nombre, 'creandose')
            elif noL == 2:
                contador = 0
                for d in linea.split(';'):
                    print(d)
                    if contador == 0:
                        for i in d.split(','):
                            EnCreacion.AgregarEstados(i)
                            EnCreacion.cadenanotermianles = d
                    elif contador == 1:
                        for i in d.split(','):
                            EnCreacion.IngresarAlfabeto(i)
                        EnCreacion.cadenaterminales = d
                    elif contador == 2:
                        EnCreacion.inicial = d
                    contador += 1
            elif linea == '*':
                print(' ')
                if EnCreacion.EsLibreDeContexto:
                    self.gramatica.append(EnCreacion)
                    print('El automata se creó correctamente')
                    self.ImprimirAutomata(EnCreacion)

                else:
                    print('No es una gramatica libre del contexto, por lo tanto está no se agregará')
                noL = 0
            else:
                EnCreacion.AgregarTransicion(linea)
        automatas.close()

    def ImprimirAutomata(self, EnCreacion):

        print('Nombre:', EnCreacion.nombre)
        print('No terminales:', EnCreacion.cadenanotermianles)
        print('Terminales: ', EnCreacion.cadenaterminales)
        print('No terminal inicial:', EnCreacion.inicial)
        print('Producciones:')
        n = 0
        for estado in EnCreacion.noterminales:
            n += 1
            no = 1
            for transicion in estado.transiciones:
                if no == 1:
                    print("producion " + str(n) + ': ' + estado.estado, '->', transicion)
                else:
                    print("\t" + "\t" + "\t" + "\t" + '|', transicion)
                no += 1

    def DevolverAutomata(self, nombre):
        for adp in self.gramatica:
            if adp.nombre == nombre:
                return adp
        return False

    def reporteError(self):
        contenido = ''
        htmFile = open("Reporte_Gramaticas" + ".html", "w", encoding='utf8')
        htmFile.write("""<!DOCTYPE HTML PUBLIC"
                   <html>
                   <head>
                       <title>Reporte de errores</title>
                    <meta charset="utf-8">
                 <meta name="viewport" content="width=device-width, initial-scale=1">
                 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                 <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>    
                   </head>
                   <body>
                   <div class="container">
                 <h2>Reporte de errores</h2>
                 <p>Lista de errores</p>            
                 <table class="table">
                   <thead>
                     <tr>
                      <th>nombre</th>
                       <th>razon</th>

                     </tr>
                   </thead>
                   """)
        for i in range(len(self.error)):
            contenido += (" <tbody>"
                          "<td>" + str(self.error[i][0]) + "</td>"
                                                           "<td>" + str(self.error[i][1]) + "</td>"
                                                                                            "</tbody>")
        htmFile.write(contenido)
        htmFile.write("""
                 </table>
            </div>
                </body>
                </html>""")
        htmFile.close()