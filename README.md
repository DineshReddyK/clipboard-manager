# clipboard-manager
Pure python tkinter based clipboard manager.\
This tool maintains a history of clipboard contents, allowing users to easily search and retrieve previously copied clips.

Most of the python installations comes with tkinter so you don't need to install any specific pacakge for this to work.\
If you don't have tkinter module installed, follow the steps below

#### Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

#### RHEL/Fedora/CentOS:
```bash
sudo dnf install python3-tkinter
```

#### Mac
```bash
brew install python-tk
```

\
Windows should have it by default.


#### Setting as a Startup Script on windows
1. Rename the `clipboard-manager.py` to `clipboard-manager.pyw`
2. Press `Windows Key + R` to open the Run dialog box.
3. Type `shell:startup` and press Enter to open the Startup folder.
4. Create a shortcut to `clipboard-manager.pyw` file and place it in this folder.

The script will run on startup without showing a console window.