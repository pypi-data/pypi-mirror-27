from setuptools import setup

setup(name='easyesn',
      version='0.1.1',
      description='',
      url='http://github.com/kalekiu/easyesn',
      author='Roland Zimmermann, Luca Thiede',
      author_email='support@flashtek.de',
      license='MIT',
      packages=['easyesn'],
      keywords = ['esn', 'echo', 'state', 'network', 'recurrent', 'neural', 'network'],
      dependencies = ['dill', 'numpy'],
      zip_safe=False)
