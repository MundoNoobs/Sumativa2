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
    print('Sistema de Gestión Académica - Menú Principal')
    if reportes is None:
        print('Advertencia: el servicio de reportes no está disponible. Revise el archivo .env')
    while True:
        try:
            print('\n--- Menú Principal ---')
            print('1. Agregar nuevo alumno')
            print('2. Agregar varios alumnos')
            print('3. Buscar / filtrar alumnos (básico)')
            print('4. Búsqueda avanzada de texto')
            print('5. Actualizar datos de un alumno')
            print('6. Actualizar varios alumnos')
            print('7. Eliminar alumno')
            print('8. Eliminar varios alumnos')
            print('9. Gestión de asignaturas')
            print('10. Gestionar calificaciones de alumnos')
            print('11. Buscar alumnos por rango de edad')
            print('12. Buscar alumno por RUT')
            print('13. Listar alumnos con promedio superior a valor')
            print('14. Buscar alumnos por nombre de asignatura')
            print('15. Buscar alumnos que tienen todas las asignaturas dadas')
            print('16. Buscar alumnos con nota mínima en materia')
            print('17. Buscar alumnos por lista de RUTs')
            print('18. Buscar alumnos que tienen un campo específico')
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
                    texto = input_non_empty('Texto a buscar en nombre: ')
                    print('Opciones: 1 Contiene  2 Empieza con  3 Termina con  4 No contiene')
                    tipo = input_non_empty('Opción (1-4): ')
                    if not tipo.isdigit() or int(tipo) not in (1,2,3,4):
                        print('Opción inválida de búsqueda avanzada.'); continue
                    reportes.buscar_alumnos_avanzado_texto(texto, int(tipo))
                else:
                    print('Sin servicio de reportes.')
            elif opc == '5':
                if reportes is not None:
                    reportes.actualizar_alumno()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '6':
                if reportes is not None:
                    reportes.actualizar_varios_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '7':
                if reportes is not None:
                    reportes.eliminar_alumno()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '8':
                if reportes is not None:
                    reportes.eliminar_varios_alumnos()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '9':
                if reportes is not None:
                    reportes.menu_asignaturas()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '10':
                if reportes is not None:
                    reportes.menu_notas()
                else:
                    print('Sin servicio de reportes.')
            elif opc == '11':
                if reportes is not None:
                    min_e = input_int('Edad mínima (0=sin mínimo): ')
                    max_e = input_int('Edad máxima (0=sin máximo): ')
                    reportes.alumnos_por_rango_edad(min_e, max_e)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '12':
                if reportes is not None:
                    rut = input_non_empty('RUT: ')
                    reportes.alumno_por_rut(rut)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '13':
                if reportes is not None:
                    thr = input_non_empty('Umbral promedio (ej 4.0): ')
                    try:
                        thr_val = float(thr)
                    except Exception:
                        print('Valor inválido.'); continue
                    reportes.alumnos_con_promedio_mayor(thr_val)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '14':
                if reportes is not None:
                    txt = input_non_empty('Texto parcial en nombre de asignatura: ')
                    reportes.alumnos_por_asignatura_nombre(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '15':
                if reportes is not None:
                    csv = input_non_empty('Nombres de asignaturas separados por coma (debe tener todas): ')
                    codes = [c.strip() for c in csv.split(',') if c.strip()]
                    reportes.alumnos_con_todas_asignaturas(codes)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '16':
                if reportes is not None:
                    mat = input_non_empty('Materia (parcial): ')
                    val = input_non_empty('Nota mínima (número): ')
                    try:
                        valf = float(val)
                    except Exception:
                        print('Valor inválido.'); continue
                    reportes.alumnos_con_nota_en_materia(mat, valf)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '17':
                if reportes is not None:
                    csv = input_non_empty('RUTs separados por coma: ')
                    ruts = [r.strip().replace('.', '') for r in csv.split(',') if r.strip()]
                    reportes.alumnos_por_ruts(ruts)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '18':
                if reportes is not None:
                    campo = input_non_empty('Nombre del campo a comprobar existencia: ')
                    reportes.alumnos_con_campo_existente(campo)
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
