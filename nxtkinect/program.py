'''
    program.py
    
    Main script.
    Usage:
    python program.py
'''
from nxtkinect.analyzer import Analyzer
import freenect

if __name__ == '__main__':
    analyzer = Analyzer()    
    freenect.runloop(depth = analyzer.new_depth, video = analyzer.new_image, body = analyzer.body)
