import os
import csv
from PIL import UnidentifiedImageError
from nudenet import NudeClassifier
import concurrent.futures

def checkval(classifier, root, file_name):
    value = os.path.join(root, file_name)
    try:
        dict_val = classifier.classify(value)
        if dict_val[value]["unsafe"] > dict_val[value]["safe"]:
            classification = "Obscene"
        else:
            classification = "SFW"

        with open("output.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([value, classification])
    except Exception as e:
        classification = "ERROR"
        with open("output.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([value, classification])


def check_directory(path):
    with open("output.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File Path", "Classification"])
    classifier = NudeClassifier()

    for root, dirs, files in os.walk(path):
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(checkval, classifier, root, file_name) for file_name in files]
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    # input_path = r"D:\obscene_images"
    input_path = r"C:\Users\Aditya\Documents\GitHub\nsfw_data_scraper\data"
    # input_path = os.path.join("C:","Users","Aditya","Documents","GitHub","nsfw_data_scraper","data")
    check_directory(input_path)
