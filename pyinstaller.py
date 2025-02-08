import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=Physics Simulators',
    '--windowed',
    '--noconsole',
    '--onedir',
    '--add-data=assets:assets',
    # '--icon=', #! Remember to add the icon file directory
])