#!/usr/bin/python
import os
import re
class TesIntf(object):
    def ComputeShandong(self, img_path):
        tmp_img = img_path + "_tmp"
        pipe_cmd = "prep_shandong " + img_path + " " + tmp_img + " ; tesseract " + tmp_img + " stdout -l shandong -psm 7 | sed 's/ //'| sed 's/xx/*/' | sed 's/++/+/' | sed 's/x/*/' | sed 's/--/-/' "
        #print pipe_cmd
        pf = os.popen(pipe_cmd)
        data = pf.readline().strip() 
        #print data
        pattern = re.compile(r'\d[+-/*]\d')
        if len(data)>=3 and pattern.match(data[0:3]):
            res = `eval(data[0:3])`
        else:
            res = None
        pf.close()
        # print command and result temporary
        print 'the recognition command and result:', pipe_cmd, res
        return res

    def ComputeLiaoning1(self, img_path):
        pipe_cmd = "tesseract " + img_path + " stdout -l shandong -psm 7 | sed 's/ //'| sed 's/xx/*/' | sed 's/++/+/' | sed 's/x/*/' | sed 's/--/-/' "
        pf = os.popen(pipe_cmd)
        data = pf.readline().strip() 
        #print data
        pattern = re.compile(r'\d[+-/*]\d')
        if len(data)>=3 and pattern.match(data[0:3]):
            res = `eval(data[0:3])`
        else:
            res = None
        pf.close()
        return res

    def ComputeLiaoning2(self, img_path):
        pipe_cmd = "tesseract " + img_path + " stdout -l chi_sim -psm 7 "
        pf = os.popen(pipe_cmd)
        res = pf.readline().strip() 
        pf.close()
        return res

    def ComputeLiaoning3(self, img_path):
        pipe_cmd = "tesseract " + img_path + " stdout -l shandong -psm 7 "
        pf = os.popen(pipe_cmd)
        res = pf.readline().strip() 
        pf.close()
        return res
    
