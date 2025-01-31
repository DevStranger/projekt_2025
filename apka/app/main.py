import os
print("Current working directory:", os.getcwd())

from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
