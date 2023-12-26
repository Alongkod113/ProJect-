# ตัวอย่างโค้ดใน app.py
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# อ่านข้อมูลจาก CSV
df = pd.read_csv('cam_exit_cole_type_Brand_P-10.csv')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # รับข้อมูลจากฟอร์ม
    license_plate = request.form['license_plate']
    car_type = request.form['car_type']
    brand = request.form['brand']
    color = request.form['color']

    # ตรวจสอบว่าผู้ใช้กรอกข้อมูล License Plate, Car Type, Brand, หรือ Color
    if license_plate:
        result_df = df[df['License Plate No.'] == license_plate]
    elif car_type:
        result_df = df[df['car_type'] == car_type]
    elif brand:
        result_df = df[df['Brand'] == brand]
    elif color:
        result_df = df[df['Color'] == color]
    else:
        # ในกรณีอื่น ๆ ทำการค้นหาจากข้อมูลทั้งหมด
        result_df = df

    # คำนวณเปอร์เซ็นต์ที่เป็นไปได้
    total_entries = len(result_df)
    if total_entries > 0:
        possible_exits = ', '.join(result_df['Camera_Exit'].unique())
        percentage = (total_entries / len(df)) * 100
    else:
        possible_exits = 'N/A'
        percentage = 0

    # ส่งผลลัพธ์กลับไปยังหน้าเว็บ
    result = {'exits': possible_exits, 'percentage': round(percentage, 2)}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
