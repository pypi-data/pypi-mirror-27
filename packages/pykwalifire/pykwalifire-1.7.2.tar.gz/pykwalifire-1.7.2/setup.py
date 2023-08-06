try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name="pykwalifire",
    version="1.7.2",
    description='Python lib/cli for JSON/YAML schema validation, fork '
                'of pykwalify with added features',
    long_description=readme,
    author="Stephan Druskat",
    author_email="mail@sdruskat.net",
    maintainer='Stephan Druskat',
    maintainer_email='mail@sdruskat.net',
    license='MIT',
    packages=['pykwalify'],
    url='http://github.com/sdruskat/pykwalifire',
    extras_require={
        'ruamel': ["ruamel.yaml>=0.11.0,<0.12.0"],
    },
    entry_points={
        'console_scripts': [
            'pykwalifire = pykwalify.cli:cli_entrypoint',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
        'PyYAML>=3.11',
        'python-dateutil>=2.4.2',
    ],
    classifiers=(
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    )
)
