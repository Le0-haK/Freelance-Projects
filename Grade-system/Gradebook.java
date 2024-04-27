import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;

public class Gradebook implements Comparator<StudentGrades> {
    private Collection<StudentGrades> grades; // Field to store StudentGrades instances

    // Constructor to initialize the grades field
    public Gradebook() {
        this.grades = new ArrayList<>();
    }

    // Method to add a StudentGrades instance to the grades field
    public void addGrade(StudentGrades sg) {
        grades.add(sg);
    }

    // Method to compute the average totalScore() of each StudentGrades in the grades field
    public double average() {
        double sum = 0;
        for (StudentGrades sg : grades) {
            sum += sg.totalScore();
        }
        return sum / grades.size();
    }

    // Method to find the StudentGrades instance with the minimum totalScore() in the grades field
    public StudentGrades min() {
        StudentGrades minStudent = null;
        double minScore = Double.MAX_VALUE;
        for (StudentGrades sg : grades) {
            double score = sg.totalScore();
            if (score < minScore) {
                minScore = score;
                minStudent = sg;
            }
        }
        return minStudent;
    }

    // Method to find the StudentGrades instance with the maximum totalScore() in the grades field
    public StudentGrades max() {
        StudentGrades maxStudent = null;
        double maxScore = Double.MIN_VALUE;
        for (StudentGrades sg : grades) {
            double score = sg.totalScore();
            if (score > maxScore) {
                maxScore = score;
                maxStudent = sg;
            }
        }
        return maxStudent;
    }

    // Method to find the median totalScore() in the grades field
    public StudentGrades median() {
        ArrayList<StudentGrades> sortedGrades = new ArrayList<>(grades);
        sortedGrades.sort(this); // Sort the grades by totalScore()
        return sortedGrades.get(sortedGrades.size() / 2); // Get the middle element
    }

    // Comparator method required by the Comparator interface
    public int compare(StudentGrades left, StudentGrades right) {
        return (int) (left.totalScore() - right.totalScore());
    }

    // Provided toString() method
    public String toString() {
        String rv = "Grades: [ ";
        for (StudentGrades sg : grades) {
            rv += "(" + sg.getStudentName() + ": " + sg.letterGrade() + "), ";
        }
        rv += "]\n";
        rv += "Max: " + max() + ", Median: " + median() + ", Average: " + average() + ", Min: " + min();
        return rv;
    }
}
