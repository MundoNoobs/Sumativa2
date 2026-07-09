def input_non_empty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print('No puede quedar vacío.')

try:
    from services import reportes_expresiones as reportes
except Exception as e:
    reportes = None
    _import_error = e

def main():
    print('CRUD MongoDB - PyMongo - Evaluación')
    if reportes is None:
        print('Advertencia: servicio de reportes no disponible. Ver .env o MONGO_URI.')
    while True:
        try:
            print('\n--- Menú Principal ---')
            print('1 Insertar alumno (insert_one)')
            print('2 Insertar varios alumnos (insert_many)')
            print('3 Buscar alumnos')
            print('4 Actualizar alumno (update_one)')
            print('5 Actualizar varios (update_many)')
            print('6 Eliminar alumno (delete_one)')
            print('7 Eliminar varios alumnos (delete_many)')
            print('8 Asignaturas')
            print('9 Notas (subdocumentos: $push/$pull)')
            print('r Reconectar BD')
            print('0 Salir')
            opc = input_non_empty('Opción: ')
            if opc == '1':
                if reportes is not None:
                    reportes.insertar_alumno()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '2':
                if reportes is not None:
                    reportes.insertar_varios_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '3':
                if reportes is not None:
                    reportes.buscar_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '4':
                if reportes is not None:
                    reportes.actualizar_alumno()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '5':
                if reportes is not None:
                    reportes.actualizar_varios_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '6':
                if reportes is not None:
                    reportes.eliminar_alumno()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '7':
                if reportes is not None:
                    reportes.eliminar_varios_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '8':
                if reportes is not None:
                    reportes.menu_asignaturas()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '9':
                if reportes is not None:
                    reportes.menu_notas()
                else:
                    print('Sin servicio de reportes.')
            elif opc.lower() == 'r':
                if reportes is not None:
                    try:
                        reportes.reconnect()
                        print('Reconectado a MongoDB.')
                    except Exception as e:
                        print('Error al reconectar:', e)
                else:
                    print('Servicio no disponible. Revise MONGO_URI.')
            elif opc == '0':
                print('Saliendo...')
                break
            else:
                print('Opción no válida')
        except KeyboardInterrupt:
            print('\nInterrupción por teclado. Use 0 para salir.')
        except Exception as e:
            print('Error inesperado en el menú:', e)

if __name__ == '__main__':
    main()
