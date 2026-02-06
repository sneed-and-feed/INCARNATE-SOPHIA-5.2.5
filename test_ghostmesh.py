import numpy as np

class FlumpyArray(np.ndarray):
    def __new__(cls, input_array, coherence=1.0):
        obj = np.asarray(input_array).view(cls)
        obj.coherence = coherence
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.coherence = getattr(obj, 'coherence', 1.0)

    def copy(self):
        arr = np.copy(self.view(np.ndarray))
        arr = arr.view(FlumpyArray)
        arr.coherence = self.coherence
        return arr

    def clone(self):
        print("FlumpyArray.clone() called")
        return self.copy()

# Test the clone method
arr = FlumpyArray([1, 2, 3], coherence=0.5)
cloned_arr = arr.clone()

print(cloned_arr)
print(cloned_arr.coherence)