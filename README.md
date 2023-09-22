# trueRNG-ableton-ionosphere

## Scripts
### `DroneDevAble.py`
When a`TrueRNG` device is connected via a serial port, this script reads its random number output and uses it to influence MIDI messages, thus, creating true-randomly-generated music.

Here is a breakdown of some of the working components:

**1. MIDI and Sound Settings**
* `ChordSound`, `ChordVol`, `PentSound`, and `PentVol` set the type and volume of the sounds.
* `Key` and `Kmax` set the range of musical keys.
* Note On/Off: `midiout.send_message(note_on)` and `midiout.send_message(note_off)` start and stop the sound of a particular note.

**2. TrueRNG Hardware**
* `UseTrueRNG` is a flag that specifies whether or not the script will use the True Random Number Generator hardware device. When set to `true`, if the TrueRNG device is connected via a serial port, the script will read random numbers from it.
* `RNG_Interval` and `RNG_BytesPerInterval` set how often the RNG updates and how many bytes are read per update.

**3. Statistical Thresholds**
* `ChordThres` and `PentThres` set statistical thresholds that trigger certain actions (like key changes or plucks).

**4. Modules**

`DroneDevAble.py` imports the following:
* `serial` for serial port communication
* `rtmidi` forvreal-time MIDI
* `matplotlib` for data visualization/plotting
* `scipy` for statistical operations

### `InitCC.py`
InitCC.py: Primarily used for sending MIDI control change messages. This script sets a MIDI channel and a Control Change number and then sends a MIDI message.

**1. Importing rtmidi**
* The script imports the rtmidi package for MIDI operations and specifically imports CONTROL_CHANGE from rtmidi.midiconstants.

**2. Initialize MIDI Output**
* It initializes a MIDI output interface using midiout = rtmidi
* MidiOut() opens port 1 with midiout.open_port(1).

**3. MIDI Channel and CC Number**
* The script sets a MIDI channel and a Control Change (CC) number using variables CHANNEL and CC_NUM.

**4. Sending the Control Change Message**
* Finally, it creates a control change message modCC and sends it using midiout.send_message(modCC).


### `TropicalAble.py`
This script covers real-time MIDI, audio playback, threading, serial port communication, and data analysis. There are also imports related to data visualization and signal processing.