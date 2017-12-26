# -*- coding: UTF-8 -*-
'''
Created on 11 Dec 2011

@author: lbarron
'''

from lxml import etree
# from corpora.meter.meter_doc import meter_pa_doc, meter_newspaper_doc

import re  # regular expressions


class meter_xml:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._pa = {}
        """pa notes"""

        self._np = {}
        """newspaper notes"""

        self._pa_index = {}
        """Index of pa notes per super id"""

        self._np_index = {}
        """Index of newspaper notes per super id"""

        self._date_pattern = re.compile("-[0-9]*-")

    def load_xml_document(self, c_file):
        """Nothing done. Just an example to learn how this process words"""
        ET = etree.parse(c_file)

    #        text_elements = ET.findall('text/group/text')     #global text
    #        for  in text_elements:
    #        for elt in ET.getiterator('div'):
    #            print 'kk', elt.tag

    def load_pa_corpus(self, files):
        """Loads the pa corpus.

        arguments
        files -- list with the files (including absolute path)"""

        for c_file in files:
            self.load_pa_notes(c_file)

    def load_pa_notes(self, c_file):
        """Loads the PA notes from an XML file.
        A note is from the PA if its identifier starts with 'A'.

        arguments
        c_file -- file with absolute path"""
        ET = etree.parse(c_file)

        for text_et in ET.getiterator('text'):
            if text_et.get('n') == None:  # there is a "super text" per date, but we don't really need it
                continue
            sup_id = text_et.get('id')
            sup_name = text_et.get('name')
            self._pa_index[sup_id] = []
            for div_et in text_et.getiterator('div'):
                if div_et.get('id').startswith('A'):  # PA NOTE
                    self._pa[div_et.get('id')] = meter_pa_doc(
                        sup_id,  # super identifier
                        sup_name,  # super name
                        div_et.get('id'),  # unique id
                        div_et.get('n'),  # pa-date-i
                        div_et.get('type'),  # court | showbiz
                        div_et.get('ana'),  # src
                        div_et.findtext('head'),  # note head
                        self._get_sentences(div_et))  # list of sentences
                    self._pa_index[sup_id].append(div_et.get('id'))  # index of newspapers per super id

    #                    print div_et.get('n')
    #                    print self._pa[div_et.get('id')]

    def load_newspaper_corpus(self, files):
        """Loads the pa corpus.

        arguments
        files -- list with the files (including absolute path)"""

        for c_file in files:
            self.load_newspaper_notes(c_file)

    def load_newspaper_notes(self, c_file):
        """Loads the newspaper notes from an XML file.
        A note is from a newspaper if its identifier starts with 'M'.

        arguments
        c_file -- file with absolute path"""
        ET = etree.parse(c_file)

        for text_et in ET.getiterator('text'):
            if text_et.get('n') == None:  # there is a "super text" per date, but we don't really need it
                continue
            sup_id = text_et.get('id')
            sup_name = text_et.get('n')
            #            for div_et in text_et.getiterator('div'):
            self._np_index[sup_id] = []
            for div_et in text_et.getiterator('div'):
                if div_et.get('id').startswith('M'):  # newspaper NOTE
                    # print div_et.get('id')
                    self._np[div_et.get('id')] = meter_newspaper_doc(
                        sup_id,  # super identifier
                        sup_name,  # super name
                        div_et.get('id'),  # unique id
                        div_et.get('n'),  # pa-date-i
                        div_et.get('type'),  # court | showbiz
                        div_et.get('ana'),  # src
                        div_et.findtext('head'),  # note head
                        self._get_sentences(div_et))  # list of sentences
                    self._np_index[sup_id].append(div_et.get('id'))  # index of newspapers per super id

    def keep_only_newspaper_courts(self):
        for key in self._np.keys():
            if self._np[key].np_type != "courts":
                self._np.pop(key)

    def keep_only_newspaper_showbiz(self):
        for key in self._np.keys():
            if self._np[key].np_type != "showbiz":
                self._np.pop(key)

    #    def _extract_sentence(self, element, sent = ""):
    #        if element.findtext('s') != None:
    #            if element.findtext('s') != '\n':
    #                sent = element.findtext('s')
    #
    #        else:
    #            if element.isinstance(element.tag, basestring):
    #                if element.text != "\n":
    #                    print  ('%s - %s' % (element.tag, element.text))
    #                elif (element.tag == 's'):
    #                    sent = element.text
    #                elif (element.tag == 'seg')
    #

    #            else:
    #                print ("SPECIAL: %s - %s" % (element.tag, element.text))
    #        return sent

    def _get_sentences(self, et_note):
        sentences = []
        for p in et_note.getiterator('p'):
            """Here we iterate over the sentences??=="""
            for i in range(0, len(p)):
                child = p[i]
                if child.tag == 's':
                    if len(child) > 0:  ##it has childs --> its a seg (verbatim)
                        sentences.append(" ".join(child[i].text for i in range(0, len(child)) if child[i].tag == 'seg'))
                    #                        print sent
                    else:
                        #                print p.findtext('child') == '\n'
                        sentences.append(p[i].text)  # findtext('child')
                elif child.tag == 'list':
                    for it in child.getiterator('item'):
                        sentences.append(it.findtext('s'))
                        # print sentences[-1]
                #                    sentences.append(" ".join(child[i][0].text for i in range(0,len(child)) if child[i].tag == 'item') )
                #                    for l in p.getiterator('list'):
                ##                        for i in l.getiterator('item'):
                ##                            sentences.append(i.findtext('child'))
                #                    print " ".join(child[i][0].text for i in range(0,len(child)) if child[i].tag == 'item')
                else:
                    print
                    "todavia otra cosa"
                # print sentences[-1]

        #            print len(child)
        #        print sentences
        return sentences

    #    def _get_sentences(self, et_note):
    #
    #        """Extracts every sentence from a given note.
    #
    #        arguments
    #        et_note -- element tree already inside of 'div', the note identifier"""
    ##        sentences = []
    ##        p = et_note.
    ##        print et_note.tostring(p, method = 'text')
    ##        print (p.xpath("//text()"))
    #
    #        for p in et_note.getiterator('p'):
    #            self._extract_sentence(p)
    #
    #
    ##        sentences = self._get_sentences(et_mopte)
    #
    ##        for p in et_note.getiterator('p'):
    ##            for element in p.iter():
    ##                self._extract_sentence(element)
    ##                if isinstance(element.tag, basestring):
    ##                    print  ('%child - %child' % (element.tag, element.text))
    ##                else:
    ##                    print ("SPECIAL: %child - %child" % (element.tag, element.text))
    #
    ##            sent = ''
    ###            print (p.xpath("//text()"))
    ###            if p.findtext('child') == None:
    ##            if p.findtext('child') == '\n':
    ##                for element in p.iter('seg'):
    ##                    print ('%child' % (element.text)),
    ##            else:
    ##                print (p.findtext('child'))
    #
    #
    #
    #
    ##            for element in p.iter('seg'):
    ##                print ('%child - %child' % (element.tag, element.text)),
    ##            if p.findtext('child') != None:
    ##                if p.findtext('child') != '\n':
    ##                    print "aqui"
    ##                for child in p.getiterator('child/seg'):
    ###                    for seg in child.getiterator('seg'):
    ##                    sentences.append(child.findtext('seg'))
    ###                for seg in p.getiterator('seg'):
    ####                    sentences.append(seg.)
    ##
    ##                sentences.append(p.findtext('child'))
    ##            else:
    ##                for l in p.getiterator('list'):
    ##                        for i in l.getiterator('item'):
    ##                            sentences.append(i.findtext('child'))
    #
    #        return sentences

    ###########
    # GETTERS #
    ###########

    def get_number_documents(self):
        return self.get_number_pa_notes() + self.get_number_np_notes()

    def get_pa_ids(self):
        return self._pa.keys()

    def get_np_ids(self):
        return self._np.keys()

    def get_title_pa_id(self, pa_id):
        """Return the title of the PA note.

        arguments:
        pa_id -- identifier of the PA note (Axxx)"""
        title = self._pa[pa_id].pa_title
        if title == None:
            return ""
        return title

    def get_sentence_pa_id(self, pa_id, number):
        """Return a specific sentence from a PA note.
        None if the sentence does not exist.

        arguments:
        pa_id  -- identifier of the PA note (Axxx)
        number -- sentence number        """
        #        TODO Not necessary now, but it should add 1 because in the corpus they start in 1
        sentences = self._pa[pa_id].pa_sentences
        if len(sentences) < number:
            return None
        else:
            return sentences[number]

    def get_number_pa_notes(self):
        """ Return the number of PA notes loaded"""
        return len(self._pa)

    def get_number_pa_notes_courts(self):
        """Return the number of PA notes on 'courts' loaded"""
        return self._get_number_pa_notes_per_genre('courts')

    def get_number_pa_notes_showbiz(self):
        """Return the number of PA notes on 'showbiz' loaded"""
        return self._get_number_pa_notes_per_genre('showbiz')

    def get_text_pa_id(self, pa_id):
        """Return the text from a PA note (title not included)

        arguments:
        pa_id ---- identifier of the PA note (Axxx)"""
        sentences = self._pa[pa_id].pa_sentences
        return ' '.join(sentences)

    def get_title_text_pa_id(self, pa_id):
        """Return the title and text from a PA note as a single string

        arguments:
        pa_id ---- identifier of the PA note (Axxx)"""
        title = self.get_title_pa_id(pa_id)
        text = self.get_text_pa_id(pa_id)
        overall = title + " " + text
        return overall

    def get_pa_ids_from_supernote(self, supernote_id):
        """Return the identifiers of the PA notes belonging to this supernote"""
        return self._pa_index[supernote_id]

    #    def get_pa_ids_from_super(self, super_id):
    #        ids = []
    #        print self._pa.get(super_id)
    #        for doc in self._pa.get(super_id):
    #            ids.append(doc.np_id)
    #        return ids

    def get_np_ids_from_supernote(self, supernote_id):
        """Return the identifiers of the newspaper notes belonging to this supernote"""
        return self._np_index[supernote_id]

    def get_relevants_for_newspaper_note(self, np_id):
        super_id = self._np[np_id].super_id
        #        print super_id
        #        prefix = self._get_super_id_prefix(self._np[np_id].np_n)
        relevants = self.get_pa_ids_from_supernote(super_id)
        #        print relevants

        #        for key in self._np_index.keys():
        #            if key.startswith(prefix) and self._np[np_id].np_n in self._np_index[key]:
        #                print key, self._np[np_id].np_n, self._pa_index[key]#.pa_id
        #                relevants.append([x for x in self._pa_index[key]])
        return relevants

    def _get_super_id_prefix(self, note_n):
        date = self._date_pattern.search(note_n).group(0)
        date = 'M' + date[1: len(date) - 1]
        return date

    def _get_number_pa_notes_per_genre(self, genre):
        """Return the number of PA notes of a given genre

        arguments:
        genre -- genre of news, either 'courts' or 'showbiz'"""
        count = 0
        for pa_id, pa_note in self._pa.iteritems():
            pa_id = pa_id
            if pa_note.pa_type == genre:
                count += 1
        return count

    def get_title_np_id(self, np_id):
        """Return the title of the newspaper note.

        arguments:
        np_id -- identifier of the newspaper note (Axxx)"""

        return self._np[np_id].np_title

    def get_sentence_np_id(self, np_id, number):
        """Return a specific sentence from a newspaper note.
        None if the sentence does not exist.

        arguments:
        np_id  -- identifier of the newspaper note (Axxx)
        number -- sentence number        """
        #        TODO Not necessary now, but it should add 1 because in the corpus they start in 1
        sentences = self._np[np_id].np_sentences
        if len(sentences) < number:
            return None
        else:
            return sentences[number]

    def get_number_np_notes(self):
        """ Return the number of newspaper notes loaded"""
        return len(self._np)

    def get_number_np_notes_courts(self):
        """Return the number of newspaper notes on 'courts' loaded"""
        return self._get_number_np_notes('courts')

    def get_number_np_notes_showbiz(self):
        """Return the number of newspaper notes on 'showbiz' loaded"""
        return self._get_number_np_notes('showbiz')

    def get_text_np_id(self, np_id):
        """Return the text from a newspaper note (title not included)

        arguments:
        np_id ---- identifier of the newspaper note (Axxx)"""
        sentences = self._np[np_id].np_sentences
        return ' '.join(sentences)

    def get_title_text_np_id(self, np_id):
        """Return the title and text from a newspaper note as a single string

        arguments:
        np_id ---- identifier of the newspaper note (Mxxx)"""
        text = self.get_title_np_id(np_id)
        text += " " + self.get_text_np_id(np_id)
        return text

    def get_number_whollyderiv_notes(self):
        """Return the number of wholly derived notes"""
        return self._get_number_derived_notes('wd')

    def get_number_whollyderiv_notes_courts(self):
        """Return the number of wholly derived notes on courts"""
        return self._get_number_derived_notes_kind('courts', 'wd')

    def get_number_whollyderiv_notes_showbiz(self):
        """Return the number of wholly derived notes on courts"""
        return self._get_number_derived_notes_kind('showbiz', 'wd')

    def get_number_partiallyderiv_notes(self):
        """Return the number of partially derived notes"""
        return self._get_number_derived_notes('pd')

    def get_number_partiallyderiv_notes_courts(self):
        """Return the number of partially derived notes on courts"""
        return self._get_number_derived_notes_kind('courts', 'pd')

    def get_number_partiallyderiv_notes_showbiz(self):
        """Return the number of partially derived notes on showbiz"""
        return self._get_number_derived_notes_kind('showbiz', 'pd')

    def get_number_nonderived_notes(self):
        """Return the number of non derived notes"""
        return self._get_number_derived_notes('nd')

    def get_number_nonderiv_notes_courts(self):
        """Return the number of non-derived notes on courts"""
        return self._get_number_derived_notes_kind('courts', 'nd')

    def get_number_nonderiv_notes_showbiz(self):
        """Return the number of non-derived notes on showbiz"""
        return self._get_number_derived_notes_kind('showbiz', 'nd')

    def _get_number_np_notes(self, kind):
        """Return the number of newspaper notes of a given kind

        arguments:
        kind -- kind of news, either 'courts' or 'showbiz'"""
        count = 0
        for np_id, np_note in self._np.iteritems():
            np_id = np_id
            if np_note.np_type == kind:
                count += 1
        return count

    def _get_number_derived_notes(self, kind):
        """Return the number of newspaper notes with a given derivation kind: wholly derived,
        partially derived, or non-derived

        arguments:
        kind -- kind of derivation, either 'wd', 'pd' or 'nd'"""
        count = 0
        for np_id, np_note in self._np.iteritems():
            np_id = np_id
            if np_note.np_ana == kind:
                count += 1
        return count

    def _get_number_derived_notes_kind(self, genre, kind):
        """Return the number of newspaper notes in a given genre (courts, showbiz) with a
        given derivation kind (wholly derived, partially derived, or non-derived)

        arguments:
        genre -- genre of the note, either 'courts' or 'showbiz'
        kind -- kind of derivation, either 'wd', 'pd' or 'nd'"""
        count = 0
        for np_id, np_note in self._np.iteritems():
            np_id = np_id
            if np_note.np_type == genre and np_note.np_ana == kind:
                count += 1
        return count

#        for subnode in nodeList:
#            if subnode.nodeType == subnode.ELEMENT_NODE:
#                obtainRefCorpus(subnode.childNodes)
#            elif subnode.nodeType == subnode.TEXT_NODE:
#                if subnode.parentNode.nodeName== "head":
#                    headID=subnode.parentNode.parentNode.getAttribute('n')
#                    if headID.split('-')[0]=="pa":
#                        PAid=headID[headID.find("-")+1:]
#                        refCorpus[PAid]=[subnode.data,[]]
#
#                if subnode.parentNode.nodeName== "s":
#                    headID=subnode.parentNode.parentNode.parentNode.getAttribute('n')
#                    if headID.split('-')[0]=="pa":
#                        PAid=headID[headID.find("-")+1:]
#                        if refCorpus.has_key(PAid):
#                            refCorpus[PAid][1].append(subnode.data)
#                        else:    #En caso de que esta nota no haya tenido "head"
#                            refCorpus[PAid]=[u'',[subnode.data]]


#################### -*- coding: iso-8859-15 -*-

# from xml.dom.ext.reader import Sax2
# from xml.dom import EMPTY_NAMESPACE
# from xml.dom.ext.reader.Sax2 import FromXmlStream        #Para explorar nodo por nodo
# from xml.dom.ext import PrettyPrint                #Escritura del XML contenido
# import sys
# from os import system, path, listdir
# from time import time
# source     =  "pa"
# newspapers = ["express","ft","guardian","independent","mail","mirror","star","sun","telegraph","times"]
#
#
# def ayuda(nombre_programa):            #-h
#    """Ayuda del programa. Parámetros para la ejecución en línea de comando"""
#    #print 'Use: cat config.txt | python klplagiarism.py'+nombre_programa + ' -[h|t|] (si se de más de un parámetro, sólo se considera el primero)' #[-hrsa]'
#
#    print """
#    -h mensaje de ayuda
#    -f     finds where are those notes with (or without) identified fragments (verbatim, rewrite or new
#             example: python meterDOM.py -f < ../../corpus/METER/meter_xml/files
#    -o     finds where are the PA notes
#             example: python meterDOM.py -o < ../../corpus/METER/meter_xml/files
#
#    -l <xml_file>    Lemmatization of all the text in the xml_file
#             example: python meterDOM.py -l xml1.xml
#             lematiser.sh is provided in order to handle multiple files
#    -n     average number of words in PA and newspaper notes
#      <r>     reference corpus (only of the PA notes)
#      <s>     suspicious corpus (only of the newspapers notes)
#        example: python meterDOM.py -n < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    -s      statistical features of the corpus
#      <a>     statistical features (only of the PA notes)
#      <n>     statistical features (only of the newspapers notes)
#             example: python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    -p <ref-corpus-base-directory>     Estimate the probability distributions P for all the documents in the reference corpus
#         Probability distribution are saved in <ref-corpus-base-directory>/P
#
#    -t <n> < <files-list>   Training stage, consider all the PA notes and create n-grams lists
#             example: python meterDOM.py -t 2 file 2 is the ngrams level and file is the list with the files to consider
#         (EN DUDA SI ESTA LINEA DE LA AYUDA ES VERDAD)
#
#    -j <ref-corpus-directory> <n> < <files-list>    Test considering reference n-grams
#             example: #python meterDOM.py -j "../../corpus/METER/meter_xml/ecir/ngrams_2" 2 < ../../corpus/.../ecir/files
#    -k <ref-corpus-base-directory> < <files-list>    Test considering the search space reduction (based on KL-distance)
#                                                and n-grams search
#          example: #python meterDOM.py -k "../../corpus/METER/meter_xml/ecir" 2 < ../../corpus/.../ecir/files
#    """
#
# def find_located(xFiles):
#    """Finds those papernews which are located (verbatim, rewrite or new)"""
#
#    for eXml in xFiles:
#        reader = Sax2.Reader()
#        doc = reader.fromStream(open(eXml))
#        elements = doc.getElementsByTagName('div')
#        for e in elements:
#            n=e.getAttributeNS(EMPTY_NAMESPACE,'n').split("-")
#            cPaper=n[0]
#            if cPaper in newspapers:
#                #print "current paper", cPaper
#                newsKey="-".join([n[1],n[2]])
#                #print "dos", "e", e
#                sentences=e.getElementsByTagName('s')
#
#                segment=sentences[0].getElementsByTagName('seg')
#                if len(segment)==0:
#                    print eXml, cPaper+"-"+newsKey, "\t\t NO"    #No está identificado
#                else:
#                    print eXml, cPaper+"-"+newsKey, "\t\t SI"    #Si está identificado
#        del(reader)
#
# def find_PA(xFiles):
#    """Finds the PA notes in all teh XML files"""
#    for eXml in xFiles:
#        reader = Sax2.Reader()
#        doc = reader.fromStream(open(eXml))
#        elements = doc.getElementsByTagName('div')
#        for e in elements:
#            n=e.getAttribute('n').split("-")
#            cPaper=n[0]
#            if cPaper==source:
#                newsKey="-".join([n[1],n[2]])
#                print eXml, cPaper+"-"+newsKey
#        del(reader)
#
#
# def _cleanW(w):
#    """Quits space lines and strange leading characters. additionally, it splits
#    words and punctuation marks"""
#    punct=['¡','¿','(','"','.',',',':',';',')','!','?',')','"','`',"'"]
#
#    cW=[""]*3
#    if len(w)==0:
#        return cW
#    clean=w
#
#    if clean!="":
#        while 1:
#            if clean=="" or clean[0].isalnum():
#                break
#            cW[0]+=clean[0]
#            clean=clean[1:]
#        while 1:
#            if clean=="" or clean[-1].isalnum():
#                break
#            cW[2]=clean[-1]+cW[2]
#            clean=clean[:-1]
#    cW[1]=clean
#    return cW
#
# def lemmatize(nodeList):
#    """Lemmatise the xml file content"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            lemmatize(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            p = PorterStemmer()
#            output=''
#            word=''
#            line = subnode.data
#
#            for eWord in line.split():
#                cleanWord=_cleanW(eWord)
#                output+=cleanWord[0]
#                output += p.stem(cleanWord[1].lower(), 0,len(cleanWord[1])-1)
#                output+=cleanWord[2]+" "
#
#            subnode.data= output[:-1]
#
# def _refrescaGwords(w):
#    """Para cada una de las palabras en w refresca los valores del diccionario de tokens"""
#    for eW in w:
#        if globalWords.has_key(eW):        globalWords[eW]+=1
#        else:                    globalWords[eW]=1.0
#
# def statGlobal(nodeList):
#    """Counts the number of tokens and types for the entire document"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statGlobal(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName in ["head","s","seg"]:
#                _refrescaGwords(subnode.data.split())
#
# def statPA(nodeList):
#    """Counts the number of tokens and types for the PA notes"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statPA(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                if subnode.parentNode.parentNode.getAttribute('n').split('-')[0]=="pa":
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "s":
#                if subnode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0]=="pa":
#                    _refrescaGwords(subnode.data.split())
#
# def statNP(nodeList):
#    """Counts the number of tokens and types for the newspaper notes"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statNP(subnode.childNodes)
#
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                #Si este titulo es de alguno de los periodicos
#                if subnode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "s":
#                if subnode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "seg":
#                if subnode.parentNode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    #print "contando seg con padre ",subnode.parentNode.parentNode.parentNode.parentNode.getAttribute
#                    _refrescaGwords(subnode.data.split())
#
# def obtainRefCorpus(nodeList):
#    """Obtain reference corpus"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            obtainRefCorpus(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                headID=subnode.parentNode.parentNode.getAttribute('n')
#                if headID.split('-')[0]=="pa":
#                    PAid=headID[headID.find("-")+1:]
#                    refCorpus[PAid]=[subnode.data,[]]
#
#            if subnode.parentNode.nodeName== "s":
#                headID=subnode.parentNode.parentNode.parentNode.getAttribute('n')
#                if headID.split('-')[0]=="pa":
#                    PAid=headID[headID.find("-")+1:]
#                    if refCorpus.has_key(PAid):
#                        refCorpus[PAid][1].append(subnode.data)
#                    else:    #En caso de que esta nota no haya tenido "head"
#                        refCorpus[PAid]=[u'',[subnode.data]]
#
# def trNgram(reference, d, grade):
#    """Receives the reference corpus and creates the n-grams dictionary
#    reference -> dictionary with the sentences of the notes
#    d         -> directory containing the reference corpus
#    grade     -> n-gram level"""
#    from trainNgram import trNgram
#    ngramsDir=d+"/ngrams_"+str(grade)+"/"
#    if not path.isdir(ngramsDir):
#        system("mkdir "+ngramsDir)
#    train=trNgram()
#
#    for keyNote in reference.keys():
#        sentences=[]
#        if reference[keyNote][0]!="":
#            sentences.append(reference[keyNote][0])
#
#        sentences.extend(reference[keyNote][1])
#        print keyNote
#        grams=train.getNgram(sentences, grade)
#        kk=grams.keys()
#        kk.sort()
#        oFile=open(ngramsDir+keyNote+"-"+str(grade),'w')
#
#        for k in kk:
#            cn=k+" "+str(grams[k])+" \n"
#            oFile.write(cn)
#        oFile.close()
#    del(train)
#
#
# def getP(tfF, tfidfF):
#    """Obtains the probability distributions P of all the reference documents
#       tfF     -> tf file
#       tfidfF  -> tfidf file
#       preP         <- P distribution probabilities for all the PA notes"""
#    #Obtaining 20 % of the vocabulary in base to tfidf
#    cFile=open(tfidfF, 'r')
#    termsInFile=cFile.readlines()
#    cFile.close()
#    selectedTerms=[]
#    for i in range (0, int(len(termsInFile)*.20)+1):
#        newT=termsInFile[i].split()[0].lower()
#        selectedTerms.append(newT)
#    #Obtaining the vocabulary with the associated tf
#    cFile=open(tfF, 'r')
#    tfTerms={}
#    for eLine in cFile.readlines():
#        cc=eLine.split()
#        cW=cc[0]
#        cTF=cc[1]
#        tfTerms[cW.lower()]=cTF
#    cFile.close()
#    #Obtaining tf values for the selected terms
#    preP={}
#    for eT in selectedTerms:
#        k=eT.lower()
#        preP[k]=tfTerms[k]
#    return preP
#
#
# def obtainSusCorpus(xFile):
#    """Obtains the suspicious corpus (only those that are identified) from the xml file
#    xFile -> the name of the xml file
#    Refreashes the global var. susCorpus (dict)
#    """
#    reader = Sax2.Reader()
#    doc = reader.fromStream(open(xFile))
#    elements = doc.getElementsByTagName('div')
#
#    for e in elements:
#        newsKey=e.getAttributeNS(EMPTY_NAMESPACE,'n')
#        cPaper=newsKey[:newsKey.find("-")]
#        if cPaper in newspapers:
#            header=e.getElementsByTagName('head')[0]    #Esto devuelve una lista aunque sólo se quiera usar uno
#            noteHeader= header.firstChild.data
#            suspiciousNote=[]
#            sentences=e.getElementsByTagName('s')
#            allSentences={}
#
#            for eSent in sentences:
#                sentence_n=eSent.getAttribute('n')
#                segments=eSent.getElementsByTagName('seg')
#                if len(segments)!=0:
#                    cSent=""
#                    verb_rewLen=0.0        #Número de palabras en verbatim o rewrite
#                    totalLen=0.0        #Número total de palabras
#                    for eSeg in segments:     #Si se determina que hay que cambiar el formato de las sentencias, aqui
#                        #if eSeg.firstChild.data:    #Necesario si el corpus tiene <segs> vacios
#                        try:
#                            ana=eSeg.getAttribute('ana')
#                            strSegment=eSeg.firstChild.data
#                            cLen=len(strSegment.split())
#                            totalLen+=cLen
#                            if ana[0]=="v" or ana[0]=="r":
#                                verb_rewLen+=cLen
#                            cSent+=strSegment+" "
#                        except: pass
#                    if verb_rewLen>= 0.4*totalLen:
#                        #allSentences[sentence_n]=cSent[:-1]
#                        allSentences[sentence_n]=[1,cSent[:-1]]
#                    else:
#                        allSentences[sentence_n]=[0,cSent[:-1]]
#            if allSentences:
#                flagIsIdentified=0
#                if noteHeader=="NO TITLE":
#                    susCorpus[newsKey]=["", allSentences]
#                else:
#                    susCorpus[newsKey]=[noteHeader, allSentences]
#    del(reader)
#
# def locatePlag(ref_dir, ng):
#    """Look for the plagiarised sentences candidates
#       ref_dir ->  directory containing the reference corpus (n-grams)
#       ng      ->  n-grams level"""
#    from trainNgram import clNgram
#
#    clasif=clNgram()
#    for eKey in susCorpus.keys():
#        Weights=clasif.calcProbs(eKey, ref_dir, susCorpus[eKey], int(ng))
#        clasif.findCandidates(Weights)
#    del(clasif)
#
# def _refreshDict(cDict, newStr):
#    """If cDict already has the key newStr, add 1, otherwise cDict[newStr]=1.0
#       cDict  -> dictionary
#       newStr -> current word
#    """
#    if cDict.has_key(newStr): cDict[newStr]+=1
#    else:              cDict[newStr]=1.0
#
# def getQprime(S):
#    """Estimates Q'(S) based on tf and the vocabulary of S (consider that n=1 always)
#       S       -> list containing note title (S[0]) and a dictionary of sentences
#       splDict <- Q'(S)"""
#    noteTitle=S[0].split()
#    sDict=S[1]
#    splDict={}
#    dS=""
#    globalFreq=0.0
#    for eW in noteTitle:
#        clWord=_cleanW(eW)
#        if clWord[0]:
#            _refreshDict(splDict, clWord[0].lower())
#            globalFreq+=1
#        if clWord[1]:
#            _refreshDict(splDict, clWord[1].lower())
#            globalFreq+=1
#        if clWord[2]:
#            _refreshDict(splDict, clWord[2].lower())
#            globalFreq+=1
#
#    for dKey in sDict.keys():
#        isPlag=sDict[dKey][0]
#        cLine=sDict[dKey][1]
#        for eW in cLine.split():
#            clWord=_cleanW(eW)
#            if clWord[0]:
#                _refreshDict(splDict, clWord[0].lower())
#                globalFreq+=1
#            if clWord[1]:
#                _refreshDict(splDict, clWord[1].lower())
#                globalFreq+=1
#            if clWord[2]:
#                _refreshDict(splDict, clWord[2].lower())
#                globalFreq+=1
#    for eW in splDict.keys():
#        splDict[eW]=splDict[eW]/globalFreq
#    return splDict
#
# def getPfromFile(pFile):
#    """Obtain the prob. distribution P from file pFile
#       pFile <- File with the estimated P
#       cP    -> dictionary with P"""
#    cP={}
#    sFile=open(pFile, 'r')
#    for eLine in sFile.readlines():
#        cL=eLine.split()
#        cT=cL[0]
#        #print cL[1]
#        cW=float(cL[1])
#        cP[cT]=float(cW)
#    sFile.close()
#    return cP
#
# def getReducedRefCorpus(Pdict, Qp):
#    """Given the reference corpus with P(c_j) (previously obtained with -p) and probability distribution Q'(S), obtain
#    the minimised reference corpus
#    Pdict -> Dictionary with all the P prob. distributions calculated
#    Qp   -> Q'(S)
#    rRef <- List with the 10 documents with min KL(P||Q) including the distance [[KL, refId],..]"""
#    from probEstimator import probDensities
#    #print Qp, rDir
#    p=probDensities()
#    distances=[]
#    for pK in Pdict.keys():
#        Q=p.getQ(Pdict[pK], Qp)
#        cDist=p.KLdist(Pdict[pK], Q)
#        new=[cDist, pK]
#        distances.append(new)
#    distances.sort()
#    del(p)
#    return distances[:10]
#
# def locateReducedPlag(refDir, susDoc, refDocs, ng, susKey):
#    """Look for the plagiarised sentences candidates
#       ref_dir ->  directory containing the reference corpus (n-grams)
#       susDoc  -> The current suspicious document
#       refDocs -> the reference corpus docs that conform the reduced searh space
#       ng      ->  n-grams level
#       susKey  -> Suspicious note id"""
#    from trainNgram import clNgram
#
#    rDir=refDir+"/ngrams_"+str(ng)+"/"
#    clasif=clNgram()
#    Weights=clasif.reducedCalcProbs(rDir, refDocs, susDoc, susKey, ng)
#    clasif.findCandidates(Weights)
#    del(clasif)
#
##################
##              #
##     main    #
##              #
##################
#
# import sys
##The directory where the work will be done
# workingDir="/home/lbarron/plagio/programs/ecir"
#
#
# parametros = sys.argv
# if len(sys.argv) > 1:
#    opciones = sys.argv[1]
# else:
#    ayuda(sys.argv[0])
#    sys.exit()
#
# if ('h' in opciones):                #Ayuda
#    ##python meterDOM.py -h
#    ayuda(sys.argv[0])
#    sys.exit()
#
# if ('f' in opciones):                #Find the located paper news
#    #python meterDOM.py -f < ../../corpus/METER/meter_xml/files
#    search=sys.argv[1]
#    fin = sys.stdin
#    xmlFiles=[x[:-1] for x in fin.readlines()]
#    find_located(xmlFiles)
#    sys.exit()
#
# if ('o' in opciones):                #Find where are the PA notes
#    #python meterDOM.py -o < ../../corpus/METER/meter_xml/files
#    #search=sys.argv[1]
#    fin = sys.stdin
#    xmlFiles=[x[:-1] for x in fin.readlines()]
#    find_PA(xmlFiles)
#    sys.exit()
#
# if ('l' in opciones):                #Lemmatise the document *.xml
#    #python meterDOM.py -l /home/lbarron/plagio/corpus/METER/meter_xml/meter07_01_2000.xml
#
#    from porter import PorterStemmer
#    xmlFile=sys.argv[2]
#
#    doc=FromXmlStream(xmlFile)
#        lemmatize(doc.childNodes)
#
#    PrettyPrint(doc)
#    sys.exit()
#
# if ('n' in opciones):                #Number of words
#    #python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    #globalWords={}
#    #filesList=sys.stdin
#    n=1
#    filesList=sys.stdin#argv[2]
#
#    lista=filesList.readlines()
#    directory=lista[0][:lista[0].rindex("/")]
#    #for xmlFile in lista[0:1]:
#    if ('r' in opciones):        #Reference corpus
#        refCorpus={}
#        #for xmlFile in lista[0:1]:
#        for xmlFile in lista:
#            print xmlFile.strip()
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#            obtainRefCorpus(doc.childNodes)
#        nGlobal=0.0
#        i=0.0
#        for eKey in refCorpus:
#            words=[]
#            title= refCorpus[eKey][0]
#            if title!="":
#                for eWord in title.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            for eLine in refCorpus[eKey][1]:
#                for eWord in eLine.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            print eKey, #len(words)
#            nGlobal+=len(words)
#            i+=1
#
#    if ('s' in opciones):        #Suspicious corpus
#        susCorpus={}
#        #for xmlFile in lista[0:2]:
#        for xmlFile in lista:
#            print xmlFile.strip()
#            xmlFile=xmlFile[:-1]
#            #doc=FromXmlStream(xmlFile)
#            obtainSusCorpus(xmlFile)#    obtainRefCorpus(doc.childNodes)
#        nGlobal=0.0
#        i=0.0
#        for eKey in susCorpus:
#            #print eKey, susCorpus
#            print
#            words=[]
#            title= susCorpus[eKey][0]
#            if title!="":
#                for eWord in title.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            for eK in susCorpus[eKey][1].keys():
#                #print susCorpus[eKey][1][eK]
#                eLine=susCorpus[eKey][1][eK][1]
#                for eWord in eLine.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            print eKey, #len(words)
#            nGlobal+=len(words)
#            i+=1
#    print
#    print nGlobal/i        #print
#    sys.exit()
#
# if ('s' in opciones):                #Statistical features of the corpus
#    #python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    globalWords={}
#    filesList=sys.stdin
#
#    if   ('a' in opciones):
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statPA(doc.childNodes)
#    elif ('n' in opciones):
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statNP(doc.childNodes)
#    else:
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statGlobal(doc.childNodes)
#    nTypes=0
#    nTokens=0
#    for eK in globalWords.keys():
#        nTypes+=1
#        nTokens+=globalWords[eK]
#    print "|Tokens| = ", nTokens
#    print "|Types|  = ", nTypes
#    sys.exit()
#
# if ('t' in opciones):                #Get the n-grams from the reference corpus
#    #python meterDOM.py -t 2 < /home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#    #python meterDOM.py -t 3 < /home/lbarron/plagio/corpus/METER/meter_xml/ecir/lemma/files
#    n=int(sys.argv[2])
#
#    filesList=sys.stdin#argv[2]
#    refCorpus={}
#    lista=filesList.readlines()
#    directory=lista[0][:lista[0].rindex("/")]
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        print xmlFile.strip()
#        xmlFile=xmlFile[:-1]
#        doc=FromXmlStream(xmlFile)
#            obtainRefCorpus(doc.childNodes)
#    trNgram(refCorpus, directory, n)
#    sys.exit()
#
# if ('j' in opciones):                #Look for plagiarised sentences based only on n-grams
#    #python meterDOM.py -j "/home/lbarron/plagio/corpus/METER/meter_xml/ecir/ngrams_2" <
#    #/home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#
#    refCorpus_dir=sys.argv[2]
#    n=sys.argv[3]
#    filesList=sys.stdin
#    susCorpus={}
#    lista=filesList.readlines()
#
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        #print xmlFile.strip()
#        xmlFile=xmlFile[:-1]
#        doc=FromXmlStream(xmlFile)
#        obtainSusCorpus(xmlFile)
#    #for eKey in susCorpus.keys():
#        #print eKey, susCorpus[eKey]
#    locatePlag(refCorpus_dir, n)        #susCorpus ya es global, así que no vale la pena enviarla como parámetro
#
#    sys.exit()
#
# if ('k' in opciones):                #Looking for plagiarised fragments over the reduced search space
#    #python meterDOM.py -k "/home/lbarron/plagio/corpus/METER/meter_xml/ecir/ngrams_2" 2 <
#    #/home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#    ##Técnica de LC+KL-Distance
#
#    refCorpus_dir=sys.argv[2]
#    n=int(sys.argv[3])
#    filesList=sys.stdin
#    susCorpus={}
#    lista=filesList.readlines()
#
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        #print xmlFile.strip()
#        xmlFile=xmlFile.strip()
#        doc=FromXmlStream(xmlFile)
#        obtainSusCorpus(xmlFile)
#    Qprime={}
#    refDocs={}
#
#    #Obtaining P
#    Pdir=refCorpus_dir+"/P/"
#    pFiles=listdir(Pdir)
#    P={}
#    for eFile in pFiles:
#        P[eFile]=getPfromFile(Pdir+eFile)
#    totLen=0.0
#
#    for eKey in susCorpus.keys():
#        iniTime=time()
#
#        Qprime[eKey]=getQprime(susCorpus[eKey])
#        refDocs[eKey]=getReducedRefCorpus(P, Qprime[eKey])
#        finTime=time()
#
#        locateReducedPlag(refCorpus_dir, susCorpus[eKey], refDocs[eKey], n, eKey)        #susCorpus y es global
#        print "XXXXX", finTime-iniTime
#    sys.exit()
#
#
# if ('p' in opciones):                #Estimation of distribution probability P
#    #python meterDOM.py -p "/home/lbarron/plagio/corpus/METER/meter_xml/ecir"
#    refCorpus_dir=sys.argv[2]
#    tfDir   =refCorpus_dir.rstrip("/")+"/tf_1/"
#    tfIdfDir=refCorpus_dir.rstrip("/")+"/"+"tfidf_1/"
#    Pdir    =refCorpus_dir.rstrip("/")+"/P/"
#    if not path.isdir(Pdir):
#        system("mkdir "+Pdir)
#    terms={}
#    for eFile in listdir(tfIdfDir):
#        print "current", eFile
#        tfFile   =tfDir+eFile
#        tfidfFile=tfIdfDir+eFile
#        Pfile    =Pdir+eFile[:-2]
#        cFile=tfIdfDir+eFile
#        cP=getP(tfFile, tfidfFile)
#        dFile=open(Pfile, 'w')
#        for eK in cP.keys():
#            cLine=eK +" "+ cP[eK]+"\n"
#            dFile.write(cLine)
#        dFile.close()
#    sys.exit()


#        for subnode in nodeList:
#            if subnode.nodeType == subnode.ELEMENT_NODE:
#                obtainRefCorpus(subnode.childNodes)
#            elif subnode.nodeType == subnode.TEXT_NODE:
#                if subnode.parentNode.nodeName== "head":
#                    headID=subnode.parentNode.parentNode.getAttribute('n')
#                    if headID.split('-')[0]=="pa":
#                        PAid=headID[headID.find("-")+1:]
#                        refCorpus[PAid]=[subnode.data,[]]
#
#                if subnode.parentNode.nodeName== "s":
#                    headID=subnode.parentNode.parentNode.parentNode.getAttribute('n')
#                    if headID.split('-')[0]=="pa":
#                        PAid=headID[headID.find("-")+1:]
#                        if refCorpus.has_key(PAid):
#                            refCorpus[PAid][1].append(subnode.data)
#                        else:    #En caso de que esta nota no haya tenido "head"
#                            refCorpus[PAid]=[u'',[subnode.data]]


#################### -*- coding: iso-8859-15 -*-

# from xml.dom.ext.reader import Sax2
# from xml.dom import EMPTY_NAMESPACE
# from xml.dom.ext.reader.Sax2 import FromXmlStream        #Para explorar nodo por nodo
# from xml.dom.ext import PrettyPrint                #Escritura del XML contenido
# import sys
# from os import system, path, listdir
# from time import time
# source     =  "pa"
# newspapers = ["express","ft","guardian","independent","mail","mirror","star","sun","telegraph","times"]
#
#
# def ayuda(nombre_programa):            #-h
#    """Ayuda del programa. Parámetros para la ejecución en línea de comando"""
#    #print 'Use: cat config.txt | python klplagiarism.py'+nombre_programa + ' -[h|t|] (si se de más de un parámetro, sólo se considera el primero)' #[-hrsa]'
#
#    print """
#    -h mensaje de ayuda
#    -f     finds where are those notes with (or without) identified fragments (verbatim, rewrite or new
#             example: python meterDOM.py -f < ../../corpus/METER/meter_xml/files
#    -o     finds where are the PA notes
#             example: python meterDOM.py -o < ../../corpus/METER/meter_xml/files
#
#    -l <xml_file>    Lemmatization of all the text in the xml_file
#             example: python meterDOM.py -l xml1.xml
#             lematiser.sh is provided in order to handle multiple files
#    -n     average number of words in PA and newspaper notes
#      <r>     reference corpus (only of the PA notes)
#      <s>     suspicious corpus (only of the newspapers notes)
#        example: python meterDOM.py -n < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    -s      statistical features of the corpus
#      <a>     statistical features (only of the PA notes)
#      <n>     statistical features (only of the newspapers notes)
#             example: python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    -p <ref-corpus-base-directory>     Estimate the probability distributions P for all the documents in the reference corpus
#         Probability distribution are saved in <ref-corpus-base-directory>/P
#
#    -t <n> < <files-list>   Training stage, consider all the PA notes and create n-grams lists
#             example: python meterDOM.py -t 2 file 2 is the ngrams level and file is the list with the files to consider
#         (EN DUDA SI ESTA LINEA DE LA AYUDA ES VERDAD)
#
#    -j <ref-corpus-directory> <n> < <files-list>    Test considering reference n-grams
#             example: #python meterDOM.py -j "../../corpus/METER/meter_xml/ecir/ngrams_2" 2 < ../../corpus/.../ecir/files
#    -k <ref-corpus-base-directory> < <files-list>    Test considering the search space reduction (based on KL-distance)
#                                                and n-grams search
#          example: #python meterDOM.py -k "../../corpus/METER/meter_xml/ecir" 2 < ../../corpus/.../ecir/files
#    """
#
# def find_located(xFiles):
#    """Finds those papernews which are located (verbatim, rewrite or new)"""
#
#    for eXml in xFiles:
#        reader = Sax2.Reader()
#        doc = reader.fromStream(open(eXml))
#        elements = doc.getElementsByTagName('div')
#        for e in elements:
#            n=e.getAttributeNS(EMPTY_NAMESPACE,'n').split("-")
#            cPaper=n[0]
#            if cPaper in newspapers:
#                #print "current paper", cPaper
#                newsKey="-".join([n[1],n[2]])
#                #print "dos", "e", e
#                sentences=e.getElementsByTagName('s')
#
#                segment=sentences[0].getElementsByTagName('seg')
#                if len(segment)==0:
#                    print eXml, cPaper+"-"+newsKey, "\t\t NO"    #No está identificado
#                else:
#                    print eXml, cPaper+"-"+newsKey, "\t\t SI"    #Si está identificado
#        del(reader)
#
# def find_PA(xFiles):
#    """Finds the PA notes in all teh XML files"""
#    for eXml in xFiles:
#        reader = Sax2.Reader()
#        doc = reader.fromStream(open(eXml))
#        elements = doc.getElementsByTagName('div')
#        for e in elements:
#            n=e.getAttribute('n').split("-")
#            cPaper=n[0]
#            if cPaper==source:
#                newsKey="-".join([n[1],n[2]])
#                print eXml, cPaper+"-"+newsKey
#        del(reader)
#
#
# def _cleanW(w):
#    """Quits space lines and strange leading characters. additionally, it splits
#    words and punctuation marks"""
#    punct=['¡','¿','(','"','.',',',':',';',')','!','?',')','"','`',"'"]
#
#    cW=[""]*3
#    if len(w)==0:
#        return cW
#    clean=w
#
#    if clean!="":
#        while 1:
#            if clean=="" or clean[0].isalnum():
#                break
#            cW[0]+=clean[0]
#            clean=clean[1:]
#        while 1:
#            if clean=="" or clean[-1].isalnum():
#                break
#            cW[2]=clean[-1]+cW[2]
#            clean=clean[:-1]
#    cW[1]=clean
#    return cW
#
# def lemmatize(nodeList):
#    """Lemmatise the xml file content"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            lemmatize(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            p = PorterStemmer()
#            output=''
#            word=''
#            line = subnode.data
#
#            for eWord in line.split():
#                cleanWord=_cleanW(eWord)
#                output+=cleanWord[0]
#                output += p.stem(cleanWord[1].lower(), 0,len(cleanWord[1])-1)
#                output+=cleanWord[2]+" "
#
#            subnode.data= output[:-1]
#
# def _refrescaGwords(w):
#    """Para cada una de las palabras en w refresca los valores del diccionario de tokens"""
#    for eW in w:
#        if globalWords.has_key(eW):        globalWords[eW]+=1
#        else:                    globalWords[eW]=1.0
#
# def statGlobal(nodeList):
#    """Counts the number of tokens and types for the entire document"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statGlobal(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName in ["head","s","seg"]:
#                _refrescaGwords(subnode.data.split())
#
# def statPA(nodeList):
#    """Counts the number of tokens and types for the PA notes"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statPA(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                if subnode.parentNode.parentNode.getAttribute('n').split('-')[0]=="pa":
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "s":
#                if subnode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0]=="pa":
#                    _refrescaGwords(subnode.data.split())
#
# def statNP(nodeList):
#    """Counts the number of tokens and types for the newspaper notes"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            statNP(subnode.childNodes)
#
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                #Si este titulo es de alguno de los periodicos
#                if subnode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "s":
#                if subnode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    _refrescaGwords(subnode.data.split())
#
#            if subnode.parentNode.nodeName== "seg":
#                if subnode.parentNode.parentNode.parentNode.parentNode.getAttribute('n').split('-')[0] in newspapers:
#                    #print "contando seg con padre ",subnode.parentNode.parentNode.parentNode.parentNode.getAttribute
#                    _refrescaGwords(subnode.data.split())
#
# def obtainRefCorpus(nodeList):
#    """Obtain reference corpus"""
#    for subnode in nodeList:
#        if subnode.nodeType == subnode.ELEMENT_NODE:
#            obtainRefCorpus(subnode.childNodes)
#        elif subnode.nodeType == subnode.TEXT_NODE:
#            if subnode.parentNode.nodeName== "head":
#                headID=subnode.parentNode.parentNode.getAttribute('n')
#                if headID.split('-')[0]=="pa":
#                    PAid=headID[headID.find("-")+1:]
#                    refCorpus[PAid]=[subnode.data,[]]
#
#            if subnode.parentNode.nodeName== "s":
#                headID=subnode.parentNode.parentNode.parentNode.getAttribute('n')
#                if headID.split('-')[0]=="pa":
#                    PAid=headID[headID.find("-")+1:]
#                    if refCorpus.has_key(PAid):
#                        refCorpus[PAid][1].append(subnode.data)
#                    else:    #En caso de que esta nota no haya tenido "head"
#                        refCorpus[PAid]=[u'',[subnode.data]]
#
# def trNgram(reference, d, grade):
#    """Receives the reference corpus and creates the n-grams dictionary
#    reference -> dictionary with the sentences of the notes
#    d         -> directory containing the reference corpus
#    grade     -> n-gram level"""
#    from trainNgram import trNgram
#    ngramsDir=d+"/ngrams_"+str(grade)+"/"
#    if not path.isdir(ngramsDir):
#        system("mkdir "+ngramsDir)
#    train=trNgram()
#
#    for keyNote in reference.keys():
#        sentences=[]
#        if reference[keyNote][0]!="":
#            sentences.append(reference[keyNote][0])
#
#        sentences.extend(reference[keyNote][1])
#        print keyNote
#        grams=train.getNgram(sentences, grade)
#        kk=grams.keys()
#        kk.sort()
#        oFile=open(ngramsDir+keyNote+"-"+str(grade),'w')
#
#        for k in kk:
#            cn=k+" "+str(grams[k])+" \n"
#            oFile.write(cn)
#        oFile.close()
#    del(train)
#
#
# def getP(tfF, tfidfF):
#    """Obtains the probability distributions P of all the reference documents
#       tfF     -> tf file
#       tfidfF  -> tfidf file
#       preP         <- P distribution probabilities for all the PA notes"""
#    #Obtaining 20 % of the vocabulary in base to tfidf
#    cFile=open(tfidfF, 'r')
#    termsInFile=cFile.readlines()
#    cFile.close()
#    selectedTerms=[]
#    for i in range (0, int(len(termsInFile)*.20)+1):
#        newT=termsInFile[i].split()[0].lower()
#        selectedTerms.append(newT)
#    #Obtaining the vocabulary with the associated tf
#    cFile=open(tfF, 'r')
#    tfTerms={}
#    for eLine in cFile.readlines():
#        cc=eLine.split()
#        cW=cc[0]
#        cTF=cc[1]
#        tfTerms[cW.lower()]=cTF
#    cFile.close()
#    #Obtaining tf values for the selected terms
#    preP={}
#    for eT in selectedTerms:
#        k=eT.lower()
#        preP[k]=tfTerms[k]
#    return preP
#
#
# def obtainSusCorpus(xFile):
#    """Obtains the suspicious corpus (only those that are identified) from the xml file
#    xFile -> the name of the xml file
#    Refreashes the global var. susCorpus (dict)
#    """
#    reader = Sax2.Reader()
#    doc = reader.fromStream(open(xFile))
#    elements = doc.getElementsByTagName('div')
#
#    for e in elements:
#        newsKey=e.getAttributeNS(EMPTY_NAMESPACE,'n')
#        cPaper=newsKey[:newsKey.find("-")]
#        if cPaper in newspapers:
#            header=e.getElementsByTagName('head')[0]    #Esto devuelve una lista aunque sólo se quiera usar uno
#            noteHeader= header.firstChild.data
#            suspiciousNote=[]
#            sentences=e.getElementsByTagName('s')
#            allSentences={}
#
#            for eSent in sentences:
#                sentence_n=eSent.getAttribute('n')
#                segments=eSent.getElementsByTagName('seg')
#                if len(segments)!=0:
#                    cSent=""
#                    verb_rewLen=0.0        #Número de palabras en verbatim o rewrite
#                    totalLen=0.0        #Número total de palabras
#                    for eSeg in segments:     #Si se determina que hay que cambiar el formato de las sentencias, aqui
#                        #if eSeg.firstChild.data:    #Necesario si el corpus tiene <segs> vacios
#                        try:
#                            ana=eSeg.getAttribute('ana')
#                            strSegment=eSeg.firstChild.data
#                            cLen=len(strSegment.split())
#                            totalLen+=cLen
#                            if ana[0]=="v" or ana[0]=="r":
#                                verb_rewLen+=cLen
#                            cSent+=strSegment+" "
#                        except: pass
#                    if verb_rewLen>= 0.4*totalLen:
#                        #allSentences[sentence_n]=cSent[:-1]
#                        allSentences[sentence_n]=[1,cSent[:-1]]
#                    else:
#                        allSentences[sentence_n]=[0,cSent[:-1]]
#            if allSentences:
#                flagIsIdentified=0
#                if noteHeader=="NO TITLE":
#                    susCorpus[newsKey]=["", allSentences]
#                else:
#                    susCorpus[newsKey]=[noteHeader, allSentences]
#    del(reader)
#
# def locatePlag(ref_dir, ng):
#    """Look for the plagiarised sentences candidates
#       ref_dir ->  directory containing the reference corpus (n-grams)
#       ng      ->  n-grams level"""
#    from trainNgram import clNgram
#
#    clasif=clNgram()
#    for eKey in susCorpus.keys():
#        Weights=clasif.calcProbs(eKey, ref_dir, susCorpus[eKey], int(ng))
#        clasif.findCandidates(Weights)
#    del(clasif)
#
# def _refreshDict(cDict, newStr):
#    """If cDict already has the key newStr, add 1, otherwise cDict[newStr]=1.0
#       cDict  -> dictionary
#       newStr -> current word
#    """
#    if cDict.has_key(newStr): cDict[newStr]+=1
#    else:              cDict[newStr]=1.0
#
# def getQprime(S):
#    """Estimates Q'(S) based on tf and the vocabulary of S (consider that n=1 always)
#       S       -> list containing note title (S[0]) and a dictionary of sentences
#       splDict <- Q'(S)"""
#    noteTitle=S[0].split()
#    sDict=S[1]
#    splDict={}
#    dS=""
#    globalFreq=0.0
#    for eW in noteTitle:
#        clWord=_cleanW(eW)
#        if clWord[0]:
#            _refreshDict(splDict, clWord[0].lower())
#            globalFreq+=1
#        if clWord[1]:
#            _refreshDict(splDict, clWord[1].lower())
#            globalFreq+=1
#        if clWord[2]:
#            _refreshDict(splDict, clWord[2].lower())
#            globalFreq+=1
#
#    for dKey in sDict.keys():
#        isPlag=sDict[dKey][0]
#        cLine=sDict[dKey][1]
#        for eW in cLine.split():
#            clWord=_cleanW(eW)
#            if clWord[0]:
#                _refreshDict(splDict, clWord[0].lower())
#                globalFreq+=1
#            if clWord[1]:
#                _refreshDict(splDict, clWord[1].lower())
#                globalFreq+=1
#            if clWord[2]:
#                _refreshDict(splDict, clWord[2].lower())
#                globalFreq+=1
#    for eW in splDict.keys():
#        splDict[eW]=splDict[eW]/globalFreq
#    return splDict
#
# def getPfromFile(pFile):
#    """Obtain the prob. distribution P from file pFile
#       pFile <- File with the estimated P
#       cP    -> dictionary with P"""
#    cP={}
#    sFile=open(pFile, 'r')
#    for eLine in sFile.readlines():
#        cL=eLine.split()
#        cT=cL[0]
#        #print cL[1]
#        cW=float(cL[1])
#        cP[cT]=float(cW)
#    sFile.close()
#    return cP
#
# def getReducedRefCorpus(Pdict, Qp):
#    """Given the reference corpus with P(c_j) (previously obtained with -p) and probability distribution Q'(S), obtain
#    the minimised reference corpus
#    Pdict -> Dictionary with all the P prob. distributions calculated
#    Qp   -> Q'(S)
#    rRef <- List with the 10 documents with min KL(P||Q) including the distance [[KL, refId],..]"""
#    from probEstimator import probDensities
#    #print Qp, rDir
#    p=probDensities()
#    distances=[]
#    for pK in Pdict.keys():
#        Q=p.getQ(Pdict[pK], Qp)
#        cDist=p.KLdist(Pdict[pK], Q)
#        new=[cDist, pK]
#        distances.append(new)
#    distances.sort()
#    del(p)
#    return distances[:10]
#
# def locateReducedPlag(refDir, susDoc, refDocs, ng, susKey):
#    """Look for the plagiarised sentences candidates
#       ref_dir ->  directory containing the reference corpus (n-grams)
#       susDoc  -> The current suspicious document
#       refDocs -> the reference corpus docs that conform the reduced searh space
#       ng      ->  n-grams level
#       susKey  -> Suspicious note id"""
#    from trainNgram import clNgram
#
#    rDir=refDir+"/ngrams_"+str(ng)+"/"
#    clasif=clNgram()
#    Weights=clasif.reducedCalcProbs(rDir, refDocs, susDoc, susKey, ng)
#    clasif.findCandidates(Weights)
#    del(clasif)
#
##################
##              #
##     main    #
##              #
##################
#
# import sys
##The directory where the work will be done
# workingDir="/home/lbarron/plagio/programs/ecir"
#
#
# parametros = sys.argv
# if len(sys.argv) > 1:
#    opciones = sys.argv[1]
# else:
#    ayuda(sys.argv[0])
#    sys.exit()
#
# if ('h' in opciones):                #Ayuda
#    ##python meterDOM.py -h
#    ayuda(sys.argv[0])
#    sys.exit()
#
# if ('f' in opciones):                #Find the located paper news
#    #python meterDOM.py -f < ../../corpus/METER/meter_xml/files
#    search=sys.argv[1]
#    fin = sys.stdin
#    xmlFiles=[x[:-1] for x in fin.readlines()]
#    find_located(xmlFiles)
#    sys.exit()
#
# if ('o' in opciones):                #Find where are the PA notes
#    #python meterDOM.py -o < ../../corpus/METER/meter_xml/files
#    #search=sys.argv[1]
#    fin = sys.stdin
#    xmlFiles=[x[:-1] for x in fin.readlines()]
#    find_PA(xmlFiles)
#    sys.exit()
#
# if ('l' in opciones):                #Lemmatise the document *.xml
#    #python meterDOM.py -l /home/lbarron/plagio/corpus/METER/meter_xml/meter07_01_2000.xml
#
#    from porter import PorterStemmer
#    xmlFile=sys.argv[2]
#
#    doc=FromXmlStream(xmlFile)
#        lemmatize(doc.childNodes)
#
#    PrettyPrint(doc)
#    sys.exit()
#
# if ('n' in opciones):                #Number of words
#    #python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    #globalWords={}
#    #filesList=sys.stdin
#    n=1
#    filesList=sys.stdin#argv[2]
#
#    lista=filesList.readlines()
#    directory=lista[0][:lista[0].rindex("/")]
#    #for xmlFile in lista[0:1]:
#    if ('r' in opciones):        #Reference corpus
#        refCorpus={}
#        #for xmlFile in lista[0:1]:
#        for xmlFile in lista:
#            print xmlFile.strip()
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#            obtainRefCorpus(doc.childNodes)
#        nGlobal=0.0
#        i=0.0
#        for eKey in refCorpus:
#            words=[]
#            title= refCorpus[eKey][0]
#            if title!="":
#                for eWord in title.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            for eLine in refCorpus[eKey][1]:
#                for eWord in eLine.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            print eKey, #len(words)
#            nGlobal+=len(words)
#            i+=1
#
#    if ('s' in opciones):        #Suspicious corpus
#        susCorpus={}
#        #for xmlFile in lista[0:2]:
#        for xmlFile in lista:
#            print xmlFile.strip()
#            xmlFile=xmlFile[:-1]
#            #doc=FromXmlStream(xmlFile)
#            obtainSusCorpus(xmlFile)#    obtainRefCorpus(doc.childNodes)
#        nGlobal=0.0
#        i=0.0
#        for eKey in susCorpus:
#            #print eKey, susCorpus
#            print
#            words=[]
#            title= susCorpus[eKey][0]
#            if title!="":
#                for eWord in title.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            for eK in susCorpus[eKey][1].keys():
#                #print susCorpus[eKey][1][eK]
#                eLine=susCorpus[eKey][1][eK][1]
#                for eWord in eLine.split():
#                    cleanWord=_cleanW(eWord)
#                    if cleanWord[0]: words.append(cleanWord[0])
#                    if cleanWord[1]: words.append(cleanWord[1])
#                    if cleanWord[2]: words.append(cleanWord[2])
#            print eKey, #len(words)
#            nGlobal+=len(words)
#            i+=1
#    print
#    print nGlobal/i        #print
#    sys.exit()
#
# if ('s' in opciones):                #Statistical features of the corpus
#    #python meterDOM.py -s < /home/lbarron/plagio/corpus/METER/meter_xml/files
#    globalWords={}
#    filesList=sys.stdin
#
#    if   ('a' in opciones):
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statPA(doc.childNodes)
#    elif ('n' in opciones):
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statNP(doc.childNodes)
#    else:
#        for xmlFile in filesList.readlines():
#            xmlFile=xmlFile[:-1]
#            doc=FromXmlStream(xmlFile)
#                statGlobal(doc.childNodes)
#    nTypes=0
#    nTokens=0
#    for eK in globalWords.keys():
#        nTypes+=1
#        nTokens+=globalWords[eK]
#    print "|Tokens| = ", nTokens
#    print "|Types|  = ", nTypes
#    sys.exit()
#
# if ('t' in opciones):                #Get the n-grams from the reference corpus
#    #python meterDOM.py -t 2 < /home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#    #python meterDOM.py -t 3 < /home/lbarron/plagio/corpus/METER/meter_xml/ecir/lemma/files
#    n=int(sys.argv[2])
#
#    filesList=sys.stdin#argv[2]
#    refCorpus={}
#    lista=filesList.readlines()
#    directory=lista[0][:lista[0].rindex("/")]
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        print xmlFile.strip()
#        xmlFile=xmlFile[:-1]
#        doc=FromXmlStream(xmlFile)
#            obtainRefCorpus(doc.childNodes)
#    trNgram(refCorpus, directory, n)
#    sys.exit()
#
# if ('j' in opciones):                #Look for plagiarised sentences based only on n-grams
#    #python meterDOM.py -j "/home/lbarron/plagio/corpus/METER/meter_xml/ecir/ngrams_2" <
#    #/home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#
#    refCorpus_dir=sys.argv[2]
#    n=sys.argv[3]
#    filesList=sys.stdin
#    susCorpus={}
#    lista=filesList.readlines()
#
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        #print xmlFile.strip()
#        xmlFile=xmlFile[:-1]
#        doc=FromXmlStream(xmlFile)
#        obtainSusCorpus(xmlFile)
#    #for eKey in susCorpus.keys():
#        #print eKey, susCorpus[eKey]
#    locatePlag(refCorpus_dir, n)        #susCorpus ya es global, así que no vale la pena enviarla como parámetro
#
#    sys.exit()
#
# if ('k' in opciones):                #Looking for plagiarised fragments over the reduced search space
#    #python meterDOM.py -k "/home/lbarron/plagio/corpus/METER/meter_xml/ecir/ngrams_2" 2 <
#    #/home/lbarron/plagio/corpus/METER/meter_xml/ecir/files
#    ##Técnica de LC+KL-Distance
#
#    refCorpus_dir=sys.argv[2]
#    n=int(sys.argv[3])
#    filesList=sys.stdin
#    susCorpus={}
#    lista=filesList.readlines()
#
#    #for xmlFile in lista[0:2]:
#    for xmlFile in lista:
#        #print xmlFile.strip()
#        xmlFile=xmlFile.strip()
#        doc=FromXmlStream(xmlFile)
#        obtainSusCorpus(xmlFile)
#    Qprime={}
#    refDocs={}
#
#    #Obtaining P
#    Pdir=refCorpus_dir+"/P/"
#    pFiles=listdir(Pdir)
#    P={}
#    for eFile in pFiles:
#        P[eFile]=getPfromFile(Pdir+eFile)
#    totLen=0.0
#
#    for eKey in susCorpus.keys():
#        iniTime=time()
#
#        Qprime[eKey]=getQprime(susCorpus[eKey])
#        refDocs[eKey]=getReducedRefCorpus(P, Qprime[eKey])
#        finTime=time()
#
#        locateReducedPlag(refCorpus_dir, susCorpus[eKey], refDocs[eKey], n, eKey)        #susCorpus y es global
#        print "XXXXX", finTime-iniTime
#    sys.exit()
#
#
# if ('p' in opciones):                #Estimation of distribution probability P
#    #python meterDOM.py -p "/home/lbarron/plagio/corpus/METER/meter_xml/ecir"
#    refCorpus_dir=sys.argv[2]
#    tfDir   =refCorpus_dir.rstrip("/")+"/tf_1/"
#    tfIdfDir=refCorpus_dir.rstrip("/")+"/"+"tfidf_1/"
#    Pdir    =refCorpus_dir.rstrip("/")+"/P/"
#    if not path.isdir(Pdir):
#        system("mkdir "+Pdir)
#    terms={}
#    for eFile in listdir(tfIdfDir):
#        print "current", eFile
#        tfFile   =tfDir+eFile
#        tfidfFile=tfIdfDir+eFile
#        Pfile    =Pdir+eFile[:-2]
#        cFile=tfIdfDir+eFile
#        cP=getP(tfFile, tfidfFile)
#        dFile=open(Pfile, 'w')
#        for eK in cP.keys():
#            cLine=eK +" "+ cP[eK]+"\n"
#            dFile.write(cLine)
#        dFile.close()
#    sys.exit()


'''
Created on 11 Dec 2011

@author: lbarron
'''


class meter_pa_doc(object):
    '''
    Meter PA doc
    '''
    super_id = ""  # ID for the overall note (including pa and newspaper)
    super_name = ""  # Name for the overall note (including pa and newspaper)
    pa_id = ""  # unique id
    pa_n = ""  # identifier 'pa-date-n'
    pa_type = ""  # type [courts | showbiz]
    pa_ana = ""  # src
    pa_title = ""  # note title
    pa_sentences = []  # note text

    def __init__(self, super_id, super_name, pa_id, pa_n, pa_type, pa_ana, pa_title, pa_text):
        '''
        Constructor
        '''
        self.super_id = super_id
        self.super_name = super_name
        self.pa_id = pa_id
        self.pa_n = pa_n
        self.pa_type = pa_type
        self.pa_ana = pa_ana
        self.pa_title = pa_title
        self.pa_sentences = pa_text


class meter_newspaper_doc(object):
    '''
    Meter newspaper doc
    '''
    super_id = ""  # ID for the overall note (including pa and newspaper)
    super_name = ""  # Name for the overall note (including pa and newspaper)
    np_id = ""  # unique id
    np_n = ""  # identifier 'pa-date-n'
    np_type = ""  # type [courts | showbizz]
    np_ana = ""  # src
    np_title = ""  # note title
    np_sentences = []  # note text

    def __init__(self, super_id, super_name, np_id, np_n, np_type, np_ana, np_title, np_text):
        '''
        Constructor
        '''
        self.super_id = super_id
        self.super_name = super_name
        self.np_id = np_id
        self.np_n = np_n
        self.np_type = np_type
        self.np_ana = np_ana
        self.np_title = np_title
        self.np_sentences = np_text