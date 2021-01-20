# ghost-archiver
This project focuses tightly on archiving ghost's work.

***

**Prerequisites:**
-
1) Google Chrome
2) python3.7 +

**Installation:**
-
`pip install -r REQUIREMENTS.txt`

`pip install .`

**Useage:**
-
`ghost-archiver` can be used as a traditional Python module:

```
import ghost_archiver as ga

##to archive the True Capitalist Radio show from a known youtube archive of it:

ga.tcr_archive() #you can specify your bitchute user and password, or have it prompt you for it.

##to archive The Ghost Show from the known existing sources:

ga.tgs_archive() #you can specify your bitchute user and password, or be prompted for it

##to archive a DLive Stream:

ga.dlive_archive() #you can specify your bitchute user and password, or be prompted for it.


```

**JUST MAKE IT WORK PLEASE**
-
Sure! If you're running Python,

`from ghost_archiver import archiveupload`

This will immediately provide you with a prompt for your Bitchute credentials, and then run three parallel processes to 
download from the existing archives to your Bitchute account and then start a monitoring thread which will watch DLive for changes.
It's recommended you use `tmux` or `screen` as the idea is to let this run forever watching DLive. Put it on a pi or on a cloud instance and forget about it!

**I am running Windows, don't want to program in any way, but I _do_ want to help archiving**
-
That's still great! I ~~have created~~ am in the process of creating an exe file of `archiveupload` which you can run standalone.