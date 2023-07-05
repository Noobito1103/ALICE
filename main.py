import subprocess
import importlib

library = ['flask', 'flask_sqlalchemy', 'flask_cors']
try:
    subprocess.run(["pip", "--version"], capture_output = True, check = True)
    print("pip is installed")
except subprocess.CalledProcessError:
    print("pip is not installed. Installing pip...")
    subprocess.run(["python", "get-pip.py"], check=True)

for data in library:
    try:
        importlib.import_module(data)
        print(f'{data} is installed')
    except ImportError:
        print(f'{data} is not installed. Installing...')
        subprocess.check_call(['pip', 'install', data])

from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True, port=5000, host='0.0.0.0')
