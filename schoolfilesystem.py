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
            with open(file_path, 'r') as file:
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
            
            student_summary = {
                'Name': name,
                'Average Score': avg_score,
                'Highest Score': highest_score,
                'Lowest Class': lowest_class,
                'Lowest Score': lowest_score,
                'Notable Observation': notable_observations,
                'Online Participation': web_data_time
            }
            self.summary_data.append(student_summary)

    def generate_summary(self):
        summary_report = "School Assessment Summary Report:\n\n"
        for student in self.summary_data:
            # Determine if there are any courses with scores below 70
            low_score_courses = [course for course, score in student.items() if isinstance(score, int) and score < 70]

            summary_report += f"1. Overall Performance of {student['Name']}:\n"
            summary_report += f"   - Highest score: {student['Highest Score']}\n"
            summary_report += f"   - Average score: {student['Average Score']:.1f}\n"
            summary_report += f"   - Lowest score: {student['Lowest Score']}\n"
            summary_report += f"2. Subject-wise Analysis:\n"
            summary_report += f"   - Highest scoring subject: {student['Notable Observation']} with the score of {student['Highest Score']}.\n"
            summary_report += f"3. Notable Observations:\n"
            summary_report += f"   - {student['Notable Observation']} shows significant achievement.\n"
            summary_report += f"4. Web Data Insights:\n"
            summary_report += f"   - Online participation time: {student['Online Participation']} minutes\n"
            summary_report += f"5. Recommendations:\n"

            # If there are courses with scores below 70, recommend focusing on those courses
            if low_score_courses:
                low_score_course_names = ', '.join(low_score_courses)
                summary_report += f"   - Focus on improving performance in {low_score_course_names}\n"
            elif student['Lowest Score'] < 70:
                summary_report += f"   - Focus on improving performance in {student['Lowest Class']}\n"
            else:
                summary_report += "   - A good grade deserves recognition.\n"

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


# Analyze content & display result area
# Sample of Output:
"""
School Assessment Summary Report:

1. Overall Performance of Student A:
   - Average score: 85.5
   - Top-performing class: Grade 10B

2. Subject-wise Analysis:
   - Mathematics: Improved by 10% compared to the last assessment.
   - Science: Consistent performance across all classes.

3. Notable Observations:
   - Grade 8A shows a significant improvement in English proficiency.

4. Web Data Insights:
   - Online participation: 95% of students accessed assessment resources online.

5. Recommendations:
   - Consider additional support for Grade 9B in Mathematics.

Report generated on: 2024-01-14
"""
