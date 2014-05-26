from distutils.core import setup

setup(
    name='Genios',
    version='0.1.0',
    author='Leandro',
    author_email='leandroferreira@cjr.org.br',
    license='LICENSE.txt',
    description='Genios',
    packages=[  'controllers', 'cache','cron','databases',
                'docs','errors','Fluxogramas','languages',
                'Mockups','models','private','sessions',
                'static','uploads','views']
    
)