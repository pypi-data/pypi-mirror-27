# -*- coding: utf-8 -*-
import os
import sys
import re

from mapser import MapFileAnalyzer
from jinja2 import Environment, FileSystemLoader

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def library_rename(name):
    match = re.findall(r'(?:lib)?(\S+)\.a', name)
    return match[0] if match else None


def main(args):
    mapfile_path = os.path.join(CUR_DIR, '../tests/assets/Application_KL26.map')

    mapser = MapFileAnalyzer()
    mapser.load(mapfile_path)

    project_name = os.path.basename(mapser.output['filename'])

    heap_memory = next((ms for ms in mapser.memory_segments if ms['name'] == 'heap'), None)

    stack_memory = next((ms for ms in mapser.memory_segments if ms['name'] == 'stack'), None)

    libraries_set = set([lib['library'] for lib in mapser.symbols_information])
    libraries = []

    for lib_name in libraries_set:
        lib_data = [data for data in mapser.symbols_information if data['library'] == lib_name]
        allowed_segments = ('text',)

        lib_functions = [lib for lib in lib_data if lib['segment'] in allowed_segments]

        lib_size = 0
        for func in lib_functions:
            lib_size += func['size']

        lib_name_new = library_rename(lib_name) if lib_name != 'application' else 'application'

        lib = {
            'name': lib_name_new if lib_name_new else lib_name,
            'functions': lib_functions,
            'size': lib_size
        }
        libraries.append(lib)

    segments = [segment for segment in mapser.memory_segments if segment['size'] and segment['origin']]

    j2_env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True, lstrip_blocks=True)
    template = j2_env.get_template('template.jinja')

    with open('ouput.html', 'w') as fd:
        result = template.render(project_name=project_name, heap=heap_memory, stack=stack_memory, libraries=libraries,
                                 segments=segments)
        fd.write(result)


if __name__ == '__main__':
    main(sys.argv)
