#!/usr/bin/env python3
"""
Seed script for MongoDB test data.

Usage:
  python scripts/seed_mongo.py         # generate data and show summary (no DB changes)
  python scripts/seed_mongo.py --insert  # insert generated documents into MongoDB using .env

The script obeys the dataset rules requested in the task description.
"""
import os
import random
import argparse
import unicodedata
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

SUBJECTS = [
    "Base de datos No estructuradas",
    "Fundamentos de Seguridad de la información",
    "Fundamentos de Hardware y Software",
    "Sistemas Operativos",
    "Programación Front End",
    "Bases de Datos Estructuradas",
    "Fundamentos de Base de Datos",
    "Álgebra",
    "Programación Segura",
    "Funciones y Matrices",
]


def dv_for_rut(num_str: str) -> str:
    total = 0
    mul = 2
    for ch in reversed(num_str):
        total += int(ch) * mul
        mul += 1
        if mul > 7:
            mul = 2
    res = 11 - (total % 11)
    if res == 11:
        return '0'
    if res == 10:
        return 'K'
    return str(res)


def gen_rut(idx: int) -> str:
    # deterministic 8-digit-like base for reproducibility
    base = 10_000_000 + idx
    return f"{base}-{dv_for_rut(str(base))}"


def slug_name(name: str) -> str:
    nfkd = unicodedata.normalize('NFKD', name)
    no_acc = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    alphas = ''.join(ch for ch in no_acc.lower() if ch.isalpha())
    return alphas or 'user'


def gen_note_between(a: float, b: float) -> float:
    return round(random.uniform(a, b), 1)


def create_students(n=40, seed=12345):
    random.seed(seed)
    # curated names to satisfy prefixes/suffixes requirements
    curated = [
        "Alvaro Campos", "Ariana Salas", "Antonio Morales",  # start with A
        "Miguel Santos", "Mariana Lopez", "Manuel Rios",    # start with M
        "Zoe Alvarez", "Zulema Ortega", "Zacarias Fuentes", # start with Z
        "Carlos Ramos", "Lucas Paredes", "Andres Silva",    # end with 's'
        "Ana Molina", "Laura Torres", "Beatriz Vega",      # end with 'a'
    ]

    first_names = [
        'Sofia','Valentina','Isabella','Camila','Emilia','Martina','Jose','Luis','Diego','Mateo',
        'Fernando','Gabriel','Pablo','Javier','Roberto','Pedro','Sergio','Esteban','Victor','Nicolas'
    ]
    last_names = [
        'Gonzalez','Perez','Rodriguez','Sanchez','Torres','Ramirez','Flores','Rivera','Vega','Silva',
        'Ortiz','Molina','Rios','Vargas','Herrera','Castro','Castillo','Marin','Alvarez','Mena'
    ]

    names = curated.copy()
    i = 0
    while len(names) < n:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        candidate = f"{fn} {ln}"
        if candidate not in names:
            names.append(candidate)
        i += 1
        if i > 5000:
            break

    # pick indices that will have email and telefono (80%)
    k = int(0.8 * n)
    email_indices = set(random.sample(range(n), k))
    phone_indices = set(random.sample(range(n), k))

    students = []
    for idx in range(n):
        name = names[idx]
        student = {
            'nombre': name,
            'rut': gen_rut(idx),
            'edad': random.randint(18, 45),
            'FechaRegistro': datetime.now().strftime('%Y-%m-%d'),
            'Asignaturas': []
        }
        if idx in email_indices:
            student['email'] = f"{slug_name(name)}@example.com"
        if idx in phone_indices:
            student['telefono'] = str(random.randint(600000000, 999999999))
        students.append(student)

    # For each subject, assign it to exactly 10 (minimum) students and ensure 2 reprobados
    for subj in SUBJECTS:
        chosen = random.sample(range(n), 10)
        failers = set(random.sample(chosen, 2))
        for idx in chosen:
            # generate notas: failing students in [1.0,3.9], others in [4.0,7.0]
            if idx in failers:
                notas = [gen_note_between(1.0, 3.9) for _ in range(3)]
            else:
                notas = [gen_note_between(4.0, 7.0) for _ in range(3)]
            # append assignment if not already present
            stu = students[idx]
            if not any(a['Nombre'] == subj for a in stu['Asignaturas']):
                stu['Asignaturas'].append({'Nombre': subj, 'Notas': notas})

    # Ensure every student has at least one asignatura (assign random ones if needed)
    for stu in students:
        if not stu['Asignaturas']:
            picks = random.sample(SUBJECTS, 3)
            for subj in picks:
                notas = [gen_note_between(4.0, 7.0) for _ in range(3)]
                stu['Asignaturas'].append({'Nombre': subj, 'Notas': notas})

    return students


def validate_dataset(students):
    subj_counts = {s: 0 for s in SUBJECTS}
    subj_fails = {s: 0 for s in SUBJECTS}
    for stu in students:
        for a in stu.get('Asignaturas', []):
            name = a['Nombre']
            subj_counts[name] += 1
            avg = sum(a.get('Notas', [])) / max(1, len(a.get('Notas', [])))
            if avg < 4.0:
                subj_fails[name] += 1

    return subj_counts, subj_fails


def insert_into_db(students):
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise RuntimeError('MONGO_URI no está configurada en .env')
    MONGO_DB = os.getenv('MONGO_DB', 'evaluacion2')
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    # test connection
    client.admin.command('ping')
    db = client[MONGO_DB]
    res = db.alumnos.insert_many(students)
    return res.inserted_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=40, help='Número de alumnos a generar (mín 40)')
    parser.add_argument('--insert', action='store_true', help='Insertar en MongoDB usando .env')
    parser.add_argument('--yes', action='store_true', help='Aceptar confirmaciones automáticamente')
    args = parser.parse_args()

    if args.num < 40:
        print('Advertencia: el número mínimo recomendado es 40; ajustando a 40.')
        n = 40
    else:
        n = args.num

    students = create_students(n=n)
    counts, fails = validate_dataset(students)

    print('\nResumen generado:')
    print('Alumnos generados:', len(students))
    for s in SUBJECTS:
        print(f'- {s}: inscritos={counts[s]}  reprobados_promedio<{4.0}={fails[s]}')

    # Basic validation checks
    ok = True
    for s in SUBJECTS:
        if counts[s] < 10:
            print(f'ERROR: asignatura "{s}" tiene menos de 10 inscritos ({counts[s]})')
            ok = False
        if fails[s] < 2:
            print(f'ERROR: asignatura "{s}" tiene menos de 2 reprobados ({fails[s]})')
            ok = False

    if not ok:
        print('\nEl dataset no cumple las garantías requeridas. Revise el script.')
    else:
        print('\nEl dataset cumple las condiciones solicitadas.')

    if args.insert:
        if not args.yes:
            resp = input('Confirmar inserción en la base de datos (s/n): ').strip().lower()
            if not resp.startswith('s'):
                print('Inserción cancelada por el usuario.')
                return
        try:
            ids = insert_into_db(students)
            print(f'Insertados {len(ids)} documentos en la colección "alumnos".')
        except Exception as e:
            print('Error al insertar en MongoDB:', e)


if __name__ == '__main__':
    main()
