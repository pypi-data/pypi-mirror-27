# random_custom_pdf

Generate random numbers with custom probability density function.
To generate the sample, the truncation method is used.

## Installation
    
        pip install https://github.com/kapot65/random_custom_pdf/archive/master.zip
		
## Usage
        
        import numpy as np
        from random_custom_pdf import rand_custom
        x = np.array([0, 2000, 4000])
        y = np.array([0, 200, 0])
        out = rand_custom(x, y, (1000, 1000))
        