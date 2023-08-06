ipyfileupload
===============================

An IPython notebook widget to upload files, using FileReader.

Installation
------------

To install use pip:

```bash
$ pip install ipyfileupload
$ jupyter nbextension enable --py --sys-prefix ipyfileupload
```

For a development installation (requires npm),

```bash
$ git clone https://github.com//ipyfileupload.git
$ cd ipyfileupload
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix ipyfileupload
$ jupyter nbextension enable --py --sys-prefix ipyfileupload
```

You might as well need to enable jupyter's widgetsnbextension

```bash
$ jupyter nbextension enable --py widgetsnbextension --sys-prefix
```

and possibly run NPM prepublish for a dev install :

```bash
$ cd js
$ npm install
$ npm run prepublish
```

Note :
    This widget uploads file content in kernel memory, it wont work with large files.

