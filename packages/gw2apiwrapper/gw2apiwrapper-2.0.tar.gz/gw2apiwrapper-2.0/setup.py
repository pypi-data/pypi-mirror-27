from setuptools import setup

setup(
    name='gw2apiwrapper',
    version='2.0',
    description='A simple wrapper around the offical Guild Wars 2 JSON API.',
    url='https://github.com/PatchesPrime/gw2apiwrapper.git',
    author='R. "Patches" S.',
    author_email='patches@nullcorp.org',
    license='MIT',
    packages=['gw2apiwrapper'],
    install_requires=['requests'],
    zip_safe=False
)
