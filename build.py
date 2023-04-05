import os

buildCommand = 'pyinstaller --onefile --paths=D:\env\Lib\site-packages --noconsole --add-binary ' \
               '"./src/chromedriver.exe;./src" --icon=app.ico --uac-admin main.py'

commandLineCommand = 'pyinstaller --onefile --paths=D:\env\Lib\site-packages --add-binary ' \
                     '"./src/chromedriver.exe;./src" --uac-admin --icon=app.ico main.py'

os.system(buildCommand)


