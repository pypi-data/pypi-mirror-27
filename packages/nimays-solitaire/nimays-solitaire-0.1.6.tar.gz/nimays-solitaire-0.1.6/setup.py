from setuptools import setup

setup(
    name='nimays-solitaire',
    version='0.1.6',
    python_requires='>=3',
    scripts=['bin/nimay-solitaire'],
    packages=['nimay_solitaire'],
    install_requires=['pygame'],
    package_data={'nimay_solitaire': ['images/*']},
)
