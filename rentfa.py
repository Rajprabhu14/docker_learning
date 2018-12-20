import csv
from bs4 import BeautifulSoup as BS
import html5lib
import requests
import time
import urllib.request
import json
class scrap:
    url = ''
    def pageNumber(url):
        # req = requests.get(url)
        req = urllib.request.urlopen(url)
        # 'https://www.remax.ca/find-agent-or-office/agent/#type=agents&minBathroomNumber=&minBedroomNumber=&minYearBuild=&maxYearBuild=&maxPrice=&minPrice=&minFee=&maxFee=&maxLotSize=&minLotSize=&minSquareFeet=&maxSquareFeet=&minTransitScore=&maxTransitScore=&parkingSize=&minWalkScore=&maxWalkScore=&showTypeIds=&propertyTypeIds=&additionalKeywords=&neighbourhood=&mode=agents&neighbourhoodId=&topQuery=&queryType=agent&isCommercial=false&language=1&refreshPins=true&officetab.index=1&mainlist.page=1'
        soup1 = BS(req, "html5lib")
        page_numbers = soup1.find_all('span',class_ ='paging-link-wrap')

        check_pageNumber = 0
        for page_number in page_numbers:
            try:
                pageNumber = int(page_number.text)
                if check_pageNumber <= pageNumber:
                    check_pageNumber = pageNumber
            except:
                print('special character on pager')
        return check_pageNumber

    def json_convert(response):
        try:
            response_json = json.loads(response.decode('utf-8-sig'))
        except:
            response_json = json.load(response.decode('utf-8'))
        return response_json
    def url_loader(ApiUrl, pagenumber):
        QueryFormatString = ApiUrl
        response = urllib.request.urlopen(QueryFormatString.format( pagenumber)).read()
        return response
    def value_get(response):
        i = {}
       # print(response)
        try:
            i['title'] = response['title']
            i['address'] = response['address'] +', ' + response['city'] + ', ' + response['province']
            if 'bedrooms' not in response:
                i['no_of_beds'] = ''
                #print('bed not there')
            else:
                i['no_of_beds'] = response['bedrooms']
            if 'baths' not in response:
                i['baths'] = ''
               # print('baths not there')
            else:
                i['baths'] = response['baths']
            i['price'] = response['price']
            i['square_feet'] = response['sq_feet']
            i['phone'] = response['phone']
            i['availability'] = response['availability']
            i['rented'] = response['rented']
            i['type'] = response['type']
            i["latitude"] = response['latitude']
            i["longitude"] = response['longitude']
            i["reference_id"] = response["ref_id"]
            i["user_id"] = response["userId"]
            return i
        except:
            #print(response)
            pass


flag = True
sl_no = 0
checking = 0
#19
#76
#119
page_number =0
length_page = 1
loop_run = True
edmonton = 'https://www.rentfaster.ca/api/search.json?keywords=&proximity_type=location-proximity&cur_page={0}&beds=&type=&price_range_adv%5Bfrom%5D=null&price_range_adv%5Bto%5D=null&novacancy=0&city_id=2'
    #'https://www.rentfaster.ca/api/search.json?beds=&type=&price_range_adv%5Bfrom%5D=null&price_range_adv%5Bto%5D=null&proximity_type=location-city&novacancy=0&city_id=2'
calgary = 'https://www.rentfaster.ca/api/search.json?keywords=&cur_page={0}&price_range_adv[from]=&price_range_adv[to]=&beds=&type=&city_id=1&proximity_type=location-city&novacancy=0'

airdrie = 'https://www.rentfaster.ca/api/search.json?keywords=&cur_page={0}&price_range_adv[from]=&price_range_adv[to]=&beds=&type=&city_id=8&proximity_type=location-city&novacancy=0'

# test = scrap.pageNumber('https://www.rentfaster.ca/ab/calgary/rentals/?keywords=&cur_page=1&proximity_type=location-city&novacancy=0&city_id=1')
while loop_run:

    url = scrap.url_loader(airdrie, page_number)
    responses = scrap.json_convert(url)
    print("page_number:" + str(page_number))
    page_number += 1
    length_page += 1
    if len(responses['listings']) == 0:
        checking += 1
        if checking == 5:
            loop_run = False
            break
    for listing in responses['listings']:
        value = scrap.value_get(listing)
        if (value is not  None):
            sl_no += 1
            #print(sl_no)
            value['sl_no'] = sl_no
            fieldnames = ['sl_no',
                          'reference_id', 'user_id',
                          'title','address','no_of_beds','baths','price', 'availability', 'rented', 'type','square_feet','phone','latitude', 'longitude']
            try:
                with open('airdrie_with_id.csv', 'a', newline='',  encoding='utf8') as csvfile:

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if flag:
                        writer.writeheader()
                        flag = False
                    writer.writerow(value)
            except:
               print("page_number:" + str(page_number))
               print(value)
