'''
    program.py
    
    Main script.
    Usage:
    python program.py
'''
from nxtkinect.analyzer import Analyzer
import freenect
import sys

if __name__ == '__main__':
    nousb = False
    for arg in sys.argv:
        if arg == '-nousb':
            nousb = True
    
    
    
    analyzer = Analyzer(nousb = nousb)    
    freenect.runloop(depth = analyzer.new_depth, video = analyzer.new_image, body = analyzer.body)
