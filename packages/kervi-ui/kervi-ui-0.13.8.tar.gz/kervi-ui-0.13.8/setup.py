from distutils.core import setup
import distutils
from kervi.ui.version import VERSION

try:
    distutils.dir_util.remove_tree("dist")
except:
    pass

setup(
    name='kervi-ui',
    packages=['kervi/ui'],
    version=VERSION,
    description='UI module for the kervi framework. It is included as dependency when kervi in installed.',
    author='Tim Wentzlau',
    author_email='tim.wentzlau@gmail.com',
    url='https://github.com/kervi/kervi-ui',
    download_url='https://github.com/wentzlau/kervi-ui/archive/v1.0-alpha.tar.gz',
    keywords=['ui', 'robotic', 'automation'],
    classifiers=[],
    package_data={
        'kervi_ui': [
            'ui/web/dist/*.html',
            'ui/web/dist/*.js',
            'ui/web/dist/*.css',
            'ui/web/dist/*.map',
            'ui/web/dist/*.ico',
            'ui/web/dist/*.png',
            'ui/web/dist/*.eot',
            'ui/web/dist/*.svg',
            'ui/web/dist/*.woff',
            'ui/web/dist/*.woff2',
            'ui/web/dist/*.ttf'
            ],
    },
)
