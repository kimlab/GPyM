#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'GPyM',
       version              = '0.5',
       description          = 'GPM Python Module',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = '',
       package_dir          = {'GPyM':'./'},
       packages             = ['alien'],
       install_requires     = ['numpy'],
      )
