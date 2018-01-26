#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#对维基百科进行分词处理

# @Author: YangGuang
# @Date:   2018-01-20T17:11:27+08:00
# @Email:  guang334419520@126.com
# @Filename: process_wiki.py
# @Last modified by:   sunshine
# @Last modified time: 2018-01-21T11:16:27+08:00



from __future__ import print_function

import logging
import os.path
import six
import sys
import codecs
import jieba
import jieba.analyse
import jieba.posseg as pseg     #引入词性标注接口
import subprocess               # 用于在终端调用调用opencc命令


from gensim.corpora import WikiCorpus   # 对XML 转 Text 需要

def xmlConversionToText(programfilename, infile, outfile):
    """
        作用：将xml文件转换成文本格式
        programfilename: 程序名称
        infile: xml文件
        outfile：text输出文件
    """
    program = os.path.basename(programfilename)
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    space = " "
    i = 0

    output = open(outfile, 'w')
    wiki = WikiCorpus(infile, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        if six.PY3:
            #output.write((b' ').join(text).decode('utf-8') + '\n')
            output.write((b' '.join(t.decode('utf-8') for t in text)) + '\n')
        #   ###another method###
        #   output.write(
        #            space.join(map(lambda x:x.decode("utf-8"), text)) + '\n')
        else:
            output.write(space.join(text).encode("utf8") + "\n")

        i = i + 1
        if (i % 10000 == 0):
            logger.info("Saved " + str(i) + " articles")

    output.close()
    logger.info("Finished Saved " + str(i) + " articles")

def traditionalToSimplified(infile):
    """
        作用：进行简繁转化
        infile:输入文件
        reutrn: 返回输出文件名
    """

    outfile = "wiki.zh.text.jian"

    subprocess.call("opencc -i " + infile + " -o " +
                     outfile + " -c t2s.json",shell = True)

    return outfile


def jiebaParticiple(infile):
    """
        作用：利用jieba对中文就行分词
        infile: 输入文件
        return: 返回存放结果对文件名
    """

    outfile = "wiki.zh.simp.seg.txt"
    f = codecs.open(infile, 'r', encoding='utf8')
    target = codecs.open(outfile, 'w', encoding='utf8')
    print('open files' + infile + '.')

    lineNum = 1
    line = f.readline()
    while line:
        print('---processing ',lineNum,' article---')
        #用jieba进行精准分词
        seg_list = jieba.cut(line,cut_all=False)
        line_seg = ' '.join(seg_list)

        #将分词类容写入文件
        target.writelines(line_seg)
        lineNum = lineNum + 1

        line = f.readline()

    print('well done.')
    f.close()
    target.close()

    return outfile

# @see 读取文件内容
def readFile(filename):
  content = ""
  try:
    fo = codecs.open(filename,'r', "utf-8")
    print ("read file name : ", filename)
    for line in fo.readlines():
      content += line.strip()
    print ("Number of words : ", len(content))
  except IOError as e:
    print ("文件不存在或者文件读取失败")
    return ""
  else:
    fo.close()
    return content



def countParticiple(source_file):
    """
        作用：对分词结果进行排序
        source_file: 源文件
        return: 返回一个字典类型
    """
    print("The word segmentation is being carried out...")
    # 词语数组
    wordList= []
    # 用于统计词频
    wordCount= {}

    # 从分词后的源文件中读取数据
    sourceData = readFile(source_file)

    print(len(sourceData))
    k = input('Pres any key to continue.')
    # 利用空格分割成数组
    wordList = sourceData.split(' ')

    i = 1
    count = 0
    # 遍历数组进行词频统计，这里使用wordCount 对象，出发点是对象下标方便查询
    for item in wordList:
        if(count % 1000 == 0):
            print('---processing ',count,' article---')
        if item not in wordCount:
            wordCount[item] = 1

        else:
            wordCount[item] += 1
        count += 1

    # 循环结束，wordCount 对象将保存所有的词语和词频

    print("The word segmentation is completed.")

    return wordCount


# 定义wordItem 类
class wordItem:
  label = ''
  times = 0
  # 构造函数
  def __init__(self, l, t):
    self.label = l
    self.times = t
  # 用于比较
  def __lt__(self, other):
    return self.times < other.times


def sortWord(wordCount):
    """
        作用：把统计结果进行排序以及把排序结果写到targetfile文件
        wordCount: 统计结果
    """
    print("The statistical results are being sorted.")
    # 定义wordItem 数组用于排序
    wordItemArray= []

    count = 0;

    targetFile = "wiki.zn.count.sort.txt"
    # 构造对象数组
    for key in wordCount:
        if(count % 1000 == 0):
            print('---processing ',count,' article---')
        wordItemArray.append(wordItem(key, wordCount[key]))
        count += 1
    # 按词频由高到低倒序排列
    wordItemArray.sort(reverse = True)


    # 写入目标文件 target
    wf = codecs.open(targetFile,'w', "utf-8")
    for item in wordItemArray:
        if(count % 1000 == 0):
            print('---processing ',count,' article---')
        wf.write(item.label+' '+str(item.times) + '\n')
        count += 1

    print("Order to complete.")



if __name__ == '__main__':
    # 检查程序输入的参数
    if len(sys.argv) != 3:
        print("Using: python process_wiki.py enwiki.xxx.xml.bz2 wiki.en.text")
        sys.exit(1)
    inp, outp = sys.argv[1:3]

    #XML 转换成 Text
    xmlConversionToText(sys.argv[0], inp, outp)

    outp = "wiki.zh.txt"

    #简繁转换
    text_filename = traditionalToSimplified(outp)

    # 分词
    result_filename = jiebaParticiple(text_filename)

    #分词统计以及排序
    result_filename = 'wiki.zh.simp.seg.txt'
    wordCount = countParticiple(result_filename)
    sortWord(wordCount)
