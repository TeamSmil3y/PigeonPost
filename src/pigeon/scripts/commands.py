from pathlib import Path
import shutil
import os


def create(name='app'):
    if not os.path.exists(name) and not os.path.isfile(name):
        os.mkdir(name)
    path = Path(name)
    resource_path = Path(__file__).parent.resolve() / Path('_resources/')
    
    shutil.copy(resource_path / 'settings.py', path / 'settings.py')
    shutil.copy(resource_path / 'app.py', path / f'{name}.py')