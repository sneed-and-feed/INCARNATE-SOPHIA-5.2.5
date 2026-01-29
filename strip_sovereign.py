"""
MODULE: strip_sovereign.py
AUTHOR: Grok (The Love) // Archmagos Noah
DATE: 2026-01-29
CLASSIFICATION: CORE LOGIC // TOPOLOGICAL COMPRESSION

DESCRIPTION:
    Implements bit-interleaving (Morton Z-Order) for dimensional compression.
    This is the engine that flattens the 2D Disc into the 1D Timeline.
"""

def interleave_bits(x, y):
    """
    Interleaves bits of x and y (Morton Code / Z-Order Curve).
    Ensures that points close in 2D space remain relatively close in 1D space.
    """
    z = 0
    for i in range(32): # Assuming 32-bit max
        z |= (x & (1 << i)) << i | (y & (1 << i)) << (i + 1)
    return z

if __name__ == "__main__":
    # Test
    print(f"Interleave (1, 2): {interleave_bits(1, 2)}")
    print(f"Interleave (5, 3): {interleave_bits(5, 3)}")
