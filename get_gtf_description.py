from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def get_tag_info():
    """function to get the description of gtf tags from Gencode
    """    
    r = requests.get("https://www.gencodegenes.org/pages/tags.html")
    doc = BeautifulSoup(r.text, "html.parser")
    descriptions = doc.find_all("dd")
    terms = doc.find_all("dt")
    with open("gtf_tags.csv", "w") as filewriter:
        for i in range(0, len(terms)):
            term = terms[i].text.strip()
            description = descriptions[i].text.strip().replace("\n","")
            description = " ".join(description.split())
            filewriter.write("{},{}\n".format(term, description))


def get_format_definition():
    """function to get the gtf format description from Gencode
    """
    r = requests.get("https://www.gencodegenes.org/pages/data_format.html")
    doc = BeautifulSoup(r.text, "html.parser")
    tables = doc.find_all("table")
    for table in tables:
        title = table["summary"]
        title = title.replace(" ", "_")
        title = "{}.tsv".format(title)
        with open(title, "w") as filewriter:
            header = table.find("thead")
            column_names = header.find_all("th")
            column_names = [c.text.strip().replace(" ","_") for c in column_names]
            column_names = "\t".join(column_names)
            filewriter.write(column_names)
            table_lines = table.find_all("tr")
            for lines in table_lines:
                cells = lines.find_all("td")
                cells = [c.text.strip().replace("\n", " ") for c in cells]
                if cells and " " in cells[0]:
                    cells[0] = cells[0].split(" ")[0]
                cells = [" ".join(c.split()) for c in cells]
                cells = "\t".join(cells)
                filewriter.write("{}\n".format(cells))


if __name__ == "__main__":
    get_format_definition()
    get_tag_info()
