import logging as log
import os
from pathlib import Path


class FileManager:
    def __init__(self):
        self.p = Path(os.path.expanduser("~"))

    def get_current_path(self):
        return str(self.p)

    def change_current_path(self, goto):
        if goto == '..':
            self.p = self.p.parent
        else:
            self.p = self.p / goto

        data = {'param': str(self.p)}
        log.debug('data={}'.format(data))
        return data

    def get_elements_in_path(self):
        elements = []
        try:
            for x in self.p.iterdir():
                if x.is_dir():
                    elements.append((x.name, 'folder'))
                else:
                    elements.append((x.name, 'plik'))
        except Exception:
            elements.append(('..', 'folder'))
        return tuple(elements)

    def open_file(self, name):
        return None

    def delete_file(self, name):
        return None

    def create_new_folder(self, name):
        return None

    def set_background(self, image_name):
        return None
