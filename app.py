from flask import Flask, render_template, jsonify, request
import psycopg2 #pip install psycopg2 
import psycopg2.extras
      
app = Flask(__name__)
      
app.secret_key = "caircocoders-ednalan"
      
DB_HOST = "localhost"
DB_NAME = "car"
DB_USER = "postgres"
DB_PASS = "root"
          
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def main():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM area ORDER BY area_id")
    area = cur.fetchall()
    return render_template('index.html', area=area)
  
@app.route("/area_position",methods=["POST","GET"])
def area_position():  
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id']     
        cur.execute("SELECT * FROM position WHERE area_id = %s ORDER BY position_name ASC", [category_id] )
        position = cur.fetchall()   
        output_array = []   
        for row in position:
            output_obj = {
                'id': row['area_id'],
                'name': row['position_name']
            }
            output_array.append(output_obj)            

    return jsonify(output_array)

if __name__ == "__main__":
    app.run(debug=True, port=5001)