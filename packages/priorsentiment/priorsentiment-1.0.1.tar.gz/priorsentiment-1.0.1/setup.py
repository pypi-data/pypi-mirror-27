from setuptools import setup, find_packages
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import nltk

setup(
    name='priorsentiment',
    version = '1.0.1',
    description='sentiment analysis using prior knowledge',
    author='WANJIE WANG, GUANDA WANG, JIAYI LIU',
    author_email='guandaw2@illinois.edu',
    packages=find_packages()

)
