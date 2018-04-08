import sys
import bms
import bmsplayer

argvs = sys.argv
argc = len(argvs)
if argc < 2:
    print("Usage: {0} <bmsfile>".format(argvs[0]))
    quit()

b = bms.BMS()
result = b.parse(argvs[1])
p = bmsplayer.BMSPlayer()
p.play(result)
