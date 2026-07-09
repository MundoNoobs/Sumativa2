def input_non_empty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print('No puede quedar vacío.')


def input_int(prompt):
    while True:
        v = input_non_empty(prompt)
        if v.isdigit():
            return int(v)
        print('Debe ingresar un número válido.')

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
            print('10 Consulta: alumnos por rango de edad')
            print('11 Consulta: alumnos por nombre parcial')
            print('12 Consulta: alumno por RUT')
            print('13 Consulta: alumnos con promedio mayor que')
            print('14 Consulta: asignaturas por código')
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
            elif opc == '10':
                if reportes is not None:
                    min_e = input_int('Edad mínima: ')
                    max_e = input_int('Edad máxima: ')
                    reportes.consulta_alumnos_por_rango_edad(min_e, max_e)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '11':
                if reportes is not None:
                    name = input_non_empty('Texto nombre (parte): ')
                    reportes.consulta_alumnos_por_nombre_parcial(name)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '12':
                if reportes is not None:
                    rut = input_non_empty('RUT: ')
                    reportes.consulta_alumno_por_rut(rut)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '13':
                if reportes is not None:
                    thr = input_non_empty('Umbral promedio (ej 4.0): ')
                    try:
                        thr_val = float(thr)
                    except Exception:
                        print('Valor inválido.'); continue
                    reportes.consulta_alumnos_con_promedio_mayor(thr_val)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '14':
                if reportes is not None:
                    code = input_non_empty('Código asignatura: ')
                    reportes.consulta_listar_asignaturas_por_codigo(code)
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
