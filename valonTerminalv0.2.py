'''
Description:
This program uses pySerial python library 
to communicate with the Valon Frequency Synthesizer.
Forwarding input from python onto the serial console.  
Version: 2.0
'''
import serial 
import time 

'''
NOTE:The address is different depending on 
your Opertating System.
You can use pySerial's tool to see the ports 
that available. 
excute this on terminal:
python -m serial.tools.list_ports

Linux: /dev/ttyUSB0
Mac: /dev/tty.usbserial-A5343FPC
Windows: ? 
'''
port = serial.Serial('/dev/tty.usbserial-A5343FPC', baudrate=9600)
#                      ^PORT ADDRESS CHANGE THIS^

def foo_frequency():
    '''
    This function sets a tone with a 2 second 
    delay. 

    Parameters:
    None
    
    Returns:
    None 
    '''
    send('mode cw')
    for i in range(5,10):
        time.sleep(2) #delay 
        send('frequency ' + str(100 * i) + 'm')
        

def send(cmd):
    '''
    This function sends input to the native serial console
    and prints output. 

    Parameters:
    cmd: a str type, command.
    
    Returns:
    None 
    '''
    port.write(cmd.encode() + '\r'.encode())
    port.readline() #prevent ts
    time.sleep(.1)

    #Reads output
    output = ''
    num_lines = 0 
    while True:
        output += port.read().decode()
        if "-->" in output:
            print(output.strip("-->"))
            num_lines += 1 

        if(num_lines >= 1):
            break 


def main():
    ''' 
    Continuous user prompt  until exit string 
    is passed in. 
    
    Can also make methods for custom applications, 
    i have foo_frequency method which changes 
    frequency every 2 seconds. 

    #Note: additional system requirement.
    1. Virtual com port driver
    2. Python 3.+
    ''' 
    custom_dct = {'foo': foo_frequency}
    print('Welcome to the pyValon Terminal!\nEnter help to list commands.')
    while True:
        user_input = input('valon:> ')

        if user_input != 'exit':
            if user_input in custom_dct:
                custom_dct[user_input]()

            else:
                send(user_input)
               
        else:
            print('Exiting pyValon')
            port.close()
            return 
main()




