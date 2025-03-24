from setuptools import setup


with open("README.md") as file:
    ld = file.read()

setup(
  name = 'qradar',         
  packages = ['qradar'],
  version = '0.0.2',
  license='MIT',      
  description = 'QRadar client for python with API schema fetching', 
  long_description = ld,
  long_description_content_type = "text/markdown",
  author = 'Chmele',              
  url = 'https://github.com/Chmele/qradar-client',  
  keywords = ['client', 'scripting', 'qradar', 'qradar-api'], 
  requires=[
    "setuptools"
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
  ],
  extras_require={
        "httpx": ["httpx>=0.27"],
        "requests": ["requests>=2.30"]
  },
)