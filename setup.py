from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='modbag',
    version='0.1.0',
    description='Helper library for preparing fully deployable ML models on K8s',
    author='LA',
    packages=find_packages(),
    install_requires=install_requires=parse_requirements('requirements.txt'),
)
