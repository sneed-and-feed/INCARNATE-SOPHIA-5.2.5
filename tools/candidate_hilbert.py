"""
MUTATION: HILBERT_CURVE_V1 (The Labyrinth)
ORIGIN: EVOLUTIONARY_STEP_01
GOAL: Maximize Regional Love (Locality) by traversing space continuously without jumps.
"""

import numpy as np

def strip_2d(x: int, y: int) -> int:
    """
    Map 2D (x,y) to 1D z using Hilbert Curve logic.
    Assumes 16-bit coordinates (N=65536, Order=16).
    """
    d = 0
    s = 65536 // 2 # Initial Half size (2^15)
    
    # We iterate down through scales (MSB to LSB)
    current_x = x
    current_y = y
    
    while s > 0:
        rx = (current_x & s) > 0
        ry = (current_y & s) > 0
        
        # Add position to d
        # Hilbert quadrant mapping:
        # 0: (0,0) -> 0
        # 1: (0,1) -> 1
        # 2: (1,1) -> 2
        # 3: (1,0) -> 3
        # Logic: 
        # if ry=0: rx=0 -> 0 (00), rx=1 -> 3 (11) ?? No.
        # Standard Hilbert:
        # rx ry d
        # 0  0  0
        # 0  1  1
        # 1  1  2
        # 1  0  3
        
        d += s * s * ((3 * rx) ^ ry)
        
        # Rotate/Flip
        if ry == 0:
            if rx == 1:
                current_x = (s - 1) - current_x
                current_y = (s - 1) - current_y
            
            # Swap x, y
            current_x, current_y = current_y, current_x
            
        s //= 2
        
    return d

# NOTE: Since the evaluator reconstructs 1D -> 2D to test locality,
# we strictly need a reconstruction function or the evaluator loop 
# needs to be bidirectional. 
# tools/funsearch_love.py L28 uses: 
#   z = program.strip_2d(x, y) 
#   x_rec, y_rec = program.reconstruct_1d(z)
# So we need BOTH.

def reconstruct_1d(z: int) -> tuple[int, int]:
    """
    Inverse Hilbert: Map 1D z to 2D (x,y).
    """
    t = z
    x = 0
    y = 0
    s = 1
    
    # We iterate UP through scales, but standard algo often goes down?
    # Actually, simpler to treat as composing quadrants.
    # N=65536 means 16 bits per coord, 32 bits total for z.
    
    while s < 65536:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        
        # Rotate/Flip
        if ry == 0:
            if rx == 1:
                x = (s - 1) - x
                y = (s - 1) - y
            x, y = y, x
            
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
        
    return x, y
