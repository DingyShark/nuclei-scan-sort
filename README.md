# nuclei-scan-sort

![sorted](https://user-images.githubusercontent.com/58632878/218885613-2fb46456-ef8e-41c9-92b8-23a150436319.jpg)
Simple Python script to sort nuclei scans by severity and URL

1. Install dependencies:
pip3 install -r requirements.txt

2. Simply save nuclei scan with -o option:

nuclei -l targets.txt -o scan.txt

3. Proceed it with script:

python3 nuclei_sort.py -i scan.txt

