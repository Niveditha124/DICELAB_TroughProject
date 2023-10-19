import jsonpickle

def encode(titleCounter, field, field_0, field_prev, par, dt):
    filename = './serialized/field' + str(titleCounter) + '.txt'
    encoded = jsonpickle.encode(field)
    f = open(filename, 'w')
    f.write(encoded)
    f.close()

def decode(filename):
    f = open(filename, 'r')
    return jsonpickle.decode(f.read())



def __init__ (self, field, values):
    self.field = field