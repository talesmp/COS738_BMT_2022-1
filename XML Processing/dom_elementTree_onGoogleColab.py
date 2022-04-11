# Abordagem DOM ElementTree (usando o Google Colab)

# Código para poder carregar o assistente de uso do Google Drive pessoal no Colab
from google.colab import drive

# Montar e autorizar o uso do Google Drive pessoal (talesmac@gmail.com)
drive.mount('/content/drive')

# Linha de código para listar todos os arquivos do seu Google Drive pessoal
#!ls "/content/drive/My Drive"

# Guardando a localização do arquivo 'cf79.xml' 
cf79_path = '/content/drive/MyDrive/Colab Notebooks/CysticFibrosis2/data/cf79.xml'

# Importando o Element Tree
import xml.etree.ElementTree as ET

# Definindo uma função simples pra indentar (ElementTree não faz isso muito bem)
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Lendo o arquivo original 'cf79.xml'
dom = ET.parse(cf79_path)

# Criando a estrutura do novo arquivo 'autores.xml'
root = ET.Element('FILE')
author = ET.SubElement(root, 'AUTHORS')

# Buscando todos os autores em 'cf79.xml'
authors = dom.findall('RECORD/AUTHORS/AUTHOR')

# Iterando para gravar os autores (apenas 1 por linha, sem repetição)
# Sem verificação de duplicidade, 752 linhas; com verificação, 586 linhas
a_temp = []
for a in authors:
  if a.text not in a_temp:    # verificação de duplicidade
    a_temp.append(a.text)
    ET.SubElement(author, 'AUTHOR').text = a.text

# Indentando a partir da raiz para melhorar a formatação
indent(root)

# Criando o arquivo 'autores.xml' com os mesmos parâmetros do arquivo original
with open('autores.xml', 'wb') as f:
  f.write('<?xml version="1.0"?><!DOCTYPE FILE SYSTEM "cfc-2.dtd">'.encode('utf8'))
  ET.ElementTree(root).write(f, 'utf-8')
