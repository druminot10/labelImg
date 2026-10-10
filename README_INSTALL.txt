LabelImg Custom

A customized version of LabelImg with additional productivity improvements for image annotation workflows.

Features
- Undo and redo support with Ctrl + Z / Ctrl + Y
- Right-click selection for boxes
- Label counter in the right panel
- Quick navigation to a specific image
- Improved zoom and selection behavior
- Preserves YOLO TXT output generation

Requirements
- Python 3.10 or 3.11
- Git
- Desktop environment (Windows, Linux, or macOS)
- Local machine with GUI support

Important: LabelImg is a desktop app. It is not intended to run in a remote environment, Jupyter Notebook, or a server without a graphical interface.

Clone the repository

git clone https://github.com/druminot10/labelImg.git
cd labelImg

Install dependencies

Windows (PowerShell)

py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install PyQt5 lxml

Linux / macOS

python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install PyQt5 lxml

Run the application

Windows

python labelImg.py

Linux / macOS

python labelImg.py

Quick start
1. Open the folder containing your images.
2. Select the label class.
3. Draw the bounding box on the image.
4. Save the annotation.
5. The label file will be exported as a .txt file in YOLO format.

Common issues

The app closes immediately
- Make sure you are using Python 3.10 or 3.11.
- Verify that PyQt5 and lxml are installed.
- Run it from a normal local terminal with a desktop environment.

PowerShell blocks activation on Windows

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then activate the venv again:

.\venv\Scripts\Activate.ps1

Qt-related errors

pip install --upgrade PyQt5

Fast install summary

git clone https://github.com/druminot10/labelImg.git
cd labelImg

# Windows
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
# python3 -m venv venv
# source venv/bin/activate

python -m pip install --upgrade pip
pip install PyQt5 lxml
python labelImg.py

Notes
This project is based on the original LabelImg repository, but includes custom improvements for annotation speed and workflow efficiency.

Original project
- Original repo: https://github.com/HumanSignal/labelImg
- This fork: https://github.com/druminot10/labelImg

Testing
The full validation of the custom features will be carried out in the next testing session.
