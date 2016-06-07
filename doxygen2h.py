import argparse
import fnmatch
import os

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Generates header files from doxygen directory.')
parser.add_argument('-i', dest='inputDir', required = True,
                    help='where you should find files like *_8hpp_source.html')
parser.add_argument('-o', dest='outputDir', required = True,
                    help='place for the output .h files')
args = parser.parse_args()

headerHtmls = []
for root, dirnames, filenames in os.walk(args.inputDir):
        for filename in fnmatch.filter(filenames, '*_8hpp_source.html'):
            headerHtmls.append(os.path.join(root, filename))

for headerHtml in headerHtmls:
    f = open(headerHtml, 'r')
    soup = BeautifulSoup(f, 'html.parser')

    fileNameSet = False
    headerFile = None
    for div in soup.find_all('div'):
        if 'class' not in div.attrs:
            continue

        if not fileNameSet and u'title' in div['class']:
            title = div.text.encode('ascii', 'ignore').strip()
            headerFile = open(os.path.join(args.outputDir, title), 'w')
            fileNameSet = True

        if fileNameSet and u'line' in div['class']:
            srcLine = div.text.encode('ascii', 'ignore').strip()
            headerFile.write(srcLine.lstrip('0123456789') + '\n')

    headerFile.close()
