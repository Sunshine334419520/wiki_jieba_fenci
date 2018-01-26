xml 转 text: 利用了gensim.corpora 中的 WikiCorpus(需要安装gensim库）
简繁准换: 利用了opencc进行转换（opencc需要安装）
分词: 利用了jieba分词（需要安装jieba库）
词频统计: 利用了jieba库
排序: sort函数  

文件作用->>>

process_siki.py: python脚本文件
zhwiki-latest-pages-articles.xml.bz2: 维基百科xml压缩包
wiki_zh_text: 维基百科经过转码对text繁体文件（结果文件）
wiki.zh.text.jian: 维基百科经过简体text文件（结果文件）
wiki.zh.simp.seg.txt: 维基百科经过jieba分词之后的文件（结果文件）
wiki.zh.count.sort.txt: 分词后的文件经过词频统计以及排序后的文件（结果文件）
