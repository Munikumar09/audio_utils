import os
from pathlib import Path

def download_file(url,save_path):
    file_name=url.split("/")[-1]
    absolute_file_path=Path(save_path)/file_name
    if absolute_file_path.exists():
        print(f"{file_name} already exists at {save_path}")
        return
    os.system(f"wget -P {save_path} {url}")
if __name__=="__main__":
    download_links=["https://storage.googleapis.com/test_public_bucket/external/labelled/Hindi_IITM_hindi_dev_09-08-2021_17-31.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/Hindi_IITM_hindi_eval_10-08-2021_05-29.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/Hindi_IITM_hindi_train_09-08-2021_17-16.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/IITM_ASR_TTS_Female_hi_28-07-2021_13-33.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/IITM_ASR_TTS_Male_hi_28-07-2021_14-10.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/Hindi_Hindi_Interspeech_Task1_Valid_lab_18-08-2021_04-42.zip",
"https://storage.googleapis.com/test_public_bucket/external/labelled/Hindi_Hindi_Interspeech_Task1_Train_lab_18-08-2021_04-43.zip",]
    save_path="/media/dataset-harddisk/munikumar/hindi_dataset/benchmarks/ekstep/extra"
    for link in download_links:
        download_file(link,save_path)