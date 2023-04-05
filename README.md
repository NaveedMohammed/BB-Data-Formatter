# BB-Data-Formatter
BB Raw log pre-processor

Project is built using python 3.10.

Cloning the project:

```sh
git clone https://github.com/NaveedMohammed/BB-Data-Formatter.git
cd BB-Data-Formatter
```
Install and run:

```sh
pip install -r requirements.txt
python data_formatter.py  
```
The python program takes Betty's Brain raw csv files as input. The files include the **raw Store csv file**, 
**raw prefs_offerings csv file** and **sessions csv file**.
The resultant output is a set of csv's required to run Bettys Brain analysis. The list of csv's generated are 
**prefs csv file**, **offerings csv file**, **subjects csv file**, **store csv file** and **sessions csv file.**

The program uses a GUI library 'tkinter' that allows for easier user access to the process. The flow of the program is 
straight forward.
1. Import raw store csv file.
2. Import raw refs_offerings csv file.
3. Import sessions csv file.
4. Select output directory to store the files.
5. Process the files. 
6. Open the output directory for further processing.

