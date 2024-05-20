import os
from rocrate.rocrate import ROCrate
from rocrate.model.person import Person


crate = ROCrate()

# authors
author1 = crate.add(Person(crate, '#Marco', {"name": "Marco Ciccalè Baztán"}))
author2 = crate.add(Person(crate, '#Jorge', {"name": "Jorge Martín Izquierdo"}))
author3 = crate.add(Person(crate, '#Gloria', {"name": "María Gloria Cumia Espinosa de los Monteros"}))

# files
# function for extension format
def get_format(filename):
    formats = {
        '.pdf': 'application/pdf',
        '.ipynb': 'application/x-ipynb+json',
        '.py': 'text/x-python',
        '.md': 'text/markdown',
        '.json': 'application/json',
        '.yaml': 'application/x-yaml',
        '.jpg': 'image/jpeg',
        '.xml': 'application/xml',
        '.cff': 'text/x-citation',
        '.ttl': 'text/turtle'
    }
    ext = os.path.splitext(filename)[1]
    if ext in formats:
        return formats[ext]
    # 'text/plain' if extension not found
    return 'text/plain'

# add files
def add_files_to_crate(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            encoding_format = get_format(file)
            # Añadir archivo al crate con su ruta relativa
            crate.add_file(file_path, dest_path=rel_path, properties={
                "name": file,
                "encodingFormat": encoding_format
            })

# Directorio raíz
root_dir = os.getcwd()

# Añadir archivos al crate
add_files_to_crate(root_dir)

# Guardar el RO-Crate
crate.write("RO-Crate")
print(f"RO-Crate guardado en {os.path.join(root_dir, 'ro-crate-metadata.json')}")