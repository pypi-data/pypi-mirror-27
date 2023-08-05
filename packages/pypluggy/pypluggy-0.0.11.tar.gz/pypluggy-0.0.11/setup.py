import setuptools

setuptools.setup(
    name='pypluggy',
    version='0.0.11',
    description='pypluggy is a lightweight plugin framework for python',
    long_description='pypluggy is a lightweight plugin framework for python',
    url='https://github.com/veltzer/pypluggy',
    download_url='https://github.com/veltzer/pypluggy',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='plugin python',
    packages=setuptools.find_packages(),
)
