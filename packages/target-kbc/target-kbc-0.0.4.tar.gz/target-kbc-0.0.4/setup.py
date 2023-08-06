
from setuptools import setup
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

setup(name='target-kbc',
      version='0.0.4',
      description='Singer.io target for importing data into KBC',
      author='Leo',
      author_email='cleojanten@hotmail.com',
      url='https://bitbucket.org/chanleoc/target-keboola',
      packages=['target_kbc'],
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['target_kbc'],
      install_requires=[
          'jsonschema==2.6.0',
          'singer-python==2.1.4',
          'kbcstorage==0.1.3.dev33+g9ee473e',
          'requests==2.13.0'
      ],
      entry_points='''
          [console_scripts]
          target-kbc=target_kbc:main
      ''',
)