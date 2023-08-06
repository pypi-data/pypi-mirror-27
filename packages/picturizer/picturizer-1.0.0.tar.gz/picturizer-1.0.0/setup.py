from setuptools import setup, find_packages

setup(
    name='picturizer',
    version='1.0.0',
    keywords=['image', 'string', 'image to string', 'Monsoir'],
    description='Transform picture into picture-like string',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],

    url='https://github.com/Monsoir/picturizer',
    author='Monsoir',
    author_email='monwingyeung@gmail.com',

    packages=find_packages(),
    include_package_data=False,
    platforms=["any"],
    install_requires=['Pillow'],
    python_requires='>3',
    entry_points={
        'console_scripts': [
            'picturize = picturizer.picturize:picturize',
        ]
    }
)