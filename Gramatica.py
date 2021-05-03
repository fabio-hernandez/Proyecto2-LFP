import os
import subprocess


class Gramatica(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.terminales = []
        self.cadenaterminales = ''
        self.noterminales = []
        self.cadenanotermianles = ''
        self.inicial = 'inicial'
        self.EsLibreDeContexto = False

    def SacarNoTerminal(self, nombre):
        for noterminal in self.noterminales:
            if noterminal.estado == nombre:
                return noterminal
        return False

    def ExisteEnTerminales(self, parteAlfabeto):
        for parte in self.terminales:
            if parte == parteAlfabeto:
                return True
        return False

    def ExisteNoTerminal(self, nombre):
        for estado in self.noterminales:
            if estado.estado == nombre:
                return True
        return False

    def IngresarAlfabeto(self, parteAlfabeto):
        if self.ExisteNoTerminal(parteAlfabeto):
            print('Este caracter esta siendo usado como un No Terminal')
            print('')
        elif self.ExisteEnTerminales(parteAlfabeto):
            print(parteAlfabeto, 'Este caracter esta siendo usado como un Terminal')
            print('')
        else:
            self.terminales.append(parteAlfabeto)

    def AgregarEstados(self, nombre):
        if self.ExisteNoTerminal(nombre):
            print('Ya existe un estado con este simbolo', nombre)
            print('')
        else:
            self.noterminales.append(NoTerminal(nombre))
            print('No Terminal', nombre, 'agregado correctamente a la gramatica', self.nombre)
            print('')

    def AgregarTransicion(self, linea):
        separador = linea.split('->')
        produccion = separador[1].split(' ')

        if self.ExisteNoTerminal(separador[0]):

            for analizador in produccion:

                if self.ExisteNoTerminal(analizador) or self.ExisteEnTerminales(analizador):
                    '''Seguimos'''
                else:
                    print('La transicion se ingreso de manera incorrecta')
                    return False
            print('La transicion fue ingresada correctamente')
        else:
            print('La transicion se ingreso de manera incorrecta')
            return False
        if len(produccion) == 2:
            if self.ExisteEnTerminales(produccion[0]) and self.ExisteNoTerminal(produccion[1]):
                '''Nada'''
            else:
                self.EsLibreDeContexto = True
        elif len(produccion) == 1 and self.ExisteEnTerminales(produccion[0]):
            '''Nada'''
        else:
            self.EsLibreDeContexto = True

        for noterminal in self.noterminales:
            if noterminal.estado == separador[0]:
                noterminal.transiciones.append(separador[1])
                print('Transicion agregada exitosamente')

    def AutomataEquivalente(self):
        alfabeto = self.cadenaterminales
        simbolospila = self.cadenaterminales + ',' + self.cadenanotermianles + ',#'
        file = open('automataPila.dot', "w")
        file.write("digraph grafica{" + os.linesep)
        file.write("rankdir=LR;" + os.linesep)
        file.write("rank=same;" + os.linesep)
        file.write("f [shape = doublecircle];" + os.linesep)
        file.write("q [margin = 1];" + os.linesep)
        file.write('"Inicio" [shape = plaintext];' + os.linesep)
        file.write('"Inicio" -> i;' + os.linesep)
        file.write('i -> p [label = "$,$;#"]' + os.linesep)
        file.write('p -> q [label = "$,$;' + self.inicial + '"]' + os.linesep)
        file.write('q -> f [label = "$,#;$"]' + os.linesep)
        for estado in self.noterminales:
            for transi in estado.transiciones:
                transicion = '"$,' + estado.estado + ';' + transi.replace(' ', '') + '"'
                file.write(transicion + ' [shape=none];')
                file.write('q -> ' + transicion + ' [dir = none]' + os.linesep)
                file.write(transicion + '-> q' + os.linesep)
        for terminal in self.terminales:
            transicion = '"' + terminal + ',' + terminal + '; $"'
            file.write(transicion + ' [shape=none];')
            file.write('q -> ' + transicion + ' [dir = none]' + os.linesep)
            file.write(transicion + '-> q' + os.linesep)
        file.write(os.linesep)
        file.write('tabla[shape=plaintext,fontsize=12, label=<')
        file.write('<TABLE BORDER="0">')
        file.write('<TR><TD>Alfabeto: { ' + alfabeto + ' }</TD></TR>')
        file.write('<TR><TD>Alfabeto de pila: { ' + simbolospila + ' }</TD></TR>')
        file.write('<TR><TD>Estados: { i,p,q,f }</TD></TR>')
        file.write('<TR><TD>Estado inicial: { i }</TD></TR>')
        file.write('<TR><TD>Estado de aceptacion: { f }</TD></TR>')
        file.write('</TABLE>')
        file.write('>];')

        file.write(os.linesep)
        file.write('Titulo [shape=plaintext,fontsize=20, label="Nombre: Automata de Pila: ' + self.nombre + '"]')
        file.write('}')
        file.close()
        subprocess.call('dot -Tpdf automataPila.dot -o automataPila.pdf')
        os.system("dot -Tpng -o graph-g.png automataPila.dot")
        os.system('AP.html')
        fileAP = open('automata.ap', "w")
        fileAP.write(str(self.nombre) + '\n')
        fileAP.write(alfabeto + '\n')
        fileAP.write(alfabeto + ',#' + '\n')
        fileAP.write('I,P,Q,F' + '\n')
        fileAP.write('I' + '\n')
        fileAP.write('F' + '\n')
        fileAP.write('P,$,$;Q,#' + '\n')
        fileAP.write('I,' + self.inicial + ',$;P,' + self.inicial + '\n')
        for estado in self.noterminales:
            for transi in estado.transiciones:
                transicion = '$,' + estado.estado + ';' + transi.replace(' ', '')
                fileAP.write(
                    'P,' + transicion[0] + transicion[1] + transicion[2] + transicion[3] + 'Q,' + transicion[4] + '\n')

        fileAP.write('Q,$,#;F,$' + '\n')
        fileAP.write('*')


class transiciones(object):
    def __init__(self, lee, extrae, destino, inserta):
        self.simboloLee = lee
        self.simboloExtrae = extrae
        self.destino = destino
        self.simboloInserta = inserta

    def Extrae(self):
        return self.simboloExtrae

    def Inserta(self):
        return self.simboloInserta

    def ImprimirTransicion(self):
        trans = ',' + self.simboloLee + ',' + self.simboloExtrae + ';' + self.destino + ',' + self.simboloInserta
        return trans


class NoTerminal(object):
    def __init__(self, nombre):
        self.estado = nombre
        self.transiciones = []
        self.consulta = 0

    def DevolverUnaTransicion(self):
        consultaActual = self.consulta
        self.consulta += 1
        if self.consulta > (len(self.transiciones) - 1):
            self.consulta = 0
        return self.transiciones[consultaActual]


class ListaGramatica(object):
        def __init__(self):
            self.gramatica = []
            self.error = []

        def ExisteGramatica(self, AFD):
            for afd in self.gramatica:
                if afd.nombre == AFD:
                    print('Existe una gramatica con ese nombre')
                    return True
            return False

        def EstaVacio(self):
            if len(self.gramatica) == 0:
                return True
            else:
                return False

        def EliminarAFD(self, nombre):
            for afd in self.gramatica:
                if afd.nombre == nombre:
                    self.gramatica.remove(afd)
                    print('Gramatica eliminada')

        def Agregar(self, AFD):
            if not self.ExisteGramatica(AFD.nombre):
                self.gramatica.append(AFD)
            else:
                '''Ya se manda mensaje desde el otro metodo'''

        def MostrarGramaticas(self):
            for afd in self.gramatica:
                print(afd.nombre)

        def CargarGramaticas(self, ruta):
            global EnCreacion
            automatas = open(ruta, 'r')
            noL = 0  # Numero de linea
            for linea in automatas.readlines():
                noL += 1
                linea = linea.replace('\n', '')

                if noL == 1:  # Ingresando titulo al automata
                    if not self.ExisteGramatica(linea):
                        EnCreacion = Gramatica(linea)
                        print(EnCreacion.nombre, 'creandose')
                    else:
                        self.EliminarAFD(linea)
                        EnCreacion = Gramatica(linea)
                        print(EnCreacion.nombre, 'creandose')
                elif noL == 2:  # Ingresando alfabeto del automata
                    contador = 0
                    for d in linea.split(';'):
                        print(d)
                        if contador == 0:
                            for alfa in d.split(','):
                                EnCreacion.AgregarEstados(alfa)
                                EnCreacion.cadenanotermianles = d
                        elif contador == 1:
                            for alfa in d.split(','):
                                EnCreacion.IngresarAlfabeto(alfa)
                            EnCreacion.cadenaterminales = d
                        elif contador == 2:
                            EnCreacion.inicial = d
                        contador += 1
                elif linea == '*':
                    print(' ')
                    if EnCreacion.EsLibreDeContexto:
                        self.gramatica.append(EnCreacion)
                        print('Automata agregado correctamente')
                        self.ImprimirAutomata(EnCreacion)

                    else:
                        print('No es una gramatica libre del contexto, no sera agregada')
                        self.error.append(['Nombre de la gramatica:  ' + str(EnCreacion.nombre),
                                           'error, no se cargo no es una gramatica de tipo 2 o Libre del contexto'])
                        ListaGramatica.reporteError(self)
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

        def DevolverADP(self, nombre):
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
