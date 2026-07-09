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
            print('15 Consulta OR: edad > X OR nombre contiene Y')
            print('16 Consulta AND: edad entre X-Y y email contiene Z')
            print('17 Consulta NOT: nombre NO contiene X')
            print('18 Consulta IN: alumnos por lista de RUTs')
            print('19 Consulta NIN: asignaturas cuyo código NO está en lista')
            print('20 Consulta NE: alumnos con RUT distinto a X')
            print('21 Consulta GT: edad mayor que X')
            print('22 Consulta LT: edad menor que X')
            print('23 Consulta REGEX ^ : nombre empieza con')
            print('24 Consulta REGEX $ : nombre termina con')
            print('25 Consulta NOT LIKE (regex negado)')
            print('26 Consulta embedded: Asignaturas.nombre contiene X')
            print('27 Consulta array $all: alumnos con todas las asignaturas dadas')
            print('28 Consulta $elemMatch: notas con materia X y nota > Y')
            print('29 Consulta $exists: campo existe')
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
            elif opc == '15':
                if reportes is not None:
                    edad = input_int('Edad umbral: ')
                    txt = input_non_empty('Texto nombre parcial: ')
                    reportes.consulta_logica_or(edad, txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '16':
                if reportes is not None:
                    min_e = input_int('Edad mínima: ')
                    max_e = input_int('Edad máxima: ')
                    emailp = input_non_empty('Texto a buscar en email: ')
                    reportes.consulta_logica_and(min_e, max_e, emailp)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '17':
                if reportes is not None:
                    txt = input_non_empty('Texto que NO debe aparecer en nombre: ')
                    reportes.consulta_logica_not_nombre(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '18':
                if reportes is not None:
                    csv = input_non_empty('RUTs separados por coma: ')
                    ruts = [r.strip().replace('.', '') for r in csv.split(',') if r.strip()]
                    reportes.consulta_in_ruts(ruts)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '19':
                if reportes is not None:
                    csv = input_non_empty('Códigos asignatura a excluir, separados por coma: ')
                    codes = [c.strip() for c in csv.split(',') if c.strip()]
                    reportes.consulta_nin_codigos(codes)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '20':
                if reportes is not None:
                    rut = input_non_empty('RUT a excluir: ')
                    reportes.consulta_ne_rut(rut.replace('.', ''))
                else:
                    print('Sin servicio de reportes.')
            elif opc == '21':
                if reportes is not None:
                    edad = input_int('Edad (GT): ')
                    reportes.consulta_edad_gt(edad)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '22':
                if reportes is not None:
                    edad = input_int('Edad (LT): ')
                    reportes.consulta_edad_lt(edad)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '23':
                if reportes is not None:
                    txt = input_non_empty('Texto que debe comenzar el nombre: ')
                    reportes.consulta_regex_empieza(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '24':
                if reportes is not None:
                    txt = input_non_empty('Texto con el que debe terminar el nombre: ')
                    reportes.consulta_regex_termina(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '25':
                if reportes is not None:
                    txt = input_non_empty('Texto a excluir (NOT LIKE): ')
                    reportes.consulta_regex_not_like(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '26':
                if reportes is not None:
                    txt = input_non_empty('Texto parcial en nombre de asignatura: ')
                    reportes.consulta_embedded_asignatura_nombre(txt)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '27':
                if reportes is not None:
                    csv = input_non_empty('Códigos de asignaturas separados por coma (debe tener todas): ')
                    codes = [c.strip() for c in csv.split(',') if c.strip()]
                    reportes.consulta_array_all_asignaturas(codes)
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
                    reportes.consulta_elemMatch_notas(mat, valf)
                else:
                    print('Sin servicio de reportes.')
            elif opc == '29':
                if reportes is not None:
                    campo = input_non_empty('Nombre del campo a comprobar existencia: ')
                    reportes.consulta_exists_field(campo)
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
