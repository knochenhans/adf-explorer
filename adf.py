import os.path
from typing import Dict, List, Optional

from amitools.fs.ADFSFile import ADFSFile
from amitools.fs.ADFSVolume import ADFSVolume
from amitools.fs.blkdev.BlkDevFactory import BlkDevFactory
from amitools.fs.FileName import FileName
from amitools.fs.Imager import Imager
from amitools.tools.xdftool import make_fsstr


class ADF:
    def __init__(self, app) -> None:
        self.app = app
        self.volume: Optional[ADFSVolume] = None
        self.blkdev = None
        self.node: Optional[ADFSFile] = None
        self.path: Optional[str] = None

    def absolutePath(self, name: str) -> str:
        return (self.path + "/" if self.path != "/" else "") + name

    def create(self, path: str) -> None:
        self.cleanUp()

        self.blkdev = BlkDevFactory().create(path)
        self.volume = ADFSVolume(self.blkdev)

        name = os.path.basename(path)

        self.volume.create(make_fsstr(name), dos_type=None)

    def open(self, path: str) -> None:
        self.cleanUp()

        self.blkdev = BlkDevFactory().open(path)
        self.volume = ADFSVolume(self.blkdev)
        self.volume.open()

    def navigate(self, path: str = "/") -> None:
        try:
            self.node = self.volume.get_path_name(make_fsstr(path))
        except:
            return

        self.path = path
        self.entries: List[Dict[str, str]] = [
            {
                "name": entry.get_file_name().get_name().__str__(),
                "type": "dir" if entry.is_dir() else "file",
            }
            for entry in self.node.get_entries_sorted_by_name()
        ]

        self.app.updatePath(self.path)
        self.app.updateBrowser(self.entries)

    def navigateDown(self, dir: str) -> None:
        if self.path == "/":
            self.navigate(dir)
        else:
            self.navigate(self.path + "/" + dir)

    def parent(self) -> None:
        path = self.path.split("/")[:-1]

        if len(path) > 1:
            self.navigate(path.join("/"))
        elif len(path) == 1:
            self.navigate(path[0])
        else:
            self.navigate()

    def volumeName(self) -> str:
        return self.volume.get_volume_name().__str__()

    def volumeInfo(self) -> str:
        return self.volume.get_info().__str__()

    def extract(self, name: str, output: str) -> None:
        path = self.absolutePath(name)
        node: ADFSFile = self.volume.get_path_name(make_fsstr(path))

        if node.is_file():
            data = node.get_file_data()
            fh = open(output, "wb")
            fh.write(data)
            fh.close()
        elif node.is_dir():
            img = Imager(meta_mode=Imager.META_MODE_NONE)
            img.unpack_dir(node, output)

    def insert(self, input: str) -> None:
        name = os.path.basename(input)

        if os.path.isfile(input):
            fh = open(input, "rb")
            data = fh.read()
            fh.close()

            self.volume.write_file(data, make_fsstr(self.path), make_fsstr(name))
        elif os.path.isdir(input):
            parent, name = self.volume.get_create_path_name(
                make_fsstr(self.path), make_fsstr(name)
            )

            node = parent.create_dir(name)
            img = Imager(meta_mode=Imager.META_MODE_NONE)
            img.pack_dir(input, node)

        self.navigate(self.path)

    def makeDir(self, name: str) -> None:
        path = self.absolutePath(name)

        self.volume.create_dir(make_fsstr(path))
        self.navigate(self.path)

    def delete(self, name: str) -> None:
        path = self.absolutePath(name)

        self.volume.delete(make_fsstr(path), all=True)
        self.navigate(self.path)

    def relabel(self, name: str) -> None:
        self.volume.relabel(make_fsstr(name))

    def cleanUp(self) -> None:
        if self.volume:
            self.volume.close()

        if self.blkdev:
            self.blkdev.close()

    def extractToMemory(self, name: str) -> str:
        """Extract the content of a file as a string."""
        if not self.volume:
            raise ValueError("No volume is currently open.")

        path = self.absolutePath(name)
        node = self.volume.get_path_name(make_fsstr(path))

        if isinstance(node, ADFSFile) and node.is_file():
            data = node.get_file_data()
            return data.decode("utf-8", errors="replace")
        else:
            raise ValueError(f"{name} is not a file.")
