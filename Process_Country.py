import json
import csv
import operator


result_list = []


def get_dates():
    may = [(5, i, j) for i in range(1, 8) for j in range(24)]
    # may = []
    june = [(6, i, j) for i in range(4, 26) for j in range(24)]
    # june = []
    return may+june


def run(addr_in):
    dict_country = {}
    with open(addr_in, "r") as file_in:
        for line in file_in:
            entry = json.loads(line)
            if entry["em"].has_key("cc"):
                country = entry["em"]["cc"]
            else:
                country = "NONE"
            if dict_country.has_key(country):
                dict_country[country] += 1
            else:
                dict_country.update({country:1})

    return dict_country


def add_result(result):
    result_list.append(result)


def get_result():
    dict_country = {}
    for result in result_list:
        for key in result:
            if dict_country.has_key(key):
                dict_country[key] += result[key]
            else:
                dict_country.update({key:result[key]})

    print "{} unique countries recorded".format(len(dict_country))
    sorted_domain = sorted(dict_country.items(), key=operator.itemgetter(1), reverse=True)
    with open("/home/ubuntu/Weiyi/countries.ods", "w") as file_out:
        wr = csv.writer(file_out)
        for item in sorted_domain:
            wr.writerow(item)