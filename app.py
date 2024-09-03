from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Load Excel data
def load_data():
    data = pd.read_excel('attendance_data.xlsx')

    # Convert all date columns (if they are datetime) to string format
    data.columns = [str(col) if isinstance(col, pd.Timestamp) else col for col in data.columns]
    return data

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        data = load_data()

        # Check if roll number exists in the data
        student = data[data['Roll Number'] == str(roll_number)]
        if not student.empty:
            session['roll_number'] = roll_number  # Save roll number in session
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Invalid Roll Number")

    return render_template('login.html')

# Route for student profile
@app.route('/profile')
def profile():
    if 'roll_number' not in session:
        return redirect(url_for('login'))

    roll_number = session['roll_number']
    data = load_data()
    student = data[data['Roll Number'] == str(roll_number)].iloc[0]



    attendance_percent = str(student['Attendance Percentage'])+"%"
    # Extract attendance columns (columns with dates in them)
    attendance_columns = [col for col in data.columns if '-' in str(col)]
    attendance_records = [(col, student[col]) for col in attendance_columns]

    # Pass student details to the template
    return render_template('profile.html', 
                           name=student['Name'], 
                           roll_number=student['Roll Number'],
                           photo_url=student['Photo'], 
                           attendance=attendance_percent,
                           batch=student['Batch'], 
                           attendance_records=attendance_records)

# Logout route
@app.route('/logout')
def logout():
    session.pop('roll_number', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
