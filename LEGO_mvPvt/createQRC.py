# -*- coding:utf-8 -*-
import sys
import os
  
PREFIX='/myTool/'
  
def searchFile(root, result):
    for file in os.listdir(root):
        fullpath = os.path.join(root, file)
          
        if os.path.isdir(fullpath):
            searchFile(fullpath, result)
          
        if file.split('.')[-1] == 'png':
            result.append(fullpath)
    return result
      
def main():
    root = sys.argv[1]
    files = searchFile(root, [])
      
    qrc = os.path.join(root, 'resource.qrc')
    fw = open(qrc, 'w')
    fw.write('<RCC>\n')
    fw.write('  <qresource prefix="%s">\n' % PREFIX)
    for file in files: 
        file = file.replace(root, './')
        fw.write('  <file>%s</file>\n' % file)
    fw.write('  </qresource>\n')        
    fw.write('</RCC>\n')
      
  
if __name__ == '__main__':
    main()