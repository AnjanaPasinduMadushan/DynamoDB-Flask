from flask import Flask, request, render_template, redirect 
import boto3

app = Flask(__name__)

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/create-table", methods=['POST'])
def create_table():
    table_name = request.form["tableName"]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'regNo',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'regNo',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    
    print("Table status:", table.table_status)

    
    return "Data written successfully"
    
if __name__ == "__main__":
    app.run(debug=True,port=8080,host='0.0.0.0')