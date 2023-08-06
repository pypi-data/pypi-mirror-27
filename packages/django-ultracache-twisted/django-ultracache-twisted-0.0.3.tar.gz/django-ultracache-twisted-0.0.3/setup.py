from setuptools import setup


setup(
    name="django-ultracache-twisted",
    version="0.0.3",
    url="http://github.com/praekelt/django-ultracache-twisted",
    license="BSD",
    description="Companion app to django-ultracache that enables proxy invalidation",
    long_description=open("README.rst", "r").read(),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    packages=[
        "purge",
        "twisted.plugins",
    ],
    package_data={
        "twisted.plugins": ["twisted/plugins/purge_plugin.py"],
    },
    include_package_data=True,
    install_requires=[
        "twisted",
        "PyYAML",
        "requests",
        "treq",
        "pika>=0.11.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)
