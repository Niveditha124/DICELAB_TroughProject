import jsonpickle
import sys

class Serializer:
    
    # def __init__ (self, field, field_0, field_prev, par, dt):
    #     '''Serializer object contains field, field_0, field_prev, par, dt'''
    #     self.field = field
    #     self.field_0 = field_0
    #     self.field_prev = field_prev
    #     self.par = par
    #     self.dt = dt
    
    def __init__ (self, **kwargs):
        '''Serializer object contains field, field_0, field_prev, par, dt'''
        if len(kwargs) == 5:
            self.field = kwargs['field']
            self.field_0 = kwargs['field_0']
            self.field_prev = kwargs['field_prev']
            self.par = kwargs['par']
            self.dt = kwargs['dt']
        # else:
        #     print('Please specify field, field_0, field_prev, par, dt variables')
        #     sys.exit()
    
    @classmethod
    def encode(self, titleCounter):
        # Perform check to see if this folder exists // actually already done in geoturbid1D.py
        filename = './serialized/field' + str(titleCounter) + '.txt'
        # Encodes the entire Serializer object that contains field, field_0, field_prev, par, dt
        encoded = jsonpickle.encode(self)
        f = open(filename, 'w')
        f.write(encoded)
        f.close()
        
    @classmethod
    def decode(self,filename):
        # Read file in that contains field, field_0, field_prev, par, dt
        f = open(filename, 'r')
        self.field = f.field
        self.field_0 = f.field_0
        self.field_prev = f.field_prev
        self.par = f.par
        self.dt = f.dt
        print(f.dt)
        
        return jsonpickle.decode(f.read())

    
    
    
    
    