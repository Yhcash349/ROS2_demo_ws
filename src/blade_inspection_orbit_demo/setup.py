import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'blade_inspection_orbit_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yhc23',
    maintainer_email='YoungHcheng@gmail.com',
    description='Nav2-based wind turbine blade inspection orbit demo.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'go_to_pose_demo = blade_inspection_orbit_demo.go_to_pose_demo:main',
        ],
    },
)
