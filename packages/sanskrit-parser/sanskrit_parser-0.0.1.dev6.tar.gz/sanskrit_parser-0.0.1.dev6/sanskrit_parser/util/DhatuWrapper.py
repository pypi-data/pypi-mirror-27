#!/usr/bin/env python
"""
Wrapper around  kRShNamAchArya dhAtupATha to extract simple dhAtu attributes
@author: Karthikeyan Madathil (@kmadathil)
"""
from __future__ import print_function
from  sanskrit_parser.base.sanskrit_base import SanskritObject,SCHEMES,SLP1
import logging
import time, datetime
import csv
import os
import requests
from tinydb import TinyDB, Query

class DhatuWrapper(object):
    """
    Class to interface with the kRShNamAchArya dhAtupATha
    https://github.com/sanskrit-coders/stardict-sanskrit/tree/master/sa-vyAkaraNa/dhAtu-pATha-kRShNamAchArya
    """
    git_url='https://raw.githubusercontent.com/sanskrit-coders/stardict-sanskrit/master/sa-vyAkaraNa/dhAtu-pATha-kRShNamAchArya/mUlam/Dhatu%20Patha%20%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3%E0%A4%BE%E0%A4%9A%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%E0%A4%B8%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%83%E0%A4%A4%E0%A5%87%E0%A4%83%20-%20Sheet1.tsv'
    base_dir = os.path.expanduser("~/.sanskrit_parser/data")
    local_filename="dhAtu-pATha-kRShNamAchArya.tsv"
    db_file = "dhAtu-pATha-kRShNamAchArya.json"
    q = Query()
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._get_file()
        self.db = TinyDB(os.path.join(self.base_dir, self.db_file))
        # Check if db is empty
        if len(self.db.all())==0:
            self._generate_db()

    def _get_file(self):
        """ Download file if not present in cache """
        if not os.path.exists(self.base_dir):
            self.logger.debug("Data cache not found. Creating.")
            os.makedirs(self.base_dir)
        filename = self.local_filename
        if not os.path.exists(os.path.join(self.base_dir, filename)):
            self.logger.debug("%s not found. Downloading it", filename)
            r = requests.get(self.git_url, stream=True)
            with open(os.path.join(self.base_dir, filename), "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
        
    def _generate_db(self):
        """ Create db from tsv file """
        self.logger.debug("Parsing files into dict for faster lookup")
        with open(os.path.join(self.base_dir, self.local_filename),"r") as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            # FIXME - Rewrite from here
            for irx,row in enumerate(reader):
                # Get Keys
                if irx==0:
                    # Only the first 9 columns are useful
                    headers=[SanskritObject(x).transcoded(SLP1) for x in row[0:8]] 
                    self.logger.debug("Found dhatu tsv headers: {}".format(str(headers)))
                else:
                    j = {}
                    for i,x in enumerate(row):
                        if i <len(headers):
                            t=SanskritObject(x).transcoded(SLP1)
                            j[headers[i]]=t
                    self.db.insert(j)
        self.logger.debug("Saved dhatus database")

 
    def _get_dhatus(self,d):
        " Get all tags for a dhatu d "
        if d is None:
            return None
        else:
            return self.db.search(self.q.DAtuH==d)
        
    def is_sakarmaka(self,d):
        " Is d sakarmaka? "
        # Tags
        tl=self._get_dhatus(d)
        if len(tl)!=0:
            r=reduce(lambda x,y: x or y,['sakarmaka' in t['karmakatvaM'] for t in tl])
            return r
        else:
            self.logger.debug("Couldn't find dhatu {} in database".format(d))
            return False
        
if __name__ == "__main__":
    from argparse import ArgumentParser
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = ArgumentParser(description='Dhatu Wrapper')
        # String to encode
        parser.add_argument('dhatu',nargs="?",type=str,default="kf")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding',type=str,default=None)
        parser.add_argument('--tags',type=str,
                            choices=["all",u'DAtuH', u'mUlaDAtuH', \
                                     u'DAtvarTaH', u'gaRaH', u'karmakatvaM',
                                     u'iwtvaM', u'padam-upagrahaH', u'rUpam'],
                            default=u'karmakatvaM')
        parser.add_argument('--debug',action='store_true')
        return parser.parse_args()

    def main():
        args=getArgs()
        print("Input Dhatu:", args.dhatu)
        if args.debug:
            logging.basicConfig(filename='DhatuWrapper.log', filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='DhatuWrapper.log', filemode='w', level=logging.INFO)
        logger=logging.getLogger(__name__)
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]
        i=SanskritObject(args.dhatu,encoding=ie)
        it=i.transcoded(SLP1)
        print("Input String in SLP1:",it)
        logger.info("Input String in SLP1: {}".format(it))
        w=DhatuWrapper(logger=logger)
        if args.tags == "all":
            res=w._get_dhatus(it)
        else:
            res=map(lambda x: x[args.tags],w._get_dhatus(it))
        print(res)
        print("Is {} sakarmaka?: {}".format(it,w.is_sakarmaka(it)))
        logger.info("Reported {}".format(res))
    main()
