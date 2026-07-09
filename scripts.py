"""Copias no interactivas de los scripts usados para añadir/editar/eliminar datos.
Funciones procedurales que llaman a la BD y realizan operaciones equivalentes
a las del menú interactivo en `bdd.py`.
"""
from bdd import connect_db, validar_rut, validar_email


def add_alumno(nombre, rut, email, edad, telefono, notas=None, test=False, db=None):
    """Inserta un alumno validando campos. Devuelve inserted_id o None."""
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD')
            return None
        if not nombre or not rut or not email:
            print('Campos obligatorios faltantes')
            return None
        if not validar_rut(rut):
            print('RUT inválido')
            return None
        if not validar_email(email):
            print('Email inválido')
            return None
        try:
            edad = int(edad)
        except:
            print('Edad inválida')
            return None
        if not str(telefono).isdigit():
            print('Teléfono inválido')
            return None
        doc = {
            'nombre': nombre,
            'rut': rut.replace('.', ''),
            'email': email,
            'edad': edad,
            'telefono': str(telefono),
            'notas': notas or [],
            'test': test
        }
        # insert_one(): inserta un documento
        res = db.alumnos.insert_one(doc)
        print('Alumno insertado _id:', res.inserted_id)
        return res.inserted_id
    except Exception as e:
        print('Error add_alumno:', e)
        return None


def add_alumnos_bulk(docs, db=None):
    """Inserta múltiples alumnos (lista de dicts)."""
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        # insert_many(): inserta múltiples documentos
        res = db.alumnos.insert_many(docs)
        print('Insert_many IDs:', res.inserted_ids)
        return res.inserted_ids
    except Exception as e:
        print('Error add_alumnos_bulk:', e)
        return None


def add_asignatura(codigo, nombre, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        doc = {'codigo': codigo, 'nombre': nombre}
        # insert_one() en colección asignaturas
        res = db.asignaturas.insert_one(doc)
        print('Asignatura insertada _id:', res.inserted_id)
        return res.inserted_id
    except Exception as e:
        print('Error add_asignatura:', e)
        return None


def add_asignaturas_bulk(lista, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        # insert_many() en asignaturas
        res = db.asignaturas.insert_many(lista)
        print('Asig IDs:', res.inserted_ids)
        return res.inserted_ids
    except Exception as e:
        print('Error add_asignaturas_bulk:', e)
        return None


def add_note_to_alumno(rut, materia, nota, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        nota_val = float(nota)
        nota_doc = {'materia': materia, 'nota': nota_val}
        # $push: agrega un elemento al array 'notas'
        res = db.alumnos.update_one({'rut': rut.replace('.', '')}, {'$push': {'notas': nota_doc}})
        print('Notas actualizadas, matched:', res.matched_count, 'modified:', res.modified_count)
        return res.modified_count
    except Exception as e:
        print('Error add_note_to_alumno:', e)
        return None


def modify_note_for_alumno(rut, materia, nueva_nota, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        nueva = float(nueva_nota)
        # update_one() con operador posicional $ para actualizar el primer elemento en el array que coincide
        res = db.alumnos.update_one({'rut': rut.replace('.', ''), 'notas.materia': materia}, {'$set': {'notas.$.nota': nueva}})
        print('Matched:', res.matched_count, 'Modified:', res.modified_count)
        return res.modified_count
    except Exception as e:
        print('Error modify_note_for_alumno:', e)
        return None


def remove_note_for_alumno(rut, materia, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        # $pull: elimina elementos del array que coinciden
        res = db.alumnos.update_one({'rut': rut.replace('.', '')}, {'$pull': {'notas': {'materia': materia}}})
        print('Notas modificadas (pull), modified_count:', res.modified_count)
        return res.modified_count
    except Exception as e:
        print('Error remove_note_for_alumno:', e)
        return None


def delete_alumno_by_rut(rut, db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        res = db.alumnos.delete_one({'rut': rut.replace('.', '')})
        print('Eliminados (delete_one):', res.deleted_count)
        return res.deleted_count
    except Exception as e:
        print('Error delete_alumno_by_rut:', e)
        return None


def delete_test_records(db=None):
    try:
        db = db or connect_db()
        if db is None:
            print('No hay conexión a BD'); return None
        res = db.alumnos.delete_many({'test': True})
        print('Eliminados (delete_many):', res.deleted_count)
        return res.deleted_count
    except Exception as e:
        print('Error delete_test_records:', e)
        return None


if __name__ == '__main__':
    # Al ejecutar: prepara colecciones y garantiza 3 alumnos de prueba.
    db = connect_db()
    if db is None:
        print('No hay conexión. Configura MONGO_URI o revisa la red.')
    else:
        # Asegurar asignaturas de ejemplo (no duplicar por código)
        sample_asigs = [
            {'codigo':'MAT101','nombre':'Matemáticas I'},
            {'codigo':'FIS101','nombre':'Física I'},
            {'codigo':'QUI101','nombre':'Química I'}
        ]
        for a in sample_asigs:
            if db.asignaturas.count_documents({'codigo': a['codigo']}) == 0:
                add_asignatura(a['codigo'], a['nombre'], db=db)
            else:
                print(f"Asignatura {a['codigo']} ya existe.")

        total = db.alumnos.count_documents({})
        if total >= 3:
            # Usar 3 alumnos ya existentes como datos de prueba: marcar test=True
            docs = list(db.alumnos.find({}, {'_id': 1}).limit(3))
            for d in docs:
                db.alumnos.update_one({'_id': d['_id']}, {'$set': {'test': True}})
            print(f'Usando {len(docs)} alumnos existentes y marcándolos como prueba (test=True).')
        else:
            # Marcar los existentes como test
            existing = list(db.alumnos.find({}, {'_id': 1}))
            for d in existing:
                db.alumnos.update_one({'_id': d['_id']}, {'$set': {'test': True}})

            # Insertar muestras hasta tener al menos 3 alumnos
            sample_students = [
                {'nombre':'Ana Perez','rut':'12345678-5','email':'ana@example.com','edad':20,'telefono':'912345678','notas':[{'materia':'MAT101','nota':6.5}],'test':True},
                {'nombre':'Luis Gomez','rut':'11111111-1','email':'luis@example.com','edad':22,'telefono':'922345678','notas':[{'materia':'FIS101','nota':5.5}],'test':True},
                {'nombre':'María Torres','rut':'22222222-2','email':'maria@example.com','edad':21,'telefono':'933334444','notas':[{'materia':'QUI101','nota':6.0}],'test':True}
            ]
            inserted = []
            for s in sample_students:
                rut_norm = s['rut'].replace('.', '')
                if db.alumnos.count_documents({'rut': rut_norm}) == 0:
                    db.alumnos.insert_one(s)
                    inserted.append(rut_norm)
                else:
                    db.alumnos.update_one({'rut': rut_norm}, {'$set': {'test': True}})
            print(f'Insertados {len(inserted)} alumnos de prueba. Ahora hay {db.alumnos.count_documents({})} alumnos.')

        # Mostrar hasta 3 alumnos marcados como prueba
        test_list = list(db.alumnos.find({'test': True}, {'nombre':1, 'rut':1, 'email':1}).limit(3))
        print('Alumnos de prueba (hasta 3):')
        for a in test_list:
            print('-', a)
