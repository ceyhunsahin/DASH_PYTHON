from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna','idna.idnadata',
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress'
        ],
        'excludes': ['tkinter'],
        'include_files': [
          'assets/tabs.css', 'assets/style.css']
    }
}

executables = [
    Executable('server.py',
               base='console',
               targetName='DashApp.exe')
]

setup(
    name='dashApp',
    packages=find_packages(),
    version='0.0.1',
    description='rig',
    executables=executables,
    options=options
)

