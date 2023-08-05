numtxt
======
A pure Python module that gives both full and approximate names for numbers

Contains functions that give the cardinal name (one, two, three, ...), the ordinal name (first, second, third, ...) as well as approximations (23.3458e45 -> '23.346 quattuordecillion'). Has four different naming methods for powers and three different suffix styles.

Suffix Styles
-------------
- **short** 
  - Assigns 'illion' to names. This is the default style.

  - 10^6 = million, 10^9 = billion, 10^12 = trillion, ...
- **long**
  - Assigns 'illion' or 'illiard' to names depending on power.

  - 10^6 = million, 10^9 = milliard, 10^12 = billion, ...
- **british**
  - Assigns 'illion' and adds 'thousand' in front of names depending on power.

  - 10^6 = million, 10^9 = thousand million, 10^12 = billion, ...


Naming Methods
--------------
- **conway-wechsler**
  - This system extends the normal Latin naming method indefinitely and follows Latin syntax closely. Can use long, short or British suffix styles (examples below are short style). This is the default method.

  - 10^6 = 1 million
  - 10^12 = 1 trillion
  - 10^51 = 1 sedecillion
  - 10^342 =  1 tredecicentillion
- **noll**
  - This system extends the normal Latin naming method indefinitely. Can use long, short or British suffix styles (examples below are short style).

  - 10^6 = 1 million
  - 10^12 = 1 trillion
  - 10^51 = 1 sexdecillion
  - 10^342 = 1 centredecillion
- **rowlett**
  - This system uses Greek prefixes for names. Introduced to prevent confusion the suffix styles can cause and therefore does not use any such styles. Currently valid up to 10^2999.

  - 10^6 = 1 million
  - 10^12 = 1 gillion
  - 10^51 = 1 heptadekillion
  - 10^342 = 1 hecatodekatetrillion
- **knuth**
  - Radically different naming method introduced to prevent confusion the suffix styles can cause and thus does not use any styles. Inherits conway-wechsler system to extend naming scheme indefinitely (original paper stopped at 10^4194304).

  - 10^6 = 100 myriad
  - 10^12 = 10 myllion
  - 10^51 = 1000 byllion tryllion
  - 10^342 = 100 myriad byllion quadryllion sextyllion
