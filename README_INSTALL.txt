# LabelImg Custom

A customized version of LabelImg with productivity improvements for image annotation. Exports labels in YOLO TXT format.

## What's new

- Undo and redo with Ctrl + Z / Ctrl + Y
- Right-click selection for boxes
- Select and move boxes with right-click
- Copy and paste boxes to another image
- Ctrl + T copies all the boxes of the current image
- Delete a label by right-clicking on it
- Label counter in the right panel
- Quick navigation to a specific image

## Requirements

Python 3.10 or 3.11, Git, and a local desktop environment (not for servers or Jupyter).

## Install and run

### Windows (PowerShell)

```powershell
git clone https://github.com/druminot10/labelImg.git
cd labelImg-master
py -3.11 -m venv venv
.\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install PyQt5 lxml
python -m PyQt5.pyrcc_main -o libs/resources.py resources.qrc
python labelImg.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

### Ubuntu / Linux / macOS

```bash
git clone https://github.com/druminot10/labelImg.git
cd labelImg-master
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install PyQt5 lxml
python -m PyQt5.pyrcc_main -o libs/resources.py resources.qrc
python labelImg.py
```

### Next times

Just activate the environment and run:

- Windows: `.\venv\Scripts\activate.bat` then `python labelImg.py`
- Ubuntu / Linux / macOS: `source venv/bin/activate` then `python labelImg.py`

## Original project

- Original repo: https://github.com/HumanSignal/labelImg
- This fork: https://github.com/druminot10/labelImg
