
from setuptools import find_packages
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna',
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress'
        ],
        'excludes': ['tkinter'],
        'include_files': [
          'assets/', 'assets/style.css']
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
    version='1.0.0',
    description='MyApp',
    executables=executables,
    options=options
)
