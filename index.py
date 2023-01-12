# Name: Tola Kan    ID: 6407012662064

from flask import Flask, request, jsonify

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Cambodia", "capital":"Phnom Penh"},
    {"id": 2, "name": "Thailand", "capital":"Bangkok"},
    {"id": 3, "name": "USA", "capital":"Washington DC"},
]


def _find_next_id(id):
    data = [x for x in countries if x['id']==id] 
    return data

@app.route('/countries', methods=["GET"])
def get_countries():
    return jsonify(countries)

# GET ---------------------------------------------------------
@app.route('/country/<id>', methods=["GET"])
def get_country(id):
    id = int(id)
    country= _find_next_id(id)
    if countries:
        return jsonify(country)
    else:
        return "ERROR 404"
    
# POST ------------------------------------------------------------
@app.route('/add_country/', methods=["POST"])
def post_country():
    id = int(request.form.get('id'))
    name = request.form.get('name')
    capital = request.form.get('capital')
    
    new_data = {
        "id": id,
        "name": name,
        "capital": capital
    }
 
    if _find_next_id(id):
        return {"error": "Bad Request"}, id
    else:
        countries.append(new_data)
        return jsonify(countries)

# Put -----------------------------------------------------------------------
@app.route('/update_country/<int:c_id>', methods=["PUT"])
def update_country(c_id): 
    global countries
    name = request.form.get('name')
    capital = request.form.get('capital')
    
    for data in countries:
        if c_id == data.get('id'):
            data["name"] = str(name)
            data["capital"] = str(capital)
            return jsonify(countries)
    else:
        return jsonify({"error": f"Bad Request: there is no country with id = {c_id} in the list."}), 404

# Patch ----------------------------------------------------------------------
@app.route('/patch_country/<int:c_id>', methods=['PATCH'])
def patch_country(c_id):
    patch_data = request.get_json()
    for country in countries:
        if country['id'] == c_id:
            country["name"]= str(patch_data['name'])
            country["capital"]= str(patch_data['capital'])
            return jsonify(countries)
            
    else:
        return jsonify({"error": f"Bad Request: there is no country with id = {c_id} in the list."}), 404

    

# DELETE --------------------------------------------------------------------
@app.route('/delete_country/<int:id>', methods=["DELETE"])
def delete_country(id): 
    global countries
    id = int(id)
    for data in countries:
        if data['id'] == id:
            countries = list(filter(lambda country : country['id'] != id, countries))
            return jsonify(countries)
        
    else:
        return {"error": f"Bad Request: wrong id = {type(id)}"}, 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)