from setuptools import find_packages, setup

VERSION = (2, 0, 1, 'final', 0)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version


setup(
    name="gofiliate",
    version=get_version(),
    author="iGP Technologies d.o.o.",
    author_email="mgm@igpte.ch",
    license="BSD",
    description="Gofiliate Python bindings.",
    url="https://github.com/mgmonteleone/py-gofiliate-client",
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['requests>=2.18', 'pytest==3.1.3', 'responses', 'numpy', 'pandas', 'arrow'],
    test_suite="tests",
)
