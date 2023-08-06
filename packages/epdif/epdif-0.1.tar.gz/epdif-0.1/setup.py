from setuptools import setup

setup(name='epdif',
      version='0.1',
      description='EPD hardware interface implements (GPIO, SPI)',
      url='https://github.com/t4skforce/epdif',
      author='Yehui from Waveshare',
      author_email='service@waveshare.com',
      license='GPL',
      packages=['epdif'],
      install_requires=[
          'spidev',
          'RPi.GPIO'
      ],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
      ],
      zip_safe=False)
