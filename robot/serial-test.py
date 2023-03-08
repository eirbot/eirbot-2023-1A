import serial 
import time 
import asyncio 
import re

#https://stackoverflow.com/questions/17589942/using-pyserial-to-send-binary-data

ser = serial.Serial('COM7', 9600) 

CommandDictionnary = {
                "led": [0x55],
                "motor": [0x57],
                "end": [0xff]
}
ResponseDictionnary = {
        "*":"ok"
}
async def AnalyseACK(response):
        if response:
                response=str(response)
                print(response[2:4])
                if 'rd' in response:
                        print("ye: command received")
                else:
                        print("no: command not received")
        else:
                print("no response")

async def ReadSerial():

        response = ser.read_all()
        if response:
                print(response)
                AnalyseACK(response)
                
        await asyncio.sleep(0.12)



async def SendCommand(): 
        """
        Send a command to the serial port and read the response
        """
        InputCommand = input("Envoie de la commande:")
        HexCommand = []
        try:
                HexCommand = CommandDictionnary[InputCommand]
        except:
                print("invalid command")

        ser.write(serial.to_bytes(HexCommand))
        
        await asyncio.sleep(0.2)
        
        try:
                response = ser.read_all()
                if response:
                        #print(response)
                        await AnalyseACK(response)

                        #response=str(response)
                        #print(response)
        except:
                print("Invalid character type")

async def Strategy(snvironnement, state):
        print("")

#run the main function in an event loopled

while True:
        asyncio.run(SendCommand())
        
        