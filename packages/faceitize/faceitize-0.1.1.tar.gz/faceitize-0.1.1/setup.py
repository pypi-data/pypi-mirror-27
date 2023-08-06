from setuptools import setup

setup(
    name='faceitize',
    version='0.1.1',
    description='The incredible human to human face swapping package',
    author='Matt Lewis',
    author_email='domattthings@gmail.com',
    license='MIT',
    url='https://github.com/mattmatters/faceitize',
    download_url='https://github.com/mattmatters/faceitize/archive/0.1.1.tar.gz',
    py_modules=['faceitize'],
    packages=['faceitize'],
    install_requires=[
        'numpy',
        'opencv-python',
        'dlib',
        'scikit-image'
    ],
    include_package_data=True
)
