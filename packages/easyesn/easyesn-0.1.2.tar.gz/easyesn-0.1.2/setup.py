from setuptools import setup, find_packages

setup(name='easyesn',
      version='0.1.2',
      description='',
      url='https://github.com/kalekiu/easyesn',
      author='Roland Zimmermann, Luca Thiede',
      author_email='support@flashtek.de',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'numpy',
            'progressbar2',
            'dill'
      ],
      zip_safe=False)