import requests
import json

ENDPOINT = "https://www.toyota.com/inventory/search"
REGION = ["500"]
DEALERS = ["32137"]
PAGE_SIZE = 100
YEARS = ["2022"]
SERIES = ["86"]

BODY = {"brand":"TOY","facetfields":[],"fields":[],"group":"false","groupfield":"","groupmode":"full","mode":"content","pagesize":str(PAGE_SIZE),"pagestart":"0","relevancy":"false","sortfield":"MSRP","sortorder":"ASC","show":{"accessory":{"derived":"true","zeroDollar":"false","extraCostColor":"false","exclude":"false"}},"filter":{"year":YEARS,"series":SERIES,"model":[],"grade":[],"enginetransmission":[],"drive":[],"bed":[],"cab":[],"exteriorcolor":[],"interiorcolor":[],"accessory":[],"packages":[],"andfields":["accessory","packages"],"dealers":DEALERS,"region":REGION}}


HEADERS = {}

def get_data(endpoint):
    r = requests.post(endpoint, json=BODY)
    if(r.status_code == 200):
        return r.json()
    else:
        print(r.status_code)


def get_dealer_info(deal_id):
    addr = "https://www.toyota.com/dealers/dealer/{}/"
    new_addr = addr.format(deal_id)
    r = requests.get(new_addr)
    if(r.status_code == 200):
        print(r.text)
    else:
        print(r.status_code)


def read_file(file_name):
    f = open(file_name)
    data = json.load(f)
    f.close()
    return data

def write_vins(raw):
    data = raw['body']['response']
    current = read_vins()
    file1 = open('vins.txt', 'a')
    new = []
    for key in data['docs']:
        if key['vin'] not in current:
            new.append(key['vin'])

    for key in new:
        file1.write(key)
        file1.write('\n')

    file1.close()

def read_vins():
    file1 = open('vins.txt', 'r')
    data = file1.read().split('\n')
    return data



def parse_data(data):
    print('VIN - availability - msrp - trans - dealerId - color')
    resp = data['body']['response']
    count = 1
    pre_vins = read_vins()
    for key in resp['docs']:
        if key['vin'] not in pre_vins:
            print("*{0}. {1} - {2} - {3} - {4} - {5} - {6}".format(count, key['vin'], key['availabilityDate'], key['msrp'], key['model']['transmission'], key['dealerFields']['dealer'], key['exteriorcolor']['title']))
        else:
            print("{0}. {1} - {2} - {3} - {4} - {5} - {6}".format(count, key['vin'], key['availabilityDate'], key['msrp'], key['model']['transmission'], key['dealerFields']['dealer'], key['exteriorcolor']['title']))
        count += 1
    write_vins(data)

    #dealer = get_dealer_info(resp['docs'][0]['dealerFields']['dealer'])
    #print(dealer)

if __name__ == "__main__":
    #data = read_file('out.json')
    data = get_data(ENDPOINT)

    parse_data(data)


