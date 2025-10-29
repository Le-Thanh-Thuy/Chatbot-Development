import json
from bs4 import BeautifulSoup
import requests

def crawl_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sections = []
    current_section = None
    
    all_elements = soup.find_all(['h2', 'i', 'p', 'ul'])
    
    element_index = 0
    while element_index < len(all_elements):
        element = all_elements[element_index]
        if element.name in ['h2']:
            current_section = {
                "section_title": [element.text.strip()],
                "content": [],
                "subsections": [],
                "items": []
            }
           
            sections.append(current_section)
           
            # Duyệt tiếp các thẻ tiếp theo cho đến khi gặp thẻ h2 mới hoặc hết tài liệu
            next_element_index = element_index + 1
            while next_element_index < len(all_elements) and all_elements[next_element_index].name not in ['h2']:
                next_element = all_elements[next_element_index]
                # Kiếm tra thẻ thuộc phần nào thì đưa vào phần đó với p là content và i là subsection
                if next_element.name == 'p':
                    current_section['content'].append(next_element.text.strip())
                elif next_element.name == 'i' : # Với subsection thì ta lại có thêm các phần tử con là p và ul lưu content và items của subsection
                    # Tạo subsection để lưu dữ liệu đó và add vào phần subsection của section
                    current_subsection = {
                        "subsection_title": [next_element.text.strip()],
                            "content":[],
                            "items": []
                    }
                    current_section['subsections'].append(current_subsection)
                    
                    # Giống với section thì ta duyệt tiếp với subsection cho đến khi gặp thẻ h2 hoặc i hoặc hết tài liệu
                    subsection_next_element_index = next_element_index + 1
                    while subsection_next_element_index < len(all_elements) and all_elements[subsection_next_element_index].name not in ['h2', 'i']:
                        subsection_next_element = all_elements[subsection_next_element_index]
                        # Nếu là thẻ p thì đưa vào content của subsection
                        if subsection_next_element.name == 'p':
                            current_subsection['content'].append(subsection_next_element.text.strip())
                        # Nếu là thẻ ul thì duyệt qua các thẻ li là list item để lấy dữ liệu và lưu vào items của subsection
                        elif subsection_next_element.name == 'ul':
                                for li in subsection_next_element.find_all('li', recursive = False):
                                    current_subsection['items'].append(li.text.strip())
                        subsection_next_element_index += 1

                    next_element_index = subsection_next_element_index -1
                # Làm tương tự với section
                elif next_element.name == 'ul':
                    for li in next_element.find_all('li', recursive = False):
                         current_section['items'].append(li.text.strip())
                next_element_index += 1

            element_index = next_element_index
            
        else:
              element_index +=1
          
    data = {"sections": sections}

    # Xuất ra file JSON
    with open('structured_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Dữ liệu đã được lưu vào structured_data.json")     