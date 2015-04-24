from setuptools import setup, find_packages

setup(
    name = "django-allcontacts",
    url = "http://github.com/suselrd/django-allcontacts/",
    author = "Susel Ruiz Duran",
    author_email = "suselrd@gmail.com",
    version = "0.1.2",
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    description = "Contacts for Django",
    install_requires=['django>=1.6.1', ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],

)
