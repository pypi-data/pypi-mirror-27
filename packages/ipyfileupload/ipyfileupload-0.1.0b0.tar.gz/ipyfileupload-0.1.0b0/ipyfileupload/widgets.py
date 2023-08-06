import base64
import io

import ipywidgets as widgets
from traitlets import Unicode, Bytes, CBytes, Dict, observe


@widgets.register
class FileUploadWidget(widgets.DOMWidget):
    '''File Upload Widget.
    This widget provides file upload using `FileReader`.
    '''
    _view_name = Unicode('FileUploadView').tag(sync=True)
    _model_name = Unicode('FileUploadModel').tag(sync=True)

    _view_module = Unicode('ipyfileupload').tag(sync=True)
    _model_module = Unicode('ipyfileupload').tag(sync=True)

    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    label = Unicode(help='Label on button.').tag(sync=True)
    filename = Unicode(help='Filename of `data`.').tag(sync=True)
    data_base64 = Unicode(help='File content, base64 encoded.'
                                    ).tag(sync=True)
    data = Bytes(help='File content.')

    def __init__(self, label="Browse", *args, **kwargs):
        super(FileUploadWidget, self).__init__(*args, **kwargs)
        self._dom_classes += ('widget_item', 'btn-group')
        self.label = label

    def _data_base64_changed(self, *args):
        self.data = base64.b64decode(self.data_base64.split(',', 1)[1])

@widgets.register
class MultiFileUploadWidget(widgets.DOMWidget):
    '''File Upload Widget.
    This widget provides file upload using `FileReader`.
    '''
    _view_name = Unicode('MultiFileUploadView').tag(sync=True)
    _model_name = Unicode('MultiFileUploadModel').tag(sync=True)

    _view_module = Unicode('ipyfileupload').tag(sync=True)
    _model_module = Unicode('ipyfileupload').tag(sync=True)

    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    label = Unicode(help='Label on button.').tag(sync=True)

    base64_files = Dict(value_trait=Unicode(), help='Uploaded files').tag(sync=True)
    files = Dict(value_trait=Bytes()).tag(sync=True)

    def __init__(self, label="Browse", *args, **kwargs):
        super(MultiFileUploadWidget, self).__init__(*args, **kwargs)
        self._dom_classes += ('widget_item', 'btn-group')
        self.label = label

    @observe('base64_files')
    def _base64_files_changed(self, *args):
        for name, file in self.base64_files.items():
            self.files[name] = base64.b64decode(file.split(',',1)[1])

    def pop(self, file = None):
        if file is None:
            file, data_base64 = self.base64_files.popitem();
            data = self.files.pop(file);
        else:
            data_base64 = self.base64_files.pop(file)
            data = self.files.pop(file)

        return {
            'base64': data_base64,
            'data': data,
            'name': file
        }

    @staticmethod
    def decode(byteStream):
        return io.StringIO(byteStream.decode('utf-8'))
        
@widgets.register
class DirectoryUploadWidget(widgets.DOMWidget):
    '''File Upload Widget.
    This widget provides file upload using `FileReader`.
    '''
    _view_name = Unicode('DirectoryUploadView').tag(sync=True)
    _model_name = Unicode('DirectoryUploadModel').tag(sync=True)

    _view_module = Unicode('ipyfileupload').tag(sync=True)
    _model_module = Unicode('ipyfileupload').tag(sync=True)

    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    label = Unicode(help='Label on button.').tag(sync=True)

    base64_files = Dict(value_trait=Unicode(), help='Uploaded files').tag(sync=True)
    files = Dict(value_trait=Bytes()).tag(sync=True)

    def __init__(self, label="Browse", *args, **kwargs):
        super(DirectoryUploadWidget, self).__init__(*args, **kwargs)
        self._dom_classes += ('widget_item', 'btn-group')
        self.label = label

    @observe('base64_files')
    def _base64_files_changed(self, *args):
        for name, file in self.base64_files.items():
            self.files[name] = base64.b64decode(file.split(',',1)[1])

    def pop(self, file = None):
        if file is None:
            file, data_base64 = self.base64_files.popitem();
            data = self.files.pop(file);
        else:
            data_base64 = self.base64_files.pop(file)
            data = self.files.pop(file)

        return {
            'base64': data_base64,
            'data': data,
            'name': file
        }

    @staticmethod
    def decode(byteStream):
        return io.StringIO(byteStream.decode('utf-8'))
        
