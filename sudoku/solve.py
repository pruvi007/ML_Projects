
import numpy as np
import random 

def safe(board,row,col):
	val = board[row][col]
	# check in row
	for i in range(0,9):
		if i!=col and board[row][i] == val:
			return False,"row"

	# check in column
	for i in range(0,9):
		if i!=row and board[i][col] == val:
			return False,"col"

	# check in box
	d = {}
	si = row
	sj = col

	# find starting and ending indices of the box
	if si%3!=0:
		while si%3!=0:
			si-=1
	if sj%3!=0:
		while sj%3!=0:
			sj-=1
	ei = si + 2
	ej = sj + 2

	# print([row,col],[si,sj],[ei,ej])
	c = 0
	for i in range(si,ei+1):
		for j in range(sj,ej+1):
			if board[i][j] == val:
				c+=1
			# c+=1
	# print(c)

	# if searched value has count > 1 
	if c > 1:
		return False,"box"
		
	return True,"Safe"
	


def get_conflicts(problem):
	conf = 0
	conf_pos = []
	
	for i in range(0,9):
		for j in range(0,9):
			b,s = safe(problem,i,j)
			if not b:
				conf+=1
				conf_pos.append((i,j,s))

	return [conf,conf_pos]

def readProblem(problem,file_name):
	file = open(file_name)
	for line in file.readlines():
		temp = []
		for c in line:
			if c!='\n' and c!=' ':
				c = int(c)
				temp.append(c)
		problem.append(temp)


def get_valid_board(problem):
	board = []
	for i in range(0,9):
		flag = [0]*9
		row = []
		for x in problem[i]:
			row.append(x)
			if x!=0:
				flag[x-1]=1
		nums = [i+1 for i in range(0,9) if flag[i]==0]
		random.shuffle(nums)
		c = 0
		for j in range(0,9):
			if row[j] == 0:
				row[j] = nums[c]
				c+=1
		board.append(row)
	return board

def generate_population(problem,pop,pop_size):
	nums = []
	for z in range(pop_size):
		board = get_valid_board(problem)
		pop.append(board)

	for board in pop:
		conf, conf_pos = get_conflicts(board)
		# print_board(board)
		# print("Conflicts: ",conf)
		# print()
	return pop

def print_board(board):
	for row in board:
		print(row)
	
def getScores(pop):
	score = []
	ind = 0
	for board in pop:
		conf,conf_pos = get_conflicts(board)
		score.append((conf,ind))
		ind += 1

	return score


def getNewRow(r1,r2,row,problem):
	r = []
	
	newRow = [-1]*9
	for i in range(0,9):
		if problem[row][i] != 0:
			newRow[i] = problem[row][i]
	# print(newRow)
	
	c = random.randint(0,8)
	for i in range(len(newRow)):
		if newRow[i] == -1:
			while r2[c] in newRow:
				c+=1
				c = c%9
			newRow[i] = r2[c]
	# print(newRow)
	return newRow


def crossOver(board1,board2,problem):

	# print_board(board1)
	# print()
	# print_board(board2)
	row = random.randint(0,8)
	# print(row)
	r1 = board1[row]
	r2 = board2[row]
	
	newRow1 = getNewRow(r1,r2,row,problem)
	newRow2 = getNewRow(r2,r1,row,problem)
	# print(r1,r2)
	
	# print(newRow)
	board1[row] = newRow1
	board2[row] = newRow2
	child1 = board1
	child2 = board2

	return child1,child2
	

def checkForSolution(pop):

	M = 99999
	pos = []
	best = []
	for board in pop:
		conf,conf_pos = get_conflicts(board)
		if conf < M:
			M = conf
			best = board
			pos = conf_pos
	return M,pos,best

def findRow(col,wrong,child):
	i = random.randint(0,8)
	while True:
		if child[i][col] == wrong:
			return i
		i = (i+1)%9

def mutate(child,problem):

	# exchange mutation on the child
	for i in range(0,9):
		d = {}
		for j in range(0,9):
			if child[j][i] not in d:
				d[ child[j][i] ] = 1
			else:
				d[ child[j][i] ] += 1

		for (k,v) in zip(d.keys(),d.values()):
			if v > 1:
				
				wrong = k
				# print(wrong)
				row = findRow(i,wrong,child)
				pos1 = [row,i]
				pos2 = [row,i]
				# print(pos1)
				l = random.randint(0,8)
				c = 0
				while True:
					if child[row][l] not in d:
						pos2 = [row,l]
						break
					l += 1
					l %= 9
					c += 1
					if c>=9:
						break
				# print(pos2)
				if problem[pos1[0]][pos1[1]] == 0 and problem[pos2[0]][pos2[1]]==0:
					temp = child[pos1[0]][pos1[1]]
					child[pos1[0]][pos1[1]] = child[pos2[0]][pos2[1]]
					child[pos2[0]][pos2[1]] = temp
					d[wrong] -= 1
					d[child[pos2[0]][pos2[1]]] = 1
					# brseak
				# 	print_board(child)
				# 	print()
				# else:
				# 	print("Can't Mutate at these set of indexes")
		
	return child



def selection(pop,pop_size,problem):
	
	# for board in sel:
	# 	print_board(board)
	# 	print(get_conflicts(board)[0])
	# 	print()

	newPop = []
	ans = []
	gen = 1
	score = getScores(pop)
	score = sorted(score)

	# get best 10 parents from the population
	sel_size = 10
	sel = [ pop[ score[i][1] ] for i in range(sel_size)  ]
	# print("Generation: ",gen)
	bestSol = []
	bestConf = 99999
	bestPos = []
	while True:

		if len(newPop) >= pop_size:
			pop = newPop
			
			print("Generation: ",gen)
			gen += 1

			M,M_POS,BEST = checkForSolution(newPop)
			if M < bestConf :
				bestConf = M
				bestSol = BEST
				bestPos = M_POS

			print_board(BEST)
			print("Conflicts: ",M)
			print()
			score = getScores(pop)
			score = sorted(score)

			# get best 10 parents from the population
			sel_size = 10
			sel = [ pop[ score[i][1] ] for i in range(sel_size)  ]
			newPop = []
		
		

		# select 2 random parents from the set
		r1 = random.randint(0,sel_size-1)
		r2 = (r1 + random.randint(0,sel_size-1) )%sel_size

		# perform crossOver on them
		child1,child2 =  crossOver( sel[r1],sel[r2],problem )
		# print_board(child1)
		# print()
		child1 = mutate(child1,problem)
		# print_board(child1)
		child2 = mutate(child2,problem)
		newPop.append(child1)
		newPop.append(child2)
		# break

		if gen >= 200:
			break
			

	print()
	print("Best Possible Conflict Count Reached: ", bestConf)
	print_board(bestSol)
	print()

	
	
	


problem = []
file_name = "problems.txt"
readProblem(problem,file_name)

# print the PROBLEM BOARD
print("The Given Problem Board: ")
print_board(problem)
print()
# conf = get_conflicts(problem)
# print(conf)

# board = get_valid_board(problem)
# for row in board:
# 	print(row)
# print()


# GENERATE THE POPULATION (with unique rows)
pop = []
pop_size = 100

generate_population(problem,pop,pop_size)

# for board in pop:
# 	for row in board:
# 		print(row)
# 	print()

selection(pop,pop_size,problem)




	
