# coding: utf-8
import re

# the greatest common divisor 
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# the least common multiple
def lcm(a, b):
    return a *b // gcd(a, b)

class BMS:
    def __init__(self):
        self.bpm = 120
        self.wav = {}
        self.data = {}
    
    def parse(self, bmsfile):
        with open(bmsfile, "r") as f:
            line = f.readline()
            while line:
                self.__parseLine(line)
                line = f.readline()
        return self.__relocate()

    def __parseLine(self, line):
        if line[0] != "#":
            return
        
        wav = re.search("#WAV(\w{2}) +(.*)", line)
        if wav:
            self.__parseWAV(wav)
        
        bpm = re.search("#BPM +(.*)", line)
        if bpm:
            self.__parseBPM(bpm)
        
        chmsg = re.search("^#([0-9]{3})([0-9]{2}):([\w\.]+)", line)
        if chmsg:
            self.__parseChannelMsg(chmsg)

    def __parseWAV(self, wav):
        i = int(wav.group(1), 36) #36進数[0-9A-Z]
        self.wav[i] = wav.group(2)
        print(str(i) + ":" + self.wav[i])

    def __parseBPM(self, bpm):
        i = int(bpm.group(1))
        self.bpm = i
        print("BPM:" + str(self.bpm))
    
    def __parseChannelMsg(self, chmsg):
        measureNum = int(chmsg.group(1))
        ch = int(chmsg.group(2))
        data = chmsg.group(3)
        
        if not measureNum in self.data:
            self.data[measureNum] = Command()

        if ch == 2: # Meter
            m = float(data)
            if m > 0:
                self.data[measureNum].meter = m
        #elif ch == 3: # BPM
        
        elif ch >= 11 and ch <= 15: # Notes
            self.data[measureNum].note[ch - 11] = self.__storeData(data, self.data[measureNum].note[ch - 11])
        elif ch == 16 or ch == 17:
            self.data[measureNum].note[ch - 9] = self.__storeData(data, self.data[measureNum].note[ch - 9])
        elif ch == 18 or ch == 19:
            self.data[measureNum].note[ch - 13] = self.__storeData(data, self.data[measureNum].note[ch - 13])
    
    def __storeData(self, msg, array):
        i = 0
        data = []
        while i < len(msg) - 1:
            data.append(int(msg[i:i+2], 36))
            i += 2
        return self.__merge(array, data)
    
    def __expand(self, array, length):
        ret = []
        if len(array) == 0:
            for i in range(length):
                ret.append(0)
            return ret
        interval = length // len(array)
        for i in range(length):
            if i % interval == 0:
                ret.append(array[i // interval])
            else:
                ret.append(0)
        return ret
    
    # ex. merge([1, 2, 3], [0, 4, 0]) == [1, 4, 3]
    # ex. merge([1, 2], [3, 4, 0]) == [3, 0, 4, 2, 0, 0]
    def __merge(self, ary1, ary2):
        if len(ary1) == 0:
            return ary2
        i = lcm(len(ary1), len(ary2))
        ret = self.__expand(ary1, i)
        for i, value in enumerate(self.__expand(ary2, lcm)):
            if value == 0:
                continue
            ret[i] = value
        return ret
    

    def __expandNote(self, note):
        length = 1
        for n in note:
            if len(n) == 0:
                continue
            length = lcm(len(n), length)
        ret = []
        for n in note:
            ret.append(self.__expand(n, length))
        return ret
            
    def __relocate(self):
        result = []
        t = 0.0
        mt = 240 / self.bpm # 一小節の時間(秒)
        for i in self.data:
            t = i * mt
            self.data[i].note = self.__expandNote(self.data[i].note)
            length = len(self.data[i].note[0])
            for j in range(length):
                r = Result()
                r.timing = t + mt / length * j
                for n, note in enumerate(self.data[i].note):
                    r.note[n] = note[j]
                print(str(r.timing) + ":{0}".format(r.note) )
                result.append(r)
        return result


class Command:
    def __init__(self):
        self.timing = 0.0
        self.bpm = 0.0
        self.meter = 1.0
        self.note=[]
        for i in range(9):
            self.note.append([])

class Result:
    def __init__(self):
        self.timing = 0.0
        self.note = [0, 0, 0, 0, 0, 0, 0, 0, 0]
