import json
from collections import OrderedDict

f = open("test.json",'w')

def make_sample_json():
    file_data = OrderedDict()
    file_data["content_id"] = 1
    file_data["created_date"]='2023-03-13'
    file_data["modified_date"]='2023-03-13'
    file_data["content_image_url"]="https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
    file_data["content_name"]="Toy Story"
    file_data["content_category"]= 3
    file_data["grade"] = "What"
    file_data["likelist"] = 10
    file_data["runnig_time"] = "2:12"
    file_data["year"] = "1995"
    
    
    return json.dumps(file_data, ensure_ascii=False, indent='\t')

f.write(make_sample_json())
f.close()
