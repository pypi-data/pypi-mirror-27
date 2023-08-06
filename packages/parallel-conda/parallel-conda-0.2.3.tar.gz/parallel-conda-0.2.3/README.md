# parallel-conda

parallel-conda is meant to be a drop-in replacement for `conda install` commands.
Instead of downloading / installing each package sequentially, it does it in parallel.  

Ready for BETA testing!  
Please submit issues if (when) you experience them.

## Install
![Anaconda](https://anaconda.org/milesgranger/parallel-conda/badges/installer/conda.svg)  
Anaconda: `conda install -c milesgranger parallel-conda`   
PyPi: `pip install --upgrade parallel-conda`  
Source: `pip install git+https://github.com/milesgranger/parallel-conda.git`

## Uninstall
`conda uninstall parallel-conda`  
`pip uninstall parallel-conda`

---

## Example:  
```commandline
pconda install pandas numpy scikit-learn
```

Installs all required packages in parallel.  
All commands you would normally pass to `conda install` works as well.

**IMPORTANT NOTE**  
Only a replacement for `conda install`, does not include any ability for uninstalling or otherwise; unless the
uninstall would take place during the install process.  
Additionally, I am in no way associated with conda or Anaconda in general, just some dude who wanted faster installs.