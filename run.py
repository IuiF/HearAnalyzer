import sys
import subprocess
import os

en_flag = "en_flag"

if not os.path.exists(en_flag):
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    open(en_flag, "w").close()

sys.path.append("./app")
from app import app

if __name__ == "__main__":
    app.run(debug=True)
