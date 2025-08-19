import PyInstaller.__main__

PyInstaller.__main__.run([
    "src/main.py",
    "--onefile",
    "--noconsole",
    "--name=BarcodeReader_Final",
    "--distpath=dist",
    "--workpath=build",
    "--clean"
])
