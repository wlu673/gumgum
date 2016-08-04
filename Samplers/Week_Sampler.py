import os
import sys
import time
import multiprocessing
import numpy as np
from scipy.sparse import csr_matrix
from scipy import vstack
import Sparse_Matrix_IO as smio


num = 100000


def get_addr(month, day):
    root = "/mnt/rips2/2016"
    return os.path.join(root, str(month).rjust(2, "0"), str(day).rjust(2, "0"), "day_samp_new.npy")


def crawl(date):
    month = date[0]
    day = date[1]
    addr_list = []
    total_line = 0
    for i in range(7):
        addr_in = get_addr(month, day+i)
        addr_list.append(addr_in)
        with open(addr_in, "r") as file_in:
            data = smio.load_sparse_csr(file_in)
            total_line += np.size(data, 0)

    line_indices = sorted(np.random.choice(total_line, num, replace=False))

    setoff = 0
    index = 0
    res = []
    for addr_in in addr_list:
        print "Sampling from {}".format(addr_in)
        sys.stdout.flush()
        with open(addr_in, "r") as file_in:
            X = smio.load_sparse_csr(file_in)
        while (index < num) and (line_indices[index]-setoff < len(X)):
            res.append(csr_matrix(X[line_indices[index]-setoff]))
            index += 1
        if index >= num:
            break
        setoff += len(X)

    X = vstack(res)
    with open("/home/ubuntu/random_samples/week_samp_"+str(month).rjust(2, "0")+str(day).rjust(2, "0")+".npy", "w") as file_out:
        smio.save_sparse_csr(file_out, X)


if __name__ == '__main__':
    cpus = multiprocessing.cpu_count()
    p = multiprocessing.Pool(cpus)
    start = time.time()
    for result in p.imap(crawl, [(6, i) for i in [4]]):
        pass

    print "Completed in {} seconds\n".format(round(time.time()-start, 2))
