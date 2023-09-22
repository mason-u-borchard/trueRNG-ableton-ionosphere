import time
# import fluidsynth
import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)
import numpy
import os
import sys
import serial
from serial.tools import list_ports
import matplotlib.pyplot as plt
import scipy.stats
import matplotlib.animation as animation


UseTrueRNG = False#set to True only if you have TrueRNG hardware
ChordSound = 101#voice of background hum
ChordVol = 100#volume of background hum
PentSound = 79#voice of plucking sound
PentVol = 100#volume of plucking sound
Key = 55#starting key, 60 = middle C
Kmax = 67#highest key before dropping octave
RNG_Interval = 0.2
RNG_BytesPerInterval = 25
ChordThres = 18#25#threshold of coherence in bitstream that triggers key change
PentThres = 13#threshold of coherence in bitstream that triggers a key pluck. Must be less than ChordThres




Rmks = "test"#sys.argv[1]
OutPath = os.getcwd()

#Pmod = scipy.stats.norm.sf(ChordThres/((RNG_BytesPerInterval*2)**0.5))*2
Pmod = 0.00049942648# set for ChordThres = 25


# init midi
midiout = rtmidi.MidiOut()
ports = midiout.get_ports()
print("selecting MIDI port: %s" %ports[1])
midiout.open_port(1)


#new insert:
def noteon(channel, note, volume):
    note_on = [0x90 | channel, note, volume]
    midiout.send_message(note_on)
    
def noteoff(channel, note):
    note_off = [0x80 | channel, note, 0]
    midiout.send_message(note_off)
#replace 
# "fs.noteon(0" -> "noteon(0"
# "fs.noteoff(0" -> "noteoff(0"
# "fs1.noteon(0" -> "noteon(1"
# "fs1.noteoff(0" -> "noteoff(1"


def Modulate():
    
    K = KeyList[-1]
    
    noteoff(0, K)
    noteoff(0, K+4)
    noteoff(0, K+7)
    noteoff(0, K+12)
    
    if (K>Kmax):
        K+= -7
    else:
        K+=5
        
    noteon(0, K, ChordVol)
    noteon(0, K+4, ChordVol)
    noteon(0, K+7, ChordVol)
    noteon(0, K+12, ChordVol)
        
    #NewPent = [K-12,K-10,K-8,K-5,K-3,K,K+2,K+4,K+7,K+9,K+12]
    
    KeyList.append(K)
    
    #return NewPent


totaltime=[]
totalmods=[]
P1=[]

def animate(i):
    
    
    #modCC = ([CONTROL_CHANGE | 2, 75, 1])
    #midiout.send_message(modCC)
    
    
    KK = KeyList[-1]
    Pent = [KK-12,KK-10,KK-8,KK-5,KK-3,KK,KK+2,KK+4,KK+7,KK+9,KK+12]
    
    current_time = time.time()
    totaltime.append(current_time-(starttime/1000.0))
    
    
    if (UseTrueRNG==True):
        ser.flushInput()
        x = ser.read(RNG_BytesPerInterval)
    else:
        x = numpy.random.randint(0,256,RNG_BytesPerInterval)
    rc=0
    for a in range (0,RNG_BytesPerInterval):
        rc+=lib[x[a]]
        outfile.write('%d,'%(x[a]))
    outfile.write('%d\n'%(int(current_time*1000)))
    if (Pul<=rc<Cul) or (Cll<rc<=Pll):
        if (len(Gigasavenote)==0):
            noteoff(1, 0)
        else:
            noteoff(1, Gigasavenote[-1])
        note = int(x[0]/23.1819)
        Gigasavenote.append(Pent[note])
        noteon(1, Pent[note], PentVol)
    #time.sleep(RNG_Interval)
    #noteoff(1, Pent[note])
    #switch = numpy.random.randint(0,20)
    if (rc>=Cul) or (rc<=Cll):
        Modulate()
        noteoff(1, 0)
        outfile.write('modulation\n')
    
    if len(totaltime)%3000==0:
        print(current_time,len(totaltime))
    
    EX = len(totaltime)*Pmod
    totalmods.append((len(KeyList)-2)-EX)
    P1.append(((len(totaltime)*Pmod*(1-Pmod))**0.5)*1.65)

    MinY = numpy.amin([numpy.amin(P1),numpy.amin(totalmods)])
    MaxY = numpy.amax([numpy.amax(P1),numpy.amax(totalmods)])
    MaxX = totaltime[-1]+1

    ax1.clear()
    # ax1.imshow(im, aspect='auto', extent=(0,MaxX,MinY,MaxY))
    ax1.set_xlim(0,MaxX)
    ax1.set_ylim(MinY,MaxY)
    ax1.plot(totaltime,totalmods)
    ax1.plot(totaltime,P1)
    #print('ok')
    
    
    
Gigasavenote=[]





starttime = int(time.time()*1000)
outfile = open('%s/Drone_%d_%s.txt'%(OutPath,starttime,Rmks),'w')
outfile.write('%s,%d,%d,%d,%d,%d,%d,%f,%d,%d,%d\n'%(UseTrueRNG,ChordSound,ChordVol,PentSound,PentVol,Key,Kmax,RNG_Interval,RNG_BytesPerInterval,ChordThres,PentThres))


lib=[]
readFile = open('%s\Conversion.txt'%(OutPath), 'r')
sepfile = readFile.read().split('\n')
for b in range (0,len(sepfile)):
    xandy = sepfile[b].split('\t')
    lib.append(float(xandy[0]))


if (UseTrueRNG==True):
    ports=dict()  
    ports_avaiable = list(list_ports.comports())
    rng_com_port = None
    for temp in ports_avaiable:
        if temp[1].startswith("TrueRNGpro"):
            print('Found:           ' + str(temp))
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=str(temp[0])
    print('Using com port:  ' + str(rng_com_port))
    print('==================================================')
    sys.stdout.flush()
    try:
        ser = serial.Serial(port=rng_com_port,timeout=10)  # timeout set at 10 seconds in case the read fails
    except:
        print('Port Not Usable!')
        print('Do you have permissions set to read ' + rng_com_port + ' ?')
    if(ser.isOpen() == False):
        ser.open()
    ser.setDTR(True)
    ser.flushInput()
    sys.stdout.flush()

"""
fs = fluidsynth.Synth()
fs.start(driver = 'dsound')  # use DirectSound driver
sfid = fs.sfload(r'FluidR3_GM.sf2')


fs1 = fluidsynth.Synth()
fs1.start(driver = 'dsound')  # use DirectSound driver
sfid1 = fs1.sfload(r'FluidR3_GM.sf2')
fs1.program_select(0, sfid, 0, PentSound)

fs.program_select(0, sfid, 0, ChordSound)
"""
Pll = (RNG_BytesPerInterval*4)-PentThres
Pul = (RNG_BytesPerInterval*4)+PentThres
Cll = (RNG_BytesPerInterval*4)-ChordThres
Cul = (RNG_BytesPerInterval*4)+ChordThres



KeyList = [Key-5]

fig = plt.figure()
ax1 = fig.add_subplot(111)



savenote = 0
#Pent = [K-12,K-10,K-8,K-5,K-3,K,K+2,K+4,K+7,K+9,K+12]


#fs.noteon(60, 60, ChordVol)
    
Modulate()
print('ok')
ani = animation.FuncAnimation(fig, animate, interval=int(RNG_Interval*1000))
plt.show()


