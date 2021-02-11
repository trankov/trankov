# The recommended way to work with files is to use a 
# context manager "with" for an open() method.
#
# But Python also provides us a chain notation.
# We can write into a file just in one line: open(path, 'w').write(str)
#
# But there we have a problem with unclosed i/o stream. We cannot
# close just written file manually if it don't assigned to variable.
# F.e., see https://bugs.python.org/issue37350
#
# The same problem with one-line command to read from file.
# In var = open(path, 'r').read() "var" is String, so we
# cannot close the file pointed in path.
#
# That's why all manuals force us to use "with" or assign open() to
# temporarly variable for closing it manually.
#
# But what with Zen? "Simple is better than complex", "Flat is better than 
# nested", "Readability counts"...
#
# One-line is simpler, flatter and much readable than any other way.
#
# To solve this issue I use a small class for wrapping 
# standard "open" metod and it's write() and read() methods.
# It works the same as "open", but controls the file for 
# it always have to be closed.
#
# The class should not be assigned to variable, 
# because it closing the file after any method
# (both read and write) and instance became useless.
# Use it only for stand-alone single line mode.

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
           {True: "File succesfully closed",
            False: "File was not closed"} \
                [w_open('test.txt', 'w').write('wow!')]
           )
    print (w_open('test.txt', 'r').read())
