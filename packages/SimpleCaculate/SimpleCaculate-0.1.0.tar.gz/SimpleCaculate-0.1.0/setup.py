from distutils.core import setup
setup (
        name='SimpleCaculate',
        version='0.1.0',
        author='Mike Hsieh',
        packages=['simplecaculate',],
        scripts=['bin/caculate.py','bin/caculate-test.py'],
        url='https://pypi.python.org/pypi/simplecaculate',
        license='LICENSE.txt',
        description='Useful math',
        long_description=open('README.txt').read(),
        install_requires=[
            "Django >=1.1.1",
            ]
        )
