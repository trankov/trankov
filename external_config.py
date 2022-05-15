# Imagine we have file /Path/to/my_settings.cfg which contains:
# {
#     'name': 'admin',
#     'password': '123'
# }

class ExternalConfig:
    '''```

    >>> import ExternalConfig
    >>> myconfig = ExternalConfig(settings_file='/Path/to/my_settings.cfg')

    >>> myconfig.settings_file
    PosixPath('/Path/to/my_settings.cfg') # or WindowsPath('C:\Path\to\my_settings.cfg')

    >>> myconfig.settings
    {'name': 'admin', 'password': '123'}

    >>> myconfig.values.name
    'admin'

    >>> myconfig.settings['password']
    '123'

    ```'''

    settings_file: Path = Path.cwd()/'settings.py'
    settings: dict = {}
    __PATH_TYPES = (PosixPath, WindowsPath, Path)

    class values:
        pass

    def __init__(self, /, **kwargs):
        if __settings_file := kwargs.get('settings_file'):
            self.settings_file = (Path(__settings_file)
                if type(__settings_file) not in self.__PATH_TYPES
                else __settings_file)
        self._read_settings()
        self._set_settings()

    def _read_settings(self):
        if type(self.settings_file) not in self.__PATH_TYPES:
            raise AttributeError('No valid settings_file')
        self.settings = ast.literal_eval(self.settings_file.read_text())
        if type(self.settings) is not dict:
            raise AttributeError('settings_file must contain a valid dict structure')

    def _set_settings(self):
        for key, value in self.settings.items():
            setattr(self.values, key, value)
