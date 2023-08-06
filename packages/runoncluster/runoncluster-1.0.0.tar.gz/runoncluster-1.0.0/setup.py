from setuptools import find_packages, setup

version = '1.0.0'

setup(
    name='runoncluster',
    version=version,
    url='https://github.com/BerkeleyBiostats/clusterit/',
    author='Marc Paré',
    author_email='marc@rvit.co',
    description='CLI tools for interaction with tl-app',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "click"
    ],
    extras_require={
    },
    zip_safe=False,
    classifiers=[
    ],
    entry_points={
        'console_scripts': [
          'runoncluster = clusterit.cli:cli',
        ]
    },
)