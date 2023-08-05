from setuptools import setup
from jjb_separator_param import __version__


p_name = 'jenkins-job-builder-separator-parameter'

setup(
    name='jjb-separator-param',
    version=__version__,
    description='Jenkins Job Builder Separator Param',
    url='https://github.com/ochirkov/{0}'.format(p_name),
    author='Chyrkov Oleksandr',
    author_email='ironloriin20@gmail.com',
    license='Apache-2.0 license',
    install_requires=['uuid'],
    entry_points={
        'jenkins_jobs.parameters': [
            'separator = jjb_separator_param.separator_param:separator']},
    packages=['jjb_separator_param'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'])
