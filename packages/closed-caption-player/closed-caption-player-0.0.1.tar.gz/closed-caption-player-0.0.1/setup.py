from distutils.core import setup

setup(
    name='closed-caption-player',
    version='0.0.1',
    author='okay',
    author_email='okay.zed+ccp@gmail.com',
    packages=['closed_caption_player' ],
    package_dir={ 'closed_caption_player': '' },
    package_data={'closed_caption_player': [
        'README.md',
        'src/*',
    ]},
    scripts=['bin/ccp'],
    url='http://github.com/autolux/closed-caption-player',
    license='MIT',
    description='a live closed captioning playback system',
    long_description=open('README.md').read(),
    install_requires=[
    "requests",
    "untangle",
    ],
    )

