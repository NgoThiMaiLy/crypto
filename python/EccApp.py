import EccCore
import time

def textToInt(text):
	encoded_text = text.encode('utf-8')
	hex_text = encoded_text.hex()
	int_text = int(hex_text, 16)
	return int_text

def intToText(int_text):
	import codecs
	hex_text = hex(int_text)
	hex_text = hex_text[2:] #remove 0x
	return codecs.decode(codecs.decode(hex_text,'hex'),'ascii')


applyBruteForce = False
applyKeyExchange = False
applyDigitalSignature = True
applySymmetricEncryption = True
applyOrderOfGroup = False
applyECDLP = False

enableBitcoinParams = True

#------------------------------------
#curve configuration

if enableBitcoinParams == True:
	mod = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
	order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
else:
	mod = 199 #F199
	order = 211 #order of group - number of points on the curve

#curve configuration
# y^2 = x^3 + a*x + b = y^2 = x^3 + 7
a = 0
b = 7

#base point on the curve
if enableBitcoinParams == True:
	x0 = 55066263022277343669578718895168534326250603453777594175500187360389116729240
	y0 = 32670510020758816978083085130507043184471273380659243275938904335757337482424
else:
	x0 = 2
	y0 = 24

print("---------------------")
print("Initial configuration")
print("---------------------")
print("Curve: y^2 = x^3 + ",a,"*x + ",b, " mod ", mod," , #F(",mod,") = ", order)
print("Base point: (",x0,", ",y0,")")
#print("modulo: ", mod)
#print("order of group: ", order)
print()
#------------------------------------

#------------------------------------
#brute force
if applyBruteForce == True:
	
	print("\n-----------------------------------------")
	print("brute force")
	print("-----------------------------------------")
	
	print("P: (", x0,", ",y0,")")

	new_x, new_y = EccCore.pointAddition(x0, y0, x0, y0, a, b, mod)

	print("2 P: (",new_x,", ",new_y,")")

	for i in range(3, 2000+1):
		try:
			new_x, new_y = pointAddition(new_x, new_y, x0, y0, a, b, mod)
			print(i,"P: (",new_x,", ",new_y,")")
		except:
			print("order of group: ",i)
			break

#------------------------------------
#key exchange

if applyKeyExchange == True:
	
	print("\n------------------------------------------")
	print("Elliptic Curve Diffie Hellman Key Exchange")
	print("------------------------------------------")

	start_time = time.time()

	alicePrivate = 2010000000000017
	alicePublicX, alicePublicY = EccCore.applyDoubleAndAddMethod(x0, y0, alicePrivate, a, b, mod)
	print("alice public key: (",alicePublicX,", ", alicePublicY,")")

	bobPrivate = 2010000000000061
	bobPublicX, bobPublicY = EccCore.applyDoubleAndAddMethod(x0, y0, bobPrivate, a, b, mod)
	print("bob public key: (",bobPublicX,", ", bobPublicY,")")
	
	print("")

	aliceSharedX, aliceSharedY = EccCore.applyDoubleAndAddMethod(bobPublicX, bobPublicY, alicePrivate, a, b, mod)
	print("alice shared key: (",aliceSharedX,", ", aliceSharedY,")")

	bobSharedX, bobSharedY = EccCore.applyDoubleAndAddMethod(alicePublicX, alicePublicY, bobPrivate, a, b, mod)
	print("bob shared key: (",bobSharedX,", ", bobSharedY,")")

	end_time = time.time()
	print('total time taken: {} (seconds)'.format(end_time - start_time))
#------------------------------------
#digital signature

if applyDigitalSignature == True:
	
	print("\n------------------------------------------")
	print("Elliptic Curve Digital Signature Algorithm")
	print("------------------------------------------")
	
	message = b"Ngo Thi Mai Ly - 21C11014"

	start_time = time.time()

	import hashlib

	hashHex = hashlib.sha1(message).hexdigest()
	hash = int(hashHex, 16)

	print("message: ", message)
	print("hash: ", hash)

	# import random
	# privateKey = random.getrandbits(256) #32 byte secret key

	privateKey = 51593096464285145885950316111141236823187319404180158951714772261245525337045

	publicKeyX, publicKeyY = EccCore.applyDoubleAndAddMethod(x0, y0, privateKey, a, b, mod)

	print("public key: ",publicKeyX, ", ", publicKeyY)

	# import random
	# randomKey = random.getrandbits(128)
	# print("random key: ", randomKey)
	randomKey = 27108379813230200991399606648638420817680374902224885321944488119274900025117

	randomPointX, randomPointY = EccCore.applyDoubleAndAddMethod(x0, y0, randomKey, a, b, mod)
	print("random point: (", randomPointX,", ",randomPointY)

	#signing

	r = randomPointX % order

	s = hash + (r * privateKey)
	s = s * EccCore.findModularInverse(randomKey, order)
	s = s % order

	print("signature")
	print("r: ", r)
	print("s: ", s)

	#verification
	print("\nverification...")

	w = EccCore.findModularInverse(s, order)
	
	u1 = EccCore.applyDoubleAndAddMethod(x0, y0, (hash * w) % order, a, b, mod)
	u2 = EccCore.applyDoubleAndAddMethod(publicKeyX, publicKeyY, (r * w) % order, a, b, mod)
	
	checkpointX, checkpointY = EccCore.pointAddition(u1[0], u1[1], u2[0], u2[1], a, b, mod)
	print("checkpoint: (",checkpointX,", ",checkpointY,")")
	
	print()
	print("(checkpoint)x ? = r")
	print(checkpointX," ?= ", r)
	print()

	if(checkpointX == r):
		print("signature is valid...")
	else:
		print("invalid signature detected!!!")

	end_time = time.time()
	print('total time taken: {} (seconds)'.format(end_time - start_time))
#------------------------------------
#symmetric encryption

if applySymmetricEncryption == True:
	print("\n------------------------------------------")
	print("Elliptic Curve ElGamal Cryptosystem")
	print("------------------------------------------")

	start_time = time.time()
	
	message = 'Ngo Thi Mai Ly - 21C11014'
	print("message:", message)

	plaintext = textToInt(message)
	plaintextX, plaintextY = EccCore.applyDoubleAndAddMethod(x0, y0, plaintext, a, b, mod)

	print("plaintext: (",plaintextX,", ",plaintextY,")")

	# import random
	# secretKey = random.getrandbits(256) #32 byte secret key
	secretKey = 51593096464285145885950316111141236823187319404180158951714772261245525337045

	publicKeyX, publicKeyY = EccCore.applyDoubleAndAddMethod(x0, y0, secretKey, a, b, mod)

	print("public key: (",publicKeyX, ", ", publicKeyY,")")

	#encryption

	randomKey = 27108379813230200991399606648638420817680374902224885321944488119274900025117
	"""import random
	randomKey = random.getrandbits(128)"""

	c1x, c1y = EccCore.applyDoubleAndAddMethod(x0, y0, randomKey, a, b, mod)

	c2x, c2y = EccCore.applyDoubleAndAddMethod(publicKeyX, publicKeyY, randomKey, a, b, mod)
	c2x, c2y = EccCore.pointAddition(c2x, c2y, plaintextX, plaintextY, a, b, mod)

	print("ciphertext")
	print("c1: (", c1x,", ",c1y,")")
	print("c2: (", c2x,", ",c2y,")")
	print("")

	#decryption
	#message = c2 - secretKey * c1

	dx, dy = EccCore.applyDoubleAndAddMethod(c1x, c1y, secretKey, a, b, mod)
	dy = dy * -1 #curve is symmetric about x-axis. in this way, inverse point found

	#print("d: (",dx,", ",dy,")")

	decrypted = EccCore.pointAddition(c2x, c2y, dx, dy, a, b, mod)
	print("decrypted: ",decrypted,"")
	
	end_time = time.time()
	print('total time taken: {} (seconds)'.format(end_time - start_time))
#------------------------------------

if applyOrderOfGroup == True:
	
	print("\n------------------------------------------")
	print("Find Order of Elliptic Curve Group")
	print("------------------------------------------")
	
	from math import sqrt
	
	Q = EccCore.applyDoubleAndAddMethod(x0, y0, mod + 1, a, b, mod)
	print("(mod + 1)P = ", mod + 1,"P = ",Q)
	
	m = int(sqrt(sqrt(mod))) + 1
	print("1 + (mod^1/4) = 1 + (",mod,")^1/4 = ",m)
	print()
	
	terminate = False
	
	for j in range (1, m+1):
		
		jP = EccCore.applyDoubleAndAddMethod(x0, y0, j, a, b, mod)
		print(j,"P = ",jP, " -> ", end="")
		
		for k in range (-m, m+1):
			
			checkpoint = EccCore.applyDoubleAndAddMethod(x0, y0, m*2*k, a, b, mod)
			checkpoint = EccCore.pointAddition(checkpoint[0], checkpoint[1], Q[0], Q[1], a, b, mod)
			
			print(checkpoint," ", end="")
			
			if checkpoint[0] == jP[0]: #check x-corrdinates of checkpoint and jP
				
				orderOfGroup = mod + 1 + m*2*k
				
				print("\norder of group should be ", orderOfGroup ," ± ", j)
				
				try:
					EccCore.applyDoubleAndAddMethod(x0, y0, orderOfGroup + j, a, b, mod)
				except:
					orderOfGroup = orderOfGroup + j
					terminate = True
					break
				try:
					EccCore.applyDoubleAndAddMethod(x0, y0, orderOfGroup - j, a, b, mod)
				except:
					orderOfGroup = orderOfGroup - j
					terminate = True
					break
		
		print()
		if terminate == True:
			break
	
	print("order of group: ", orderOfGroup)

#-----------------------------------

if applyECDLP == True:

	print("\n------------------------------------------")
	print("Find k such that Q = k x P")
	print("------------------------------------------")
	
	from math import sqrt
	
	k = 177
	publicKey = EccCore.applyDoubleAndAddMethod(x0, y0, k, a, b, mod)
	print("public key: ", publicKey)

	print("Find k such that ",publicKey," = k x (",x0,", ",y0,")")

	terminate = False
	step = 0
	
	#------------------------
	
	m = int(sqrt(order)) + 1
	
	for i in range(1, m):
		iP = EccCore.applyDoubleAndAddMethod(x0, y0, i, a, b, mod)
		#print("look for", iP," in the following series ")
		
		for j in range(1, m):
			checkpoint = EccCore.applyDoubleAndAddMethod(x0, y0, j*m, a, b, mod)
			checkpoint = EccCore.pointAddition(publicKey[0], publicKey[1], checkpoint[0], -checkpoint[1], a, b, mod)
			#print(checkpoint, " ",end ="")
			
			#if iP[0] == checkpoint[0] and iP[1] == checkpoint[1]:
			if iP == checkpoint:
				
				print(i+j*m," mod ",order)
				print("ECDLP solved in", i+m,"th step")
				terminate = True
				break
		
		if terminate == True:
			break
