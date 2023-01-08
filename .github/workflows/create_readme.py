print('-Creating README')

import csv, collections

# read csv
csv_data = {}
try:
    with open('./Parts/bom.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            csv_data[row['cad_name']] = row
except:
    print('No bom.csv found!')

categories = {}
for part in csv_data:
    if csv_data[part]['category'] not in categories and csv_data[part]['category'] != '':
        categories[csv_data[part]['category']] = csv_data[part]['type']
categories = collections.OrderedDict(
    sorted(categories.items()))  # sort cats

#create table strings
printed_table = ''
printed_header = '| Part Name | STL | STEP | Amount | Print Time | Weight (g)|\n| --- | --- | --- | --- | --- | --- |\n'
mechanical_table = ''
mechanical_header = '| Part Name | Link | Alt Link | Amount | Price | Note |\n| --- | --- | --- | --- | --- | --- |\n'

for category in categories:
    if categories[category] == 'printed':
        printed_table+='\n### '+str(category).upper()+':\n' + printed_header
    if categories[category] == 'mechanical':
        mechanical_table+='\n### '+str(category).upper()+':\n' + mechanical_header
    
    #parts with category
    for row in csv_data:
        entry = csv_data[row]
        if entry['category'] != category: continue  #skip if no category
        if entry['type'] == 'printed':
            printed_table += '| '+str(entry['cad_name'])+ ' | [STL](./Printed%20Parts/STL/'+str(entry['cad_name'])+'.stl) | [STEP](./Printed%20Parts/STEP/'+str(entry['cad_name'])+'.step) | '+str(entry['amount'])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[0])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[1].split(']')[0])+' |\n'
        elif entry['type'] == 'mechanical':
            mechanical_table += '| ['+str(entry['cad_name'])+'](./Mechanical%20Parts/'+str(entry['cad_name'])+'.stl) | ['+('link' if str(entry['link']) != '---' else ':small_red_triangle:')+']('+str(entry['link'])+') | ['+('link' if str(entry['alt_link']) != '---' else ':small_red_triangle:')+']('+str(entry['alt_link'])+') | '+str(entry['amount'])+' | '+str(entry['price'])+' | '+str(entry['note'])+' |\n'

#set header for parts without category
if 'printed' in categories.values():
    printed_table += '\n'+ printed_header
else:
    printed_table = '\n' + printed_header
if 'mechanical' in categories.values():
    mechanical_table += '\n'+ mechanical_header
else:
    mechanical_table = '\n' + mechanical_table

for row in csv_data:
    entry = csv_data[row]
    if entry['category'] != '': continue  #skip if has category
    if entry['type'] == 'printed':
        printed_table += '| '+str(entry['cad_name'])+ ' | [STL](./Printed%20Parts/STL/'+str(entry['cad_name'])+'.stl) | [STEP](./Printed%20Parts/STEP/'+str(entry['cad_name'])+'.step) | '+str(entry['amount'])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[0])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[1].split(']')[0])+' |\n'
    elif entry['type'] == 'mechanical':
        mechanical_table += '| ['+str(entry['cad_name'])+'](./Mechanical%20Parts/'+str(entry['cad_name'])+'.stl) | ['+('link' if str(entry['link']) != '---' else ':small_red_triangle:')+']('+str(entry['link'])+') | ['+('link' if str(entry['alt_link']) != '---' else ':small_red_triangle:')+']('+str(entry['alt_link'])+') | '+str(entry['amount'])+' | '+str(entry['price'])+' | '+str(entry['note'])+' |\n'


#README update
lines = None
with open('./Parts/README.md', "r") as f:
    lines = f.readlines()

printed_line, mechanical_line = 0, 0
for i, line in enumerate(lines):
    if '## Printed Parts' in line:
        printed_line = i
    if '## Mechanical Parts' in line:
        mechanical_line = i +1

lines_iter = iter(lines)
with open('./Parts/README.md', "w") as f:
    
    line = next(lines_iter)

    #Fing begining of printed table
    while '## Printed Parts' not in line:
        f.write(line)
        line = next(lines_iter)
    f.write(line)

    #write printed table
    for x in printed_table:
        f.write(x)
    
    #find end of table
    while line[:2] != '``':
        line = next(lines_iter)
    f.write('\n')

    #Fing begining of mechanical table
    while '## Mechanical Parts' not in line:
        f.write(line)
        line = next(lines_iter)
    f.write(line)

    #write mechanical table
    for x in mechanical_table:
        f.write(x)
    
    #find end of table
    while line[:2] != '``':
        line = next(lines_iter)
    f.write('\n')

    while line:
        f.write(line)
        line = next(lines_iter,False)