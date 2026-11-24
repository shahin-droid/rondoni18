#!/usr/bin/env python3
"""Prepara le pagine da pubblicare come artifact (versione ufficiale e di prova) a partire da
gestionale/index.html. Non contiene dati: la versione ufficiale parte vuota e si riempie con
"Importa backup" dal gestionale.

Uso:  python3 gestionale/tools/build_artifact.py <cartella_di_uscita>
Crea <uscita>/ufficiale/index.html e <uscita>/prova/index.html (pdf.js incorporato, immagini in img/).
"""
import os, shutil, sys
G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(G, '..', 'build-artifact')
src = open(os.path.join(G, 'index.html'), encoding='utf-8').read().replace('../img/', 'img/')
avvio = '<script>/* dentro Claude confirm/alert non sono disponibili */window.confirm=()=>true;window.alert=m=>console.log(m);</script>'
vuoto = '{"version":1,"demo":false,"users":[],"clienti":[],"commesse":[],"unita":[],"rate":[],"eventi":[],"fornitori":[],"preventivi":[],"ordini":[],"azienda":{}}'
uff = '<script>/* versione ufficiale: dati nell\'archivio condiviso */window.BTWN_UFFICIALE=true;window.BTWN_PULITO=' + vuoto + ';</script>'
w = open(os.path.join(G, 'lib', 'pdf.worker.min.js'), encoding='utf-8').read().replace('</script', '<\\/script')
l = open(os.path.join(G, 'lib', 'pdf.min.js'), encoding='utf-8').read().replace('</script', '<\\/script')
pdf = '<script>/* pdf.js incorporato */' + w + '</script><script>' + l + '</script>'
for nome, extra in (('ufficiale', avvio + uff), ('prova', avvio)):
    d = os.path.join(OUT, nome); os.makedirs(d, exist_ok=True)
    h = src.replace('<head>', '<head>' + extra, 1)
    h = h.replace('<title>BTWN · Bussola</title>', '<title>BTWN · Bussola – ' + nome + '</title>', 1)
    i = h.rindex('</body>'); h = h[:i] + pdf + h[i:]
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
    img = os.path.join(G, '..', 'img')
    if os.path.isdir(img): shutil.copytree(img, os.path.join(d, 'img'), dirs_exist_ok=True)
    print('pronto:', os.path.join(d, 'index.html'))
