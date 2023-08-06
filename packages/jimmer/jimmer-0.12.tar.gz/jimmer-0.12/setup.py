from setuptools import setup, find_packages

setup(
    name='jimmer',
    version='0.12',
    description='An example of messenger based on JIM protocol.',
    long_description='Jimmer is a simple messenger (server+client) written on Python. Message transfer based on JSON IM Protocol',
    url='https://github.com/ealesid/jimmer',
    keywords=['python', 'messenger', 'JIM', 'JSON IM Protocol'],
    author='Aleksey Sidorov',
    author_email='ealesid@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'PyQt5==5.9', 'SQLAlchemy==1.1.14'
    ],
)
