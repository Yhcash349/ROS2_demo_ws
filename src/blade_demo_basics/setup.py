from setuptools import find_packages, setup

package_name = 'blade_demo_basics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yhc23',
    maintainer_email='YoungHcheng@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'status_publisher = blade_demo_basics.status_publisher:main',
            'status_subscriber = blade_demo_basics.status_subscriber:main',
        ],
    },
)
