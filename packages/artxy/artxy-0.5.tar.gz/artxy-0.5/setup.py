from distutils.core import setup
setup(
  name = 'artxy',
  packages = ['artxy'],
  version = '0.5',
  description = 'ASCII Art Collection In Python',
  long_description='ASCII Art Collection In Python',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  url = 'https://github.com/kingheshan/xyart',
  download_url = 'https://github.com/kingheshan/xyart/archive/master.zip',
  keywords = ['ascii', 'art', 'python3','python','text'],
  install_requires=[
	  'codecov',
      ],
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Topic :: Text Processing :: Fonts',
    ],
  license='MIT',
)
