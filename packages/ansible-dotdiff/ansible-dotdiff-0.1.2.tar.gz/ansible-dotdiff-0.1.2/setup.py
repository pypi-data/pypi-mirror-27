from setuptools import setup, find_packages

# py_files = [
#     "ansible/module_utils/dotdiff"
# ]

long_description=open('README.rst', 'r').read()
version=open('VERSION', 'r').read()

setup(
    name='ansible-dotdiff',
    version=version,
    description='Nested structure diff library with dot-path notation for Ansible',
    long_description=long_description,
    author='Timo Beckers',
    author_email='timo.beckers@klarrio.com',
    url='https://github.com/Klarrio/ansible-dotdiff',
    # py_modules=py_files, # required for single-file modules (like the files in module_utils)
    packages=find_packages(),
    install_requires = [
        'ansible>=2.1.0'
    ],
)
