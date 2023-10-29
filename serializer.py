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
        elif len(kwargs) == 0:
            pass
        else:
            print('Please specify field, field_0, field_prev, par, dt variables')
            sys.exit()
    
    @classmethod
    def encode(self, obj, titleCounter, filepath):
        # Perform check to see if this folder exists // actually already done in geoturbid1D.py
        filepath += '/field' + str(titleCounter) + '.txt'
        # Encodes the entire Serializer object that contains field, field_0, field_prev, par, dt
        encoded = jsonpickle.encode(obj)
        f = open(filepath, 'w')
        f.write(encoded)
        f.close()
        
    @classmethod
    def decode(self,filepath):
        # Read file in that contains field, field_0, field_prev, par, dt
        f = open(filepath, 'r')
        # Decode file content to obj Object
        obj = jsonpickle.decode(f.read())
        f.close()
        # Assign parsed values to our variables
        decodedObj = Serializer(field = obj.field, 
                                field_0 = obj.field_0,
                                field_prev = obj.field_prev, 
                                par = obj.par, dt = obj.dt
                                )
        # Return our instance of the object
        return decodedObj
   
