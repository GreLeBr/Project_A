from csv import DictWriter
import json
import os
def get_data():
    with open("/raw_data/project_A.json") as text:
        test=json.load(text)
    return test
def create_csv(test):
    test_dict={}
    all_headers=['headline', 'status', 'founded', 'dateOfInvestment', 'management', 'location', 'segment', 'investment', 'investmentType', 'website', 'Description', 'id', 'contentType', 'businessModel', 'subheadline', "exit"]
    file_name="project_a.csv"
    for i in range (len(test["props"]["pageProps"]["page"]["content"][2]["initialItems"])):
        for k,v in test["props"]["pageProps"]["page"]["content"][2]["initialItems"][i].items():
            if k not in ["logo", "website", "content", "updatedAt", "createdAt", "highlightContent","focusImage", "focus"]:
                test_dict[k]=v
            if k =="website":
                test_dict["website"]=test["props"]["pageProps"]["page"]["content"][2]["initialItems"][i]["website"]["url"]
            if k =="content":
                description=test["props"]["pageProps"]["page"]["content"][2]["initialItems"][i]["content"]["content"][0]["content"][0]["value"]
            if len(test["props"]["pageProps"]["page"]["content"][2]["initialItems"][i]["content"]["content"])>1:
                exit=test["props"]["pageProps"]["page"]["content"][2]["initialItems"][i]["content"]["content"][1]["content"][0]["value"]
                test_dict["exit"]=exit
            test_dict["Description"]=description
        if os.path.isfile(file_name):
            with open(file_name, 'a', newline='') as write_obj:
                dict_writer = DictWriter(write_obj, fieldnames=all_headers, restval='NaN')
                dict_writer.writerow(test_dict)
        else:
            with open(file_name, 'a+', newline='') as write_obj:
                dict_writer = DictWriter(write_obj, fieldnames=all_headers,restval='NaN' )
                dict_writer.writeheader()
                dict_writer.writerow(test_dict)
        test_dict={}

if __name__ == '__main__':
    test=get_data()
    create_csv(test)