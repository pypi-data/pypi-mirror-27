import sys
from typing import List, Dict, Union

import mako
import mako.exceptions
import mako.lookup
import mako.template
import os

from pydmt.api.builder import Builder
from pydmt.core.utils import makedirs_for_file, sha1_files


class Mako(Builder):
    def get_sources(self) -> List[str]:
        return [self.source]

    def __init__(self,
                 source: str,
                 target: str,
                 data: Union[Dict[str, object], None],
                 dep_files: List[str],
                 ):
        super().__init__()
        self.source = source  # type: str
        self.target = target  # type: str
        self.dep_files = dep_files  # type: List[str]
        if data is None:
            self.data = dict()
        else:
            self.data = data

    def get_signature(self) -> str:
        # FIXME: this should be the sha1 of the source + all the definition files
        # and even a better correction:
        # sha1 of the source file + the sha1 of all the variables references from within
        # the source file.
        return sha1_files(self.dep_files+[self.source])

    def build(self):
        try:
            template = mako.template.Template(filename=self.source)
            makedirs_for_file(self.target)
            with open(self.target, 'w') as file_handle:
                file_handle.write(template.render(**self.data))
        except Exception as e:
            if os.path.isfile(self.target):
                os.unlink(self.target)
            raise e

    def get_targets(self) -> List[str]:
        return [self.target]


def print_full_exception():
    print('printing full exception')
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function_name, line) in traceback.traceback:
        print('File {0}, line {1}, in {2}'.format(filename, line_number, function_name))
        print(line)
    print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))


def print_exception(e, input_file):
    found = False
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function_name, line) in traceback.traceback:
        if filename == input_file:
            print('{0}: error {1} in {2}, line {3}'.format(sys.argv[0], str(e), filename, line_number, function_name))
            print('{0}'.format(line))
            found = True
    if not found:
        for (filename, line_number, function_name, line) in traceback.traceback:
            print('File {0}, line {1}, in {2}'.format(filename, line_number, function_name))
            print(line)
        print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))
