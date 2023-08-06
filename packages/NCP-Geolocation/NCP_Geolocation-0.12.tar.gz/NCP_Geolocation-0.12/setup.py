from setuptools import setup, find_packages

setup(name='NCP_Geolocation',
      description="""
    This is for Geolocation service of Naver Cloud Platfrom
    
    It is simple to use
    
    1. Import and fill your security code
    ncp_geolocation = NCP_Geolocation_API(oauth_consumer_key="$oauth_consumer_key", secret_key="$secret_key")
    
    2. execute `get_geolocation` function 
    print(ncp_geolocation.get_geolocation("125.209.222.142"))
    
    results : 
    {"returnCode": 0,"requestId": "c2032c47-f678-4de1-b595-461906ea90c4","geoLocation": {"country": "KR","code": "4113558000","r1": "경기도","r2": "성남시 분당구"}}
    """,
      version='0.012',
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
