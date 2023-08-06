from setuptools import setup, find_packages

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='sky-utils',
    url='https://bitbucket.org/sekomy/skypy-utils',
    author='Sekom Yazilim',
    author_email='info@sekomyazilim.com.tr',
    license='MIT',
    description='Sky Utils',
    long_description=long_description,
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=['pytz>=2017.2',
                      'httplib2>=0.10.3',
                      'mock>=2.0.0'],
    setup_requires=[
        'setuptools-scm>1.5.4'
    ],
    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'dirty-tag',
        'write_to': 'sky/utils/__version__.py'
    }
)
