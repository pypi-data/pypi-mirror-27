from setuptools import setup, find_packages

setup(
    name='django-ajax-csrf',
    version='1.0.2',
    description='Django app - bundle csrf token additioner for JavaScript',
    long_description=open('README.rst', 'r').read(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    author='nnsnodnb',
    author_email='ahr63_gej@me.com',
    url='https://github.com/nnsnodnb/django-ajax-csrf',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    keywords='django csrf staticfiles',
    platforms=['any'],
    install_requires=['Django>=1.7'],
)

