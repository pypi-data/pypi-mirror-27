from setuptools import setup, find_packages

with open('README.md') as fd:
    long_desc = fd.read()

setup(
    name='mapser',
    version='0.2.0',
    author='kazbeel',
    author_email='woozycoder@gmail.com',
    description='Generated map file analyzer',
    license='MIT',
    keywords='embedded arm cortex-m map-file analyzer',
    url='https://gitlab.com/kazbeel/mapser',
    packages=find_packages(),
    long_description=long_desc,
    setup_requires=['pytest-runner'],
    tests_require=['mock', 'coverage', 'pytest>=2.8', 'pytest-cov'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development'
    ])
