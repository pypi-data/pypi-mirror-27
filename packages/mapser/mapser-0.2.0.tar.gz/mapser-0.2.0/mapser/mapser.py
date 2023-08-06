#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re


class MapFileAnalyzer(object):
    _MAP_FILE_SECTION_DISPATCHER = [
        {
            'name': 'Archive member included because of file (symbol)',
            'handler': '_process_archive_member'
        },
        {
            'name': 'Allocating common symbols',
            'handler': '_process_common_symbols'
        },
        {
            'name': 'Discarded input sections',
            'handler': '_process_discarded_sections'
        },
        {
            'name': 'Memory Configuration',
            'handler': '_process_memory_configuration'
        },
        {
            'name': 'Linker script and memory map',
            'handler': '_process_memory_map'
        },
        {
            'name': 'Cross Reference Table',
            'handler': '_process_cross_reference'
        }
    ]

    def __init__(self):
        """
        Base class that analyzes the entire `.map` file and stores all data in a structured way.
        """
        self.archive_members = []
        """
        Items under the map-file section "Archive member included because of file (symbol)".
        
        Note:
            Not yet implemented.
        """
        self.common_symbols = []
        """
        Items under the map-file section "Allocating common symbols".
        
        Keys:
            name (str): Name.
            origin (int): Memory address where it is allocated.
            size (int): Size (in bytes).
            fill (int): Dummy reserved size (in bytes) to keep the memory alignment.
            path (str): Absolute or relative path of the object that contains the symbol.
            library (str): Library name that owns the object file.
            object (str): Name of the object file.
            
        Example:
            {
                'name': 'errno',
                'origin': 536868240,
                'size': 4,
                'fill': 0,
                'path': 'c:/freescale/kds_v3/toolchain/bin/../lib/gcc/arm-none-eabi/4.8.4/../../../../arm-none-eabi/lib/armv6-m',
                'library': 'libg.a',
                'object': 'lib_a-reent.o',
            }
        """
        self.discarded_sections = []
        """
        Items under the map-file section "Discarded input sections".
        
        Note:
            Not yet implemented.
        """
        self.memory_regions = []
        """
        Items under the map-file section "Memory Configuration".
        
        Keys:
            name (str): Name.
            origin (int): Memory address where it is allocated.
            size (int): Size (in bytes).
            attributes (str): Permissions flags: `R` (read-only), `W` (read & write), `X` (executable),
                `A` (allocated), `I` or `L` (initialized).
        
        Example:
            {
                'name': 'm_sys_services',
                'origin': 0x00000300,
                'size': 0x00000100,
                'attributes': 'xr'
            }
        """
        self.app_files = []
        """
        List of all files included in the final application defined under the map-file section 
        "Linker script and memory map".
        
        Keys:
            path (str): Absolute or relative path of the object that contains the symbol.
            library (str): Library name that owns the object file.
            object (str): Name of the object file.
            
        Example:
            {
                'path': r'./programa/source/',
                'object': 'access_control.o',
                'library': 'application'
            }

        """
        self.stack = {}
        """
        Stack memory reserved for the application defined under the map-file section "Linker script and memory map".
        
        Keys:
            size (int): Size (in bytes).
            
        Example:
            {
                'size': 0x0300
            }
        """
        self.heap = {}
        """
        Heap memory reserved for the application defined under the map-file section "Linker script and memory map".
        
        Keys:
            size (int): Size (in bytes).
            
        Example:
            {
                'size': 0x0300
            }
        
        """
        self.memory_segments = []
        """
        Items under the map-file section "Linker script and memory map".
        
        Keys:
            name (str): Name.
            origin (int): Memory address where it is allocated.
            size (int): Size (in bytes).
            
        Example:
            {
                'name': 'text',
                'origin': 0x0000a200,
                'size': 0xa48
            }
        """
        self.symbols_information = []
        """
        Items under the map-file section "Linker script and memory map".
        
        Keys:
            segment (str): Name of the segment that contains the symbol.
            symbol (str): Name of symbol (function, variable, constant,...).
            origin (int): Memory address where it is allocated.
            size (int): Size (in bytes).
            fill (int): Dummy reserved size (in bytes) to keep the memory alignment.
            path (str): Absolute or relative path of the object that contains the symbol.
            library (str): Library name that owns the object file.
            object (str): Name of the object file.
        
        Example:
            {
                'segment': 'text',
                'symbol': 'SCH_isEmpty',
                'origin': 0x0000aa50,
                'size': 0x1c,
                'fill': 0
                'path': 'C:/WoozyCoder/Workspaces/KDS_v3/root/libs/scheduler/v0_6',
                'library': 'libscheduler_v0_6.a',
                'object': 'scheduler.o',
            }
        """
        self.cross_references = []
        """
        Items under the map-file section "Cross Reference Table".
        
        Keys:
            symbol (str): Name of the symbol.
            path (str): Absolute or relative path of the object that contains the symbol.
            library (str): Library name that owns the object file.
            object (str): Name of the object file.
        
        Example:
            {
                'symbol': 'AC_requestAccess',
                'path': './programa/source',
                'object': 'access_control.o',
                'library': 'application'
            }
        """
        self.output = {}
        """
        Items under the map-file section "Linker script and memory map".
        
        Keys:
            filename (str): Name of the output file.
            arch (str): Architecture of the memory (i.e. elf32-littlearm).
        """

    def load(self, map_file):
        """
        Load the input file :map_file and analyzes its content.

        Args:
            map_file (str): Absolute path of the `.map` file.
        """
        with open(map_file, 'r') as fd:
            self._file_dissection(fd.read())

    def find_common_symbol(self, key, value):
        """
        Find Common Symbol with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.common_symbols, key, value)

    def find_memory_regions(self, key, value):
        """
        Find Memory Region with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.memory_regions, key, value)

    def find_app_files(self, key, value):
        """
        Find Application Files with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.app_files, key, value)

    def find_memory_segments(self, key, value):
        """
        Find Memory Segment with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.memory_segments, key, value)

    def find_symbols_information(self, key, value):
        """
        Find Symbol with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.symbols_information, key, value)

    def find_cross_references(self, key, value):
        """
        Find Cross Reference with `key` and `value`.

        Args:
            key (str): Key.
            value (str or int): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        return self._find_attribute_element(self.cross_references, key, value)

    @staticmethod
    def _find_attribute_element(attr, key, value):
        """
        Find Memory Region with `key` and `value`.

        Args:
            attr (list): List of objects in which to search.
            key (str): Key.
            value (str): Value.

        Returns:
            Result of the operation::
                []. If nothing found
                dict. If one element found
                [dict]. If multiple elements found
        """
        try:
            data = [elem for elem in attr if elem[key] == value]
        except KeyError:
            data = []

        if len(data) == 1:
            return data[0]

        return data

    def _common_symbol_append_or_update(self, value):
        """
        Append or update (if already exists) a common symbol to the list.

        Args:
            value (dict): Common symbol.
        """
        if value and value.get('name'):
            found = next((item for item in self.common_symbols if item['name'] == value['name']), None)

            if found:
                found.update(value)
            else:
                self.common_symbols.append(value)

    def _file_dissection(self, content):
        """
        Parse the entire `.map` file detecting each section and passing its content to the right analyzer.

        Args:
            content (str): Content of the `.map` file (plain text).
        """
        section_titles = [section['name'] for section in self._MAP_FILE_SECTION_DISPATCHER]
        found_section = None
        section_content = ''

        if isinstance(content, str):
            content = content.splitlines()

        for line in content:
            if line in section_titles:  # If new section is found
                # First, process the last section found
                if found_section:
                    getattr(self, found_section['handler'])(section_content)

                # Empty section content and remember current file section
                section_content = ''
                found_section = next(
                    (item for item in self._MAP_FILE_SECTION_DISPATCHER if item['name'] == line.rstrip()), None)
            else:  # Else store its content
                section_content += (line + '\n')

        # Process the last file section
        if found_section:
            getattr(self, found_section['handler'])(section_content)

    def _process_archive_member(self, content):
        """
        Analyze the section *'Archive member included because of file (symbol)'*.

        Args:
            content: Content of the section (plain text).
        """
        pass

    def _process_common_symbols(self, content):
        """
        Analyze the section *'Allocating common symbols'*.

        Args:
            content: Content of the section (plain text).
        """
        for match in re.finditer(r'^(\S+)\s+(0x\S+)\s+([^(\s]+)\(?([^)\s]+)?', content, re.M):
            symbol = {
                'name': match.group(1),
                'size': int(match.group(2), 0)
            }

            lib_path = match.group(3).replace('\\', '/')

            if match.group(4):
                symbol['path'], symbol['library'] = os.path.split(lib_path)
                symbol['object'] = match.group(4)
            else:
                symbol['path'], symbol['object'] = os.path.split(lib_path)
                symbol['library'] = 'application'

            self._common_symbol_append_or_update(symbol)

    def _process_discarded_sections(self, content):
        """
        Analyze the section *'Discarded input sections'*.

        Args:
            content: Content of the section (plain text).
        """
        pass

    def _process_memory_configuration(self, content):
        """
        Analyze the section *'Memory Configuration'*.

        Args:
            content: Content of the section (plain text).
        """
        for match in re.finditer(r'^(\S+)\s+(0x\S+)\s+(0x\S+)\s+(\S+)', content, re.M):
            elem = {
                'name': match.group(1),
                'origin': int(match.group(2), 0),
                'size': int(match.group(3), 0),
                'attributes': match.group(4)
            }

            self.memory_regions.append(elem)

    def _process_memory_map(self, content):
        """
        Analyze the section *'Linker script and memory map'*.

        Args:
            content: Content of the section (plain text).
        """
        # Retrieve application files
        for match in re.finditer(r'^LOAD\s(\S+[/\\])(\S+\.(\S))', content, re.M):
            app_file = {
                'path': match.group(1).replace('\\', '/'),
                'object': None,
                'library': 'application'
            }

            if match.group(3) == 'o':
                app_file['object'] = match.group(2)
            else:
                app_file['library'] = match.group(2)

            self.app_files.append(app_file)

        # Retrieve heap and stack sizes
        match = re.search(r'heap_size.*(0x\S+)', content, re.M)
        if match:
            self.heap = {
                'size': int(match.group(1), 0)
            }
        match = re.search(r'stack_size.*(0x\S+)', content, re.M)
        if match:
            self.stack = {
                'size': int(match.group(1), 0)
            }

        # Retrieve output information: filename and architecture
        match = re.search(r'OUTPUT\((\S+) (\S+)\)', content, re.M)
        if match:
            self.output = {
                'filename': match.group(1),
                'arch': match.group(2)
            }

        # Retrieve all memory segments information
        for match in re.finditer(r'^\.(\S+)\s+(0x\S+)\s+(0x\S+)', content, re.M):
            memory_segment = {
                'name': match.group(1),
                'origin': int(match.group(2), 0),
                'size': int(match.group(3), 0)
            }

            self.memory_segments.append(memory_segment)

        # Retrieve all objects and functions information
        for match in re.finditer(
            r'^ \.([^.\s]+)\.?(\S+)?\s*(0x\S+)\s+(0x\S+)\s+([^(\s]+)\(?([^)\s]+)?\)?(.*(?:[\r\n](?! ?[.*]).*)*)',
            content, re.M):
            symbol_information = {
                'segment': match.group(1),
                'origin': int(match.group(3), 0),
                'size': int(match.group(4), 0),  # If size is 0, the symbol should be ignored
                'library': match.group(5) if match.group(6) else None,
                'object': match.group(5) if not match.group(6) else match.group(6),
                'symbol': match.group(2) if match.group(2) else None,
                'fill': 0  # int(match.group(8), 0) if match.group(8) else 0
            }

            # Some symbols (like comments) or information generated by the debugger or the linker must be ignored
            if symbol_information['origin'] == 0 or symbol_information['size'] == 0:
                continue

            if symbol_information['library']:
                lib_path = symbol_information['library'].replace('\\', '/')
                symbol_information['path'], symbol_information['library'] = os.path.split(lib_path)
            else:
                lib_path = symbol_information['object'].replace('\\', '/')
                symbol_information['path'], symbol_information['object'] = os.path.split(lib_path)
                symbol_information['library'] = 'application'

            # There are some situations where the symbol is placed in the last group
            if not symbol_information['symbol']:
                # Some data must be filtered. e.g. 'PROVIDE (end, .)'
                symbol_filters = ['PROVIDE']

                for m in re.finditer(r'^\s+(0x\S+)\s+(\w+)', match.group(7), re.M):
                    if m.group(2) not in symbol_filters:
                        sym_nfo = symbol_information.copy()
                        sym_nfo['origin'] = int(m.group(1), 0)
                        sym_nfo['symbol'] = m.group(2)
                        self.symbols_information.append(sym_nfo)
            else:
                self.symbols_information.append(symbol_information)

        # Extend common symbols information
        self._process_memory_map_common_symbols(content)

    def _process_cross_reference(self, content):
        """
        Analyze the section *'Cross Reference Table'*.

        Args:
            content: Content of the section (plain text).
        """
        for match in re.finditer(r'^(\S+)\b(?<!Symbol)\s+(.+(?:[\r\n]+\s+.+)*)', content, re.M):
            for m in re.finditer(r'^\s*([^(\r\n]+)(?:\((\S+)\))?', match.group(2), re.M):
                cross_reference = {
                    'symbol': match.group(1)
                }

                lib_path = m.group(1).replace('\\', '/')

                if m.group(2):
                    cross_reference['path'], cross_reference['library'] = os.path.split(lib_path)
                    cross_reference['object'] = m.group(2)
                else:
                    cross_reference['path'], cross_reference['object'] = os.path.split(lib_path)
                    cross_reference['library'] = 'application'

                self.cross_references.append(cross_reference)

    def _process_memory_map_common_symbols(self, content):
        """
        Analyze the section *'Linker script and memory map'* searching for the Common Symbols in order
        to extend their information.

        Args:
            content: Content of the section (plain text).
        """
        # The last '[\r\n]' is to take the end of line so that the inner regex matches also the last line
        for match in re.finditer(r'^ COMMON\s+(.*(?:[\r\n](?! COMMON|[\r\n]).*)*[\r\n])', content, re.M):
            last_symbol = ''

            for m in re.finditer(r'^(?:\s+(0x\S+)\s+(\w+)[\r\n])|(?:\s+\*fill\*\s+(0x\S+)\s+(0x\S+))', match.group(1),
                                 re.M):
                common_symbol = {}

                if m.group(1) and m.group(2):
                    last_symbol = m.group(2)
                    common_symbol = {
                        'origin': int(m.group(1), 0),
                        'name': m.group(2),
                        'fill': 0
                    }
                elif m.group(4):
                    common_symbol = {
                        'name': last_symbol,
                        'fill': int(m.group(4), 0)
                    }

                self._common_symbol_append_or_update(common_symbol)
