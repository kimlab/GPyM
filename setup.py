from distutils.core import setup

'''
gpmDir  = ''

if gpmDir == '':
    print gpmDir
    raise ValueError, 'gpmDir should be specificed'

setupFile   = open('settings.py','w')
setupFile.write('baseDir = "%s"\n'%gpmDir)
setupFile.close()
'''

setup( name                 = 'GPyM',
       version              = '0.60b',
       description          = 'GPM Python Module',
       long_description     = ''' long_description to be written. ''',

       classifiers          = [
                            'Development Status :: 4 - Beta',
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 2.7',
                            'Topic :: Scientific/Engineering :: Atmospheric Science',
                            ],
       keywords             = 'precipitation satellite gpm trmm jaxa',
       url                  = 'https://github.com/kimlab/GPyM',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       license              = 'MIT',

       package_dir          = {'GPyM':''},
       packages             = ['GPyM','GPyM.alien'],
       package_data         = {'': ['config'],
                            },
       install_requires     = ['numpy'],
       include_package_data = True,
       zip_safe             = True,
      )
