# UPDATE
# After Python 3.9 with walrus operator we able to use muc simpler synthax:

(f := open(filename, 'w')).write(something)
f.closed or f.close()

# All follows written before this invention and not actual anymore.




# We can read/write files just in one line: 
#
# >>> open(path, 'w').write(string)
# or 
# >>> print(open(path, 'r').read())
#
# But there we have a problem with unclosed I/O stream. We cannot
# close just readen/written file manually. Even via deep inspection.
# F.e., see https://bugs.python.org/issue37350
#
# Using "with" or assign "open()" to the variable 
# are not applicable if we need a single-line syntax.
#
# This class works the same as "open", but controls the file for 
# it always have to be closed after this methods done.
#
# Also it helps to avoid "with" construction making code flatter.
#
# Usage:
# from w_open import WOpen


class WOpen:
    """ Wraps open().write() and open().read() for keeping files always closed """
    
    def __init__(self, *args, **kwargs):
        self.f = open(*args, *kwargs)
        self.is_closed = False
    
    def write(self, src):
        self.f.write(src)
        self.f.close()
        if self.f.closed: self.is_closed = True
        return self.is_closed
    
    def read(self):
        n = self.f.read()
        self.f.close()
        if self.f.closed: self.is_closed = True
        return n

    
if __name__ == "__main__":
    
    print (
           { True:  "File succesfully written",
             False: "File was not closed" } [ WOpen('test.txt', 'w').write('wow!') ]
           )
    
    print ( WOpen('test.txt', 'r').read() )
