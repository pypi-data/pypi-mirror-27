from django.template.loaders.app_directories import  Loader as AppDirectoriesLoader
from django.template.loaders.filesystem import Loader as FileSystemLoader
from .compiler import Compiler
from pyjade.utils import process


class Loader(AppDirectoriesLoader):

    is_usable = True

    def get_dirs(self):
        return list(AppDirectoriesLoader.get_dirs(self)) + list(FileSystemLoader.get_dirs(self))

    def get_contents(self, origin):
        result = super(Loader, self).get_contents(origin)

        if origin.template_name.endswith('.jade'):
            include_dirs = self.get_dirs()
            result = process(result, filename=origin.template_name, compiler=Compiler, include_dirs=include_dirs)

        return result
