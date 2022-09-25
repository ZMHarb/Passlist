
# Passlist

A study shows that 59% of people use their names and birth dates as passwords. 
This tool generates a wordlist based on given personal information about the person.

Furthermore, we will be releasing new features regarding this tool !!

## Installation

```bash
  git clone https://github.com/ZMHarb/Passlist.git
  cd Passlist
```
    
## Configuration

```bash
    pip install -r requirements.txt
    chmod u+x passlist.py
```


## Usage

To get the tool's options
```bash
    ./passlist.py --help
```

Options

```bash
optional arguments:

  -h, --help            show this help message and exit
  --help-all            More detailed help
                        
  -o OUTPUT, --output OUTPUT
                        Name of The output file
                        

Arguments:
  -p {1,2,3}, --phase {1,2,3}
                        
                        Specify the phase of your desired passlist (1, 2, 3),         
                        1: Simple combinations between the provided categories        
                        2: Substitutions of the letters with special characters        
                        3: Adding characters between words

Categories:
  -f FIRST, --first FIRST
                        First Name
  -l LAST, --last LAST  
                        Last Name
  -d DATE DATE DATE, --date DATE DATE DATE
                        
                        Date of birth

```

## Examples

```bash
    ./passlist.py -p 1 -f john -l smith
    ./passlist.py -p 2 -f john -l smith -d 1 1 1990
    ./passlist.py -p 3 -f john -l smith
```
