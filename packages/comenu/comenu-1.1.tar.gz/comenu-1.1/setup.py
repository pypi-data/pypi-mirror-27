from setuptools import setup

with open('requirements.txt') as requirements_file:
    required = requirements_file.read().splitlines()

setup(
    name='comenu',
    version='1.1',
    license='MIT',
    description='Command line menu and helper utility',
    long_description=open('README.rst').read(),
    author='Dmitry Rubtsov',
    author_email='dmitry@rubtsov.eu',
    url='https://github.com/dmirubtsov/comenu',
    packages=['comenu'],
    install_requires=required,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    entry_points={
        'console_scripts': ['comenu=comenu.comenu:main']
    }
)
