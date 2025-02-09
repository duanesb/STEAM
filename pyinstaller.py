import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=Physics Simulators',
    '--windowed',
    '--noconsole',
    '--onedir',
    '--add-data=assets:assets',
    '--icon=App_Icon.png',
])


#! Remember that to reload using the spec, you use: pyinstaller Physics-Simulators.spec