from ._version import version_info, __version__

from .widgets import FileUploadWidget

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'ipyfileupload',
        'require': 'ipyfileupload/extension'
    }]
