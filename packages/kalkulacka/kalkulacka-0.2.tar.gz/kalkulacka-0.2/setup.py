from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='kalkulacka',
    version='0.2',
    description='A demo calculator',
    long_description=long_description,
    author='Petr Viktorin',
    author_email='encukou@gmail.com',
    license='MIT',
    url='https://github.com/encukou/kalkulacka',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
    package_data={
        'kalkulacka.resources': ['*'],
    },
    install_requires=[
        'importlib_resources',
        'PyQt5',
    ],
)
