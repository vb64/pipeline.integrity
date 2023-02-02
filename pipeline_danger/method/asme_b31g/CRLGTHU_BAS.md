# CRLGTHU.BAS

A computer program which provides the same type of infonnation and printout as CRLGTH.BAS,
except that the program does not need to be modified with each usage, and the user is asked for pipe diameter,
the minimum pit depth to begin with, and up to 10 wall thicknesses.
The program prompts the user for this information, in increasing order of thicknesses.
(A thickness that is out of order will prompt a request to re-enter all of the thicknesses.)

THIS PROGRAM IS A UNIVERSAL PROGRAM. AND ALLOWS ENTRY OF ANY DIAMETER OF PIPE AND UP TO 10 WALL THICKNESSES TO EXAMINE FOR ALLOWABLE CORROSION LENGTHS.

PROGRAM CRLGTHU.BAS BY R.L.SEIFERT TO LIST ALLOWED LENGTHS OF CORROSION FOR GIVEN DEPTHS OF CORROSION FOR SPECIFIED DIAMETER AND WALL THICKNESSES.
FOR IBM-PC AND EPSON FX SERIES PRINTERS OR COMPATIBLE EQUIPMENT. 

Revision of 2/17/89 by Richard L. Seifert, P.L Consultant for Pipeline Corrosion Control and Use and Application of Personal Computers
15602 Valley Bend Drive Houston, Texas 77068

This program prints a list of allowed lengths of corroded areas on underground pressure piping for given pit depths.
It is a generalized, conservative listing of allowed lengths, and if any corroded area is 'condemned' by this listin,
the corroded area should be examined further using Seifert's program CRVL.BAS.
CRVL.BAS will examine the corroded pipe using precise input parameters, and may allow the use of the pipe,
when this program, CRLGTHU.BAS, condemns it.

```BASIC
40 CLEAR 5000:DIM T(l7):WIDTH "LPT1:",255
50 LPRINT CHR$(27);"@";:COLOR 7,1,0:CLS

240 LPRINT CHR$(27);"@";
: CLS
: PRINT: INPUT "AOJUST PRINTER PAPER TO TOP OF FORM, TURN PRINTER ON, THEN PRESS <ENTER>";EN
```
