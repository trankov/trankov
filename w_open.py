# We can read/write just in one line: open(path, 'w').write(str)
# or var = open(path, 'r').read()
#
# But there we have a problem with unclosed I/O stream. We cannot
# close just written file manually.
# F.e., see https://bugs.python.org/issue37350
#
# That's why all manuals force us to use "with", or assign open() to
# temporarly variable for closing it manually.
#
# But "Flat is better than nested" and "Readability counts".
# One-line is simpler, flatter and much readable than any other way.
#
# To solve this issue I use a small class for wrapping 
# standard "open" metod and it's write() and read() methods.
# It works the same as "open", but controls the file for 
# it always have to be closed after this methods done.
#
# Usage:
# from w_open import w_open

class w_open:
    "Wraps open().write() and open().read() for keeping files always closed"
    
    def __init__(self, *args, **kwargs):
        self.f = open(*args, *kwargs)
    
    def write(self, src):
        self.f.write(src)
        self.f.close()
        return self.f.closed
    
    def read(self):
        n = self.f.read()
        self.f.close()
        return n

if __name__ == "__main__":
    print (
           {True:  "File succesfully closed",
            False: "File was not closed"} \
                [w_open('test.txt', 'w').write('wow!')]
           )
    print (w_open('test.txt', 'r').read())
