from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="oslo.config.comparator",
    version="0.3",
    packages=find_packages(),
    install_requires=['click'],
    author="Yang Youseok",
    author_email="ileixe@gmail.com",
    url="https://github.com/Xeite/oslo.config.comparator",
    description="OpenStack configure file comparator.",
    long_description=readme(),
    license="MIT",
    keywords='OpenStack oslo.config',
    python_requires='>=3.6',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],

    entry_points={
        'console_scripts': [
            'oslo-config-comparator = oslo_config_comparator.config_comparator:main',
        ],
    }
)
