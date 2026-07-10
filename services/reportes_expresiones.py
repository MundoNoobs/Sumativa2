import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError('MONGO_URI environment variable is required')
MONGO_DB = os.getenv('MONGO_DB', 'evaluacion2')
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

def get_db():
    return client[MONGO_DB]


def generar_reporte(cursor, title):
    header = f'=== {title} ==='
    print('\n' + header)
    print('=' * len(header))
    i = 0
    for doc in cursor:
        i += 1
        print(f'\n--- Documento {i} ---')
        print('Nombre:', doc.get('nombre', 'N/A'))
        print('RUT:', doc.get('rut', 'N/A'))
        print('Email:', doc.get('email', 'N/A'))
        print('Edad:', doc.get('edad', 'N/A'))
        print('Telefono:', doc.get('telefono', 'N/A'))
        asignaturas = doc.get('Asignaturas', [])
        if not asignaturas:
            print('Asignaturas promedio:', 'N/A')
        else:
            total = 0.0
            cnt = 0
            for a in asignaturas:
                notas_list = a.get('Notas', [])
                if isinstance(notas_list, list):
                    for n in notas_list:
                        try:
                            total += float(n)
                            cnt += 1
                        except Exception:
                            continue
            promedio = round(total / cnt, 2) if cnt > 0 else None
            print('Asignaturas promedio:', promedio if promedio is not None else 'N/A')


def reconnect():
    global client, MONGO_URI, MONGO_DB
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise RuntimeError('MONGO_URI environment variable is required')
    MONGO_DB = os.getenv('MONGO_DB', 'evaluacion2')
    try:
        client.close()
    except Exception:
        pass
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)


def validar_rut(rut):
    rut = rut.replace('.', '').replace(' ', '').upper()
    if not re.match(r'^\d{1,8}-[\dK]$', rut):
        return False
    num, dv = rut.split('-')
    try:
        reversed_digits = map(int, reversed(num))
    except ValueError:
        return False
    seq = [2,3,4,5,6,7]
    s = 0
    i = 0
    for d in reversed_digits:
        s += d * seq[i]
        i = (i + 1) % len(seq)
    res = 11 - (s % 11)
    if res == 11:
        dv_expected = '0'
    elif res == 10:
        dv_expected = 'K'
    else:
        dv_expected = str(res)
    return dv == dv_expected


def validar_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None


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


def insertar_alumno():
    try:
        db = get_db()
        nombre = input_non_empty('Nombre: ')
        rut = input_non_empty('RUT (ej: 12345678-5 o 12.345.678-5): ')
        if not validar_rut(rut):
            print('RUT inválido. No se inserta.')
            return
        email = input_non_empty('Email: ')
        if not validar_email(email):
            print('Email inválido. No se inserta.')
            return
        edad = input_int('Edad: ')
        telefono = input_non_empty('Teléfono (solo dígitos): ')
        if not telefono.isdigit():
            print('Teléfono inválido. No se inserta.')
            return
        alumno = {
            'nombre': nombre,
            'rut': rut.replace('.', ''),
            'email': email,
            'edad': edad,
            'telefono': telefono,
            'Asignaturas': []
        }
        res = db.alumnos.insert_one(alumno)
        print('Alumno insertado _id:', res.inserted_id)
    except Exception as e:
        print('Error al insertar alumno:', e)


def insertar_varios_alumnos():
    try:
        db = get_db()
        n = input_int('¿Cuántos alumnos desea insertar? ')
        if n <= 0:
            print('Cantidad inválida. Cancelado.')
            return
        docs = []
        for i in range(1, n + 1):
            print(f'\nIngresando alumno {i} de {n}')
            nombre = input_non_empty('Nombre: ')
            rut = input_non_empty('RUT (ej: 12345678-5 o 12.345.678-5): ')
            while not validar_rut(rut):
                print('RUT inválido. Intente nuevamente.')
                rut = input_non_empty('RUT (ej: 12345678-5 o 12.345.678-5): ')
            email = input_non_empty('Email: ')
            while not validar_email(email):
                print('Email inválido. Intente nuevamente.')
                email = input_non_empty('Email: ')
            edad = input_int('Edad: ')
            telefono = input_non_empty('Teléfono (solo dígitos): ')
            while not telefono.isdigit():
                print('Teléfono inválido. Intente nuevamente.')
                telefono = input_non_empty('Teléfono (solo dígitos): ')
            alumno = {
                'nombre': nombre,
                'rut': rut.replace('.', ''),
                'email': email,
                'edad': edad,
                'telefono': telefono,
                'Asignaturas': []
            }
            docs.append(alumno)
        confirmar = input_non_empty(f'Insertar {len(docs)} alumnos? s/n: ')
        if confirmar.lower().startswith('s'):
            res = db.alumnos.insert_many(docs)
            print('Insert_many IDs:', res.inserted_ids)
        else:
            print('Operación cancelada.')
    except Exception as e:
        print('Error insertar_varios_alumnos:', e)


def buscar_alumnos():
    try:
        db = get_db()
        print('Buscar por: 1)rut 2)nombre 3)todos')
        op = input_non_empty('Opción: ')
        q = {}
        if op == '1':
            rut = input_non_empty('RUT: ')
            q['rut'] = rut.replace('.', '')
        elif op == '2':
            nombre = input_non_empty('Nombre (o parte): ')
            q['nombre'] = {'$regex': nombre, '$options': 'i'}
        else:
            q = {}
        proy = {'nombre': 1, 'rut': 1, 'email': 1, 'edad': 1, 'telefono': 1, 'Asignaturas': 1}
        cursor = db.alumnos.find(q, proy)
        generar_reporte(cursor, 'Resultados de búsqueda')
    except Exception as e:
        print('Error en búsqueda:', e)


def actualizar_alumno():
    try:
        db = get_db()
        rut = input_non_empty('RUT del alumno a actualizar: ')
        campo = input_non_empty('Campo a actualizar (nombre,email,edad,telefono): ')
        valor = input_non_empty('Nuevo valor: ')
        if campo == 'email' and not validar_email(valor):
            print('Email inválido. Abortando.')
            return
        if campo == 'edad':
            if not valor.isdigit():
                print('Edad inválida. Abortando.'); return
            valor = int(valor)
        if campo == 'telefono' and not valor.isdigit():
            print('Teléfono inválido. Abortando.'); return
        res = db.alumnos.update_one({'rut': rut.replace('.', '')}, {'$set': {campo: valor}})
        print('Matched:', res.matched_count, 'Modified:', res.modified_count)
    except Exception as e:
        print('Error al actualizar:', e)


def actualizar_varios_alumnos():
    try:
        db = get_db()
        n = input_int('¿Cuántos alumnos desea actualizar? ')
        if n <= 0:
            print('Cantidad inválida. Cancelado.'); return
        updates = []
        for i in range(1, n + 1):
            print(f'\nAlumno {i} de {n}:')
            rut = input_non_empty('RUT del alumno (ej: 12345678-5): ')
            while not validar_rut(rut):
                print('RUT inválido. Intente nuevamente.')
                rut = input_non_empty('RUT del alumno (ej: 12345678-5): ')
            rut_db = rut.replace('.', '')
            campo = input_non_empty('Campo a actualizar (nombre,email,edad,telefono): ')
            while campo not in ('nombre','email','edad','telefono'):
                print('Campo inválido. Elija entre nombre,email,edad,telefono.')
                campo = input_non_empty('Campo a actualizar (nombre,email,edad,telefono): ')
            if campo == 'email':
                valor = input_non_empty('Nuevo email: ')
                while not validar_email(valor):
                    print('Email inválido. Intente nuevamente.')
                    valor = input_non_empty('Nuevo email: ')
            elif campo == 'edad':
                valor = input_int('Nueva edad: ')
            elif campo == 'telefono':
                valor = input_non_empty('Nuevo teléfono (solo dígitos): ')
                while not valor.isdigit():
                    print('Teléfono inválido. Intente nuevamente.')
                    valor = input_non_empty('Nuevo teléfono (solo dígitos): ')
            else:
                valor = input_non_empty('Nuevo valor para nombre: ')
            updates.append({'rut': rut_db, 'campo': campo, 'valor': valor})
        print('\nResumen de actualizaciones:')
        for u in updates:
            print('-', u['rut'], u['campo'], u['valor'])
        confirmar = input_non_empty('Confirmar ejecución? s/n: ')
        if confirmar.lower().startswith('s'):
            for u in updates:
                res = db.alumnos.update_one({'rut': u['rut']}, {'$set': {u['campo']: u['valor']}})
                print(f'RUT {u["rut"]}: matched {res.matched_count} modified {res.modified_count}')
        else:
            print('Operación cancelada.')
    except Exception as e:
        print('Error actualizar_varios_alumnos:', e)


def eliminar_alumno():
    try:
        db = get_db()
        rut = input_non_empty('RUT a eliminar: ')
        res = db.alumnos.delete_one({'rut': rut.replace('.', '')})
        print('Eliminados (delete_one):', res.deleted_count)
    except Exception as e:
        print('Error delete_one:', e)


def eliminar_varios_alumnos():
    try:
        db = get_db()
        entrada = input_non_empty('Ingrese RUTs separados por coma para eliminar: ')
        ruts = [r.strip().replace('.', '') for r in entrada.split(',') if r.strip()]
        if not ruts:
            print('No se proporcionaron RUTs. Operación cancelada.'); return
        print('RUTs a eliminar:', ', '.join(ruts))
        confirmar = input_non_empty('Confirmar eliminación? s/n: ')
        if confirmar.lower().startswith('s'):
            res = db.alumnos.delete_many({'rut': {'$in': ruts}})
            print('Eliminados (delete_many):', res.deleted_count)
        else:
            print('Operación cancelada.')
    except Exception as e:
        print('Error eliminar_varios_alumnos:', e)


def insertar_asignatura():
    try:
        db = get_db()
        codigo = input_non_empty('Código materia: ')
        nombre = input_non_empty('Nombre materia: ')
        doc = {'codigo': codigo, 'nombre': nombre}
        res = db.asignaturas.insert_one(doc)
        print('Asignatura insertada _id:', res.inserted_id)
    except Exception as e:
        print('Error asignatura:', e)


def insertar_varias_asignaturas():
    try:
        db = get_db()
        n = input_int('¿Cuántas asignaturas desea insertar? ')
        if n <= 0:
            print('Cantidad inválida. Cancelado.'); return
        docs = []
        for i in range(1, n + 1):
            print(f'\nIngresando asignatura {i} de {n}')
            codigo = input_non_empty('Código materia: ')
            nombre = input_non_empty('Nombre materia: ')
            docs.append({'codigo': codigo, 'nombre': nombre})
        confirmar = input_non_empty(f'Insertar {len(docs)} asignaturas? s/n: ')
        if confirmar.lower().startswith('s'):
            res = db.asignaturas.insert_many(docs)
            print('Asig IDs:', res.inserted_ids)
        else:
            print('Operación cancelada.')
    except Exception as e:
        print('Error insertar_varias_asignaturas:', e)


def listar_asignaturas():
    try:
        db = get_db()
        proy = {'codigo': 1, 'nombre': 1}
        for s in db.asignaturas.find({}, proy):
            print(s)
    except Exception as e:
        print('Error listar asignaturas:', e)


def agregar_nota():
    try:
        db = get_db()
        rut = input_non_empty('RUT: ')
        materia = input_non_empty('Nombre materia: ')
        valor = input_non_empty('Valor nota (número): ')
        try:
            nota_val = float(valor)
        except:
            print('Nota debe ser numérica.'); return
        rut_db = rut.replace('.', '')
        res = db.alumnos.update_one({'rut': rut_db, 'Asignaturas.Nombre': materia}, {'$push': {'Asignaturas.$.Notas': nota_val}})
        if res.matched_count == 0:
            res2 = db.alumnos.update_one({'rut': rut_db}, {'$push': {'Asignaturas': {'Nombre': materia, 'Notas': [nota_val]}}})
            print('Asignatura agregada con nota, matched:', res2.matched_count, 'modified:', res2.modified_count)
        else:
            print('Nota agregada a asignatura existente, matched:', res.matched_count, 'modified:', res.modified_count)
    except Exception as e:
        print('Error agregar nota:', e)


def ver_notas():
    try:
        db = get_db()
        rut = input_non_empty('RUT: ')
        a = db.alumnos.find_one({'rut': rut.replace('.', '')}, {'Asignaturas': 1, 'nombre':1})
        if not a:
            print('Alumno no encontrado.')
            return
        print('Alumno:', a.get('nombre'))
        for s in a.get('Asignaturas', []):
            nombre = s.get('Nombre', 'N/A')
            notas = s.get('Notas', [])
            print('-', nombre, ':', notas)
    except Exception as e:
        print('Error ver notas:', e)


def modificar_nota():
    try:
        db = get_db()
        rut = input_non_empty('RUT: ')
        materia = input_non_empty('Código materia a modificar: ')
        nueva = input_non_empty('Nueva nota (número): ')
        try:
            nueva_val = float(nueva)
        except:
            print('Valor inválido.'); return
        rut_db = rut.replace('.', '')
        res = db.alumnos.update_one({'rut': rut_db, 'Asignaturas.Nombre': materia}, {'$set': {'Asignaturas.$.Notas.0': nueva_val}})
        print('Matched:', res.matched_count, 'Modified:', res.modified_count)
    except Exception as e:
        print('Error modificar nota:', e)


def eliminar_nota():
    try:
        db = get_db()
        rut = input_non_empty('RUT: ')
        materia = input_non_empty('Nombre materia a eliminar de las asignaturas: ')
        res = db.alumnos.update_one({'rut': rut.replace('.', '')}, {'$pull': {'Asignaturas': {'Nombre': materia}}})
        print('Asignaturas eliminadas (pull), modified_count:', res.modified_count)
    except Exception as e:
        print('Error eliminar nota:', e)


def menu_notas():
    while True:
        print('\n-- Menú Notas --')
        print('1 Agregar nota  2 Ver notas  3 Modificar nota  4 Eliminar nota  0 Volver')
        opc = input_non_empty('Opción: ')
        if opc == '1': agregar_nota()
        elif opc == '2': ver_notas()
        elif opc == '3': modificar_nota()
        elif opc == '4': eliminar_nota()
        elif opc == '0': break
        else: print('Opción inválida')


def menu_asignaturas():
    while True:
        print('\n-- Menú Asignaturas --')
        print('1 Insertar asignatura  2 Insertar varias (ejemplo)  3 Listar  0 Volver')
        opc = input_non_empty('Opción: ')
        if opc == '1': insertar_asignatura()
        elif opc == '2': insertar_varias_asignaturas()
        elif opc == '3': listar_asignaturas()
        elif opc == '0': break
        else: print('Opción inválida')


def alumnos_por_rango_edad(min_edad, max_edad):
    db = get_db()
    filtro = {}
    if min_edad > 0 and max_edad > 0:
        filtro = {'edad': {'$gte': min_edad, '$lte': max_edad}}
    elif min_edad > 0:
        filtro = {'edad': {'$gte': min_edad}}
    elif max_edad > 0:
        filtro = {'edad': {'$lte': max_edad}}
    proy = {'nombre': 1, 'rut': 1, 'email': 1, 'edad': 1, 'telefono': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos con edad entre {min_edad} y {max_edad}')



def alumno_por_rut(rut):
    db = get_db()
    filtro = {'rut': rut.replace('.', '')}
    proy = {'nombre': 1, 'rut': 1, 'email': 1, 'edad': 1, 'telefono': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumno con RUT {rut}')


def alumnos_rut_distinto(rut):
    db = get_db()
    filtro = {'rut': {'$ne': rut}}
    proy = {'nombre': 1, 'rut': 1, 'email': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos cuyo RUT es distinto a {rut}')





def alumnos_nombre_empieza_con(texto):
    db = get_db()
    pattern = f'^{re.escape(texto)}'
    filtro = {'nombre': {'$regex': pattern, '$options': 'i'}}
    proy = {'nombre': 1, 'rut': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos cuyo nombre empieza con "{texto}"')


def alumnos_nombre_termina_con(texto):
    db = get_db()
    pattern = f'{re.escape(texto)}$'
    filtro = {'nombre': {'$regex': pattern, '$options': 'i'}}
    proy = {'nombre': 1, 'rut': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos cuyo nombre termina con "{texto}"')


def alumnos_nombre_no_coincide_con(texto):
    db = get_db()
    filtro = {'nombre': {'$not': {'$regex': texto, '$options': 'i'}}}
    proy = {'nombre': 1, 'rut': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos cuyo nombre no coincide con "{texto}"')


def alumnos_por_asignatura_nombre(nombre_parcial):
    db = get_db()
    filtro = {'Asignaturas.Nombre': {'$regex': nombre_parcial, '$options': 'i'}}
    proy = {'nombre': 1, 'rut': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos con asignatura cuyo nombre contiene "{nombre_parcial}"')


def alumnos_con_todas_asignaturas(codigos):
    db = get_db()
    filtro = {'Asignaturas': {'$all': [{'$elemMatch': {'Nombre': c}} for c in codigos]}}
    proy = {'nombre': 1, 'rut': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos que tienen todas las asignaturas: {", ".join(codigos)}')

def alumnos_con_nota_en_materia(materia, nota_minima):
    db = get_db()
    filtro = {'Asignaturas': {'$elemMatch': {'Nombre': {'$regex': materia, '$options': 'i'}, 'Notas': {'$elemMatch': {'$gt': nota_minima}}}}}
    proy = {'nombre': 1, 'rut': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos con nota mayor a {nota_minima} en materia que contiene "{materia}"')


def alumnos_con_campo_existente(campo):
    db = get_db()
    filtro = {campo: {'$exists': True}}
    proy = {'nombre': 1, 'rut': 1, campo: 1}
    cursor = db.alumnos.find(filtro, proy)
    generar_reporte(cursor, f'Alumnos con campo existente "{campo}"')
