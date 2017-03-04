'''
Created on 2016年9月19日

@author: scott
'''
import requests
from bs4 import BeautifulSoup
import json

class ishadowsocks(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._ssURL = "http://www.ishadowsocks.org/"
        self.auths = []
        self._lastModified=None
        
        
    def update(self):
        if self._lastModified is None:
            page = requests.get(self._ssURL)
        else:
            page = requests.get(self._ssURL,headers={'If-Modified-Since':self._lastModified})
            
        if page.status_code == 304:
            return False
        self._lastModified = page.headers['Last-Modified']
        soup = BeautifulSoup(page.content,"html.parser")     
        authALL = soup.findAll(class_="col-sm-4 text-center" )
        auths=[]
        for server in authALL[:3]:
            lis = []
            for info in server.children:
                if info != "\n":
                        lis.append(info.string.split(":")[1])
                        if info.string.split(":")[1] == "aes-256-cfb":
                            break
            print(lis)
            auth = {
                    'server':lis[0],
                    'server_port':int(lis[1]),
                    'password':lis[2],
                    'method':lis[3]
                    }
            auths.append(auth)
        self.auths=auths
        print( auths)
        return True
    
    def outputProperties(self,fileName):
        idx=0;
        for auth in self.auths:
            json.dump(auth, open(fileName+str(idx)+'.json','w'))
            idx+=1
            
            
if __name__ == '__main__':
    iss = ishadowsocks()
    iss.update()
    iss.outputProperties('config')