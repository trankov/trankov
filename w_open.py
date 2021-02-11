class w_open:
    "Wraps open().write() and open().read() for close i/o w/out with ... as..."
    
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
