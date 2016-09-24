#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import random
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from copy import copy
import pickle
import sys
import time
import os

class TurCrypter:
	def __init__(self):
		pass

	def encrypt(self, string, mastr):
		lim = ((len(string) > 30000) * 10 * len(string)) + ((len(string) < 30000) * 500000)
		pwd = random.randint(lim, (lim * 4) + 200000)
		info = ''
		for char in string:
			info += bin(int(hexlify(char), 16))[2:].zfill(7)
		#Converts to array
		info = list(info)
		rslt = self.doTuring(info, pwd)
		eInfo = rslt[0]
		code = [hex(pwd * 3)[2:], '.', hex(rslt[1] * 7)[2:], '.', rslt[2]]
		code = ''.join(code)
		print(" ")
		finpwd = self.EmasterPass(code, mastr)
		for i in range(len(eInfo)):
			eInfo[i] = unhexlify(hex(int(eInfo[i], 2))[2:].zfill(2))
		return ''.join(eInfo), finpwd

	def decrypt(self,finData, mstrPwd, string, outLoc):
		pwd = self.DmasterPass(finData, mstrPwd)
		pwd = pwd.split('.')
		iters = int(pwd[0], 16) / 3
		p = int(pwd[1], 16) / 7
		s = pwd[2]
		dat = ''
		for char in string:
			dat += bin(int(hexlify(char), 16))[2:].zfill(7)
		unEnc = self.unTuring(list(dat), s, p, iters)
		for i in range(len(unEnc)):
			unEnc[i] = unhexlify(hex(int(unEnc[i], 2))[2:].zfill(2))
		if outLoc == "empty":
			print("Done! Message Follows: ")
			print ''.join(unEnc)
		else:
			print("Done!")
			open(outLoc, 'wb+').write(''.join(unEnc))
			print("Output appended to " + outLoc)

	def doTuring(self, data, iters):
		tape = copy(data)
		place = random.randint(0, len(tape) - 1)
		state = '1'
		interval = iters/70
		for i in range(iters):
			if state == '1' and tape[place] == '1':
				tape[place] = '0'
			elif state == '1'and tape[place] == '0':
				tape[place] = '1'
				state = '0'
			elif state == '0':
				state = tape[place]
			place += 1
			if place >= len(tape):
				place = place % len(tape)
			if i % interval == 0:
				print('.'.rjust((60 * i) / iters))
				sys.stdout.write("\033[F")
		tape = ''.join(tape)
		nData = [tape[i:i+7].zfill(8) for i in range(0, len(tape), 7)]
		return [nData, place, state]

	def unTuring(self, t, st, pl, n):
		tp = copy(t)
		interval = n/70
		for x in range(n):
			pl -= 1
			if pl == -1:
				pl += len(tp)
			if st == '1' and tp[pl] == '1':
				st = '0'
			elif st == '1' and tp[pl] == '0':
				tp[pl] = '1'
			elif st == '0' and tp[pl] == '1':
				st = '1'
				tp[pl] = '0'
			if x % interval == 0:
				print('.'.rjust((60 * x) / n))
				sys.stdout.write("\033[F")
		tp = ''.join(tp)
		return [tp[i:i+7].zfill(8) for i in range(0, len(tp), 7)]

	def DmasterPass(self, encData, mstr):
		dataOne = ''
		nCode = str(int(hexlify(b64decode(encData)),16))
		locOrd = range(len(nCode))
		random.seed(mstr)
		random.shuffle(locOrd)
		shift = random.randint(0, 10)
		code = ''
		for i in range(len(locOrd)):
			code += nCode[locOrd.index(i)]
		for char in code:
			dataOne += str((int(char) - shift) % 10)
		h = hex(int(dataOne))[2:-1]
		return unhexlify(h.zfill(len(h)+(len(h)%2)))

	def EmasterPass(self, dataOne, mstr):
		locOrd = []
		i=0
		dataOne = str(int(hexlify(dataOne), 16))
		locOrd = range(len(dataOne))
		random.seed(mstr)
		random.shuffle(locOrd)
		shift = random.randint(0, 10)
		code = ""
		for char in dataOne:
			code += str((int(char) + shift) % 10)
		nCode = ""
		for i in locOrd:
			nCode += code[i]
		nCode = hex(int(nCode))[2:-1]
		return b64encode(unhexlify(nCode.zfill(len(nCode)+(len(nCode)%2))))

def main():
	z = TurCrypter()

	parser = argparse.ArgumentParser(description="Xander's magic decryptifier.")
	parser.add_argument("method", metavar="m", type=str, help="Encryption (e) or decryption (d)")
	parser.add_argument("infile", metavar="i", type=str, help="Input file")
	parser.add_argument("password", metavar="p", type=str, help="Master Password")
	parser.add_argument('-o', dest="output", type=str, metavar="output", help='optional filepath for output', default="empty")
	args = parser.parse_args()

	if args.method == "e":
		startTime = time.time()
		if os.path.exists(args.infile):
			contents = open(args.infile).read()
		else:
			contents = args.infile
		data = list(contents)
		enc = z.encrypt(data, args.password)
#		print(enc[1])
		pickle.dump(enc, open(args.output, 'wb'), 2)
		endTime = time.time()
		print str(endTime - startTime) + " Seconds for Operation"
		print str(n/(endTime - startTime)) + " Iterations / Second"
	elif args.method == "d":
		startTime = time.time()
		file, findata = pickle.load(open(args.infile, 'rb'))
#		print findata	
		z.decrypt(findata, args.password, file, args.output)
		print str(time.time() - startTime) + " Seconds for Operation"

if __name__ == '__main__':
	main()



