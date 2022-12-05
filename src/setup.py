from setuptools import setup

install_requires = [
      'loguru==0.6.0',
      'requests==2.28.1',
      'vk-api==11.9.9',
]


setup(name='PyVkBot',
      python_requires='>3.10',
      version='1.0.1',
      description='Chat bot for vk.com',
      packages=['PyVkBot'],
      author='zeph1rr',
      author_email='grianton535@gmail.com',
      license='MIT',
      install_requires=install_requires,
      zip_safe=False,
      url='https://github.com/zeph1rrinc/pyvkbot'
      )
