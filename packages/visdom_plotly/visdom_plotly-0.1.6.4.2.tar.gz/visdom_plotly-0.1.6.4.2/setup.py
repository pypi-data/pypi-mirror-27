from setuptools import setup

readme = open('README.md').read()

requirements = [
    'numpy>=1.8',
    'pillow',
    'requests',
    'tornado',
    'pyzmq',
    'six',
    'torchfile',
    'plotly',
]

setup(
    # Metadata
    name='visdom_plotly',
    version='0.1.6.4.2',
    author='Hadi Rahmat-Khah',
    author_email='rahmatkhah@gmail.com',
    url='https://github.com/rahmatkhah/visdom',
    download_url='https://github.com/rahmatkhah/visdom/archive/0.1.6.4.1.tar.gz',
    description='Visdom with the plot.ly support',
    long_description=readme,
    license='CC-BY-4.0',

    # Package info
    packages=['visdom_plotly'],
    package_dir={'visdom_plotly': 'py'},
    package_data={'visdom_plotly': ['static/*.*', 'static/**/*']},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
)
