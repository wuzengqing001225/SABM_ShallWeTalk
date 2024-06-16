import csv
import os
from UtilityModule.utilsDataProcess import formatListtoStr, formatDicttoStr
    
def fileLogOutput(filename, data, N):
    headers = ['player_' + str(i + 1) for i in range(N)]

    if data["discussion"] == []:
        rowTitles = [f'Round {data["round"]} reasoning', f'Round {data["round"]} choice']
    else:
        rowTitles = [f'Round {data["round"]} reasoning', f'Round {data["round"]} choice', f'Round {data["round"]} discussion']

    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        if not file_exists:
            csvwriter.writerow(['Round'] + headers)
        
        csvwriter.writerow([rowTitles[0]] + data["reasoning"])
        csvwriter.writerow([rowTitles[1]] + data["choice"])
        if data["discussion"] != []: csvwriter.writerow([rowTitles[2]] + data["discussion"])

def fileOverviewOutput(filename, data, N):
    headers = ['Avg', '2/3 Avg', 'Winner(s)', 'Variance'] + ['player_' + str(i + 1) for i in range(N)]

    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        if not file_exists:
            csvwriter.writerow(['Round'] + headers)

        csvwriter.writerow([f'Round {data["round"]}'] + data["result"] + [data["variance"]] + data["choice"])

def fileMessageOutput(filename, dictMessage):
    dataList = []

    for key, value in dictMessage.items():
        dataList.append({
            "ID": key,
            "message": value.message,
            "type": formatDicttoStr(value.type),
            "indexMessageOrigin": formatListtoStr(value.indexMessageOrigin),
            "indexAgentDestination": value.indexAgentDestination,
            "remark": value.remark,
            "timestampStart": value.display('timestamp')
        })
        
    def parseTimestamp(timestamp):
        parts = timestamp.split('-')
        return (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    dataList = sorted(dataList, key=lambda x: parseTimestamp(x['timestampStart']))

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["ID", "message", "indexMessageOrigin", "type", "indexAgentDestination", "remark", "timestampStart"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in dataList:
            writer.writerow(row)
