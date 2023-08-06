import sys, os
import requests
import argparse


from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

def create_callback(encoder):
    encoder_len = encoder.len
    bar = ProgressBar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)

    return callback

def create_upload(filename):
    return MultipartEncoder(
    fields={'file': (filename, open(filename, 'rb'))})

def upload_core(file_path,presigned_url):
    encoder = create_upload(file_path)
    callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)

    try:
        r = requests.put(presigned_url, data=monitor)
        print('\nUpload finished! (Returned status {0} {1})'.format(r.status_code, r.reason))
    except requests.exceptions.ConnectionError as e:
        print(e)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to the file that is to be uploaded', required=True)
    parser.add_argument('-u', '--url', help='Pre-siged URL generated from browser', required=True)
    return parser.parse_args()

def main():
    args = parse_args(sys.argv[1:]) 
    upload_core(args.path, args.url)

if __name__ == "__main__":
    try:
        status = main()
    except:
        raise
    else:
        raise SystemExit(status)

