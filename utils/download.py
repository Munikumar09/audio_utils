import os
import sys
sys.path.append("..")
from utils.common import create_dir
from pathlib import Path

def download_file(url,save_path):
    url_path=Path(url)
    file_save_path=Path(save_path)/url_path.parent.name/url_path.name
    print(file_save_path.parent)
    create_dir(file_save_path.parent,parents=True)
    if file_save_path.exists():
        print(f"{file_save_path} already exists at {save_path}")
        return
    os.system(f"wget -P {str(file_save_path.parent)} {url}")
if __name__=="__main__":
    download_links=["https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/kathbath.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/kathbath.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/kathbath_noisy.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/kathbath_noisy.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/commonvoice.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/commonvoice.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/fleurs.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/fleurs.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/indictts.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/indictts.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/mucs.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/mucs.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar/gramvaani.zip",
"https://objectstore.e2enetworks.net/indic-asr-public/indicwhisper/vistaar_benchmarks/gramvaani.zip"]
    save_path="/media/dataset-harddisk/munikumar/hindi_dataset/vistaar"
    for link in download_links:
        download_file(link,save_path)