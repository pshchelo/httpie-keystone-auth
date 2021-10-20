from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-keystone-auth',
    description='OpenStack Keystone auth plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.1.1',
    author='Pavlo Shchelokovskyy',
    author_email='shchelokovskyy@gmail.com',
    license='MIT',
    url='https://github.com/pshchelo/httpie-keystone-auth',
    download_url='https://github.com/pshchelo/httpie-keystone-auth',
    py_modules=['httpie_keystone_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_keystone_auth = httpie_keystone_auth:KeystoneAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=2.0.0',
        'openstacksdk>=0.59.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
