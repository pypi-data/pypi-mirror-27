### notebook-wide-screen

This module enables very wide screen notebook display.  
It will work **only** for <span style="color: red">**trusted**</span> notebooks.  

#### 1 - Settings

+ `width` (default='95%') represents the width of the notebook and header containers in css parlance.  
+ `verbose` (default=False) gives you more info about the mechanism.  

#### 2 - Security

Because a notebook is designed to allow the user to write arbitrary code, it has full access to many resources.  

The typical risks are the following:
+ A notebook has access to your file system and can therefore potentially read/modify/delete any of your files or send them to an attacker, or write a new file (virus).  
+ A notebook may contain javascript in output cells which can read you cookies and local storage and potentially send them to an attacker.  

See the [Security in notebook documents](https://jupyter-notebook.readthedocs.io/en/stable/security.html#security-in-notebook-documents) section of the official [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/stable/index.html) for more info.  

Therefore you **should review** and **must trust** the notebook before you can use **notebook-wide-screen**.
