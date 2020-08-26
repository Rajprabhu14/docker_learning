import csv
import json
import os
import sys
import time
import urllib.request

import requests
from bs4 import BeautifulSoup as BS


class scrap:
    url = ''
    # def pageNumber(url):
    #     # req = requests.get(url)
    #     req = urllib.request.urlopen(url)
    #     # 'https://www.remax.ca/find-agent-or-office/agent/#type=agents&minBathroomNumber=&minBedroomNumber=&minYearBuild=&maxYearBuild=&maxPrice=&minPrice=&minFee=&maxFee=&maxLotSize=&minLotSize=&minSquareFeet=&maxSquareFeet=&minTransitScore=&maxTransitScore=&parkingSize=&minWalkScore=&maxWalkScore=&showTypeIds=&propertyTypeIds=&additionalKeywords=&neighbourhood=&mode=agents&neighbourhoodId=&topQuery=&queryType=agent&isCommercial=false&language=1&refreshPins=true&officetab.index=1&mainlist.page=1'
    #     soup1 = BS(req, "html5lib")
    #     page_numbers = soup1.find_all('span',class_ ='paging-link-wrap')
    #
    #     check_pageNumber = 0
    #     for page_number in page_numbers:
    #         try:
    #             pageNumber = int(page_number.text)
    #             if check_pageNumber <= pageNumber:
    #                 check_pageNumber = pageNumber
    #         except:
    #             print('special character on pager')
    #     return check_pageNumber

    def json_convert(response):
        try:
            response_json = json.loads(response.decode('utf-8-sig'))
        except:
            response_json = json.load(response.decode('utf-8'))
        return response_json

    def url_loader(ApiUrl, pagenumber):
        QueryFormatString = ApiUrl
        response = urllib.request.urlopen(
            QueryFormatString.format(pagenumber)).read()
        return response

    def value_get(response):
        i = {}
       # print(response)
        try:
            i['title'] = response['title']

            if 'bedrooms' not in response:  # check bed parameter on json
                i['no_of_beds'] = ''
                #print('bed not there')
            else:
                i['no_of_beds'] = response['bedrooms']
            if 'baths' not in response:  # check bath parameter on json
                i['baths'] = ''
               # print('baths not there')
            else:
                i['baths'] = response['baths']
            if response['address'] is None:
                response['address'] = ''
            i['address'] = response['address'] + ', ' + response['city'] + \
                ', ' + response['province']  # address merging
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
            print('errors')
            print(response)
            pass  # pass if issue found on record


print('Demo')
file_path = os.environ.get('LOCAL_DATA_LOCATION')
if file_path is None:
    file_path = os.getcwd()
print(file_path)
print(os.environ.get('LOCAL_DATA_LOCATION'))
flag = True  # flag for writing Header
sl_no = 0
checking = 0  # page number checking
fieldnames = ['sl_no',
              'reference_id', 'user_id',
              'title', 'address', 'no_of_beds', 'baths', 'price', 'availability', 'rented', 'type', 'square_feet',
              'phone', 'latitude', 'longitude']
page_number = 0
length_page = 1
loop_run = True  # end loop of Location
location = {}

# URL of location needs to be scrapped
location[
    'edmonton'] = 'https://www.rentfaster.ca/api/search.json?keywords=&proximity_type=location-proximity&cur_page={0}&beds=&type=&price_range_adv%5Bfrom%5D=null&price_range_adv%5Bto%5D=null&novacancy=0&city_id=2'
# https://www.rentfaster.ca/ab/edmonton/
location['calgary'] = 'https://www.rentfaster.ca/api/search.json?keywords=&cur_page={0}&price_range_adv[from]=&price_range_adv[to]=&beds=&type=&city_id=1&proximity_type=location-city&novacancy=0'
# https://www.rentfaster.ca/ab/calgary/
location['airdrie'] = 'https://www.rentfaster.ca/api/search.json?keywords=&cur_page={0}&price_range_adv[from]=&price_range_adv[to]=&beds=&type=&city_id=8&proximity_type=location-city&novacancy=0'
# https://www.rentfaster.ca/ab/airdrie/
locations = [
    'airdrie',
    #  'edmonton',
    #  'calgary'
]

for location_name in locations:
    flag = True
    flag_without_id = True
    sl_no = 0
    checking = 0
    page_number = 0
    loop_run = True
    length_page = 1
    print(location_name)
    file_location = os.path.join(
        file_path, (location_name + '_with_id.csv'))
    print(file_location)
    while loop_run:
        # load json data for page for particular URL
        url = scrap.url_loader(location[location_name], page_number)
        responses = scrap.json_convert(url)
        # print("page_number:" + str(page_number)) # value scrapped page print
        page_number += 1  # prepare for next page
        length_page += 1
        if len(responses['listings']) == 0:  # termination of page check
            checking += 1
            if checking == 5:  # terminate Loop if Last 5 page have zero listing
                #     loop_run = False
                #     f = pd.read_csv(location_name + '_with_id.csv')
                #     d = f.drop(["reference_id", "user_id"], axis=1)
                #     d.to_csv(location_name + '_without_id.csv', index=False)
                break
        for listing in responses['listings']:  # json value looping
            value = scrap.value_get(listing)
            if (value is not None):
                sl_no += 1
                # print(sl_no)
                value['sl_no'] = sl_no
                # fieldnames = ['sl_no',
                #               'reference_id', 'user_id',
                #               'title','address','no_of_beds','baths','price', 'availability', 'rented', 'type','square_feet','phone','latitude', 'longitude']
                try:

                    with open(file_location, 'a', newline='',  encoding='utf8') as csvfile:

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        if flag:  # header writing
                            writer.writeheader()
                            flag = False
                        writer.writerow(value)
                except:  # print error page number
                    print('errors')
                    print("page_number:" + str(page_number))
                    print(value)
