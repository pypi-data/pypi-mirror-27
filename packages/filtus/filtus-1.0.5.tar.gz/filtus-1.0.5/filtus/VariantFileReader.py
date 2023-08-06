import FiltusUtils
import DataContainer
import csv
import re

class VariantFileReader(object):
    def __init__(self):
        pass
        
    def readNonVCF(self, filename, sep, splitAsInfo=None, split_general=None, skiplines=0, prefilter=None, **params): # gtCol, homSymbol:
        with open(filename, "rU") as ifile:
            if isinstance(skiplines, (int, long)):
                for i in range(skiplines): ifile.next()
                headerline = ifile.next()
            elif isinstance(skiplines, basestring):
                line = ifile.next()
                while line.startswith(skiplines):
                    line = ifile.next()
                headerline = line
            headers = csv.reader([headerline], delimiter = sep, skipinitialspace = True, strict=True).next() # must do this before prefilter
            if prefilter is not None: 
                ifile = self._applyPrefilter(ifile, prefilter)
            reader = csv.reader(ifile, delimiter = sep, skipinitialspace = True, strict=True)
            if splitAsInfo or split_general:
                variants = [row for row in reader]
            else:
                variants = [tuple(row) for row in reader]
        
        if splitAsInfo or split_general: # this is allowed also in nonVCF files
            if splitAsInfo:
                infoInd = headers.index(splitAsInfo)
                headers[:], variants[:] = self._splitINFO_slow(headers, variants, infoInd)
                
            for col, sep in split_general:  
                headers[:], variants[:] = self._splitGeneral(headers, variants, col, sep)        
            variants[:] = map(tuple, variants)    
        
        if len(variants)>0 and len(headers) > len(variants[0]):
            raise csv.Error("Format error: The number of headings is greater than the number of entries in the first row.")
        
        ## Nijmegen fix: If a blank line appears, delete it everything after it. (For speed: Only last 200 lines checked)
        blank_tail = [all(len(entry.strip()) == 0 for entry in line) for line in reversed(variants[-200:])]
        if any(blank_tail):
            variants[:] = variants[:-blank_tail.index(True)-1]

        #create instance
        return DataContainer.VariantData(filename=filename, columnNames=headers, variants=variants, **params)

    def readVCFlike(self, filename, sep, chromCol, posCol, geneCol, keep00=0, split_general=[],
                    splitAsInfo="", splitCsq=0, formatCol="FORMAT", splitFormat=1, commentChar="##", prefilter=None):
        preambleLines = []
        with open(filename, "rU") as ifile:
            line = ifile.next()
            while commentChar and line.startswith(commentChar):
                preambleLines.append(line)
                line = ifile.next()
            headers = csv.reader([line], delimiter=sep, skipinitialspace=False, strict=True).next()
            if prefilter is not None: 
                ifile = self._applyPrefilter(ifile, prefilter)
            data = [row for row in csv.reader(ifile, delimiter = sep, skipinitialspace = False, strict=True)] # saving time (?) with skip.. = False
        
        colDescriptions = self._parseColumnDescriptions(preambleLines)
        descriptions = self._prettyDescriptions(colDescriptions)
        
        if len(data) == 0: 
            raise RuntimeError("No variants in file")
        
        if headers[-1] == "Otherinfo": ### Annovar fix: Re-inserting VCF column names.
            headers = self._fixAnnovarOtherinfo(headers, firstvar=data[0])
        if headers[0] == '#CHROM': ### VCF tweak
            headers[0] = 'CHROM'
        
        if splitAsInfo:
            infoInd = headers.index(splitAsInfo)
            try:
                headers[:], data[:] = self._splitINFO_fast(headers, data, infoInd, colDescriptions, splitCsq=splitCsq)
            except KeyError:
                headers[:], data[:] = self._splitINFO_slow(headers, data, infoInd)
            
        split_general_common = [(x,y) for x,y in split_general if x in headers]
        split_general_special = [(x,y) for x,y in split_general if x not in headers]
        
        for col, sep in split_general_common:  
                headers[:], data[:] = self._splitGeneral(headers, data, col, sep)
        
        formatIndex = headers.index(formatCol)    
        if splitFormat:
            formatHeads, allEqual = self._getFormatHeads(data, formatIndex)
        else: 
            formatHeads, allEqual = None, None
            
        if keep00:
            def missing(val): return len(val) < 3 or (val[0]==val[2]=='.')
        else:
            def missing(val): return len(val) < 3 or (val[2] in ['0', '.'] and val[0] in ['0', '.'])
        
        paramsVCF = dict(chromCol=chromCol, posCol=posCol, geneCol=geneCol, prefilter=prefilter,
                 splitFormat=splitFormat, splitInfo=bool(splitAsInfo), keep00=keep00, formatHeads=formatHeads)
        VFlist = []
        Nsamples = len(data[0]) - (formatIndex+1) 
        for i in range(formatIndex+1, len(data[0])):
            samplename = headers[i]
            fname = filename + '_' + samplename if samplename!="<sample>" else filename
            if splitFormat:
                h, variants = self._splitFORMAT(headers[:], data, formatIndex, i, formatHeads, allEqual, missingFunc=missing)
                for col, sep in split_general_special:  
                    h[:], variants[:] = self._splitGeneral(h, variants, col, sep)
                    
                variants[:] = map(tuple, variants)
            else:
                common = formatIndex + 1
                variants = [tuple(x[:common] + [x[i]]) for x in data if not missing(x[i])]
                h = headers[:common] + [samplename]
            VFlist.append(DataContainer.VCFtypeData(fname, h, descriptions, variants, **paramsVCF))
            
        return VFlist

    def _applyPrefilter(self, fileObject, prefilter):
        operatorText, value = prefilter
        operatorDic = {'start with' : FiltusUtils.mystartswith, 'do not start with' : FiltusUtils.not_mystartswith,
                      'contain' : FiltusUtils.contains, 'do not contain' : FiltusUtils.not_contains}
        if operatorText not in operatorDic:
            raise KeyError('Unknown prefilter operator: "%s". Legal values are "start with", "do not start with", "contain" and "do not contain".' % operatorText)
        operator = operatorDic[operatorText]
        return (line for line in fileObject if operator(line, value))
        
    def _getFormatHeads(self, data, formatIndex):
        formats = set(x[formatIndex] for x in data)
        allEqual = len(formats) == 1
        if allEqual:
            formatHeads = list(formats)[0].split(':')
        else:
            formatHeads = FiltusUtils.listUnique([field for F in formats for field in F.split(':')])
        return formatHeads, allEqual

    def _splitFORMAT(self, h, data, formatIndex, sampleIndex, formatHeads, allEqual, missingFunc):
        L = formatIndex + len(formatHeads)

        if allEqual:
            variants = [x[:formatIndex] + x[sampleIndex].split(':') for x in data if not missingFunc(x[sampleIndex])]
            [x.extend(['']*(L-len(x))) for x in variants if len(x) < L]
        else:
            variants = []
            for x in data:
                if missingFunc(x[sampleIndex]): continue
                dic = dict(zip(x[formatIndex].split(':'), x[sampleIndex].split(':')))
                variants.append(x[:formatIndex] + [dic.get(tag, '') for tag in formatHeads])

        h[formatIndex:] = formatHeads
        return h, variants

    def _splitINFO_slow(self, h, variants, infoInd):
        info = [dict(s.split('=', 1) if '=' in s else [s,'1'] for s in r[infoInd].split(';')) for r in variants]
        all_tagheads = sorted(set(tag for dic in info for tag in dic))
        h[infoInd:(infoInd + 1)] = [tag + '_INFO' for tag in all_tagheads]
        for x, infodic in zip(variants, info):
            x[infoInd:(infoInd + 1)] = [infodic.get(tag, '') for tag in all_tagheads]
        return h, variants

    def _splitINFO_fast(self, h, variants, infoInd, colDescriptions, splitCsq):
        infoDesc = colDescriptions['INFO']
        all_infotags = sorted(infoDesc)
        h[infoInd:(infoInd + 1)] = [tag + '_INFO' for tag in all_infotags]
        
        if splitCsq:
            # index of 'CSQ' in the sorted list of info tags (used for extraction in each variant line)
            csqInInfo = all_infotags.index('CSQ')
            
            # fix headers
            csq_heads = infoDesc['CSQ'].split("Format: ")[1].split("|")
            csqInd = h.index('CSQ_INFO')
            h[csqInd:(csqInd + 1)] = csq_heads
            
        for v in variants:
            info_dict = dict(s.split('=', 1) if '=' in s else [s,'1'] for s in v[infoInd].split(';'))
            info_values = [info_dict.get(tag, '') for tag in all_infotags]
            if splitCsq:
                csq1 = info_values[csqInInfo].split(',')[0] # first consequence only
                info_values[csqInInfo:(csqInInfo + 1)] = csq1.split('|')
            v[infoInd:(infoInd + 1)] = info_values
        
        return h, variants

        
    def _splitGeneral(self, h, variants, splitCol, sep):
        if not variants:
            return h, variants
        if splitCol not in h:
            err = "Something is wrong: Column '%s' to be split, is not among the current column names:\n\n%s" %(splitCol, ', '.join(h))
            raise RuntimeError(err)
        ind = h.index(splitCol)
        counts = set(v[ind].count(sep) for v in variants)
        maxL = max(counts) + 1
        if len(counts) == 1:
            for v in variants:
                v[ind:(ind+1)] = v[ind].split(sep)
        else:
            for v in variants:
                s = v[ind].split(sep)
                if len(s) < maxL: s.extend(['']*(maxL-len(s)))
                v[ind:(ind+1)] = s
        h[ind:(ind+1)] = [h[ind]+'_%d' %i for i in range(1, maxL+1)]
        return h, variants
       
    def _fixAnnovarOtherinfo(self, headers, firstvar):
        lenh = len(headers)
        lenfst = len(firstvar)
        if (lenfst - lenh) == 9 and firstvar[lenh+7].startswith('GT'):
            headers[-1:] = ['CHROM', 'POS', 'rsID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', '<sample>'] 
        if (lenfst - lenh) == 10 and firstvar[lenh+8].startswith('GT'):
            headers[-1:] = ['zygosity', 'CHROM', 'POS', 'rsID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', '<sample>'] 
        return headers
        
    def _parseColumnDescriptions(self, lines):
        '''
        Parses the column description lines in the preamble of a VCF file. 
        Returns a dict of dicts, e.g. {'FORMAT': {'GT': "Genotype", 'AD': 'Allele depth'}}
        '''
        column_descriptions = dict()
        PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
        for line in lines:
            try:
                col = line[2:line.index('=')]
                start, stop = line.index('<')+1, line.rindex('>')
                tagvalues = dict([b.split('=', 1) for b in PATTERN.split(line[start:stop])[1::2]])
                id, descr = tagvalues['ID'], tagvalues['Description']
                if not col in column_descriptions:
                    column_descriptions[col] = dict()
                column_descriptions[col][id] = descr
            except:
                pass
                
        return column_descriptions 
            
    def _prettyDescriptions(self, descriptions): # TODO include remaining columns
        pretty = {}
        if 'FORMAT' in descriptions:
            for key,val in descriptions['FORMAT'].iteritems():
                pretty[key] = val
        if 'INFO' in descriptions:
            for key,val in descriptions['INFO'].iteritems():
                pretty[key + 'INFO'] = val
        if 'FILTER' in descriptions:
            filters = list(descriptions['FILTER'].iteritems())
            max_width = max(len(x[0]) for x in filters)
            pretty['FILTER'] = '\n'.join('%-*s %s' %(max_width, x[0] + ':', x[1]) for x in filters)
        
        return pretty


if __name__ == "__main__":
    reader = VariantFileReader()
    testfile = "testfiles\\CSQ_test1.vcf"
    vflist = reader.readVCFlike(testfile, sep="\t", chromCol="CHROM", posCol="POS", geneCol="", splitAsInfo="INFO", splitCsq=1, keep00=1)
    
    testfile = "testfiles\\test_file.csv"
    vflist = reader.readVCFlike(testfile, sep=",", chromCol="CHROM", posCol="POS", geneCol="Gene", splitAsInfo="INFO", keep00=1)
    assert vflist[0].length == 425
    vflist = reader.readVCFlike(testfile, sep=",", chromCol="CHROM", posCol="POS", geneCol="Gene", splitAsInfo="INFO", keep00=1, prefilter=("contain", "splic"))
    assert vflist[0].length == 10
    #vflist = reader.readVCFlike(testfile, sep=",", chromCol="CHROM", posCol="POS", geneCol="Gene", splitAsInfo="INFO", keep00=1, prefilter=("contain", "BOGUS TEXT"))
    #assert vflist[0].length == 10
    
    
    
    