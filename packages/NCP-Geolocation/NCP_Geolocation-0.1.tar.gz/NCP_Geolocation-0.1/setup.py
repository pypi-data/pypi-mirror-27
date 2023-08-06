from setuptools import setup, find_packages

setup(name='NCP_Geolocation',
      description='This is for Geolocation service of Naver Cloud Platfrom',
      version='0.01',
      url='https://github.com/ultimatelife/NCP_Geolocation.git',
      author='geonwoo.kim',
      author_email='drama0708@gmail.com',
      license='Naver Cloud Platform',
      classifiers=[
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(),
      install_requires=[
          'requests>=2.17.3'
      ]
      )
