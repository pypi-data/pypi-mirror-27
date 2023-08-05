import argparse
import datetime
import requests
import os
import csv

def format_date(date):
    parsed_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

def find_urls(data):
    result = {}
    for history_item in data['result']:
        if not 'calls' in history_item or len(history_item['calls']) == 0:
            continue
        for call in history_item['calls']:
            if not 'record_url' in call:
                continue
            remote_number = call['remote_number']
            result[remote_number] = call['record_url']
    return result


def load_media_urls(account, apikey, count, from_date=None, to_date=None):
    url = "https://api.voximplant.com/platform_api/GetCallHistory?account_id={}&api_key={}&with_calls=true&desc_order=true&count={}&with_calls=true".format(account, apikey, count)
    if from_date:
        url += "&from_date=" + format_date(from_date)
    if to_date:
        url += "&to_date=" + format_date(to_date)
    r = requests.get(url)
    if r.status_code != 200:
        raise IOError("Wrong status code received from VoxImplant: " + r.status_code)
    
    return find_urls(r.json())

def load_audio(phone, url, folder_name):
    r = requests.get(url)
    cur_time = datetime.datetime.now().strftime("%d-%m-%y")

    with open(folder_name + "/" + cur_time + "-" + phone + ".mp3", 'wb') as mp3:
        mp3.write(r.content)    

def read_csv(path):
    with open(path, 'rb') as file:
        r = csv.reader(file)
        headers = r.next()
        phone_idx = headers.index('phone')
        result = []
        for row in r:
            result.append(row[phone_idx])
        return result
        

def main():
    parser = argparse.ArgumentParser(description = 'Tool for downloading audio files from VoxImplant')
    parser.add_argument("--apikey", required=True, help="api key to VoxImplant")
    parser.add_argument("--account", required=True, help="account ID for VoxImplant")
    parser.add_argument("--csv", help="path to csv file with phone numbers to download")
    parser.add_argument("--from_date", help="from filter in format: DD-MM-YYYY")
    parser.add_argument("--to_date", help="to filter in format: DD-MM-YYYY")
    parser.add_argument("--numbers", nargs="*", help="path to csv file with phone numbers to download")

    args = parser.parse_args()

    phone_numbers = []

    if args.csv:
        phone_numbers.extend(read_csv(args.csv))

    if len(args.numbers) > 0:
        phone_numbers.extend(args.numbers)
    
    if len(phone_numbers) == 0:
        print('phone numbers to download not found. Use --csv or --numbers flag')
        sys.exit(1)

    if args.csv:
        count = len(phone_numbers) + 100
    else:
        print('only numbers flag provided: searching for the last 300 records in voximplant')
        count = 300

    urls = load_media_urls(args.account, args.apikey, count, args.from_date, args.to_date)

    folder_name = "audio"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for phone in phone_numbers:
        url = urls.get(phone)
        if not url:
            print('no media file found for number: {}'.format(phone))
        else:
            load_audio(phone, url, folder_name)




if __name__ == '__main__':
    main()
