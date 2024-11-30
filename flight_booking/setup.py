from setuptools import setup, find_packages

setup(
    name='flight_booking',  # Package name
    version='1.0.0',  # Initial version
    author='Your Name',  # Your name or organization
    author_email='your.email@example.com',  # Your email
    description='A Python package for flight booking functionality',  # Short description
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
)
