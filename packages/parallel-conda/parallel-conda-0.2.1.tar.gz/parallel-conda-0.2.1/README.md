# parallel-conda
Dev Area for Prototype of a parallel wrapper of conda  
(NOT SUITABLE FOR USE,....it barely works right now and has no tests)

---

Use:  
```commandline
pconda install pandas --name <env_name>
```

Installs all required packages in parallel.  
All commands you would normally pass to `conda install` works as well.

**NOTE**  
Only a replacement for `conda install`, does not include any ability for uninstalling or otherwise.  
Additionally, I am in no way associated with conda or Anaconda in general, just some dude who wanted faster installs.