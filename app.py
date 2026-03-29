from flask import Flask, render_template, jsonify, request
from data.semo_data.semo import get_daily_load_forecast
from data.eirgrid_data.eirgrid import get_wind, get_demand

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/semo/load_forecast')
def api_semo_load_forecast():
    start = request.args.get('start')
    end = request.args.get('end')
    
    if not start or not end:
        return jsonify({'error': 'Missing start or end date'}), 400
    
    try:
        df = get_daily_load_forecast(start, end)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/eirgrid/wind')
def api_eirgrid_wind():
    start = request.args.get('start')
    end = request.args.get('end')
    region = request.args.get('region', 'ALL')
    
    if not start or not end:
        return jsonify({'error': 'Missing start or end date'}), 400
    
    try:
        df = get_wind(start, end, region)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/eirgrid/demand')
def api_eirgrid_demand():
    start = request.args.get('start')
    end = request.args.get('end')
    region = request.args.get('region', 'ALL')
    
    if not start or not end:
        return jsonify({'error': 'Missing start or end date'}), 400
    
    try:
        df = get_demand(start, end, region)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)