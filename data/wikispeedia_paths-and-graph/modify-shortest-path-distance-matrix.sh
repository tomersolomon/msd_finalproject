#!/bin/bash

# ignore lines that start with #, replace all instaces of _ with 0, 
grep -E "^[^#]" shortest-path-distance-matrix.txt |

# replace all instance of _ with 0
tr '_' '0' |

# add spaces between all numbers for each row in the matrix in order to be able 
# to be read by numpy and pandas 
sed -e 's/\(.\)/\1 /g' > mod-shortest-path-distance-matrix.txt 


