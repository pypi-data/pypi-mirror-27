from setuptools import setup, find_packages

setup(
    name="pypeep",
    version="0.1.0",
    keywords=("PyCharm", "debug", "remote debug"),
    description="debug configurator",
    long_description="Configure Pycharm for remote debugging",
    license="MIT",

    url="https://github.com/cuyu/pypeep",
    author="cuyu",
    author_email="cuyu@splunk.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["paramiko",
                      "docker",
                      "colorama",
                      "psutil"],
    entry_points={
        'console_scripts': ['pypeep = pypeep.main:main']
    }
)
