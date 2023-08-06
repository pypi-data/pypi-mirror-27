from setuptools import setup

setup(
    name='nimays-solitaire',
    version='1.0.0',
    python_requires='>=3',
    scripts=['bin/nimay-solitaire'],
    packages=['nimay_solitaire'],
    install_requires=['pygame'],
    package_data={'nimay_solitaire': ['images/*']},
)
