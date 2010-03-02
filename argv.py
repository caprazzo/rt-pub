import sys
step = 3
offset = int(sys.argv[1])

count = 0
for i in range(100):
	if i % 3 != offset:
		continue
	print i, count
	count += 1
