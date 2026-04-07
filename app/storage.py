from pathlib import Path
import json

DATA_DIR=Path(__file__).parent/"data"
DATA_FILE=DATA_DIR/"issues.json"

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE,"r") as f:
            content=f.read()
            if content.strip():
                return json.loads(content) #Whatever is in the file it converts from json string to python objects
    return []

def save_data(data):
    DATA_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(DATA_FILE,"w") as fw:
        json.dump(data,fw,indent=2)
