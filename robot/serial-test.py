import serial
import time 
import asyncio 
import re

#https://stackoverflow.com/questions/17589942/using-pyserial-to-send-binary-data

startTime = time.time()

ser = serial.Serial('COM7', 9600) 
#/dev/ttyACM0 pour linux (débrancher et rebrancher en tapant ls /dev/tty* pour trouver le bon port)

CommandDictionnary = {
                "led": [0x4c, 0x3a,],
                "led_2": [0x6c, 0x3a,],
                "motor": [0x4d, 0x3a],
                "motor_2": [0x6d, 0x3a],
                "servo": [0x53,0x3a,],
                "servo_2": [0x73,0x3a,],
                "nothing": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                "end": [0xff]
                }
TimeOut1Dictionnary = {
                "\x4c": 2,
                "\x6c": 2,
                "\x4d": 2,
                "\x6d": 2,
                "\x53": 2,
                "\x73": 2,
                "\x00": 0,
                "": 0
                }

commandStack = []
trashStack = []

async def CheckTimer():
        print("Checking timer---")
        for commandPacket in list(commandStack):
                print(commandPacket, "in commandStack")
                if commandPacket[1]=='TimeOut0':
                        
                        timeOut0value = 1
                
                        print(time.time()-commandPacket[2])
                        if time.time()-commandPacket[2]>timeOut0value:
                                print("TimeOut0 for command:", commandPacket[0], "; sending command again")
                                commandStack.remove(commandPacket)
                                await SendCommand([0x55])#commandPacket[0])
                
                elif commandPacket[1]=='TimeOut1':
                        
                        timeOut1value = TimeOut1Dictionnary[commandPacket[0][0:1]]
                        
                        print(time.time()-commandPacket[2])
                        if time.time()-commandPacket[2]>timeOut1value:
                                print("TimeOut1 for command:", commandPacket[0], "; sending command again")
                                commandStack.remove(commandPacket)
                                #await SendCommand([0x55])#commandPacket[0])


async def SetTimeOut1(response):
        print("Setting timeout1---")
        for commandPacket in commandStack:
                if commandPacket[0][0:1]==response[0:1]: #check if response is in commandStack
                        commandPacket[1]='TimeOut1'
                        commandPacket[2]=time.time()
                        break

async def CheckResponse(response):
        print("Checking response---")
        for command in commandStack:
                if command[0][0:5]==response[0:5]: #check if response is in commandStack
                        if command[-2:]=='ok': #check if response is ok
                                commandStack.remove(command) #remove command from commandStack
                        else:#response is not ok
                                await SendCommand(command[0]) #send command again
                        break
                
async def ReadSerial():   
        print("Reading serial---")
        response = ser.read_all()
        if response:
                print("rec-",response.decode() )
                if 'rd' in response.decode():
                        print("command received:", response.decode())
                        await SetTimeOut1(response.decode())
                else:
                        print("CheckingResponse")
                        await CheckResponse(response.decode())#command pas response
        else:
                print("No response")


#ser.write(serial.to_bytes(HexCommand))
async def SendCommand(argCOMMAND=None):
        print("Sending command---") 
        print("commandStack:", commandStack)
        if argCOMMAND:
                command = argCOMMAND
                print("argCOMMAND:", argCOMMAND)
        else:
                
                inputCommand = input("Command: ")
                
                try:    
                        inputCommand = inputCommand.split(":") #split inputCommand into a list
                        #inputCommand[1] = [int(inputCommand[1][0])+48, int(inputCommand[1][1])+48, int(inputCommand[1][2])+48, int(inputCommand[1][3])+48 ]
                        #inputCommand[2] = [int(inputCommand[2][0])+48, int(inputCommand[2][1])+48, int(inputCommand[2][2])+48, int(inputCommand[2][3])+48 ]
                        
                        dotIndex = inputCommand[1].index('.')
                        i = 0
                        command1=[]
                        while(i != dotIndex):
                                command1.append(int(inputCommand[1][i])+48)
                                i+=1
                        command1.append(0x2E)
                        i = dotIndex+1 
                        while (i != len(inputCommand[1])):
                                command1.append(int(inputCommand[1][i])+48)
                                i+=1
                        #print(command1)
                        
                        dotIndex = inputCommand[2].index('.')
                        i = 0
                        command2=[]
                        while(i != dotIndex):
                                command2.append(int(inputCommand[2][i])+48)
                                i+=1
                        command2.append(0x2E)
                        i = dotIndex+1
                        while (i != len(inputCommand[2])):
                                command2.append(int(inputCommand[2][i])+48)
                                i+=1
                        #print(command2)
                        
                        dotIndex = inputCommand[3].index('.')
                        i = 0
                        command3=[]
                        while(i != dotIndex):
                                command3.append(int(inputCommand[3][i])+48)
                                i+=1
                        command3.append(0x2E)
                        i = dotIndex+1
                        while (i != len(inputCommand[3])):
                                command3.append(int(inputCommand[3][i])+48)
                                i+=1
                        #print(command3)
                        
                        #inputCommand[1] = [int(inputCommand[1][0])+48, 0x2E, int(inputCommand[1][2])+48, int(inputCommand[1][3])+48 ]
                        #inputCommand[2] = [int(inputCommand[2][0])+48, 0x2E, int(inputCommand[2][2])+48, int(inputCommand[2][3])+48 ]
                        inputCommand[1] = command1
                        inputCommand[2] = command2
                        inputCommand[3] = command3
                        
                        command = CommandDictionnary[inputCommand[0]]+inputCommand[1]+[0x3a]+inputCommand[2]+[0x3a]+inputCommand[3]+[0x3a,0x7e]
                except:
                        print("Command not found")
                        return 0

        commandStartTime=time.time()
        commandStack.append([bytearray(command).decode(), 'TimeOut0', commandStartTime])
        

        ser.write(bytearray(command))

        time.sleep(0.1)#dangereux
        
async def Strategy(snvironnement, state):
        print("")
#run the main function in an event loopled

def commandStackState():
        print(commandStack)
        
async def main():

        while True:
                task_1 = asyncio.create_task(SendCommand())
                task_2 = asyncio.create_task(ReadSerial())
                task_3 = asyncio.create_task(CheckTimer())
                
                await asyncio.wait([task_1, task_2, task_3])


        
        #while True:
                #await asyncio.gather(ReadSerial(), CheckTimer())

async def readOnly():
        await SendCommand()
        task_2 = asyncio.create_task(ReadSerial())
        task_3 = asyncio.create_task(CheckTimer())
        #await asyncio.sleep(0.5)
        await asyncio.wait([task_2, task_3])


#asyncio.run(main())
asyncio.run(readOnly())
#print(commandStack)
#asyncio.run(SendCommand())



#asyncio.run(ReadSerial())
#print(commandStack)