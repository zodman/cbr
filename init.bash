rm -rf *.db
cp origin.csv out.csv
shuf -n 3 out.csv > test.csv
