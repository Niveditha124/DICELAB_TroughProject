import init1D

def stringify_field(filename: str, field):
    '''
    Takes filename and field object to output to file like .mat file in Matlab
    '''

    f = open(filename, 'w')
    output = 'field.x: ' + str(field.x) + '\n\n'
    output += 'field.y: '+ str(field.y) + '\n\n'
    output += 'field.z_m: ' + str(field.z_m) + '\n\n'
    output += 'field.c_m: ' + str(field.c_m) + '\n\n'
    output += 'field.k_m: ' + str(field.k_m) + '\n\n'
    output += 'field.z_r: ' + str(field.z_r) + '\n\n'
    output += 'field.z_b:' + str(field.z_b) + '\n\n'
    output += 'field.u: ' + str(field.u) + '\n\n'
    output += 'field.v: ' + str(field.v) + '\n\n'
    # output += 'L1: ' + str(field.L1) + '\n'
    # output += 'S1: ' + str(field.S1) + '\n'
    # output += 'p1: ' + str(field.p1) + '\n'
    # output += 'L2: ' + str(field.L2) + '\n'
    # output += 'S2: ' + str(field.S2) + '\n'
    # output += 'p2: ' + str(field.p2) + '\n'
    # output += 'L3: ' + str(field.L3) + '\n'
    # output += 'S3: ' + str(field.S3) + '\n'
    # output += 'p3: ' + str(field.p3) + '\n'

    output += 'L: ' + str(field.L) + '\n'
    output += 'S: ' + str(field.S) + '\n'
    output += 'p: ' + str(field.p) + '\n'


    output += 'n: ' + str(field.n) + '\n'
    output += 'U_up: ' + str(field.U_up) + '\n'
    output += 'H_up: ' + str(field.H_up) + '\n'
    output += 'C_up: ' + str(field.C_up) + '\n'
    output += 'Q_up: ' + str(field.Q_up) + '\n'
    output += 'K_up: ' + str(field.K_up) + '\n'
    output += 't: ' + str(field.t) + '\n\n'
    f.write(output)
    f.close()

def parse_field(filename: str, field):
    print('to be completed')
    
    