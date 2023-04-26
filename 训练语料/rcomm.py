# 需要安装 pip install bayoo-docx

import docx

document = docx.Document("句式.docx")

p = document.paragraphs[0]

print( [ r.comments for r in p.runs])

iis = [ix for ix, e in enumerate( [len(r.comments) for r in p.runs]) if e !=0]

for i in iis:
    print(p.runs[i-1].text, "<-", p.runs[i].comments[0].text)

