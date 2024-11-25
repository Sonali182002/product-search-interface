import requests




# this function call the google search engine api to search product
def search_product(product_name):
    API_KEY='AIzaSyC3c7TetZHtChBytTHLXK39Vzsz5OvK-XU'
    SERACH_ENGINE_ID='01c8fe6215a734dd2'
    url="https://www.googleapis.com/customsearch/v1"
    
    params={
        "key":API_KEY,
        "cx":SERACH_ENGINE_ID,
        "q":product_name,
    }

    response=requests.get(url,params=params)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    if response.status_code == 200:
        data = response.json()
        product_links = []

        for item in data.get("items", []):
            product_links.append({
                "title": item.get("title"),
                "link": item.get("link")
            })

        return product_links
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []
 # this function is for calling the ebay API 

def search_product_on_ebay(product_name):
    EBAY_APP_ID='sonalisi-project-SBX-afe5d9474-4f879381'
    url="https://api.ebay.com/buy/browse/v1/item_summary/search"

    params={
        "OPERATING-NAME": "findItemsByKeywords",
        "SERVICE-VERSION":"1.0.0",
        "SECURTIY-APPNAME":EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT":"JSON",
        "keywords":product_name,
        "paginationInput.enteriesPerPage":8
    }


    response=requests.get(url,params=params)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    if response.status_code==200:
        items=response.json().get("findItemsByKeywordsResponse",[{}])[0].get("searchResult",[{}])[0].get("item",[])


        links=[item["viewItemURL"][0] for item in items if "viewItemURL" in item]
        return links
    else:
        print("Error:",response.status_code,response.text) 
        return[]   


