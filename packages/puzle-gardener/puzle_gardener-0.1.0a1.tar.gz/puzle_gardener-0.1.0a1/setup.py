from setuptools import setup, find_packages

config_files = ["src/config/prompt_models/gardener_config.yml"]

def parse_requirements(filename):
    lines = (line.strip() for line in open(filename))
    return [line for line in lines if line and not line.startswith("#")]


# Get requirements from file generated by pipreqs freeze
install_requirements = parse_requirements('src/requirements.txt')
requirements = [str(item) for item in install_requirements]


setup(
    name="puzle_gardener",
    version="0.1.0a1",
    description="With Gardener, bootstrap a project has never been so easy !",
    author="Cedric Chariere Fiedler",
    author_email="chariere.fiedler.cedric@gmail.com",
    install_requires=requirements,
    packages=find_packages(),
    package_data={'': config_files},
    python_requires='>=3.6',
    include_package_data=True,
    license='GPL',
    entry_points={'console_scripts':['gardener = src:main'] },
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    ]
)
