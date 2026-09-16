from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'brain'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tanmeet',
    maintainer_email='tanmeet.sachdeva@gmail.com',
    description='Brain Transformations Node for broadcasting static transforms.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'brain_transformations = brain.brain_transformations:main',
            'brain_node = brain.brain_node:main',
            'inventory_manager = inventory.inventory_manager:main',
            'inventory_transformations = inventory.inventory_transformations:main',
            'arm = arm.arm:main',
            'perception = perception.perception:main'
        ],
    },
)
