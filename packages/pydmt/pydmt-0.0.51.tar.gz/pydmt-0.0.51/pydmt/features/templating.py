import os

from pydmt.api.feature import Feature
from pydmt.builders.mako import Mako
from pydmt.core.pydmt import PyDMT
from pydmt.core.utils import files_under_folder


class Templating(Feature):
    def __init__(
            self,
            data=None,
            templates_folder: str="templates",
            config_folder: str="config",
    ):
        self.data = data
        self.templates_folder = templates_folder
        self.config_folder = config_folder

    def setup(self, pydmt: PyDMT) -> None:
        for root, directories, filenames in os.walk(self.templates_folder):
            for filename in filenames:
                source = os.path.join(root, filename)
                target_base, ext = os.path.splitext(source)
                if ext == '.mako':
                    target = os.sep.join(target_base.split(os.sep)[1:])
                    builder = Mako(
                        source=source,
                        target=target,
                        data=self.data,
                        dep_files=files_under_folder(self.config_folder),
                    )
                    pydmt.add_builder(builder)
