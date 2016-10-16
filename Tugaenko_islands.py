class Cell():
	"""one cell of the island table"""
	def __init__(self, i, j, value):
		self.i = i
		self.j = j
		self.value = value
		self.forbidden = False   # water can never be above forbidden cells
	def forbide(self):
		self.forbidden = True
	def __str__(self):
		return str(self.i) + " " + str(self.j) + " " + str(self.value) + "-" +  str(self.forbidden)

class Island():
	"""Island"""
	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.island = []       # here will be cells
		self.capacity = 0      # we will increment this parameter while considering and changing the island
	def add(self, cell):       		# add sells to island. gen_islands does it
		self.island.append(cell)
	def get_cell(self, i, j):
		return self.island[i*(self.columns) + j]
	def __str__(self):
		string = ""
		for i in range(self.rows):
			for j in range(self.columns):
				string = string + str(self.get_cell(i,j).value) + " "
			string = string + '\n'
		return string #str(self.rows) + "-" + str(self.columns) + "-" + str(len(self.island))

def gen_islands(islands_input):           # Create all islands-objects and fill them with cells-objects using input string
	island_list = islands_input.split()
	N = int(island_list[0])
	starting_point = 1    # index. to be updated while considering other cells
	islands = []
	for isl in xrange(N):
		islands.append(Island(int(island_list[starting_point]), int(island_list[starting_point + 1]))) # init new island-object
		starting_point +=  2     # make starting point at the beginning of the island
		for i in xrange(islands[isl].rows):
			for j in xrange(islands[isl].columns):
				islands[isl].add( Cell(i, j, int(island_list[ starting_point]) ))  # new cell
				starting_point += 1     # updating starting point
	return islands

def set_forbidden(island):    # init forbidden with edge elements -- water could never be above them
	for i in range(island.rows):
		island.get_cell(i,0).forbide()
		island.get_cell( i, island.columns -1 ).forbide()
	for j in range(island.columns):
		island.get_cell(0, j).forbide()
		island.get_cell(  (island.rows -1), j ).forbide()

def island_capacity(island):
	reservoir = 0          # current capacity
	set_forbidden(island)

	while True:  # repeat until layer_bonus == 0
		used_for_one_layer_equals = set()
		layer_bonus = 0       # consider island by layers -- one by one
		for i in xrange(1, island.rows - 1 ):       		 # consider each cell except edges
			for j in xrange(1, island.columns - 1 ):  
				higher_list = []   		 	# holds values (height) of higher neighbours
				equals_queue = []				# holds equal neighbours(cells-objects) 
				used_equals_set = set()  			# holds equal cells that was considered
				current = island.get_cell(i,j)      	 # cell we are considering now

				if current.forbidden: continue    		# do not consider useless elements
				if current in used_for_one_layer_equals: continue
				min_nei_value = 1001
				smaller_nei_forbidden = False

				# consider neighbours and get current state
				equals_queue, used_equals_set, higher_list, go_to_next_cell, min_nei_value, smaller_nei_forbidden = consider_neighbours(
					False, current, island, equals_queue, used_equals_set, higher_list, min_nei_value, smaller_nei_forbidden)

				if go_to_next_cell: continue  			# time to consider next cell

				while equals_queue:  # considering connected cells with equal values
					temp_cell = equals_queue.pop(0)
					used_equals_set.add(temp_cell)
					quals_queue, used_equals_set, higher_list, go_to_next_cell, min_nei_value, smaller_nei_forbidden = consider_neighbours(
						True, temp_cell, island, equals_queue, used_equals_set, higher_list, min_nei_value, smaller_nei_forbidden)

				if (min_nei_value > current.value) and smaller_nei_forbidden is False:			# all neighboors are higher. So...
					for cell in used_equals_set:
						layer_bonus += min_nei_value - cell.value 				# ... cell can hold this volume of water. update layer_bonus
						cell.value += min_nei_value - cell.value 				# fill it with water! (change values)
						used_for_one_layer_equals.add(cell)
				elif smaller_nei_forbidden is True:			# make all these cells forbidden
					for cell in used_equals_set:
						cell.forbide()
						used_for_one_layer_equals.add(cell)
				used_equals_set = set()
		if layer_bonus == 0:    # island is full or can not be filled
			break
		reservoir += layer_bonus	
		
	if layer_bonus == 0:     # => all possible water volumes are allready filled
		return reservoir		# total capacity

def consider_neighbours(consider_all, current, island, equals_queue, used_equals_set, higher_list, min_nei_value, smaller_nei_forbidden):
	neighbours  = [ island.get_cell(current.i-1, current.j) , 		 # upper,
				 island.get_cell(current.i+1,current.j) ,				#lower
				  island.get_cell(current.i,current.j-1) ,				#left
				   island.get_cell(current.i, current.j+1) ]   			 # right	
	used_equals_set.add(current) 
	for nei in neighbours:     # for each neigbour
		if nei in used_equals_set: 
			continue
		go_to_next_cell = False
		if current.value != nei.value:
			min_nei_value = min(min_nei_value, nei.value)
		if  nei.forbidden:      # consider forbidden neighbour
			if current.value >= nei.value:   # current cell is higher then edge
				current.forbide()        # so, water never will be above the current cell. New edge born.
				go_to_next_cell = True  
				smaller_nei_forbidden = True
				if not consider_all:
					break 				# no need to consider other neighbours
			else: 					# if (current  < nei) # there is a potential to fill this cell
				higher_list.append(nei.value) 
		else:
			if current.value > nei.value:
				go_to_next_cell = True
				if not consider_all:  		# no need to consider other neighbours this time
					break 					# We will consider this element on next iteration
			elif current.value < nei.value:   # there is a potential to fill this cell
				higher_list.append(nei.value)
			elif current.value == nei.value:   # most difficult case ...
				equals_queue.append(nei)
				
	return equals_queue, used_equals_set, higher_list, go_to_next_cell, min_nei_value, smaller_nei_forbidden





input_string = raw_input()      # stdin

for island in gen_islands(input_string):
	print island_capacity(island)   # stdout






#   ------   test cases  -------

test_islands_input = '''
6
3 3
4 5 4
3 1 5
5 4 1
4 4
5 3 4 5
6 2 1 4
3 1 1 4
8 5 4 3
4 3
2 2 2
2 1 2
2 1 2
2 1 2
5 5
1 5 5 5 1
5 3 2 1 5
5 1 4 2 5
5 2 3 1 5
1 5 5 5 1
5 5
1 5 5 5 1
5 3 3 3 5
5 3 3 1 5
5 0 1 1 5
1 5 5 5 1
3 5
1 5 5 5 1
5 7 3 3 5
1 5 5 5 1
'''

results = [2, 7, 0, 26, 27, 4]
ind = 0
for island in gen_islands(test_islands_input):
	assert (results[ind] == island_capacity(island))
	ind += 1











	
