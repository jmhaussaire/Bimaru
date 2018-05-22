# Bimaru
Bimaru solver in python

This program solves a bimaru.
Given an input grid and a size (determining the number and size of boats), it returns the solution to this bimaru. 

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

The size argument determines the amount of boats in the grid. 
It is supposed that there are :
    1 boat of maximum size
    2 boats of size max-1
    3 boats of size max-2
    n boats of size max+1-n
    
