from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robu'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[  #am nde vom vompilieren führt er data_files aus
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name, 'launch'), glob('launch/*launch.py')) #Zielpfad; glob = kopiert den Pfad von 
    ],                                                                         #ausschlielich dateien mit launch.py am Ende
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robu',
    maintainer_email='kapemn19@htl-kaindorf.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'helloworld = robu.helloworld:main',
            'remotectrl = robu.ex02_remotectrl:main',
            'oas = robu.ex03_obstacleavoidance_simple:main'

        ],
    },
)

