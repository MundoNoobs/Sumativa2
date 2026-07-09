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
            print('3. Buscar alumnos')
            print('4. Actualizar datos de un alumno')
            print('5. Actualizar varios alumnos')
            print('6. Eliminar alumno')
            print('7. Eliminar varios alumnos')
            print('8. Gestión de asignaturas')
            print('9. Gestionar calificaciones de alumnos')
            print('10. Buscar alumnos por rango de edad')
            print('11. Buscar alumnos por nombre')
            print('12. Buscar alumno por RUT')
            print('13. Listar alumnos con promedio superior a valor')
            print('14. Buscar asignatura por código')
            print('15. Buscar alumnos por edad o nombre')
            print('16. Buscar alumnos por rango de edad y correo')
            print('17. Buscar alumnos excluyendo texto en nombre')
            print('18. Buscar alumnos por lista de RUTs')
            print('19. Listar asignaturas excluyendo códigos')
            print('20. Buscar alumnos con RUT distinto')
            print('21. Buscar alumnos con edad mayor que')
            print('22. Buscar alumnos con edad menor que')
            print('23. Buscar alumnos cuyo nombre comienza con texto')
            print('24. Buscar alumnos cuyo nombre termina con texto')
            print('25. Buscar alumnos cuyo nombre no coincide con texto')
            print('26. Buscar alumnos por nombre de asignatura')
            print('27. Buscar alumnos que tienen todas las asignaturas dadas')
            print('28. Buscar alumnos con nota mínima en materia')
            print('29. Buscar alumnos que tienen un campo específico')
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
                    reportes.alumnos_por_rango_edad(min_e, max_e)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '11':
                if reportes is not None:
                    name = input_non_empty('Texto nombre (parte): ')
                    reportes.alumnos_por_nombre_parcial(name)
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
                    code = input_non_empty('Código asignatura: ')
                    reportes.asignaturas_por_codigo(code)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '15':
                if reportes is not None:
                    edad = input_int('Edad umbral: ')
                    txt = input_non_empty('Texto nombre parcial: ')
                    reportes.alumnos_edad_o_nombre(edad, txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '16':
                if reportes is not None:
                    min_e = input_int('Edad mínima: ')
                    max_e = input_int('Edad máxima: ')
                    emailp = input_non_empty('Texto a buscar en email: ')
                    reportes.alumnos_edad_rango_con_email(min_e, max_e, emailp)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '17':
                if reportes is not None:
                    txt = input_non_empty('Texto que NO debe aparecer en nombre: ')
                    reportes.alumnos_nombre_excluye(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '18':
                if reportes is not None:
                    csv = input_non_empty('RUTs separados por coma: ')
                    ruts = [r.strip().replace('.', '') for r in csv.split(',') if r.strip()]
                    reportes.alumnos_por_ruts(ruts)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '19':
                if reportes is not None:
                    csv = input_non_empty('Códigos asignatura a excluir, separados por coma: ')
                    codes = [c.strip() for c in csv.split(',') if c.strip()]
                    reportes.asignaturas_excluyendo_codigos(codes)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '20':
                if reportes is not None:
                    rut = input_non_empty('RUT a excluir: ')
                    reportes.alumnos_rut_distinto(rut.replace('.', ''))
                else:
                    print('Sin servicio de reportes.')
            elif opc == '21':
                if reportes is not None:
                    edad = input_int('Edad (mayor que): ')
                    reportes.alumnos_edad_mayor_que(edad)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '22':
                if reportes is not None:
                    edad = input_int('Edad (menor que): ')
                    reportes.alumnos_edad_menor_que(edad)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '23':
                if reportes is not None:
                    txt = input_non_empty('Texto que debe comenzar el nombre: ')
                    reportes.alumnos_nombre_empieza_con(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '24':
                if reportes is not None:
                    txt = input_non_empty('Texto con el que debe terminar el nombre: ')
                    reportes.alumnos_nombre_termina_con(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '25':
                if reportes is not None:
                    txt = input_non_empty('Texto a excluir (NOT LIKE): ')
                    reportes.alumnos_nombre_no_coincide_con(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '26':
                if reportes is not None:
                    txt = input_non_empty('Texto parcial en nombre de asignatura: ')
                    reportes.alumnos_por_asignatura_nombre(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '27':
                if reportes is not None:
                    csv = input_non_empty('Códigos de asignaturas separados por coma (debe tener todas): ')
                    codes = [c.strip() for c in csv.split(',') if c.strip()]
                    reportes.alumnos_con_todas_asignaturas(codes)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '28':
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
            elif opc == '29':
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
