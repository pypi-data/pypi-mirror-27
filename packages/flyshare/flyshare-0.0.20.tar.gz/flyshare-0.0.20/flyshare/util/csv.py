import csv

def save_csv(data, name, column=None, location = None):
    """
    :param data: list
    :param name: filename
    :param column: column name list
    :param location: optional location
    :return:
    """
    assert isinstance(data, list)
    if location is None:
        path = './' + str(name) + '.csv'
    else:
        path = location + str(name) + '.csv'
    with open(path, 'w', newline='') as f:
        csvwriter = csv.writer(f)
        if column is None:
            pass
        else:
            csvwriter.writerow(column)

        for item in data:
            if isinstance(item, list):
                csvwriter.writerow(item)
            else:
                csvwriter.writerow([item])