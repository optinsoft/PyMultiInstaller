# PyMultiInstaller

PyMultiInstaller allows to create multiple exe files in one folder.

## Installation

```bash
pip install git+https://github.com/optinsoft/PyMultiInstaller.git
```

## Dependencies

[PyInstaller 5.13.2](https://pyinstaller.org/en/v5.13.2/)

## Usage

```python
from PyMultiInstaller import make_all_installer, zip_install
import os

if __name__ == '__main__':
    make_all_installer([
        [
            'ljreg.py',
            '--add-data',
            'ljreg-config.0.yml;.',
            '--noconfirm'
        ],
        [
            'ljcheck.py',
            '--add-data',
            'ljcheck-config.0.yml;.'
        ]
    ])
    zip_install(os.path.join('.', 'dist', 'ljreg'))
```
