import re
import csv

data = """8/12/2026, 3:43:08 PM TRAVEL BOTTLE 350ML 1 Cash Owner - Ksh. 550
8/12/2026, 2:36:44 PM Sugar 5 Cash Owner - Ksh. 800
8/12/2026, 2:36:44 PM Pika 10L 1 Cash Owner - Ksh. 2,650
8/12/2026, 2:33:17 PM Shujaa 1Kg 1 Cash Owner - Ksh. 85
8/12/2026, 2:33:17 PM Toilet brush 1 Cash Owner - Ksh. 150
8/12/2026, 2:33:17 PM Afya Mangoe 500ml 2 Cash Owner - Ksh. 160
8/12/2026, 2:33:17 PM Kensalt 500g 1 Cash Owner - Ksh. 30
8/12/2026, 2:33:17 PM Omo kupima 0.34 Cash Owner - Ksh. 51
8/12/2026, 2:33:17 PM Tissue poa 1 Cash Owner - Ksh. 20
8/12/2026, 2:33:17 PM Yellow beans 1 Cash Owner - Ksh. 150
8/12/2026, 2:33:17 PM FARAGELLO 1 Cash Owner - Ksh. 40
8/12/2026, 2:33:17 PM Mount Kenya 200ml 1 Cash Owner - Ksh. 30
8/12/2026, 2:33:17 PM Eggs 2 Cash Owner - Ksh. 34
8/11/2026, 8:48:51 PM Kamande 6 Cash Owner Ksh. 500 Ksh. 1,000
8/11/2026, 8:48:51 PM Yellow beans 0 Cash Owner - Ksh. 0
8/11/2026, 8:48:51 PM Sugar 0.25 Cash Owner - Ksh. 40
8/11/2026, 8:48:51 PM Omo kupima 10 Cash Owner Ksh. 200 Ksh. 1,300
8/11/2026, 8:37:01 PM DAWN JUMBO 100M 30 Cash Owner - Ksh. 3,600
8/11/2026, 8:37:01 PM Kitchen towel @150 2 Cash Owner Ksh. 100 Ksh. 200
8/11/2026, 8:37:01 PM Kitchen towel @80 2 Cash Owner - Ksh. 160
8/11/2026, 8:37:01 PM Geisha soap 200g 25 Cash Owner - Ksh. 3,000
8/11/2026, 8:37:01 PM Bathing towel 4 Cash Owner Ksh. 1,400 Ksh. 4,600
8/11/2026, 8:37:01 PM Match box 4 Cash Owner - Ksh. 20
8/11/2026, 8:37:01 PM Mwiko heavy 1 Cash Owner - Ksh. 150
8/11/2026, 8:37:01 PM Sumo candle 2 Cash Owner - Ksh. 30
8/11/2026, 8:37:01 PM Scour power scrubber 1 Cash Owner - Ksh. 50
8/11/2026, 8:37:01 PM YE-208-1 2 Cash Owner - Ksh. 140
8/11/2026, 8:37:01 PM A.E.S.L, DIYA,P-2226, PLATES 1 Cash Owner - Ksh. 120
8/11/2026, 8:37:01 PM Kensalt 200g 1 Cash Owner - Ksh. 15
8/11/2026, 8:23:59 PM Mella mine DIYA 3001 2 Cash Owner - Ksh. 180
8/11/2026, 8:23:59 PM White metallic mug small 1 Cash Owner - Ksh. 90
8/11/2026, 8:23:59 PM Blue band 100g 1 Cash Owner - Ksh. 80
8/11/2026, 8:23:59 PM Yellow beans 2 Cash Owner - Ksh. 300
8/11/2026, 8:23:59 PM Predator 2 Cash Owner - Ksh. 140
8/11/2026, 8:23:59 PM Afya Mangoe 500ml 2 Cash Owner - Ksh. 160
8/11/2026, 8:23:59 PM Jiko No.2 1 Cash Owner - Ksh. 300
8/11/2026, 8:23:59 PM Kensalt 200g 2 Cash Owner - Ksh. 30
8/11/2026, 8:23:59 PM AJAB wheat flour 1kg 7 Cash Owner - Ksh. 700
8/11/2026, 8:23:59 PM Gomba 10 Cash Owner - Ksh. 20
8/11/2026, 8:23:59 PM Big G 10 Cash Owner - Ksh. 50
8/11/2026, 8:23:59 PM FARAGELLO 3 Cash Owner - Ksh. 120
8/11/2026, 8:23:59 PM Tissue poa 2 Cash Owner - Ksh. 40
8/11/2026, 8:23:59 PM Eggs 2 Cash Owner - Ksh. 34
8/11/2026, 8:23:59 PM Ariel,sunlight,doffy 1 Cash Owner - Ksh. 10
8/11/2026, 8:23:59 PM Downy 5 Cash Owner - Ksh. 100
8/11/2026, 8:23:59 PM Omo kupima 0.33 Cash Owner - Ksh. 49.5
8/11/2026, 8:23:59 PM Sugar 4 Cash Owner - Ksh. 640
8/11/2026, 8:23:59 PM Mount Kenya 500ml 28 Cash Owner - Ksh. 1,680
8/9/2026, 1:10:44 PM crow Brush @250 1 Cash Owner - Ksh. 250
8/9/2026, 1:08:51 PM A.E.S.L, DIYA,P-2226, PLATES 1 Cash Owner - Ksh. 120"""

pattern = re.compile(r'^(\d+/\d+/\d+), \d+:\d+:\d+ [AP]M (.*?) ([\d.]+) Cash (\w+) (?:-|Ksh\. [\d.,]+) Ksh\. ([\d.,]+)$')

rows = []
for line in data.strip().split('\n'):
    match = pattern.match(line)
    if match:
        date, product, qty, cashier, total = match.groups()
        total = total.replace(',', '')
        rows.append([date, product, qty, total, cashier])
    else:
        print(f"Failed to match: {line}")

with open('sells.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Product', 'Quantity', 'Total', 'Cashier'])
    writer.writerows(rows)
