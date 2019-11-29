import scrapy
import urllib
import json
from alamo.items import AlamoItem
import datetime
import time
import pdb

class Alamocar(scrapy.Spider):
    name = "alamo_cars"

    def start_requests(self):
        count = 0
        indexDate = datetime.datetime.now()
        # indexDate = indexDate + datetime.timedelta(days = 1)
        fromDate = indexDate
        fromDateStr = indexDate.strftime("%m/%d/%y")
        indexDate = indexDate + datetime.timedelta(days = 1)
        toDate = indexDate
        toDateStr = indexDate.strftime("%m/%d/%y")
        url = "https://www.alamo.com/content/data/apis/live/reservation/start/submit.sfx.json/channelName%3Dalamo/locale%3Den_US.json"
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": """loc=US%7Cen_US%7C%7C; Rental-alamo_com=!AodPtjadAkIyYJ0484WoLKftvzfAoG1v91AT9/0181Rj9kkXVM8QINFVRp54uud4Enwz3Z5V2AD8Zg==; TLTSID=8D7E76F7CCDA9DA31F0A40BF32698CBA; TLTUID=13183FDEBD0CE8DE693E4E3B91BCF3D5; ORIGIN=etc; akacd_www_alamo_com_PC=3740462951~rv=97~id=268ee02d367592469baa57eb7fca399b; Akamai-Edgescape=georegion=247,country_code=US,region_code=CO,city=LITTLETON,dma=751,pmsa=2080,msa=2082,areacode=303,county=ARAPAHOE+JEFFERSON+DOUGLAS,fips=08005+08059+08035,lat=39.5942,long=-105.0086,timezone=MST,zip=80120-80130+80160-80163+80165-80166,continent=NA,throughput=vhigh,bw=5000,asnum=53889; check=true; AMCVS_30545A0C536B768C0A490D44%40AdobeOrg=1; geo=US; AMCV_30545A0C536B768C0A490D44%40AdobeOrg=-330454231%7CMCIDTS%7C18091%7CMCMID%7C12911477000803509030086999346678043528%7CMCAAMLH-1563619949%7C9%7CMCAAMB-1563619949%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1563022349s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; mboxEdgeCluster=28; _sdsat_FUNNEL_START=HOME; _ga=GA1.2.2056695165.1563015152; _gid=GA1.2.744856561.1563015152; _gat_ehiglobal=1; s_cc=true; _gcl_au=1.1.1668666716.1563015153; notice_behavior=none; seerses=e; seerses=e; seerid=78476.87913809033; seerid=78476.87913809033; WRIgnore=true; WRUIDAWS20170419=2342006914991445; ki_r=; _fbp=fb.1.1563015160994.1971356423; _pickUpDate=2019-07-13 12:00:00; _dropOffDate=2019-07-15 12:00:00; JSESSIONID=sdrzpgz8n26z16k0gcedp7uzu; res=1019124%7CSan+Francisco+Union+Square%7C1563044400000%7CAmerica%2FLos_Angeles%7C1019124%7CSan+Francisco+Union+Square%7C1563217200000%7CAmerica%2FLos_Angeles%7CUS%7C%7C%7C25%7C; _resDrop=SFOC78; ly_segs=%7B%22alamo_abandon_cart_onsite_modals%22%3A%22alamo_abandon_cart_onsite_modals%22%2C%22treatment_group%22%3A%22treatment_group%22%2C%22ly_alamo_abandon_cart%22%3A%22ly_alamo_abandon_cart%22%2C%22smt_new%22%3A%22smt_new%22%2C%22all%22%3A%22all%22%2C%22ly_treatment_group_1of2_5050split%22%3A%22ly_treatment_group_1of2_5050split%22%7D; ki_t=1563015157677%3B1563015157677%3B1563015194094%3B1%3B4; mbox=session#c0fe9f3c17ca46b08d5a4582c1661068#1563017055|PC#c0fe9f3c17ca46b08d5a4582c1661068.28_134#1626259952; PathforaPageView=4; __CT_Data=gpv=4&ckp=tld&dm=alamo.com&apv_16618_www03=4&cpv_16618_www03=4&rpv_16618_www03=4; RT="sl=4&ss=1563015143846&tt=23544&obo=0&bcn=%2F%2F173e2514.akstat.io%2F&sh=1563015195495%3D4%3A0%3A23544%2C1563015192739%3D3%3A0%3A21120%2C1563015181852%3D2%3A0%3A18697%2C1563015157708%3D1%3A0%3A13853&dm=alamo.com&si=2becded8-c51e-4690-9fb1-f8efd1456a6b&ld=1563015195495"; _4c_=fVJRa9swEP4rQw99Sm3JtiQrUEaaltHRNauTsEeh2EptZltGUpqF0v%2Fes51kgY69CN2nu%2B%2B7T3dvaF%2FqFk0JZTEmlAhOEjpBv%2FXBoekbyrv%2BfO2Pna3RFJXed24ahvv9PlC1akyQmybUrVwvw1zZa6tbr%2BqwNI0OSt%2FUaIJmfZp8aF1VaOvkwx3QAPyo2xdfSrOV2VAzonNl5bxWDtSH0Ow608q5KfQR2DkP3FY%2B7ZqNtiOYaaftq%2FIVpN4eusvq1tvDqNHLt7mW80UGr%2Btl%2F77I5KM5qNofxoKfVnfqeF8Dp1wdul44015VvZdLpeVu48258cuX1V%2F4UatCrqrm2P7Gmj3kQTAvLfj4wimg%2BWiPiCAOOMRb%2BHUUYcqYoITR4DQcGsGj6c39qtoCmCC0equtPf2Eq3zPdJ4MQF7b5vgfix%2BrTN7ez%2BaLp4tRukZ7W%2BUugDFo29nK6WGom9C5UJcvtdmourOmmJwCVe%2F1ZudCEn5fXkeBCPD1HX9%2BCl1MCMWRiKIkhZa%2Fzp5vb8hVUxU3JBKEJJxjjFMcUyxwDDcmhIgTxniKk5hG6dXs%2Bf6GQKMdbBxK4FKbXNW9I9jRCfo2k%2Bthff79N%2B8T9GfcZAKIoDERYN%2FDJFKWgDLGkGGr4rjSSNHttkgZS5OcRyRimhO%2BJYlWPBYFZxgUBz6OOXRPWRTHQNAB31BPznJgmdIU45McSc5yvZMhO%2FnUXPq5uXE9%2FlPzydD7%2Bwc%3D; s_tps=6; s_pvs=5; s_sess=%20s_ppvl%3D%252Fen_US%252Fcar-rental%252Fhome.html%252C67%252C67%252C1169%252C1249%252C969%252C1920%252C1080%252C1%252CL%3B%20s_ptc%3D0.00%255E%255E0.00%255E%255E0.00%255E%255E0.00%255E%255E0.26%255E%255E0.01%255E%255E1.91%255E%255E0.03%255E%255E2.42%3B%20s_ppv%3D%252Fen_US%252Fcar-rental%252Fhome.html%252C69%252C69%252C1193%252C1249%252C969%252C1920%252C1080%252C1%252CL%3B%20SC_LINKS%3D%252Fen_US%252Fcar-rental%252Fhome.html%255E%255EBook%2520Now%255E%255E%2523%255E%255Ebuttons%255E%255E%3B; s_pers=%20s_dfa%3Dehglobalprod%252Cehglobalalwebus%7C1563016994276%3B%20s_vs%3D1%7C1563017000527%3B%20gpv_v5%3D%252Fen_US%252Fcar-rental%252Fhome.html%7C1563017000543%3B%20s_visit%3D1%7C1563017000548%3B; s_sq=ehglobalprod%252Cehglobalalwebus%3D%2526c.%2526a.%2526activitymap.%2526page%253D%25252Fen_US%25252Fcar-rental%25252Fhome.html%2526link%253DBook%252520Now%2526region%253Dbuttons%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c""",
            "csrf-token": "undefined",
            "origin": "https://www.alamo.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        formdata = {
            "pickUpLocation.searchCriteria": "San Francisco Union Square",
            "pickUpLocation.peopleSoftId": "1019124",
            "returnToSameLocation": "on",
            "dropOffLocation.searchCriteria": "San Francisco Union Square",
            "dropOffLocation.peopleSoftId": "1019124",
            "countryOfResidenceResident": "on",
            "countryOfResidence": "US",
            "pickUpDateTime.date": fromDateStr,
            "pickUpDateTime.time": "1200",
            "pickUpDateTime.blackOut": "", 
            "dropOffDateTime.date": toDateStr,
            "dropOffDateTime.time": "1200",
            "dropOffDateTime.blackOut": "",
            "renterAge": "25",
            "couponCodeList[0]": "",
            "couponToRemove": "",
            "customerNumber": "",
            "productCode": "",
            "username": "",
            "password": "",
            "IATA": "false",
            "customerNumber": "",
            "enableReservationReset": "true",
            "homepage": "true",
            "secureToken": "62a7a28b-9910-4687-8794-66861b21af53",
            "secureToken2": "e4b37529-a976-4ddd-8e12-bc4ebb5044ac",
        }

        yield scrapy.FormRequest(url, formdata=formdata, callback=self.parse_detail, headers=headers, method="POST", meta = {'from': fromDateStr, 'to': toDateStr, 'count': count, 'period': 1})


    def parse_detail(self, response):

        url = "https://www.alamo.com/content/data/apis/live/reservation/vehicleList.sfx.json/channelName%3Dalamo/locale%3Den_US.json?id={}"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "cookie": """loc=US%7Cen_US%7C%7C; Rental-alamo_com=!AodPtjadAkIyYJ0484WoLKftvzfAoG1v91AT9/0181Rj9kkXVM8QINFVRp54uud4Enwz3Z5V2AD8Zg==; TLTSID=8D7E76F7CCDA9DA31F0A40BF32698CBA; TLTUID=13183FDEBD0CE8DE693E4E3B91BCF3D5; ORIGIN=etc; akacd_www_alamo_com_PC=3740462951~rv=97~id=268ee02d367592469baa57eb7fca399b; Akamai-Edgescape=georegion=247,country_code=US,region_code=CO,city=LITTLETON,dma=751,pmsa=2080,msa=2082,areacode=303,county=ARAPAHOE+JEFFERSON+DOUGLAS,fips=08005+08059+08035,lat=39.5942,long=-105.0086,timezone=MST,zip=80120-80130+80160-80163+80165-80166,continent=NA,throughput=vhigh,bw=5000,asnum=53889; check=true; AMCVS_30545A0C536B768C0A490D44%40AdobeOrg=1; geo=US; AMCV_30545A0C536B768C0A490D44%40AdobeOrg=-330454231%7CMCIDTS%7C18091%7CMCMID%7C12911477000803509030086999346678043528%7CMCAAMLH-1563619949%7C9%7CMCAAMB-1563619949%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1563022349s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; mboxEdgeCluster=28; _sdsat_FUNNEL_START=HOME; _ga=GA1.2.2056695165.1563015152; _gid=GA1.2.744856561.1563015152; _gat_ehiglobal=1; s_cc=true; _gcl_au=1.1.1668666716.1563015153; notice_behavior=none; seerses=e; seerses=e; seerid=78476.87913809033; seerid=78476.87913809033; WRIgnore=true; WRUIDAWS20170419=2342006914991445; ki_r=; _fbp=fb.1.1563015160994.1971356423; _pickUpDate=2019-07-13 12:00:00; _dropOffDate=2019-07-15 12:00:00; res=1019124%7CSan+Francisco+Union+Square%7C1563044400000%7CAmerica%2FLos_Angeles%7C1019124%7CSan+Francisco+Union+Square%7C1563217200000%7CAmerica%2FLos_Angeles%7CUS%7C%7C%7C25%7C; _resDrop=SFOC78; ly_segs=%7B%22alamo_abandon_cart_onsite_modals%22%3A%22alamo_abandon_cart_onsite_modals%22%2C%22treatment_group%22%3A%22treatment_group%22%2C%22ly_alamo_abandon_cart%22%3A%22ly_alamo_abandon_cart%22%2C%22smt_new%22%3A%22smt_new%22%2C%22all%22%3A%22all%22%2C%22ly_treatment_group_1of2_5050split%22%3A%22ly_treatment_group_1of2_5050split%22%7D; ki_t=1563015157677%3B1563015157677%3B1563015194094%3B1%3B4; PathforaPageView=4; __CT_Data=gpv=4&ckp=tld&dm=alamo.com&apv_16618_www03=4&cpv_16618_www03=4&rpv_16618_www03=4; s_tps=6; s_pvs=5; s_sq=ehglobalprod%252Cehglobalalwebus%3D%2526c.%2526a.%2526activitymap.%2526page%253D%25252Fen_US%25252Fcar-rental%25252Fhome.html%2526link%253DBook%252520Now%2526region%253Dbuttons%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c; s_sess=%20s_ppvl%3D%252Fen_US%252Fcar-rental%252Fhome.html%252C67%252C67%252C1169%252C1249%252C969%252C1920%252C1080%252C1%252CL%3B%20s_ptc%3D0.00%255E%255E0.00%255E%255E0.00%255E%255E0.00%255E%255E0.26%255E%255E0.01%255E%255E1.91%255E%255E0.03%255E%255E2.42%3B%20SC_LINKS%3D%252Fen_US%252Fcar-rental%252Fhome.html%255E%255EBook%2520Now%255E%255E%2523%255E%255Ebuttons%255E%255E%3B%20s_ppv%3D%252Fen_US%252Fcar-rental%252Fhome.html%252C69%252C69%252C1193%252C1249%252C969%252C1920%252C1080%252C1%252CL%3B; JSESSIONID=ceamvqufgi251xvetlhp9drgx; _4c_=fVLLbtswEPyVgoecHImkRFIyEBSOExQp0rjxAz0StERHQiVRIOm4RuB%2Fz%2BoR10CKXgjucHdmh7tv6FDoBk0J4xEmjGJKSTpBv%2FXRoekbytrufO2Ova3QFBXet24ahofDIVCVqk2QmTrUjdyswkzZa6sbr6qwMLUOCl9XaIJmXZp8aFyZa%2Bvkwx3QAPyomxdfSLOTy75mQOfKynmlHKj3odm3ppFzk%2BsR2DsP3FY%2B7euttgO41E7bV%2BVLSL09tpfVjbfHQaOTbzIt54slvG5W3ftiKR%2FNUVX%2BOBT8tLpV430DnHJ9bDvhpfaq7LxcKq32W2%2FOjV%2B%2BrP%2FCj1rlcl3WY%2Ftbaw6QB8G8sODji2CAZoM9kgZRICDewa8jihnnKSOcBeNwYDzwaDpzv8omByYIrd5paz9%2BwpW%2BYzpPBiCvbT3%2Bx%2BLHeilv72fzxdPFKF2tvS0zF8AYtG1t6XQ%2F1G3oXKiLl8psVdVak08%2BAlUd9HbvQhJ%2BX13TIA3w9Z14fgpdRAjDNKU0TqDlr7Pn2xtyVZf5DaEpIbEQGOMERwynOIIbT9M0ijkXCY4jRpOr2fP9DYFGW9g4FMOlMpmqOkewoxP0bSY3%2Ffr8%2B29OE%2FRn2GQCSMqibpO9h0kkPAZljCHDlvm40kix3S5POE%2FiTFBCuRZE7EislYjSXHAMij2fwAK6Z5xGERC0wNfXk7McWGYswfhDjsRnuc5Jnx1%2Fai753NywHv%2Bp%2BWTodHoH; RT="sl=4&ss=1563015143846&tt=23544&obo=0&bcn=%2F%2F173e2514.akstat.io%2F&sh=1563015195495%3D4%3A0%3A23544%2C1563015192739%3D3%3A0%3A21120%2C1563015181852%3D2%3A0%3A18697%2C1563015157708%3D1%3A0%3A13853&dm=alamo.com&si=2becded8-c51e-4690-9fb1-f8efd1456a6b"; mbox=session#c0fe9f3c17ca46b08d5a4582c1661068#1563017063|PC#c0fe9f3c17ca46b08d5a4582c1661068.28_134#1626259952; s_pers=%20s_vs%3D1%7C1563017000527%3B%20gpv_v5%3D%252Fen_US%252Fcar-rental%252Fhome.html%7C1563017000543%3B%20s_visit%3D1%7C1563017000548%3B%20s_dfa%3Dehglobalprod%252Cehglobalalwebus%7C1563017002996%3B""",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        yield scrapy.Request(url=url.format(response.meta['count']), callback=self.parse_first, headers=headers, method="GET", meta = response.meta)


    def parse_first(self, response):
        print(response.body)
        if 'vehicleSummary' in json.loads(response.body):
            data = json.loads(response.body)['vehicleSummary']['vehicleDetail']
            for car in data:
                if 'name' in car:
                    item = AlamoItem()
                    item['pickupDate'] = response.meta['from']
                    item['returnDate'] = response.meta['to']
                    item['carClass'] = car['name']
                    item['carType'] = car['similarVehicles']
                    item['dailyPrice'] = car['vehicleRate']['highestUsedPayLaterRate']
                    item['totalPrice'] = car['vehicleRate']['totalPrice']
                    item['period'] = response.meta['period']
                    yield item
        count = response.meta['count'];
        if count <= 90:
            count += 1
            period = 1
            fromDate = datetime.datetime.strptime(response.meta['from'], '%m/%d/%y') + datetime.timedelta(days = 1)
            toDate = fromDate + datetime.timedelta(days = 1)
            fromDateStr = datetime.datetime.strftime(fromDate, '%m/%d/%y')
            toDateStr = datetime.datetime.strftime(toDate, '%m/%d/%y')
        elif count <= 182:
            period = 2
            if count == 91:
                indexDate = datetime.datetime.now()
                indexDate = indexDate + datetime.timedelta(days = 1)
                fromDate = indexDate
                fromDateStr = indexDate.strftime("%m/%d/%y")
                indexDate = indexDate + datetime.timedelta(days = 2)
                toDate = indexDate
                toDateStr = indexDate.strftime("%m/%d/%y")
            else:
                fromDate = datetime.datetime.strptime(response.meta['from'], '%m/%d/%y') + datetime.timedelta(days = 1)
                toDate = fromDate + datetime.timedelta(days = 2)
                fromDateStr = datetime.datetime.strftime(fromDate, '%m/%d/%y')
                toDateStr = datetime.datetime.strftime(toDate, '%m/%d/%y')
            count += 1
        elif count <= 274:
            period = 3

            if count == 183:
                indexDate = datetime.datetime.now()
                indexDate = indexDate + datetime.timedelta(days = 1)
                fromDate = indexDate
                fromDateStr = indexDate.strftime("%m/%d/%y")
                indexDate = indexDate + datetime.timedelta(days = 3)
                toDate = indexDate
                toDateStr = indexDate.strftime("%m/%d/%y")
            else:
                fromDate = datetime.datetime.strptime(response.meta['from'], '%m/%d/%y') + datetime.timedelta(days = 1)
                toDate = fromDate + datetime.timedelta(days = 3)
                fromDateStr = datetime.datetime.strftime(fromDate, '%m/%d/%y')
                toDateStr = datetime.datetime.strftime(toDate, '%m/%d/%y')
            count += 1
        elif count <= 366:
            period = 7

            if count == 275:
                indexDate = datetime.datetime.now()
                indexDate = indexDate + datetime.timedelta(days = 1)
                fromDate = indexDate
                fromDateStr = indexDate.strftime("%m/%d/%y")
                indexDate = indexDate + datetime.timedelta(days = 7)
                toDate = indexDate
                toDateStr = indexDate.strftime("%m/%d/%y")
            else:
                fromDate = datetime.datetime.strptime(response.meta['from'], '%m/%d/%y') + datetime.timedelta(days = 1)
                toDate = fromDate + datetime.timedelta(days = 7)
                fromDateStr = datetime.datetime.strftime(fromDate, '%m/%d/%y')
                toDateStr = datetime.datetime.strftime(toDate, '%m/%d/%y')
            count += 1
        if count<= 367:
            url = "https://www.alamo.com/content/data/apis/live/reservation/start/submit.sfx.json/channelName%3Dalamo/locale%3Den_US.json"
            headers = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "csrf-token": "undefined",
                "origin": "https://www.alamo.com",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            formdata = {
                "pickUpLocation.searchCriteria": "San Francisco Union Square",
                "pickUpLocation.peopleSoftId": "1019124",
                "returnToSameLocation": "on",
                "dropOffLocation.searchCriteria": "San Francisco Union Square",
                "dropOffLocation.peopleSoftId": "1019124",
                "countryOfResidenceResident": "on",
                "countryOfResidence": "US",
                "pickUpDateTime.date": fromDateStr,
                "pickUpDateTime.time": "1200",
                "pickUpDateTime.blackOut": "", 
                "dropOffDateTime.date": toDateStr,
                "dropOffDateTime.time": "1200",
                "dropOffDateTime.blackOut": "",
                "renterAge": "25",
                "couponCodeList[0]": "",
                "couponToRemove": "",
                "customerNumber": "",
                "productCode": "",
                "username": "",
                "password": "",
                "IATA": "false",
                "customerNumber": "",
                "enableReservationReset": "true",
                "homepage": "true",
                "secureToken": "62a7a28b-9910-4687-8794-66861b21af53",
                "secureToken2": "e4b37529-a976-4ddd-8e12-bc4ebb5044ac",
            }

            yield scrapy.FormRequest(url, formdata=formdata, callback=self.parse_detail, headers=headers, method="POST", meta = {'from': fromDateStr, 'to': toDateStr, 'count': count, 'period': period})
