from __future__ import with_statement
from __future__ import unicode_literals
import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "django",
    "PyCryptodome",
]
setup(
    name="ezrsa",
    version="0.1.1",
    description="Easy Rsa Django Application",
    long_description=long_description,
    url="https://github.com/appstore-zencore/ezrsa",
    author="Appstore Zencore",
    author_email="appstore@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords=['ezrsa'],
    packages=find_packages("src", exclude=["src", "manage.py"]),
    package_dir={'':'src'},
    requires=requires,
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
    package_data={
        "": ["*.*"],
    },
)
