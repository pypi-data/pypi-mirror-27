### notebook-autorun

This module enables auto-run of certains cells at notebook kernel start.  
It will work **only** for <span style="color: red">**trusted**</span> notebooks.  

#### 1 - Settings

The cells to autorun can be determined by one of the 3 args below.  
Only one of them must be specified:  
+ `cells`: List of 0-indexed cells or String representing a list of cells. [Python list slices](https://docs.python.org/2.3/whatsnew/section-slices.html) are allowed. Default is `None`. `cells` is stringified to `str_cells` before passing to javascript. Invalid cell numbers (e.g. greater than the notebook number of cells) are ignored. Examples: [2, 3], '2,3', '2:', ':-2', '4:8', '::-1'  
+ `metadata`: Boolean (default is `False`). If `True`, all cells with medatada `"autorun": true` are concerned.  
+ `comment`: Boolean (default is `False`). If `True`, all cells containing a comment `comment_flag` (default is `# AUTORUN`) are concerned.  


#### 2 - Security

Because a notebook is designed to allow the user to write arbitrary code, it has full access to many resources.   

The typical risks are the following:
+ A notebook has access to your file system and can therefore potentially read/modify/delete any of your files or send them to an attacker, or write a new file (virus).  
+ A notebook may contain javascript in output cells which can read you cookies and local storage and potentially send them to an attacker.  

See the [Security in notebook documents](https://jupyter-notebook.readthedocs.io/en/stable/security.html#security-in-notebook-documents) section of the official [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/stable/index.html) for more info.  

Therefore you **should review** and **must trust** the notebook before you can use **notebook-autorun**.
