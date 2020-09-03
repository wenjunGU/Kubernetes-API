#!//usr/bin/env python
# --*-- coding:utf-8 --*--

from utils.swaps import swap
from copy import deepcopy

class main(object):

    def select_sort(self,lis_):
       lis = deepcopy(lis_)
       length = len(lis)
       for i in xrange(0, length):
           min = i
           for j in xrange(i+1, length):
               if lis[j] < lis[min]:
                   min = j
           if min != i:
               lis[i], lis[min] = swap(lis[i], lis[min])
       return lis
 
if __name__ == "__main__":
     obj = main()
     lis = [2,34,21,8,9,56,2,30]
     print obj.select_sort(lis)
