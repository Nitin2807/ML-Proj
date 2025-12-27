from setuptools import setup, find_packages
HYPHEN_E_DOT = '-e .'
def get_requirements(file_path):
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements
setup(
    name='my_ML_project',
    version='0.0.1',
    author='Nitin Srivastav',
    author_email= 'nitinsrivastav2005@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt')   
) 