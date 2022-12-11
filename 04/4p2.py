with open('input.txt') as f:
	l = f.read()
	l= l.strip().split("\n")
	summ = 0
	for line in l:
		line = line.split(",")
		r1 = list(map(lambda c: int(c), line[0].split("-")))
		r2 = list(map(lambda c: int(c), line[1].split("-")))
		if r1[0] >= r2[0] and r1[0] <= r2[1]:
			summ += 1
		elif r2[0] >= r1[0] and r2[0] <= r1[1]:
			summ += 1
		elif r1[1] >= r2[0] and r1[1] <= r2[1]:
			summ += 1
		elif r2[1] >= r1[0] and r2[1] <= r1[1]:
			summ += 1

	print(summ)
			
		