import boto3
import bs4
from bs4 import BeautifulSoup

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('reports')
client = boto3.client('comprehend',region_name='us-west-2')

with open("index.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt)

new_link = soup.new_tag("div", class='post')
soup.body.append(new_link)

with open("index.html", "w") as outf:
    outf.write(str(soup))

def sentimenter(txt):
    response = table.get_item(
        Key={
            'title': txt,
        }
    )

    report_item = response['Item']['report']

    response = client.detect_sentiment(
        Text=report_item,
        LanguageCode='en'
    )

    star_count = int(response['SentimentScore']['Positive']*5)

    table.update_item(
        Key={
            'title': txt,
        },
        UpdateExpression='SET rating = :val1',
        ExpressionAttributeValues={
            ':val1': star_count
        }
    )

to_analyze = str(input())
sentimenter(to_analyze)