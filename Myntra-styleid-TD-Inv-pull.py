#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium webdriver_manager')


# In[ ]:





# In[51]:


from selenium import webdriver
from lxml import etree
import pandas as pd
import json

def extract_substring(string):
    start_index = string.find('{')
    end_index = string.rfind('}')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        substring = string[start_index:end_index+1]
        return substring
    else:
        return None

def extract_item_data(item, label, script_json):
    size_seller_data = item.get('sizeSellerData', [])
    extracted_data = []
    for seller_data in size_seller_data:
        style_id = item.get('styleId')
        extracted_item = {
            'style_id': style_id,
            'sellerPartnerId': seller_data.get('sellerPartnerId'),
            'availableCount': seller_data.get('availableCount'),
            'sellableInventoryCount': seller_data.get('sellableInventoryCount'),
            'warehouses': seller_data.get('warehouses'),
            'discountedPrice': seller_data.get('discountedPrice'),
            'manufacturerInfo': seller_data.get('manufacturerInfo'),
            'importerInfo': seller_data.get('importerInfo'),
            'packerInfo': seller_data.get('packerInfo'),
            'label': label
        }
        extracted_item['mrp'] = script_json['pdpData']['price']['mrp']
        extracted_item['brand_name'] = script_json['pdpData']['brand']['name']
        extracted_data.append(extracted_item)
    return extracted_data

def extract_data(driver, style_id):
    url = f"https://www.myntra.com/{style_id}"

    # Navigate to the URL
    driver.get(url)

    # Get the page source and parse it using lxml
    response = driver.page_source
    tree = etree.HTML(response)

    # Extract buyers data using XPath
    buyers = tree.xpath('/html/body/script[3]/text()')
    if len(buyers):
        json_string = extract_substring(buyers[0])
        try:
            script_json = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for style ID {style_id}: {e}")
            return []

        extracted_data = []
        for item in script_json['pdpData']['sizes']:
            label = item.get('label')
            extracted_item_data = extract_item_data(item, label, script_json)
            extracted_data.extend(extracted_item_data)
        return extracted_data
    else:
        print(f"No buyers data found for style ID {style_id}")
        return []

def main():
    ndf = pd.read_csv(r"C:\Ajio Assets\Python automation\web scrapping\Myntra web scrapping\Pull_Image.csv")
    style_ids = ndf['Style ID'].to_list()
    #style_ids = ["24109732"]

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    extracted_data = []
    for style_id in style_ids:
        print("Processing ", style_id)
        try:
            out = extract_data(driver, style_id)
            extracted_data.extend(out)
        except Exception as e:
            print(f"Error processing style ID {style_id}: {e}")

    # Close the browser window
    driver.quit()

    df = pd.DataFrame(extracted_data)
    df.to_csv(r'C:\Ajio Assets\Python automation\web scrapping\Myntra web scrapping\extracted_data.csv', index=False)
    print("Data extraction and processing completed.")

if __name__ == "__main__":
    main()


# In[49]:


script_json['pdpData']['brand']['name']

