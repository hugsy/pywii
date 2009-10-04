from config import *

def byte_to_button(byte_value , byte_number):
    """get the list of all buttons set"""
    if not byte_number in (0,1):
        print "Invalid byte range"
        return [ ]

    index = 0
    flag  = 1
    list = [ ]
    
    while index < 0x10 :
#         examining each bit of the 2 first bytes
        button = None
        
        if byte_value & flag :
            if DEBUG :
                print "flag %s up on byte %d at index %s"%(hex(flag),
                                                           byte_number,
                                                           hex(index))
            button = assign_flag_to_button(index, byte_number)
            
            list.append( button )

        flag = flag << 1
        index += 1

    for str_button in list :
        if str_button != '' :
            print str_button+" "
            
    return list

def assign_flag_to_button (idx, byte_num):
    """match a flag to corresponding button"""
#     bit/buttons matching table
    values = range(0,8)
    values[0] = ["left", "2"]
    values[1] = ["right", "1"]
    values[2] = ["down", "B"]
    values[3] = ["up", "A"]
    values[4] = ["+", "-"]
    values[5] = ["", ""]
    values[6] = ["", ""]
    values[7] = ["n/a", "home"]

    try:
        ret = values[idx][byte_num]
    except Exception , e:
        ret = "n/a"
        print "[-]Exception was raised on values (%d, %d) : %s" % (idx,
                                                                   byte_num,
                                                                   e)
            
    return ret
