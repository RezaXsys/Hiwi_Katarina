import subprocess
import yaml

def get_conda_packages():
    """Erhalte alle mit conda installierten Pakete."""
    result = subprocess.run(['conda', 'list'], capture_output=True, text=True)
    return result.stdout

def get_pip_packages():
    """Erhalte alle mit pip installierten Pakete."""
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    return result.stdout

def create_requirements_txt(conda_output, pip_output):
    """Schreibe conda und pip Pakete in requirements.txt"""
    with open('requirements.txt', 'w') as req_file:
        req_file.write(conda_output)
        req_file.write("\n")
        req_file.write(pip_output)

def create_env_yaml():
    """Erstelle env.yml aus conda Umgebung"""
    conda_env = {
        "name": "hiwi_env",
        "channels": ["defaults", "conda-forge"],
        "dependencies": []
    }

    conda_dependencies = subprocess.run(['conda', 'list', '--export'], capture_output=True, text=True)
    pip_dependencies = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

    conda_env["dependencies"] = [dep for dep in conda_dependencies.stdout.splitlines() if dep and not dep.startswith("#")]
    conda_env["dependencies"].extend([dep for dep in pip_dependencies.stdout.splitlines() if dep])

    # YAML speichern
    with open('env.yml', 'w') as yaml_file:
        yaml.dump(conda_env, yaml_file, default_flow_style=False)

    print("env.yml wurde erstellt.")

if __name__ == "__main__":
    conda_output = get_conda_packages()
    pip_output = get_pip_packages()

    create_requirements_txt(conda_output, pip_output)
    create_env_yaml()

    print("All required files (requirements.txt & env.yml) have been created.")
