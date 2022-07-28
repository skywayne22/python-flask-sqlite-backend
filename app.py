
from flask import Flask, make_response, request, json, jsonify
import sqlite3 as sql
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

#Saving order
@app.route('/createCart', methods=['POST'])
@cross_origin(supports_credentials=True)
def createCart():

    if request.method == 'POST':
        try:
            content = request.get_json(silent=True)
            title = content['title']
            price = content['price']
            imageURL = content['imageURL']
            qty = content['qty']
            sizeLabel = content['sizeLabel']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO orders (title, price, imageURL, qty, sizeLabel) VALUES (?,?,?,?,?)''',
                            (title, price, imageURL, qty, sizeLabel))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            con.close()
            print(msg)
            return json.dumps({'success': True, 'message': msg})

    else:
        msg = "invalid request method"
        return json.dumps({'success': False, 'message': msg}), 400,

#Retrieve orders
@app.route('/getCart', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCart():
    #{ "sizeLabel":"3"}
    sizeLabel = request.args.get('sizeLabel')
    list = {}
    try:
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            if (sizeLabel):
                cur.execute(
                    '''SELECT * FROM orders WHERE sizeLabel = \''''+sizeLabel+'\''' ''')
            else:
                cur.execute('''SELECT * FROM orders''')
            rows = cur.fetchall()
            list = json.dumps([dict(ix) for ix in rows])
            con.commit()

    except:
        con.rollback()
        msg = "Error in fetching operation"
        return json.dumps({'success': False, 'message': msg}), 400
    finally:
        con.close()
        return jsonify({"orderList": list}), 200

#Updating order
@app.route('/updateCart', methods=['GET'])
@cross_origin(supports_credentials=True)
def updateCart():

    sizeLabel = request.args.get('sizeLabel')
    list = {}
    if (sizeLabel):
        try:
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    '''UPDATE orders SET qty = qty+1 WHERE sizeLabel = \''''+sizeLabel+'\''' ''')
                con.commit()

                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute('''SELECT * FROM orders''')
                rows = cur.fetchall()
                list = json.dumps([dict(ix) for ix in rows])
                con.commit()

        except:
            con.rollback()
            msg = "Error in updating operation"
            return json.dumps({'success': False, 'message': msg}), 400

        finally:
            con.close()
            print("Record successfully updated")
            return jsonify({"orderList": list}), 200
    else:
        msg = "sizeLabel required"
        return json.dumps({'success': False, 'message': msg}), 400

if __name__ == '__main__':
    app.run(debug=True)
