#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-twitter',
      version='1.0.6',
      description='Singer.io tap for fetching data from Twitter API',
      author='Bernard Tai',
      author_email='bernietai@gmail.com',
      url='http://singer.io',
      classifiers=['Programming Language :: Python'],
      install_requires=['singer-python>=0.1.0',
                        'python-twitter',
                        'httplib2',
                        'oauth2',
                        'apiclient',
                        'google-api-python-client',
                        'discovery',
                        'oauth2client'
                      ],
      entry_points='''
          [console_scripts]
          tap_twitter=tap_twitter:main
      ''',
      py_modules=['tap-twitter'],      
      data_files = [
          ('schemas', [
            'schemas/blocks.json',
            'schemas/favorites.json',
            'schemas/followers.json',
            'schemas/friends.json',
            'schemas/home_timeline.json',                          
            'schemas/lists.json',
            'schemas/memberships.json',
            'schemas/mentions.json',
            'schemas/replies.json',            
            'schemas/retweets_of_me.json',
            'schemas/subscriptions.json',
            'schemas/user_retweets.json',
            'schemas/user_timeline.json',
            ]
          ),
          ('configs', ['config.json'])
      ],
      include_package_data=True,      
)