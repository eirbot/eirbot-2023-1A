import serial
import serial.tools.list_ports
import time 
import asyncio 
import re

#https://stackoverflow.com/questions/17589942/using-pyserial-to-send-binary-data

startTime = time.time()

class SerialControl:
        
        #ser = serial.Serial('COM7', 9600)
        #/dev/ttyACM0 pour linux (débrancher et rebrancher en tapant ls /dev/tty* pour trouver le bon port)

        CommandDictionnary = {
                "led": [0x4c, 0x3a,],
                "led_2": [0x6c, 0x3a,],
                "motor": [0x4d, 0x3a],
                "motor_2": [0x6d, 0x3a],
                "servor": [0x53,0x3a,],
                "servol": [0x54,0x3a,],
                "canondeploy": [0x73, 0x3a,],
                "canonretract": [0x74, 0x3a,],
                "canonfire": [0x5a, 0x3a,],
                "nothing": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                "pause": [0x7d, 0x3a],
                "unpause": [0x7c, 0x3a]
                }
        
        TimeOut1Dictionnary = {
                        "\x4c": 2,
                        "\x6c": 2,
                        "\x4d": 2,
                        "\x6d": 2,
                        "\x53": 2,
                        "\x54": 2,
                        "\x73": 2,
                        "\x74": 2,
                        "\x7c": 2,
                        "\x5a": 2,
                        "\x7d": 2,
                        "\x00": 0,
                        "": 0
                        }
        
        commandStack = []
        trashStack = []
                
        def __init__(self):
                print("Listing ports---")
                ports = serial.tools.list_ports.comports()
                for port in ports:
                        if "STMicroelectronics" in port.description:
                                print("Found STM32 port:", port.device)
                                self.ser = serial.Serial(port.device, 9600)
                                #break
                        if "Silicon Labs" in port.description:
                                print("Found Lidar port:", port.device)
                                self.lidarport = port.device
                                #break
                
        async def CheckTimer(self):
                print("Checking timer---")
                for commandPacket in list(self.commandStack):
                        print(commandPacket, "in commandStack")
                        if commandPacket[1]=='TimeOut0':

                                timeOut0value = 1

                                print(time.time()-commandPacket[2])
                                if time.time()-commandPacket[2]>timeOut0value:
                                        print("TimeOut0 for command:", commandPacket[0], "; sending command again")
                                        self.commandStack.remove(commandPacket)
                                        #await self.SendCommand([0x55])#commandPacket[0])

                        elif commandPacket[1]=='TimeOut1':

                                timeOut1value = self.TimeOut1Dictionnary[commandPacket[0][0:1]]

                                print(time.time()-commandPacket[2])
                                if time.time()-commandPacket[2]>timeOut1value:
                                        print("TimeOut1 for command:", commandPacket[0], "; sending command again")
                                        self.commandStack.remove(commandPacket)
                                        #await SendCommand([0x55])#commandPacket[0])


        async def SetTimeOut1(self, response):
                print("Setting timeout1---")
                for commandPacket in self.commandStack:
                        if commandPacket[0][0:1]==response[0:1]: #check if response is in commandStack
                                commandPacket[1]='TimeOut1'
                                commandPacket[2]=time.time()
                                break

        async def CheckResponse(self, response):
                print("Checking response---")
                for command in self.commandStack:
                        if command[0][0:5]==response[0:5]: #check if response is in commandStack
                                if command[-2:]=='ok': #check if response is ok
                                        self.commandStack.remove(command) #remove command from commandStack
                                else:#response is not ok
                                        await self.SendCommand(command[0]) #send command again
                                break

        async def ReadSerial(self):
                print("Reading serial---")
                response = self.ser.read_all()
                if response:
                        print("rec-",response.decode() )
                        if 'rd' in response.decode():
                                print("command received:", response.decode())
                                #await self.SetTimeOut1(response.decode())
                        else:
                                print("CheckingResponse")
                                #await self.CheckResponse(response.decode())#command pas response
                else:
                        print("No response")


        #ser.write(serial.to_bytes(HexCommand))
        async def SendCommand(self, argCOMMAND=None):
                print("Sending command---")
                print("commandStack:", self.commandStack)
                if argCOMMAND:
                        inputCommand = argCOMMAND
                else:
                        inputCommand = input("Command: ")

                try:
                        inputCommand = inputCommand.split(":") #split inputCommand into a list

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
                        
                        inputCommand[1] = command1
                        inputCommand[2] = command2
                        inputCommand[3] = command3

                        command = self.CommandDictionnary[inputCommand[0]]+inputCommand[1]+[0x3a]+inputCommand[2]+[0x3a]+inputCommand[3]+[0x3a,0x7e]
                except:
                        print("Command not found")
                        return 0

                commandStartTime=time.time()
                self.commandStack.append([bytearray(command).decode(), 'TimeOut0', commandStartTime])


                self.ser.write(bytearray(command))

                time.sleep(0.1)#dangereux

        def commandStackState(self):
                print(self.commandStack)
                          
        async def CreateTask(self, func):
                task = asyncio.create_task(func)
                await asyncio.wait([task])
        
        async def SendAndRead(self):
                await self.SendCommand()
                task_0 = asyncio.create_task(self.ReadSerial())
                task_1 = asyncio.create_task(self.CheckTimer())
                await asyncio.wait([task_0, task_1])
                
        async def WaitStart(self):
                read = self.ser.read_all()
                if read:
                        print("start received")
                        return 1
                        
        async def ApplyStrategy(self, strategy_command_list): 
                for command in strategy_command_list:
                        await self.SendCommand(command)
                        task_0 = self.ReadSerial()
                        task_1 = self.CheckTimer()
                        await asyncio.wait([task_0, task_1])
                        time.sleep(2)
                
                        

SerialClass = SerialControl()

'''
while asyncio.run(SerialClass.WaitStart())!=1:
        print("waiting for start")
        time.sleep(0.1)
'''
#strategy_command_list = ["motor:0.00:0.00:1.57", "led:1.00:0.00:0.00", "motor:0.00:0.00:1.57", "led:1.00:0.00:0.00"]
#asyncio.run(SerialClass.ApplyStrategy(strategy_command_list))
#SerialClass.commandStackState()

#strategy relative to the corner of the table
#strategy_commands_relative = ["motor:1.70:0.00:0.00", "motor:-1.70:0.00:0.00"]
#line_strategy_relative = ["motor:0.67:0.00:0.00", "motor:0.00:0.00:0.00", "motor:0.00:0.50:0.00", "motor:0.00:0.00:0.00", "motor:2.00:0.00:0.00"]
#strategy ??? to the corner of the table
#strategy_commands_??? = ["motor:0.00:1.70:0.00", "motor:0.00:-1.70:0.00"]
#line_strategy_??? = ["motor:0.77:0.00:0.00", "motor:0.00:0.00:0.00", "motor:0.00:0.72:0.00", "motor:0.00:0.00:0.00", "motor:2.77:0.00:0.00"]