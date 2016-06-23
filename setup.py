import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-fcm',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    description='A Django package that enables sending messages using FCM (Firebase Cloud Messaging).',
    long_description=README,
    url='https://www.example.com/',
    author='Chitrank Dixit',
    author_email='chitrankdixit@gmail.com',
    zip_safe=False,
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=1.9',
        'djangorestframework>=3.3.2',
        'pytz>=2015.7',
        'requests>=2.9.1'
    ],
)