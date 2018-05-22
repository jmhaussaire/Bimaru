# -*- coding: utf-8 -*-

import numpy as np
import argparse
import sys


# This is my grid for the bimaru
# _ = blank
# w = water
# O = circle (single boat)
# X = square (in the middle of a boat)
# P = Top of boat
# C = left side of boat
# B = Bottom of boat
# D = right side of boat
# T = boat, but undetermined yet (could be edge, could be middle ...)

VERBOSE = 0
N_COL = 0
N_LINE = 0

###########################
## Could / should probably define a cell class with these methods
## Attributes: 
##   character
##   changeability
## Define an order like X > T 
###########################

## Function checks if a cell is part of a boat
def is_boat(grid,i,j):
    return (is_boat_car(grid[i,j]))
def is_boat_car(cell):
    return (cell in ["O","X","P","C","U","D","T"])

## Function checks if a cell is a valid cell (water, boat or empty)
def is_valid(target):
    return (target in ["w","_","O","X","P","C","U","D","T"])

## Function checks if a cell is a valid cell for a new grid (cant be T)
def is_valid_beginning(target):
    return (target in ["w","_","O","X","P","C","U","D"])
    
## Function checks if a cell is changeable (only _ and T are changeable).
def is_changeable(grid,i,j):
    return grid[i,j] in ["_","T"]
            
## Function checks if a cell is empty
def is_empty(grid,i,j):
    return (grid[i,j]=="_") 

##############################
##############################

###########################
## Could / should probably define a grid class with these methods
## Attributes: 
##   the grid
##   the boats in line /col
## Methods:
##   Print grid with boats on the side
###########################
## Print the grid with the boats on the side
def print_grid(grid,boat_in_col,boat_in_line,final=False):
    if final:
        dim = (N_LINE-1, N_COL-1)
        total_grid = np.zeros(dim,dtype=str)
        for i in range(dim[0]-1):
            for j in range(dim[1]-1):
                total_grid[i,j]=grid[i+1,j+1]
        total_grid[:,-1] = boat_in_line[1:-1]+["-"]
        total_grid[-1,:] = boat_in_col[1:-1]+["-"]

    else:
        dim = (N_LINE+1, N_COL+1)
        total_grid = np.zeros(dim,dtype=str)
        for i in range(dim[0]-1):
            for j in range(dim[1]-1):
                total_grid[i,j]=grid[i,j]        
        total_grid[:,-1] = boat_in_line+["-"]
        total_grid[-1,:] = boat_in_col+["-"]
    print(total_grid)
    return total_grid

## Check if a grid is valid :
##  - right amount of boats per line/col
##  - no touching boats
##  - good amount of boats
def check_valid_grid(grid,boat_in_col,boat_in_line,boat_types):
    ## Checks if the amount of boats is right
    for i in range(N_LINE):
        if count_boat(grid[i,:])>boat_in_line[i]:
            return False
        if count_boat(grid[i,:])+count_empty(grid[i,:])<boat_in_line[i]:
            return False
        
    for j in range(N_COL):
        if count_boat(grid[:,j])>boat_in_col[j]:
            return False
        if count_boat(grid[:,j]) + count_empty(grid[:,j]) <boat_in_col[j]:
            return False
        
    ## Checks if the boat are not touching
    for i in range(N_LINE):
        for j in range(N_COL):
            if is_boat(grid,i,j):
                to_check = [(i+1,j+1) , (i-1,j+1) , (i+1,j-1) , (i-1,j-1)]
                if grid[i,j]=="O":
                    to_check = to_check+[(i+1,j) , (i,j-1) , (i-1,j) , (i,j+1)]
                if grid[i,j] =="P":
                    to_check = to_check+[          (i,j-1) , (i-1,j) , (i,j+1)]
                if grid[i,j]=="D":
                    to_check= to_check+[(i+1,j) ,           (i-1,j) , (i,j+1)]
                if grid[i,j]=="U":
                    to_check= to_check+[(i+1,j) , (i,j-1) ,           (i,j+1)]
                if grid[i,j]=="C":
                    to_check= to_check+[(i+1,j) , (i,j-1) , (i-1,j)          ]
                for (x,y) in to_check:
                    if (grid[x,y]!="w" and grid[x,y]!="_") :
                        return False
        
    ## Checks if I have the good amount of boats
    try:
        check_remaining(grid,boat_types)
    except ValueError: 
        return False
                
    return True

##########################
##########################

        
## count the number of boats in a line/col
def count_boat(line):
    return [is_boat_car(line[i]) for i in range(len(line))].count(True)

## count the number of empty spaces in a line/col
def count_empty(line):
    return [line[i]=="_" for i in range(len(line))].count(True)

## Function provides the list of surrounding cells:
def surroundings(i,j):
    return [(i+1,j+1) , (i-1,j+1) , (i+1,j-1) , (i-1,j-1) , (i+1,j) , (i,j-1) , (i-1,j) , (i,j+1)]
        
## Function provides the four corners around the cell:
def corners(i,j):
    return [(i+1,j+1) , (i-1,j+1) , (i+1,j-1) , (i-1,j-1)]

## Function provides the list of cells up-left-down-right of a cell:
def cross(i,j):
    return [(i+1,j) , (i,j-1) , (i-1,j) , (i,j+1)]

## Function returns the opposite cell of a given cell:
def opposite(i,j,x,y):  
    return (i+i-x , j+j-y)

## Function returns the perpendicular to a opposite:
def cross_rest(i,j,x,y):  
    if i==x:
        return [(i+1,j), (i-1,j)]
    else:
        return [(i,j+1), (i,j-1)]    


## Function checks if a cell is surrounded by things already
def is_surrounded(grid,i,j):
    answer = True
    for (x,y) in surroundings(i,j):
        if not is_empty(grid,x,y):
            answer = False
    return answer

## Function checks if a T can be determined into O P B C D or X
def check_T(grid,i,j):
    for (x,y) in cross(i,j):
        if is_boat(grid,x,y):
            (a,b) = opposite(i,j,x,y)
            if grid[a,b]=="_":
                return
            if is_boat(grid,a,b):
                change_cell(grid,i,j,"X")
                return
            if grid[a,b]=="w":
                target=""
                if a>i:
                    target = "U"
                if a<i:
                    target = "P"
                if b>j:
                    target = "D"
                if b<j:
                    target = "C"
                change_cell(grid,i,j,target)
                return
    
    if np.all([grid[x,y]=="w" for (x,y) in cross(i,j)]):
        change_cell(grid,i,j,"O")

    return
                
## Function changes the content of the cell i,j to the given target
def change_cell(grid,i,j,target):
    if is_valid(target):
        if is_changeable(grid,i,j):
            grid[i,j]=target
        else:
            if grid[i,j]!=target:
                if not (target=="T" and is_boat(grid,i,j)):
                    if VERBOSE>2:
                        print("OK, now we have a problem")      
                    raise ValueError
    else:
        if VERBOSE>2:
            print("What are you having me do ?")
        raise ValueError
    return

## Function that changes all surrounding cells if there's a boat
def found_boat(grid,i,j):
    if not is_boat(grid,i,j):
        if VERBOSE>2:
            print("heu I made a mistake here")
        raise ValueError
        return
    
    to_change = [(i+1,j+1) , (i-1,j+1) , (i+1,j-1) , (i-1,j-1)]
    if grid[i,j]=="O":
        to_change = to_change+[(i+1,j) , (i,j-1) , (i-1,j) , (i,j+1)]
    if grid[i,j] =="P":
        to_change = to_change+[          (i,j-1) , (i-1,j) , (i,j+1)]
        change_cell(grid,i+1,j,"T")
    if grid[i,j]=="D":
        to_change = to_change+[(i+1,j) ,           (i-1,j) , (i,j+1)]
        change_cell(grid,i,j-1,"T")
    if grid[i,j]=="U":
        to_change = to_change+[(i+1,j) , (i,j-1) ,           (i,j+1)]
        change_cell(grid,i-1,j,"T")
    if grid[i,j]=="C":
        to_change = to_change+[(i+1,j) , (i,j-1) , (i-1,j)          ]
        change_cell(grid,i,j+1,"T")
    if grid[i,j]=="T":
        check_T(grid,i,j)
    if grid[i,j]=="X":
        for (x,y) in cross(i,j):
            if is_boat(grid,x,y):
                change_cell(grid,opposite(i,j,x,y)[0],opposite(i,j,x,y)[1],"T")
            if grid[x,y]=="w":
                change_cell(grid,opposite(i,j,x,y)[0],opposite(i,j,x,y)[1],"w")
                for (a,b) in cross_rest(i,j,x,y):
                    change_cell(grid,a,b,"T")
    
    for (x,y) in to_change:
        change_cell(grid,x,y,"w")
        
    return        


## Function checks if a line has all its boats or just enough holes to fill it
def check_line(grid,n_boat,i):
    boat_count=count_boat(grid[i,:]) 
    empty_count=count_empty(grid[i,:])
            
    if boat_count==n_boat:
        for j in range(N_COL):
            if is_empty(grid,i,j):
                change_cell(grid,i,j,"w")
    
    if (empty_count == (n_boat-boat_count)):
        for j in range(N_LINE):
            if is_empty(grid,i,j):
                change_cell(grid,i,j,"T")

def check_col(grid,n_boat,j):
    boat_count=count_boat(grid[:,j])
    empty_count=count_empty(grid[:,j])
            
    if boat_count==n_boat:
        for i in range(N_LINE):
            if is_empty(grid,i,j):
                change_cell(grid,i,j,"w")
   
    if (empty_count == (n_boat-boat_count)):
        for i in range(N_LINE):
            if is_empty(grid,i,j):
                change_cell(grid,i,j,"T")
        

## Function check the amount of remaining boats to put in the grid        
def check_remaining(grid,boat_types):
    remaining_boats=boat_types.copy()
    try:
        for i in range(N_LINE):
            boat_size=0
            on_a_boat=False
            for j in range(N_COL):
                if on_a_boat:
                    boat_size+=1
                    if not is_boat(grid,i,j):
                        on_a_boat=False
                        boat_size=0
                        
                if grid[i,j]=="C":
                    boat_size+=1
                    on_a_boat=True
                if grid[i,j]=="D": 
                    if on_a_boat:
                        remaining_boats.remove(boat_size)
                    boat_size=0
                    
                if grid[i,j]=="O":
                    remaining_boats.remove(1)
        for j in range(N_COL):
            boat_size=0
            on_a_boat=False
            for i in range(N_LINE):
                if on_a_boat:
                    boat_size+=1
                    if not is_boat(grid,i,j):
                        on_a_boat=False
                        boat_size=0
                        
                if grid[i,j]=="P":
                    boat_size+=1
                    on_a_boat=True
                if grid[i,j]=="U": 
                    if on_a_boat:
                        remaining_boats.remove(boat_size)
                    boat_size=0
                    
    except ValueError:
        if VERBOSE>2:
            print("I made a mistake in the kind of boats I put")
        raise
                    
    return remaining_boats

## Function that checks if the boats can be closed, according to the remaining boats.
def check_T_remaining(grid,remaining):
    for i in range(N_LINE):
        if "T" in grid[i,:]:
            on_a_boat=False
            boat_size=0
            has_T=False
            T_indices=(0,0)
            for j in range(N_COL):
                if grid[i,j]=="T":  
                    if on_a_boat:
                        boat_size+=1
                        if boat_size==max(remaining):
                            change_cell(grid,i,j,"D")
                        has_T=False
                    else:
                        has_T=True
                        T_indices=(i,j)

                if is_boat(grid,i,j):
                    on_a_boat=True
                    boat_size+=1
                    if grid[i,j]=="D" and has_T and boat_size==max(remaining):
                        change_cell(grid,T_indices[0],T_indices[1],"C")
                        has_T=False
                else:
                    on_a_boat=False
                    boat_size=0
                    has_T=False
    
    for j in range(N_COL):
        if "T" in grid[:,j]:
            on_a_boat=False
            boat_size=0
            has_T=False
            T_indices=(0,0)
            for i in range(N_LINE):
                if grid[i,j]=="T":  
                    if on_a_boat:
                        boat_size+=1
                        if boat_size==max(remaining):
                            change_cell(grid,i,j,"U")
                        has_T=False
                    else:
                        has_T=True
                        T_indices=(i,j)

                if is_boat(grid,i,j):
                    on_a_boat=True
                    boat_size+=1
                    if grid[i,j]=="U" and has_T and boat_size==max(remaining):
                        change_cell(grid,T_indices[0],T_indices[1],"P")
                        has_T=False
                else:
                    on_a_boat=False
                    boat_size=0
                    has_T=False
    
    
## Function that looks where to put the biggest boats. Puts them in if possible
def look_for_space(grid,remaining_boats,boat_in_col,boat_in_line,value=0):
    size=0
    if value==0:
        size = max(remaining_boats)
    else:
        size = min(value,max(remaining_boats))
    
    ## First check for the remaining boats in line and col
    remain_boat_in_line=[]
    for i in range(N_LINE):
        n_boat=0
        on_a_boat=False
        boat_size=0
        full_boat=True
        for j in range(N_COL):            
            if is_boat(grid,i,j):
                on_a_boat=True
                boat_size+=1
                if grid[i,j-1]=="_":
                    full_boat=False
                    
            if grid[i,j]=="w" and on_a_boat:
                on_a_boat=False
                n_boat += (boat_size*full_boat)
                boat_size=0
                full_boat=True
                
            if grid[i,j]=="_" and on_a_boat:
                on_a_boat=False
                boat_size=0
                full_boat=True

        remain_boat_in_line.append(boat_in_line[i]-n_boat)
        
    remain_boat_in_col=[]
    for j in range(N_COL):
        n_boat=0    
        on_a_boat=False
        boat_size=0
        full_boat=True
        for i in range(N_LINE):            
            if is_boat(grid,i,j):
                on_a_boat=True
                boat_size+=1
                if grid[i-1,j]=="_":
                    full_boat=False
                    
            if grid[i,j]=="w" and on_a_boat:
                on_a_boat=False
                n_boat += (boat_size*full_boat)
                boat_size=0
                full_boat=True
                
            if grid[i,j]=="_" and on_a_boat:
                on_a_boat=False
                boat_size=0
                full_boat=True

        remain_boat_in_col.append(boat_in_col[j]-n_boat)
    
    
        
    ## Now look for space in the rows and columns that have big enough boat_in
    n_spaces=0
    space_indices=[]
    
    for i in range(N_LINE):
        if remain_boat_in_line[i]<size:
            continue
        n_empty=0
        origin=(0,0)
        boat_size=0
        for j in range(N_COL):
            if is_empty(grid,i,j):
                n_empty+=1
                if origin==(0,0):
                    origin=(i,j)
            elif is_boat(grid,i,j):
                boat_size+=1
                if origin==(0,0):
                    origin=(i,j)
            elif grid[i,j]=="w":
                if n_empty>0:
                    n_empty+=boat_size                
                    if n_empty>=size:
                        n_spaces+=1
                        space_indices.append((origin,(i,j-1)))
                n_empty=0
                origin=(0,0)
                boat_size=0


                
    for j in range(N_COL):
        if remain_boat_in_col[j]<size:
            continue
        n_empty=0
        origin=(0,0)
        boat_size=0
        for i in range(N_LINE):
            if is_empty(grid,i,j):
                n_empty+=1
                if origin==(0,0):
                    origin=(i,j)
            elif is_boat(grid,i,j):
                boat_size+=1
                if origin==(0,0):
                    origin=(i,j)
            elif grid[i,j]=="w":
                if n_empty>0:
                    n_empty+=boat_size
                    if n_empty>=size:
                        n_spaces+=1 
                        space_indices.append((origin,(i-1,j)))
                n_empty=0
                origin=(0,0)
                boat_size=0
    

    ## checks if there wasnt a mistake : 
    ## _,_,_,w,_T,D,3 would give me 2 possibilities
        ## In fact, I dont need to check this. 
        ## With the possibility to add a boat at random
        ## Then I will simply add a boat in that hole 
        ## and notice I have too many in the row and exclude this possibility
    ## _,_,_,_,_,_,_,6 would give me only 1 possibility for a 3 space    
    for ((x1,y1),(x2,y2)) in space_indices[:]:
        n_boat=0
        if x1==x2:
            n_boat = count_boat(grid[x1,:]) - count_boat(grid[x1,y1:y2+1])
            if n_boat+size > boat_in_line[x1]:
                space_indices.remove(((x1,y1),(x2,y2)))
                
            n_possible_boat = int(np.floor((y2-y1+2)/(size+1)))
            for i in range(2,n_possible_boat+1):
                if i*size + n_boat <= boat_in_line[x1]:
                    space_indices.append(((x1,y1),(x2,y2)))
                
        else: #y1==y2
            n_boat = count_boat(grid[:,y1]) - count_boat(grid[x1:x2+1:,y1])
            if n_boat+size > boat_in_col[y1]:
                space_indices.remove(((x1,y1),(x2,y2)))

            n_possible_boat = int(np.floor((x2-x1+2)/(size+1)))            
            for i in range(2,n_possible_boat+1):
                if i*size + n_boat <= boat_in_col[y1] :
                    space_indices.append(((x1,y1),(x2,y2)))
        
                                            
    if VERBOSE>2:
        print("spaces for boat ",size," after : ",space_indices)
    if len(space_indices)<[i>size-1 for i in remaining_boats].count(True):
        if VERBOSE>2:
            print("c'est bizarre")
        print_grid(grid,boat_in_col,boat_in_line)
        raise ValueError
    if len(space_indices) ==  [i>size-1 for i in remaining_boats].count(True):
        for space in space_indices:
            fit_boat_in_space(grid,size,space)
        
    return space_indices

## Function fits a boat in a given space
def fit_boat_in_space(grid,boat_size,space):
    space_size = max(space[1][0]-space[0][0] , space[1][1] - space[0][1])+1
    
    if space_size<boat_size:
        if VERBOSE>2:
            print("houston, we have a problem")
        raise ValueError
    
    step=0
    for i in range(space[0][0],space[1][0]+1):
        for j in range(space[0][1], space[1][1]+1):            
            if not (step<space_size-boat_size or step>=boat_size):
                change_cell(grid,i,j,"T")            
            step+=1
    return


## Checks if the game is done:
def is_done(grid):
    return not ("_" in grid)


## The different iterations to be done
def iterate(grid,boat_in_col,boat_in_line,boat_types,iterations=0):
    while True:
        if VERBOSE>1:
            print("iter : ",iterations)
        if VERBOSE>3:
            print_grid(grid,boat_in_col,boat_in_line)
        iterations+=1
        old_grid = grid.copy()  
    
        
    ### Step 1 : fill water according to boats
    ###########
        for i in range(1,N_LINE):
            for j in range(1,N_COL):            
                if (is_boat(grid,i,j)):
                    found_boat(grid,i,j)
        
        if np.any(old_grid!=grid):
            continue
        
        if is_done(grid):
            return grid
    
    ### Step 2 : check lines and columns for the number of boats
    ###########    
        for i in range(len(boat_in_col)):
            check_col(grid,boat_in_col[i],i)
        for i in range(len(boat_in_line)):
            check_line(grid,boat_in_line[i],i)
    
        if np.any(old_grid!=grid):
            continue
        
        if is_done(grid):
            return grid


    ### Step 3 : Check if some boats can be closed off
    ###########    
        remaining_boats=check_remaining(grid,boat_types)
        check_T_remaining(grid,remaining_boats)
        if np.any(old_grid!=grid):
            continue
        
        if is_done(grid):
            return grid

    ### Step 4 : Check for the big boats
    ###########        
        remaining_boats=check_remaining(grid,boat_types)
        if VERBOSE>2:
            print("remaining_boats = ",remaining_boats)
        if len(remaining_boats)>0:
            to_continue=True            
            for value in sorted(set(remaining_boats),reverse=True):
                if value>1 and to_continue:
                    look_for_space(grid,remaining_boats,boat_in_col,boat_in_line,value)
                    if np.any(old_grid!=grid):
                        to_continue=False
        if np.any(old_grid!=grid):
            continue
        else:
            break

    return grid


## Add a random cell and checks the consequences it has
def add_random(grid,boat_in_col,boat_in_line,boat_types,target):
    if target not in ["w","T"]:        
        print("i think there has been a confusion with the parameter")
        raise ValueError 
        
    to_fill = np.where(grid=="_")
    safe_grid=grid.copy()        
    for (i,j) in list(zip(to_fill[0],to_fill[1])):
        if VERBOSE>3:
            print_grid(grid,boat_in_col,boat_in_line)
        
        if VERBOSE>2:
            print("Trying to change cell : ",i,j," with a ",target)
        #input("waiting")
        change_cell(grid,i,j,target)
        try:
            iterate(grid,boat_in_col,boat_in_line,boat_types)
        except:
            if VERBOSE>2:
                print("there has been a mistake so I guess this test failed")
        if VERBOSE>2:
            print("after trying, is grid valid : ", check_valid_grid(grid,boat_in_col,boat_in_line,boat_types))
        if VERBOSE>3:
            print_grid(grid,boat_in_col,boat_in_line)
        if check_valid_grid(grid,boat_in_col,boat_in_line,boat_types) and is_done(grid):
            return grid
        else:
            if not check_valid_grid(grid,boat_in_col,boat_in_line,boat_types):
                if target=="w":
                    new_target="T"
                else: #target =="T"
                    new_target="w"
                change_cell(safe_grid,i,j,new_target)
                grid=safe_grid.copy()
                break
            grid=safe_grid.copy()    
    return grid

## Add a random boat and checks the consequences it has
def add_random_boat(grid,remaining_boats,boat_in_col,boat_in_line,boat_types):
    if VERBOSE>2:
        print("remaining_boats = ",remaining_boats)
    safe_grid=grid.copy()
    if len(remaining_boats)>0:  
        for value in sorted(set(remaining_boats),reverse=True):
            if value>1:
                spaces = look_for_space(grid,remaining_boats,boat_in_col,boat_in_line,value)
            
            for ((x1,y1,),(x2,y2)) in spaces:
                new_spaces=[]
                if (x1==x2):
                    for i in range(y1,y2-value+2):
                        new_spaces.append((x1,i),(x2,i+value-1))
                else: #y1==y2
                    for i in range(x1,x2-value+2):
                        new_spaces.append((i,y1),(i+value-1,y2))
                for new_space in new_spaces:
                    try:
                        grid = fit_boat_in_space(grid,value,new_space)
                        iterate(grid,boat_in_col,boat_in_line,boat_types)
                    except:
                        if VERBOSE>2:
                            print("there has been a mistake so I guess this test failed")
                    if VERBOSE>2:
                        print("after trying, is grid valid : ", check_valid_grid(grid,boat_in_col,boat_in_line,boat_types))
                    if VERBOSE>3:
                        print_grid(grid,boat_in_col,boat_in_line)
                    if check_valid_grid(grid,boat_in_col,boat_in_line,boat_types) and is_done(grid):
                        return grid
                    else:
                        grid=safe_grid.copy()
    return safe_grid


## The different iterations to be done
## This time, it includes trying things at random
def iterate_random(grid,boat_in_col,boat_in_line,boat_types,iterations=0):
    while True:

        grid= iterate(grid,boat_in_col,boat_in_line,boat_types)
        old_grid = grid.copy()
        
        ### Step 1 : Add a random boat_point somewhere
        ###########
        grid = add_random(grid,boat_in_col,boat_in_line,boat_types,"T")
        if np.any(old_grid!=grid):
            continue
        if is_done(grid):
            return grid
        
        ### Step 2 : Add a random water somewhere
        ###########
        grid = add_random(grid,boat_in_col,boat_in_line,boat_types,"w")
        if np.any(old_grid!=grid):
            continue
        if is_done(grid):
            return grid
        
        ### Step 3 : Add a boat at random
        ###########
        remaining_boats=check_remaining(grid,boat_types)
        check_T_remaining(grid,remaining_boats)
        remaining_boats=check_remaining(grid,boat_types)
        grid = add_random_boat(grid,remaining_boats,boat_in_col,boat_in_line,boat_types)
            
    return grid

## Load a grid from file and check its consistency
def load_grid(path_to_grid):
    grid_list = []
    boat_in_line = []
    boat_in_col = []
    water_line=[]

    n_line = 0
    n_col = 0

    with open(path_to_grid) as grid_in: 
        for l in grid_in:
            if VERBOSE>1:
                print(l)
            n_line+=1
            line_arr = l.strip().split(sep=',')
            
            # First line, get the numer of columns and add a line full of water
            if n_col==0:
                n_col = len(line_arr)
            
            if n_line ==1:        
                for i in range(n_col+1):
                    water_line.append("w")
                grid_list.append(water_line)
                boat_in_line.append(0)
                
            
            if len(line_arr)!= n_col:
                print("Error in the size of the grid : inconsistent amount of columns")
                sys.exit(0)
        
            if n_line!= n_col:
                for c in line_arr[:-1]:
                    if not is_valid_beginning(c):
                        print("Error in the grid : invalid character ",c)
                        sys.exit(0)
                grid_list.append(["w"]+line_arr[:-1]+["w"])
                boat_in_line.append(int(line_arr[-1]))
            else:
                grid_list.append(water_line)
                boat_in_line.append(0)
                boat_in_col = [0]+[int(i) for i in line_arr[:-1]]+[0]
        
            
    if n_line!=n_col:
        print("Error in the size of the grid : grid not square")
        sys.exit(0)

    ### Last check for the grid
    total_boats = sum(boat_types)
    boats_line = sum(boat_in_line)
    boats_col = sum(boat_in_col)    
    if boats_line != boats_col:
        print("Check your initial grid, you made a mistake",boats_line,boats_col)
        raise ValueError
    if total_boats != boats_col:
        print("Check your initial grid, you made a mistake",total_boats,boats_col)
        raise ValueError
    
    grid = np.array(grid_list)

    return grid,boat_in_col,boat_in_line
        
###################################
##########   main   ###############
###################################
        
#if __name__ = main
if __name__ == "__main__":
    text_grid = u"""
The grid should be square and follow the following standards :
    _ = blank ;
    w = Water ;
    O = Circle (single boat) ;
    X = Square (in the middle of a boat) ;
    P = Top of boat ;
    C = Left side of boat ;
    U = Bottom of boat ;
    D = Right side of boat ;
each cell is separated by a comma (,)
        
Example of a grid:
    _,_,_,_,_,_,_,_,_,5
    _,_,_,_,_,_,_,_,_,0
    _,_,_,_,_,_,w,_,_,2
    _,_,_,_,_,_,_,_,_,3
    _,_,_,_,_,_,C,_,_,3
    _,_,_,_,U,_,_,_,_,2
    _,_,X,_,_,_,_,_,_,1
    _,_,_,_,_,_,_,_,_,4
    _,_,_,_,_,_,_,_,_,0
    2,1,3,0,6,0,3,3,2,
    """
            
    text_size = """
The size argument determines the amount of boats in the grid. 
It is supposed that there are :
    1 boat of maximum size
    2 boats of size max-1
    3 boats of size max-2
    n boats of size max+1-n
    """
    
    text_output = """Path to output the grid.
Default = [path]_answer.[ext]"""


    parser = argparse.ArgumentParser(
            description="This program solves a bimaru.",
            formatter_class=argparse.RawTextHelpFormatter
            )
    parser.add_argument('path',  type=str,
                    help='Path to the grid' + text_grid)
    parser.add_argument('size', type=int,                
                    help='Size of the biggest boat.'+text_size)
    parser.add_argument('--output', type=str,
                    help=text_output)
    parser.add_argument('--verbose', type=int,default=0,
                    help='verbose level.')
        
    args = parser.parse_args()
    path_to_grid = args.path
    max_boat_size = args.size
    ofile=args.output
    VERBOSE = args.verbose
    
    if ofile==None:
        if len(path_to_grid.split("."))>2:
            print("dont put dots in your paths you psycho!")
            exit
        else:
            ofile = path_to_grid.split(".")[0]+"_answer."+path_to_grid.split(".")[1]
    
    ## Define the list of boats from size
    boat_types=[]
    for i in range(max_boat_size,0,-1):
        boat_types = boat_types+list(range(i,0,-1))
    boat_types = sorted(boat_types,reverse=True)
    
    ## Get the grid
    grid,boat_in_col,boat_in_line = load_grid(path_to_grid)
    N_LINE = grid.shape[0]
    N_COL = grid.shape[1]

    ## The main work          
    grid = iterate_random(grid,boat_in_col,boat_in_line,boat_types)

    ## Over
    ########    
    if check_valid_grid(grid,boat_in_col,boat_in_line,boat_types) and is_done(grid):
        print("wouhou, Im done !")
        print("here is the answer:")
        output = print_grid(grid,boat_in_col,boat_in_line,final=True)
        np.savetxt(ofile,output,fmt="%s",delimiter=",")
            
    else:
        print_grid(grid,boat_in_col,boat_in_line)
        print("Im stuck, I need help")
        