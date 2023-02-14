# nuclei-scan-sort

Simple Python script to sort nuclei scans by severity and URL

pip3 install -r requirements.txt

Simply save nuclei scan with -o option:

nuclei -l targets.txt -o scan.txt

Then proceed it with script:

python3 nuclei_sort.py -i scan.txt
