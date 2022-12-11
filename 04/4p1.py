with open('input.txt') as f:
	l = f.read()
	list = l.strip().split("\n")
	summ = 0
	for line in list:
		line = line.split(",")
		r1 = line[0].split("-")
		r2 = line[1].split("-")
		if int(r1[0]) < int(r2[0]):
			if int(r1[1]) >= int(r2[1]):
				summ += 1
		elif int(r1[0]) > int(r2[0]):
			if int(r1[1]) <= int(r2[1]):
				summ += 1
		elif int(r1[0]) == int(r2[0]):
			summ += 1

	print(summ)
			
		