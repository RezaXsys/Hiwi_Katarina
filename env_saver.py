#import os
#import yaml

# YAML-Datei lesen
#with open("env.yaml", "r") as file:
#    config = yaml.safe_load(file)

# Variablen in die Umgebungsvariablen setzen
#for key, value in config["env"].items():
#   os.environ[key] = value

# Testen
#print(os.getenv("VARIABLE_1"))  # Gibt "Wert1" aus


import os
import yaml

# Alle Umgebungsvariablen abrufen
#env_vars = dict(os.environ)

# YAML-Datei erstellen
#with open("env.yaml", "w") as file:
   # yaml.dump({"env": env_vars}, file, default_flow_style=False)

#print("Umgebungsvariablen wurden in env.yaml gespeichert.")


import os

# Environment dictionary (dein YAML-oder JSON-Load-Output, Beispiel)
env = {
    'env': {
        'COLORTERM': 'truecolor',
        'COMMAND_MODE': 'unix2003',
        'CONDA_DEFAULT_ENV': 'hiwi_env',
        'CONDA_EXE': '/opt/anaconda3/bin/conda',
        'CONDA_PREFIX': '/opt/anaconda3/envs/hiwi_env',
        'CONDA_ROOT': '/opt/anaconda3',
        'GIT_ASKPASS': '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass.sh',
        'HOME': '/Users/apple',
        'LANG': 'de_DE.UTF-8',
        'PATH': '/opt/anaconda3/envs/hiwi_env/bin:/opt/anaconda3/condabin:/usr/local/bin:/bin',
        'SHELL': '/bin/zsh',
        'VSCODE_GIT_ASKPASS': '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass-main.js',
    }
}

# Python packages list (manuelle Ergänzungen oder automatisierte Erfassung)
required_installs = set()

# Allgemeine Umgebungspfade/Binärdateien extrahieren
for key, value in env['env'].items():
    if "PATH" in key or "EXE" in key or any(ext in value for ext in ['bin', 'conda', 'python', '/usr/local']):
        required_installs.add(value)

# Manuelle Ergänzungen von Python-Paketen
python_packages = [
    'torch',
    'numpy',
    'pandas',
    'scikit-learn',
    'matplotlib',
    'tensorflow',
    'openai',  # Falls OpenAI API verwendet wird
]

# Alle Pakete zusammenführen
required_installs.update(python_packages)

# Anforderungen speichern
with open('requirements.txt', 'w') as req_file:
    for install in required_installs:
        req_file.write(install + '\n')

print("Requirements gespeichert in requirements.txt")
