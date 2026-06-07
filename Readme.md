# CLaunch Help

This repository contains the source files for the CLaunch Help documentation.

The same HTML files are used for both the offline CHM help file and the online documentation published via GitHub Pages.

## Online Documentation

### English

https://pyonky.github.io/CLaunch-Help/en/

### Japanese

https://pyonky.github.io/CLaunch-Help/ja/

## Repository Structure

```text
en/
    *.htm          HTML help pages
    *.hhc          Table of contents for HTML Help Workshop
    *.hhk          Index for HTML Help Workshop
    *.hhp          Project file for HTML Help Workshop
    images/        Images used by the documentation
    help.css       Stylesheet for help pages
    online.css     Stylesheet for online documentation
    index.html     Online help frame
    toc.html       Generated table of contents

ja/
    ...

tools/
    hhc_to_toc.py
```

## Generating toc.html

The online table of contents is generated from the corresponding `.hhc` file.

Example:

```bash
python tools/hhc_to_toc.py en/CLaunch.hhc en/toc.html --encoding cp1252 --title "CLaunch Help" --lang en

python tools/hhc_to_toc.py ja/CLaunch.hhc ja/toc.html --encoding cp932 --title "CLaunch Help" --lang ja
```

## Character Encoding

HTML Help Workshop does not reliably support UTF-8 encoded project files.

The following files should be saved using the appropriate ANSI code page for each language:

```text
*.hhc
*.hhk
*.hhp
```

The HTML help pages (`*.htm`) may be stored in UTF-8.

## Contributions

Corrections, improvements, and translations are welcome.

Please submit a Pull Request or open an Issue if you find any problems in the documentation.

<br/>

------------------------------------------------------------

Author : Pyonkichi  
Website : https://ss1.xrea.com/pyonkichi.g1.xrea.com/en/  
&emsp; &emsp; &emsp; &nbsp; http://pyonkichi.g1.xrea.com/  
E-mail : pyonky_claunch@yahoo.co.jp

------------------------------------------------------------
