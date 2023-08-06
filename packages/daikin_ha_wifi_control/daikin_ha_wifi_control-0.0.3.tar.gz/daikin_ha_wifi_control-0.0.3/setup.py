from setuptools import setup

setup(
    name='daikin_ha_wifi_control',  # Required
    version='0.0.3',  # Required
    description='Classes for controlling Daikin AC and air purifiers over WLAN',  # Required
    url='https://github.com/lmpprk/daikin_ha_wifi_control',  # Optional
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='daikin homeautomation',
    py_modules=["DaikinInterface"],
    install_requires=['requests'],
)
