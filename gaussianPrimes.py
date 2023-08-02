import sys
import cv2
import numpy
import math

def primality(n):
	if (n == 2):
		return True
	# First factor must be less than or equal to sqrt(n)
	for i in range(2, math.ceil(math.sqrt(n)) + 1):
		if (n % i == 0):
			return False
	return True

# Reading arguments
if (len(sys.argv) != 3):
	exit("Incorrect number of arguments; should be `python3 gaussianPrimes.py <maximum component integer> <Coordinate system (\"cartesian\" or \"polar\")>`")
maxComponentInteger = int(sys.argv[1])
coordinateSystem = sys.argv[2]

# Generating Gaussian primes
#
# Let z = a + bi
# a = 0 => z is a Gaussian prime iff |b| is prime and |b| = 3 (mod 4)
# b = 0 => z is a Gaussian prime iff |a| is prime and |a| = 3 (mod 4)
# a != 0 and b != 0 => z is a Gaussian prime iff a^2 + b^2 is prime
gaussianPrimes = []
for a in range(-maxComponentInteger, maxComponentInteger + 1):
	for b in range(-maxComponentInteger, maxComponentInteger + 1):
		if (a == 0):
			if (primality(abs(b)) and abs(b) % 4 == 3):
				gaussianPrimes.append([a, b])
		elif (b == 0):
			if (primality(abs(a)) and abs(a) % 4 == 3):
				gaussianPrimes.append([a, b])
		else:
			if (primality(a**2 + b**2)):
				gaussianPrimes.append([a, b])

# Creating image to display Gaussian primes
image = None
if (coordinateSystem == "cartesian"):
	w = 2 * maxComponentInteger + 1
	h = w
	xCenter = maxComponentInteger
	yCenter = maxComponentInteger
	# Greyscale image
	image = numpy.full((h, w, 1), 255, numpy.uint8)
	for i in range(len(gaussianPrimes)):
		a = gaussianPrimes[i][0]
		b = gaussianPrimes[i][1]
		image[a + xCenter][b + yCenter][0] = 0
elif (coordinateSystem == "polar"):
	SCALING_FACTOR = 20
	# Each point is now a sphere with a radius of 5 pixels to account for polar coordinates needing a higher resolution to be placed accurately
	w = SCALING_FACTOR * (2 * maxComponentInteger + 1)
	h = w
	xCenter = SCALING_FACTOR * maxComponentInteger
	yCenter = SCALING_FACTOR * maxComponentInteger
	# Greyscale image
	image = numpy.full((h, w, 1), 255, numpy.uint8)
	for i in range(len(gaussianPrimes)):
		r = gaussianPrimes[i][0]
		theta = gaussianPrimes[i][1]
		x = int(round(r * math.cos(theta)))
		y = int(round(r * math.sin(theta)))
		# Points are circles instead of pixels
		cv2.circle(image, (SCALING_FACTOR * x + xCenter, SCALING_FACTOR * y + yCenter), round(SCALING_FACTOR / 4), 0, -1)
else:
	exit("Unknown coordinate system; must be either polar or Cartesian")

# GUI
# 	S: Save
#	X: Close window
cv2.imshow("Gaussian primes, |a|, |b| <= " + str(maxComponentInteger), image)
key = None
while (key != 0x78):
	key = cv2.waitKey(0)
	if (key == 0x73):
		cv2.imwrite("gaussianPrimes" + coordinateSystem.capitalize() + str(maxComponentInteger) + ".png", image)
cv2.destroyAllWindows()
