import csv
import pandas as pd
from urllib.request import urlopen

class SchoolAssessmentSystem:
    def __init__(self):
        self.data = pd.DataFrame()
        self.summary_data = []

    def process_file(self, file_path):
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            # This section is incomplete. You should define the logic for processing .txt files.
            pass

    def transfer_data(self, criteria, source_file, destination_file):
        filtered_data = self.data.query(criteria)
        filtered_data.to_csv(destination_file, index=False)

    def analyze_content(self):
        self.summary_data = []
        for name, group in self.data.groupby('Name'):
            avg_score = group[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].mean(axis=1).mean()
            highest_score = group[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].max().max()
            lowest_class = group[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].mean().idxmin() 
            lowest_score = group[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].min().min() 
            notable_observations = group[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].idxmax(axis=1).value_counts().idxmax()
            web_data_time = group['Time Spent'].str.extract(r'(\d+)m').astype(int).sum().values[0]
            
            # Calculate overall grade
            overall_grade = self.calculate_grade(avg_score)
            
            student_summary = {
                'Name': name,
                'ID': group['Id'].iloc[0],  # Get the ID of the first row in the group
                'Average Score': avg_score,
                'Highest Score': highest_score,
                'Lowest Class': lowest_class,
                'Lowest Score': lowest_score,
                'Notable Observation': notable_observations,
                'Online Participation': web_data_time,
                'Overall Grade': overall_grade
            }
            self.summary_data.append(student_summary)

    def calculate_grade(self, avg_score):
        if avg_score >= 90:
            return 'A'
        elif avg_score >= 80:
            return 'B'
        elif avg_score >= 70:
            return 'C'
        elif avg_score >= 60:
            return 'D'
        else:
            return 'F'

    def generate_summary(self):
        summary_report = "School Assessment Summary Report:\n\n"
        for student in self.summary_data:
            summary_report += f"*** Summary Report of {student['Name']}, ID: {student['ID']}\n"  # Include ID here
            summary_report += f"1. Overall Performance:\n"
            summary_report += f"   - Overall Grade: {student['Overall Grade']}\n"
            summary_report += f"   - Highest score: {student['Highest Score']}\n"
            summary_report += f"   - Average score: {student['Average Score']:.1f}\n"
            summary_report += f"   - Lowest score: {student['Lowest Score']}\n"
            summary_report += f"2. Subject-wise Analysis:\n"
            summary_report += f"   - Highest scoring subject: {student['Notable Observation']} with the score of {student['Highest Score']}.\n"
            summary_report += f"   - Lowest scoring subject: {student['Lowest Class']} with the score of {student['Lowest Score']}.\n"
            summary_report += f"3. Web Data Insights:\n"
            summary_report += f"   - Online participation time: {student['Online Participation']} minutes\n"
            summary_report += "\n"

        summary_report += f"Report generated on: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n"
        return summary_report

# Example Usage
analyzer = SchoolAssessmentSystem()

# Process files
analyzer.process_file('high_achievers.csv')

# Analyze content
analyzer.analyze_content()

# Generate summary
summary = analyzer.generate_summary()
print(summary)
