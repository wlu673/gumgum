import json
import csv
import operator


result_list = []


def get_dates():
    may = [(5, i, j) for i in range(1, 8) for j in range(24)]
    # may = []
    # june = [(6, i, j) for i in range(4, 26) for j in range(24)]
    june = []
    return may+june


def run(addr_in):
    dict_bkc = {}
    with open(addr_in, "r") as file_in:
        for line in file_in:
            entry = json.loads(line)
            try:
                bkc_str = entry["auction"]["user"]["bkc"]
                bkc_list = bkc_str.split(",")
            except:
                bkc_list =[]
            for bkc in bkc_list:
                if dict_bkc.has_key(bkc):
                    dict_bkc[bkc] += 1
                else:
                    dict_bkc.update({bkc:1})
    return dict_bkc


def add_result(result):
    result_list.append(result)


def get_result():
    dict_bkc = {}
    for result in result_list:
        for key in result:
            if dict_bkc.has_key(key):
                dict_bkc[key] += result[key]
            else:
                dict_bkc.update({key:result[key]})

    print "{} unique bkc ids recorded".format(len(dict_bkc))
    sorted_domain = sorted(dict_bkc.items(), key=operator.itemgetter(1), reverse=True)
    with open("/home/ubuntu/Weiyi/bkcids.ods", "w") as file_out:
        wr = csv.writer(file_out)
        for item in sorted_domain:
            wr.writerow(item)