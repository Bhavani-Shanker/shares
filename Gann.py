# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 18:11:55 2023

@author: user
"""

import numpy as np
import math
L = [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1]
def Gann(Close):
    f4 = Close
    g4= np.sqrt(f4)
    e4 =  math.floor(g4)
    d4 = e4-1
    #=IF(INT(G4)=G4,G4+1,CEILING(G4,1))
    if int(g4) == g4:
        h4 = g4+1
    else:
        h4 = math.ceil(g4)
    
    i4 = h4+1    
    
    e9 = np.power(d4,2,dtype=int)
    d9 = np.round(np.power((d4+L[0]),2),2)
    d8 = np.round(np.power((d4+L[1]),2),2)
    #=POWER(($D$4+L7),2)    
    e10 = np.round(np.power((d4+L[6]),2),2)
    
    #=POWER(($D$4+L3),2)
    e8 = np.round(np.power((d4+L[2]),2),2)
    
    #=POWER(($D$4+L4),2)
    f8 = np.round(np.power((d4+L[3]),2),2)
    
    #=POWER(($D$4+L5),2)
    f9 = np.round(np.power((d4+L[4]),2),2)
    
    #=POWER(($D$4+L6),2)
    f10 = np.round(np.power((d4+L[5]),2),2)
    
    #=($E$4+L6)*($E$4+L6)
    g11 = round((e4+L[5])*(e4+L[5]),2)
    
    #=($E$4+L7)*($E$4+L7)
    e11 = round((e4+L[6])*(e4+L[6]),2)
    
    #=IF(AND($F$4>=G11,$F$4<E11),VALUE($F$4),"")
    if (f4 >= g11 and f4<e11):
        f11 = f4
    else:
        f11 = ''

    #=($E$4+L8)*($E$4+L8)
    c11 = round((e4+L[7])*(e4+L[7]),2)
        
    #=IF(AND($F$4>=E11,$F$4<C11),VALUE($F$4),"")
    if (f4 >=e11 and f4<c11):
        d11 = f4
    else:
        d11 = ''
        
    #=POWER(($D$4+L8),2)
    d10= round((d4+L[7])*(d4+L[7]),2)    
    
    #=($E$4+L1)*($E$4+L1)
    c9 = round((e4+L[0])*(e4+L[0]),2)    
    
    #=IF(AND($F$4>=D10,$F$4<C9),VALUE($F$4),"")
    if (f4>=d10 and f4<c9):
        c10 = f4
    else:
        c10 = ''

    #=($E$4+L2)*($E$4+L2)
    c7 =round((e4+L[1])*(e4+L[1]) ,2)
    
    #=IF(AND($F$4>=C9,$F$4<C7),VALUE($F$4),"")
    if (f4>=c9 and f4<c7):
        c8 = f4
    else:
        c8 = ''
    
    #=($E$4+L3)*($E$4+L3)
    e7 = round((e4+L[2])*(e4+L[2]) ,2)
    
    #=IF(AND($F$4>=C7,$F$4<E7),VALUE($F$4),"")
    if (f4>=c7 and f4<e7):
        d7= f4
    else:
        d7 = ''
    
    #=($E$4+L4)*($E$4+L4)
    g7 = round((e4+L[3])*(e4+L[3]) ,2)
    
    #=IF(AND($F$4>=E7,$F$4<G7),VALUE($F$4),"")
    if (f4 >= e7 and f4<g7):
        f7 = f4
    else:
        f7 = ''
    
    #=($E$4+L5)*($E$4+L5)
    g9 = round((e4+L[4])*(e4+L[4]) ,2)
    
    #=IF(AND($F$4>=G7,$F$4<G9),VALUE($F$4),"")
    if (f4>=g7 and f4<g9):
        g8 = f4
    else:
        g8 = ''
    
    #=($E$4+L6)*($E$4+L6)
    g11= round((e4+L[5])*(e4+L[5]) ,2)
    
    
    #=IF(AND($F$4>=G9,$F$4<G11),VALUE($F$4),"")
    if (f4>=g9 and f4<g11):
        g10 = f4
    else:
        g10 = ''
    
    
    #=($H$4+L7)*($H$4+L7)
    e12 = round((h4+L[6])*(h4+L[6]) ,2)
    
    #=($H$4+L8)*($H$4+L8)
    b12 = round((h4+L[7])*(h4+L[7]) ,2)
    
    #=IF(AND($F$4>=E12,$F$4<B12),VALUE($F$4),"")
    if (f4>=e12 and f4<b12):
        d12 = f4
    else:
        d12 = ''
    

    #=IF(AND($F$4>=C11,$F$4<B9),VALUE($F$4),"")
    if (f4>=c11 and f4<b9):
        b11 = f4
    else:
        b11 = ''
        
    #=($H$4+L1)*($H$4+L1)
    b9 = round((h4+L[0])*(h4+L[0]) ,2)    
    
    #=IF(AND($F$4>=B9,$F$4<B6),VALUE($F$4),"")
    if (f4>=b9 and f4<b6):
        b8 = f4
    else:
        b8 = ''
        
    #=($H$4+L2)*($H$4+L2)
    b6 = round((h4+L[1])*(h4+L[1]) ,2)        
    
    #=IF(AND($F$4>=B6,$F$4<E6),VALUE($F$4),"")
    if (f4>=b6 and f4<e6):
        c6 = f4
    else:
        c6 = ''
        
    #=($H$4+L3)*($H$4+L3)
    e6 = round((h4+L[2])*(h4+L[2]) ,2)            
    
    #=IF(AND($F$4>=E6,$F$4<H6),VALUE($F$4),"")
    if (f4>=e6 and f4<h6):
        f6 = f4
    else:
        f6 = ''
        
    #=($H$4+L4)*($H$4+L4)
    h6 =     round((h4+L[3])*(h4+L[3]) ,2)            
    
    #=IF(AND($F$4>=H6,$F$4<H9),VALUE($F$4),"")
    if (f4>=h6 and f4<h9):
        h7 = f4
    else:
        h7 = ''
    
    #=($H$4+L5)*($H$4+L5)
    h9 =     round((h4+L[4])*(h4+L[4]) ,2)            
    
    #=IF(AND($F$4>=H9,$F$4<H12),VALUE($F$4),"")
    if (f4>=h9 and f4<h12):
        h10 = f4
    else:
        h10 = ''
        
    #=($H$4+L6)*($H$4+L6)
    h12 =    round((h4+L[5])*(h4+L[5]) ,2)            
    
    #=IF(AND($F$4>=H12,$F$4<E12),VALUE($F$4),"")
    if (f4 >=h12 and f4<e12):
        g12 = f4
    else:
        g12 = ''

    if c10!='':
    	Buy_At = c9
    elif c8!= '':
    	Buy_At = c7
    elif d7!= '':
    	Buy_At = e7
    elif f7!= '':
    	Buy_At = g7	
    elif g8!= '':
    	Buy_At = g9
    elif g10!= '':
    	Buy_At = g11
    elif f11!= '':
    	Buy_At = e11
    elif d11!= '':
    	Buy_At = c11
    elif b8!= '':
    	Buy_At = b6
    elif c6!= '':
    	Buy_At = e6
    elif f6!= '':
    	Buy_At = h6
    elif h7!= '':
    	Buy_At = h9
    elif h10!= '':
    	Buy_At = h12
    elif g12!= '':
    	Buy_At = e12
    elif d12!= '':
    	Buy_At = b12
    else:
    	Buy_At = ''	
    

    if c10!='':
    	Resistance1 = c7
    elif c8!= '':
    	Resistance1 = e7
    elif d7!= '':
    	Resistance1 = g7
    elif f7!= '':
    	Resistance1 = g9	
    elif g8!= '':
    	Resistance1 = g11
    elif g10!= '':
    	Resistance1 = e11
    elif f11!= '':
    	Resistance1 = c11
    elif d11!= '':
    	Resistance1 = b9
    elif b11!= '':
    	Resistance1 = b6
    elif b8!= '':
    	Resistance1 = e6	
    elif c6!= '':
    	Resistance1 = h6
    elif f6!= '':
    	Resistance1 = h9
    elif h7!= '':
    	Resistance1 = h12
    elif h10!= '':
    	Resistance1 = e12
    elif g12!= '':
    	Resistance1 = b12
    elif d12!= '':
    	Resistance1 = b12
    else:
    	Resistance1 = ''


    if c10!='':
    	Resistance2 = e7
    elif c8!= '':
    	Resistance2 = g7
    elif d7!= '':
    	Resistance2 = g9
    elif f7!= '':
    	Resistance2 = g11	
    elif g8!= '':
    	Resistance2 = e11
    elif g10!= '':
    	Resistance2 = c11
    elif f11!= '':
    	Resistance2 = b9
    elif d11!= '':
    	Resistance2 = b6
    elif b11!= '':
    	Resistance2 = e6
    elif b8!= '':
    	Resistance2 = h6	
    elif c6!= '':
    	Resistance2 = h9
    elif f6!= '':
    	Resistance2 = h12
    elif h7!= '':
    	Resistance2 = e12
    elif h10!= '':
    	Resistance2 = b12
    elif g12!= '':
    	Resistance2 = b12
    elif d12!= '':
    	Resistance2 = b12
    else:
    	Resistance2 = ''	


    if c10!='':
    	Resistance3 = g7
    elif c8!= '':
    	Resistance3 = g9
    elif d7!= '':
    	Resistance3 = g11
    elif f7!= '':
    	Resistance3 = e11	
    elif g8!= '':
    	Resistance3 = c11
    elif g10!= '':
    	Resistance3 = b9
    elif f11!= '':
    	Resistance3 = b6
    elif d11!= '':
    	Resistance3 = e6
    elif b11!= '':
    	Resistance3 = h6
    elif b8!= '':
    	Resistance3 = h9	
    elif c6!= '':
    	Resistance3 = h12
    elif f6!= '':
    	Resistance3 = e12
    elif h7!= '':
    	Resistance3 = b12
    elif h10!= '':
    	Resistance3 = b12
    elif g12!= '':
    	Resistance3 = b12
    elif d12!= '':
    	Resistance3 = b12
    else:
    	Resistance3 = ''

    if c10!='':
    	Resistance4 = g9
    elif c8!= '':
    	Resistance4 = g11
    elif d7!= '':
    	Resistance4 = e11
    elif f7!= '':
    	Resistance4 = c11	
    elif g8!= '':
    	Resistance4 = b9
    elif g10!= '':
    	Resistance4 = b6
    elif f11!= '':
    	Resistance4 = e6
    elif d11!= '':
    	Resistance4 = h6
    elif b11!= '':
    	Resistance4 = h9
    elif b8!= '':
    	Resistance4 = h12	
    elif c6!= '':
    	Resistance4 = e12
    elif f6!= '':
    	Resistance4 = b12
    elif h7!= '':
    	Resistance4 = b12
    elif h10!= '':
    	Resistance4 = b12
    elif g12!= '':
    	Resistance4 = b12
    elif d12!= '':
    	Resistance4 = b12
    else:
    	Resistance4 = ''

    if c10!='':
    	Resistance5 = g11
    elif c8!= '':
    	Resistance5 = e11
    elif d7!= '':
    	Resistance5 = c11
    elif f7!= '':
    	Resistance5 = b9	
    elif g8!= '':
    	Resistance5 = b6
    elif g10!= '':
    	Resistance5 = e6
    elif f11!= '':
    	Resistance5 = h6
    elif d11!= '':
    	Resistance5 = h9
    elif b11!= '':
    	Resistance5 = h12
    elif b8!= '':
    	Resistance5 = e12	
    elif c6!= '':
    	Resistance5 = b12
    elif f6!= '':
    	Resistance5 = b12
    elif h7!= '':
    	Resistance5 = b12
    elif h10!= '':
    	Resistance5 = b12
    elif g12!= '':
    	Resistance5 = b12
    elif d12!= '':
    	Resistance5 = b12
    else:
    	Resistance5 = ''	        

    Buy_Target1 = round((Resistance1*0.9995),2)
    Buy_Target2 = round((Resistance2*0.9995),2)
    Buy_Target3 = round((Resistance3*0.9995),2)
    Buy_Target4 = round((Resistance4*0.9995),2)
    Buy_Target5 = round((Resistance5*0.9995),2)

    if c10!='':
    	Sell_At = d10
    elif c8!= '':
    	Sell_At = c9
    elif d7!= '':
    	Sell_At = c7
    elif f7!= '':
    	Sell_At = e7	
    elif g8!= '':
    	Sell_At = g7
    elif g10!= '':
    	Sell_At = g9
    elif f11!= '':
    	Sell_At = g11
    elif d11!= '':
    	Sell_At = e11
    elif b11!= '':
    	Sell_At = c11
    elif b8!= '':
    	Sell_At = b9	
    elif c6!= '':
    	Sell_At = b6
    elif f6!= '':
    	Sell_At = e6
    elif h7!= '':
    	Sell_At = h6
    elif h10!= '':
    	Sell_At = h9
    elif g12!= '':
    	Sell_At = h12
    elif d12!= '':
    	Sell_At = e12
    else:
    	Sell_At = ''	
    
    if c10!='':
    	Support1 = e10
    elif c8!= '':
    	Support1 = d10
    elif d7!= '':
    	Support1 = c9
    elif f7!= '':
    	Support1 = c7	
    elif g8!= '':
    	Support1 = e7
    elif g10!= '':
    	Support1 = g7
    elif f11!= '':
    	Support1 = g9
    elif d11!= '':
    	Support1 = g11
    elif b11!= '':
    	Support1 = e11
    elif b8!= '':
    	Support1 = c11	
    elif c6!= '':
    	Support1 = b9
    elif f6!= '':
    	Support1 = b6
    elif h7!= '':
    	Support1 = e6
    elif h10!= '':
    	Support1 = h6
    elif g12!= '':
    	Support1 = h9
    elif d12!= '':
    	Support1 = h12
    else:
    	Support1 = ''	
        

    if c10!='':
    	Support2 = f10
    elif c8!= '':
    	Support2 = e10
    elif d7!= '':
    	Support2 = d10
    elif f7!= '':
    	Support2 = c9	
    elif g8!= '':
    	Support2 = c7
    elif g10!= '':
    	Support2 = e7
    elif f11!= '':
    	Support2 = g7
    elif d11!= '':
    	Support2 = g9
    elif b11!= '':
    	Support2 = g11
    elif b8!= '':
    	Support2 = e11	
    elif c6!= '':
    	Support2 = c11
    elif f6!= '':
    	Support2 = b9
    elif h7!= '':
    	Support2 = b6
    elif h10!= '':
    	Support2 = e6
    elif g12!= '':
    	Support2 = h6
    elif d12!= '':
    	Support2 = h9
    else:
    	Support2 = ''

    if c10!='':
    	Support3 = f9
    elif c8!= '':
    	Support3 = f10
    elif d7!= '':
    	Support3 = e10
    elif f7!= '':
    	Support3 = d10	
    elif g8!= '':
    	Support3 = c9
    elif g10!= '':
    	Support3 = c7
    elif f11!= '':
    	Support3 = e7
    elif d11!= '':
    	Support3 = g7
    elif b11!= '':
    	Support3 = g9
    elif b8!= '':
    	Support3 = g11	
    elif c6!= '':
    	Support3 = e11
    elif f6!= '':
    	Support3 = c11
    elif h7!= '':
    	Support3 = b9
    elif h10!= '':
    	Support3 = b6
    elif g12!= '':
    	Support3 = e6
    elif d12!= '':
    	Support3 = h6
    else:
    	Support3 = ''        
        

    if c10!='':
    	Support4 = f8
    elif c8!= '':
    	Support4 = f9
    elif d7!= '':
    	Support4 = f10
    elif f7!= '':
    	Support4 = e10	
    elif g8!= '':
    	Support4 = d10
    elif g10!= '':
    	Support4 = c9
    elif f11!= '':
    	Support4 = c7
    elif d11!= '':
    	Support4 = e7
    elif b11!= '':
    	Support4 = g7
    elif b8!= '':
    	Support4 = g9	
    elif c6!= '':
    	Support4 = g11
    elif f6!= '':
    	Support4 = e11
    elif h7!= '':
    	Support4 = c11
    elif h10!= '':
    	Support4 = b9
    elif g12!= '':
    	Support4 = b6
    elif d12!= '':
    	Support4 = e6
    else:
    	Support4 = ''        
        
    if c10!='':
    	Support5 = e8
    elif c8!= '':
    	Support5 = f8
    elif d7!= '':
    	Support5 = f9
    elif f7!= '':
    	Support5 = f10	
    elif g8!= '':
    	Support5 = e10
    elif g10!= '':
    	Support5 = d10
    elif f11!= '':
    	Support5 = c9
    elif d11!= '':
    	Support5 = c7
    elif b11!= '':
    	Support5 = e7
    elif b8!= '':
    	Support5 = g7	
    elif c6!= '':
    	Support5 = g9
    elif f6!= '':
    	Support5 = g11
    elif h7!= '':
    	Support5 = e11
    elif h10!= '':
    	Support5 = c11
    elif g12!= '':
    	Support5 = b9
    elif d12!= '':
    	Support5 = b6
    else:
    	Support5 = ''        
        
    Sell_target1 = round((Support1*1.0005),2)
    Sell_target2 = round((Support2*1.0005),2)
    Sell_target3 = round((Support3*1.0005),2)
    Sell_target4 = round((Support4*1.0005),2)
    Sell_target5 = round((Support5*1.0005),2)
    
    return(Buy_At,Sell_At,Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,Sell_target1, Sell_target2, Sell_target3, Sell_target4,Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,Support1, Support2, Support3, Support4,Support5)

