import sys
import os
import shutil

sys.path.append("./app")
from app import app


folder_path = "./app/tmp"
shutil.rmtree(folder_path)
os.mkdir(folder_path)


if __name__ == "__main__":
    app.run(debug=True)
