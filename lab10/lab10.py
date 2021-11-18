import re

txt1 = "jox r.nohre@jth.hj.se, bjox@se, adam@example.com, jox@jox@jox.com."
# with look ahead (?<=[\s])[\w._-]+@[\w]+(?:\.\w+)+
reg1 = re.findall(r"\s([\w._-]+@[\w]+(?:\.\w+)+)", txt1)
# print(reg1)

htmltxt =   """ bla bla bla
                <h1> My Rubric </h1>
                bla bla bla. """

reg2 = re.findall(r"<h1>\s*(.*?)\s*</h1>", htmltxt)
# print(reg2)

f = open("tabla.html", encoding="utf-8")
tablatxt = f.read()

tablaReg = re.findall(r'<td class="svtTablaTime">\s*(\d+\.\d+)\s*</td>', tablatxt)
# print(tablaReg)

tablaReg2 = re.findall(
    r'<td class="svtTablaTime">\s*(\d+\.\d+)\s*</td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*</h4>(?:\s.*){0,4}\s*[\w\såäö-]*.\s([\w\såöä]*).\s([\w\såöä]*).\s([\w\såöä]*)'
    , tablatxt)

print(tablaReg2)
for obj in tablaReg2:
    splitEpisode = obj[2].split(' ')
    episode = splitEpisode[1] + "/" + splitEpisode[-1]
    print(f"------------------------------------\nTid: {obj[0]}\nSäsong: {obj[1].split(' ')[-1]}\nAvsnitt: {episode}\nHandling: {obj[3]}")
