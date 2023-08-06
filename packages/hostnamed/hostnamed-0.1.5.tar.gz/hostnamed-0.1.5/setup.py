import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "django",
    "zencore_django",
    "zencore_utils",
    "click",
    "requests",
]

setup(
    name="hostnamed",
    version="0.1.5",
    description="Dynamic hostname manage and update.",
    long_description=long_description,
    url="https://github.com/appstore-zencore/hostnamed",
    author="zencore",
    author_email="appstore@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['hostnamed'],
    packages=find_packages("src", exclude=["src", "manage.py"]),
    package_dir={"": "src"},
    requires=requires,
    install_requires=requires,
    scripts=[
        "src/scripts/hostname-ctrl.py",
        "src/scripts/hostname-ctrl",
    ],
    zip_safe=False,
    include_package_data=True,
    package_data={
        "": ["*.*"],
    },
)
