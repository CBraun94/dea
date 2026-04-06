PATH_INPUT = '/home/chris/dev/dea/input/'
FE_MERMAID = '.mermaid'


def dir_walk(start_path=PATH_INPUT) -> list[str]:
    import os
    _r = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            _r.append(os.path.join(root, file))
    return _r


def files_mermaid(files: list[str], file_extension: str = FE_MERMAID) -> list[str]:
    import pathlib

    _r = []
    for file in files:
        _file_extension = pathlib.Path(file).suffix
        if _file_extension.lower() == file_extension.lower():
            _r.append(file)
    return _r
