# Abordagem DOM (usando o Google Colab)

# Código para poder carregar o assistente de uso do Google Drive pessoal no Colab
from google.colab import drive

# Montar e autorizar o uso do Google Drive pessoal (talesmac@gmail.com)
drive.mount('/content/drive')

# Linha de código para listar todos os arquivos do seu Google Drive pessoal
#!ls "/content/drive/My Drive"

# Guardando a localização do arquivo 'cf79.xml' 
cf79_path = '/content/drive/MyDrive/Colab Notebooks/CysticFibrosis2/data/cf79.xml'

# Importando o MiniDOM
import xml.dom.minidom as MDOM

# Lendo o arquivo original 'cf79.xml'
dtree = MDOM.parse(cf79_path)

# Buscando todos os títulos em 'cf79.xml'
titles = dtree.getElementsByTagName('TITLE')

# Criando a estrutura do novo arquivo 'titulo.xml'
tituloXml = MDOM.getDOMImplementation()
titulo = tituloXml.createDocument(None, 'FILE', None)
rootElement = titulo.documentElement
titlesElement = titulo.createElement('TITLES')
rootElement.appendChild(titlesElement)


# Iterando para gravar os títulos (apenas 1 por linha, sem repetição)
# Sem verificação de duplicidade, 259 linhas; com verificação, 257 linhas
t_temp = []
t_temp_dupl = []
i=0
for t in titles:
  if t.firstChild.data not in t_temp:   # verificação de duplicidade
    t_temp.append(t.firstChild.data)
    titleElement = titulo.createElement('TITLE')
    titleElement.appendChild(titulo.createTextNode(t.firstChild.data))
    titlesElement.appendChild(titleElement)
    rootElement.appendChild(titlesElement)
#    i=i+1                               # infos da verificação de duplicidade
#  else:
#    t_temp_dupl.append(t.firstChild.data)
#print(i)
#print(t_temp_dupl)
# 'Dying children need help too.' aparece 2x, sendo ambas dos mesmos autores, Chapman-J-A e Goodall-J.
# Já 'Alkaline phosphatase induction in cystic fibrosis fibroblasts [letter].' aparece uma vez com Hahnel-R e Hosli-P, e outra com Carey-W-F e Pollard-A-C

# Criando o arquivo 'titulo.xml'
with open('titulo.xml', 'w') as f:
  f.write(titulo.toprettyxml())