import csv

def txtToCsv(txtFilePath, csvFilePath):
    with open(txtFilePath, 'r', encoding='utf-8') as txtfile, open(csvFilePath, 'w', newline='', encoding='utf-8') as csvfile:        
        lines = txtfile.readlines()
        
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['text'])

        for i, line in enumerate(lines, start=1):
            csvWriter.writerow([line.strip()])