from Analizador import *
import time

listaglc = ListGram()

def menu():
    print('\n')
    print('\n')
    print('-------------------- BIENVENIDO --------------------')
    print("1. Cargar archivo\n"
          "2. Mostrar información general de la gramática\n"
          "3. Mostrar autómata de pila equivalente\n"
          "4. Reporte recorrido\n"
          "5. Reporte en tabla\n"
          "6. Salir\n")
    valor = input(">>>Por favor seleccione una opción: ")
    return valor


def flowWork():
    print("                       Proyecto 2 - LFP                 ")
    print(" -------------------------------------------------------- ")
    print(" |    Nombre: Fabio Josué Hernández Martinez            |")
    print(" |    Carnet: 201801005                                 |")
    print(" |    Correo: fabioher2901@gmail.com                    |")
    print(" |    Curso: Lenguajes Formales y de Programación B-    |")
    print(" -------------------------------------------------------- ")

    num = 5
    for i in range(num):
        print('                      * ' + str(num) + ' segundos *                      ')
        time.sleep(1)
        num -= 1


flowWork()
bandera = True

while bandera:
    opcion = int(menu())
    if opcion == 1:
        fichero = FileDialog.askopenfilename(title="Seleccione un archivo")
        print('*Ruta: ' + fichero + '*')
        listaglc.CargarGramaticas(fichero)
    elif opcion == 2:
        listaglc.MostrarGramaticas()
        eleccion = input('>>>Por favor ingrese el nombre de la gramatica que desea visualizar:')
        automata = listaglc.DevolverAutomata(eleccion)
        try:
            listaglc.ImprimirAutomata(automata)
            input('>>>Presione Enter para continuar')
            os.system('cls')
        except:
            print('No eligio un automata correcto')
    elif opcion == 3:
        print('Listando gramaticas disponibles: ')
        listaglc.MostrarGramaticas()
        eleccion = input('>>>Ingrese el nombre de la gramatica de la que desea el AP: ')
        input('>>>Presione Enter para continuar')
        automata = listaglc.DevolverAutomata(eleccion)
        automata.AutomataEquivalente()
    elif opcion == 4:
        print("Arriba la esperanza abuelita")
    elif opcion == 5:
        print("Sale lol? xd")
    elif opcion == 6:
        bandera = False
    else:
        print("Opción invalida, por favor seleccione una opción valida")
