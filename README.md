# PyMultiInstaller

PyMultiInstaller allows to create multiple exe files in one folder.

## Installation

```bash
pip install git+https://github.com/optinsoft/PyMultiInstaller.git
```

## Usage

```python
from PyMultiInstaller import make_all_installer

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
```
