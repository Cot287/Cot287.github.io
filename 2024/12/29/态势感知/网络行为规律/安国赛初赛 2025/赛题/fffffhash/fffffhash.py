import os
from Crypto.Util.number import *
def f(hex_string):
	base_num = 0x6c62272e07bb014262b821756295c58d
	x = 0x0000000001000000000000000000013b
	MOD = 2**128
	for i in hex_string:
		base_num = (base_num * x) & (MOD - 1) 
		base_num ^^= i
	return base_num

h = 201431453607244229943761366749810895688
# hex_string = '030603070004040a003d030203000207011e0704fd00021c0600060005010302060707070101040d'
hex_string = '020101081b04390001051a020a3d0f0f'
s = bytes.fromhex(hex_string)
if f(s) == h:
	print('success')