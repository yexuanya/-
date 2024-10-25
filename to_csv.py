import csv

def to_csv(header,two_list):
    with open('output_with_header.csv', mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)

        # 写入表头
        writer.writerow(header)

        # 写入二维列表数据
        writer.writerows(two_list)
