#!/usr/bin/env python3
"""
List all alumnos and their Asignaturas from MongoDB (uses .env).
"""
import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient


def main():
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        print('MONGO_URI not set in .env', file=sys.stderr)
        sys.exit(1)
    MONGO_DB = os.getenv('MONGO_DB', 'evaluacion2')
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    try:
        client.admin.command('ping')
    except Exception as e:
        print('Cannot connect to MongoDB:', e, file=sys.stderr)
        sys.exit(1)
    db = client[MONGO_DB]
    proy = {'nombre': 1, 'rut': 1, 'edad': 1, 'FechaRegistro': 1, 'email': 1, 'telefono': 1, 'Asignaturas': 1}
    cursor = db.alumnos.find({}, proy)
    docs = list(cursor)
    print(f'Total alumnos: {len(docs)}')
    for i, doc in enumerate(docs, 1):
        print('\n--- Alumno', i, '---')
        print('Nombre:', doc.get('nombre', 'N/A'))
        print('RUT:', doc.get('rut', 'N/A'))
        print('Edad:', doc.get('edad', 'N/A'))
        if 'FechaRegistro' in doc:
            print('FechaRegistro:', doc.get('FechaRegistro'))
        if 'email' in doc:
            print('Email:', doc.get('email'))
        else:
            print('Email: (no tiene)')
        if 'telefono' in doc:
            print('Telefono:', doc.get('telefono'))
        else:
            print('Telefono: (no tiene)')
        asignaturas = doc.get('Asignaturas', [])
        if asignaturas:
            print('Asignaturas:')
            for a in asignaturas:
                nombre = a.get('Nombre', 'N/A')
                notas = a.get('Notas', [])
                print(' -', nombre, ':', notas)
        else:
            print('Asignaturas: (ninguna)')
    client.close()


if __name__ == '__main__':
    main()
