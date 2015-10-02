
import xml.etree.ElementTree as ET
import json, os


array_data = []


def parse_xml(file):
    """lee el xml y hace append en nuestro arreglo que se escribira como json"""
    tree = ET.parse(file)
    root = tree.getroot()
    for author in root.iter('author'):
        array_data.append(author.attrib)
    for document in root.iter('document'):
        array_data.append({"data":escape_data(document.text) })

def escape_data(data):
    """escapa todas las etiquetas html"""
    escaped_data = ""
    jump = False
    for letter in data:
		if(jump == False):
			if(letter == "<"):
				jump = True
			else:
				escaped_data +=letter
		else:
			if(letter ==">"):
				jump = False
    return escaped_data

def append_files_to_read(path):
    """Crea un arreglo para poder leer cada archivo xml"""
    files_to_read = []
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            for name in files:
                files_to_read.append(os.path.join(root,name)) 
    return files_to_read





def write_json(name):
    """Escribe el archivo json"""
    with open(name, "w") as json_file :
        json.dump(array_data, json_file)
        json_file.close()


def parse(path) :
    """Funcion Principal"""
    files_to_read = append_files_to_read(path)
    for file in files_to_read:
        if file.find('.xml') >= 0:
            parse_xml(file)
    write_json(array_data[0]['type']+"_"+array_data[0]['lang']+".json")
    
			

def json_name():
    """Regresa el nombre del archivo json generado"""
    return array_data[0]['type']+"_"+array_data[0]['lang']+".json"


