from setuptools import setup, find_packages

setup(
    name='pnock',
    version='0.1.1',
    description='Quickly finds which hosts are running a server on a given port on your local network.',
    url='https://github.com/wildarch/pnock',
    author='Daan de Graaf',
    author_email='daandegraaf9@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: System :: Networking',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='ssh discover raspberry pi',

    py_modules=['pnock'],

    install_requires=[],

    entry_points={  # Optional
        'console_scripts': [
            'pnock=pnock:main',
        ],
    },
)
