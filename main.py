from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# 정렬 기준 상태 토글
sort_by_status = False

@app.route('/')
def index():
    global sort_by_status

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # JSON 데이터를 리스트로 변환
    students = []
    for name, info in data.items():
        students.append({
            'name': name,
            'password': info['비번'],
            'animal': info['동물'],
            'status': info['상태'],
            'number': info.get('출석번호', 99)  # 출석번호 없으면 뒤로
        })

    if sort_by_status:
        status_order = {'green': 0, 'yellow': 1, 'red': 2}
        students.sort(key=lambda x: (status_order.get(x['status'], 3), x['number']))
    else:
        students.sort(key=lambda x: x['number'])

    return render_template('home.html', students=students, sort_by_status=sort_by_status)

@app.route('/toggle_sort')
def toggle_sort():
    global sort_by_status
    sort_by_status = not sort_by_status
    return redirect(url_for('index'))

@app.route('/update_status', methods=['POST'])
def update_status():
    username = request.form['username']
    password = request.form['password']
    new_status = request.form['status']

    with open(DATA_FILE, 'r', encoding='utf-8') as f:  # 데이터 파일 열기
        data = json.load(f)

    if username not in data:
        return "사용자를 찾을 수 없습니다.", 400    #사용자 이름 없음

    if str(data[username]['비번']) != password:    #비번 틀림, 필요시 비번 틀렸다고 나오는 알림 입력창 아래 위치에 추가하기
        return "비밀번호가 틀렸습니다.", 403

    data[username]['상태'] = new_status  # 상태 변경, 선택지 누르면 문자열로 변환하도록 코드 추가하기

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
