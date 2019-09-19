# I'm sorry
This is, by far, the worst code I can remember writing. I'm mostly leaving it here because, reading the source several years after writing it, I keep finding hidden gems:
`unEnc[i] = unhexlify(hex(int(unEnc[i], 2))[2:].zfill(2))`
I like to think I'm at least a little better these days.

## Anyway...
The rest of the readme and source are presented as-is, typos and all.

# TurCrypt
Turing Machine-based encryption mechanism

TDCStndrd and TECStndrd are the standard eencryption systems. TEC and TDCBool are experimental optimizations of the code which turn out to run more slowly than the originla version.
