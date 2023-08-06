from setuptools import setup

setup(name='cutecare-py',
      version='0.16',
      description='Library to read data from CuteCare Bluetooth LE DIY sensor',
      url='https://github.com/cutecare/cutecare-py',
      author='Evgeny Savitsky',
      author_email='evgeny.savitsky@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: System :: Hardware :: Hardware Drivers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      packages=['cutecare','cutecare.backends'],
      keywords='home assistant sensor bluetooth low-energy ble',
      zip_safe=False,
      extras_require={'testing': ['pyest']}
      )
