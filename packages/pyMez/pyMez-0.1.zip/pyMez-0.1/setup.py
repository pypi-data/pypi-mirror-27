#-----------------------------------------------------------------------------
# Name:        setup
# Purpose:    
# Author:      Aric Sanders
# Created:     12/30/2017
# License:     MIT License
#-----------------------------------------------------------------------------
""" Module for distribution """
#-----------------------------------------------------------------------------
# Standard Imports
from distutils.core import setup
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':


    setup(
        name='pyMez',
        packages=['pyMez'],  # this must be the same as the name above
        version='0.1',
        description='Measurement, Analysis and Data Management Software. To load the API interface use from pyMeasure import *.',
        author='Aric Sanders',
        author_email='aric.sanders@gmail.com',
        url='https://github.com/aricsanders/pyMez',  # use the URL to the github repo
        download_url='https://github.com/aricsanders/pyMez.git',  # I'll explain this in a second
        keywords=['measurement', 'data handling', 'example'],  # arbitrary keywords
        classifiers=[],
		install_requires=['markdown'],
    )
    