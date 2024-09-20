from setuptools import find_packages, setup
import os
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

if __name__ == '__main__':
    setup(
        name='alphax-entertainments',
        version='1.1.1',
        description='This project is about AI Applications using Prompt Engineering',
        author='Qadeer Ahmad',
        license='',
        packages=find_packages(),
        install_requires=get_requirements('requirements.txt')
    )