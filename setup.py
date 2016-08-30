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
       version              = '0.52b',
       description          = 'GPM Python Module',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = 'https://github.com/kimlab/GPyM',
       #package_dir          = {'GPyM':'./'},
       package_dir          = {'GPyM':''},
       packages             = ['GPyM','GPyM.alien'],
       #install_requires     = ['numpy'],

       #include_package_data = True,
       data_files           = [('','config')],

       license              = 'MIT',
      )
