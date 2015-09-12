#coding:utf-8
import sys
from InformationRetrival import *

ir = InformationRetrival(sys.argv[1], float(sys.argv[2]), sys.argv[3])

#"w7Hv5UCrrHE3bZysRWRvuBCbibeduPuGJSfKqM1rc7Y",0.9,"gates"

while True:
    ir.infoQuery()
    if ir.stop == 1:       
        break
    ir.update()

    
