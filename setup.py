#!/usr/bin/env python

from distutils.core import setup

gpmDir  = ''
#gpmDir  = '/tank/hjkim/GPM'

if gpmDir == '':
    raise ValueError, 'gpmDir should be specificed'

setupFile   = open('settings.py','w')
setupFile.write('baseDir = "%s"\n'%gpmDir)
setupFile.close()

setup( name                 = 'GPyM',
       version              = '0.5',
       description          = 'GPM Python Module',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = '',
       package_dir          = {'GPyM':'./'},
       packages             = ['GPyM','GPyM.alien'],
       install_requires     = ['numpy'],
      )
