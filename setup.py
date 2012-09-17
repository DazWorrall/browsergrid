from distutils.core import setup

setup(name='browsergrid',
      version='0.1',
      author='Darren Worrall',
      author_email='darren@iweb.co.uk',
      url='https://github.com/DazWorrall/browsergrid',
      description="Grab screenshots in many browsers, powered by selenium",
      include_package_data=True,
      packages=['browsergrid'],
      package_data={'browsergrid': [
        'templates/*.html', 
      ]},
      scripts = ['bin/bg_runner'],
      install_requires = open('requirements.txt').readlines(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                  ],
     )
