#!/usr/bin/python
from tesintf import TesIntf

def main():
    
    tesf=TesIntf()
    print tesf.ComputeShandong("./shandong_test.jpg")
    print tesf.ComputeLiaoning1("./liaoning1_test.jpg")
    print tesf.ComputeLiaoning2("./liaoning2_test.jpg")
    print tesf.ComputeLiaoning3("./liaoning3_test.jpg")

if __name__ == '__main__':
    main()
