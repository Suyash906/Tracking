class fileObject:
    parts = []
    extension = ""
    filename = ""
    size = ""

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def add_part(self, part):
        self.parts.append(part)

    def set_extension(self, extension):
        #check for supported extension
        self.extension = extension

    def set_filename(self, filename):
        #create a new unique filename
        self.filename = filename

    def set_size(self, size):
        #create a new unique filename
        self.size = size

    def get_filename(self):
        return self.filename