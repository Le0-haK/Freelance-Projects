import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class StudentGrades {
    // Fields to store grades and weights
    private double participation;
    private double midterm;
    private double finalExam;
    private Collection<Double> labs;
    private Collection<Double> exercises;
    private Collection<Double> projects;
    private List<Double> readings;
    private double participationWeight;
    private double readingsWeight;
    private double labsWeight;
    private double exercisesWeight;
    private double projectsWeight;
    private double midtermWeight;
    private double finalExamWeight;
    private String studentName;
    private String gNumber;

    // Constructor to initialize the object with student information and category weights
    public StudentGrades(String name, String gNumber, double[] weights) {
        this.studentName = name;
        this.gNumber = gNumber;
        setWeights(weights);
        this.readings = new ArrayList<>();
        this.labs = new ArrayList<>();
        this.exercises = new ArrayList<>();
        this.projects = new ArrayList<>();
    }

    // Setters for participation, midterm, and finalExam
    public void setParticipation(double participation) {
        this.participation = participation;
    }

    public void setMidterm(double midterm) {
        this.midterm = midterm;
    }

    public void setFinalExam(double finalExam) {
        this.finalExam = finalExam;
    }

    // Set weights for each category
    public void setWeights(double[] weights) {
        this.participationWeight = weights[0];
        this.readingsWeight = weights[1];
        this.labsWeight = weights[2];
        this.exercisesWeight = weights[3];
        this.projectsWeight = weights[4];
        this.midtermWeight = weights[5];
        this.finalExamWeight = weights[6];
    }

    // Add individual scores to respective categories
    public void addReading(double d) {
        readings.add(d);
    }

    public void addLab(double d) {
        labs.add(d);
    }

    public void addExercise(double d) {
        exercises.add(d);
    }

    public void addProject(double d) {
        projects.add(d);
    }

    // Calculate unweighted score for the readings category
    public double unweightedReadingsScore() {
        if (readings.size() < 16)
            return 100;
        List<Double> sortedReadings = new ArrayList<>(readings);
        Collections.sort(sortedReadings);
        double sum = 0;
        for (int i = 15; i < sortedReadings.size(); i++) {
            sum += sortedReadings.get(i);
        }
        return sum / (sortedReadings.size() - 15);
    }

    // Calculate unweighted scores for labs, exercises, and projects categories
    public double unweightedLabsScore() {
        return calculateUnweightedScore(labs);
    }

    public double unweightedExercisesScore() {
        return calculateUnweightedScore(exercises);
    }

    public double unweightedProjectsScore() {
        return calculateUnweightedScore(projects);
    }

    // Helper method to calculate unweighted score for a category
    private double calculateUnweightedScore(Collection<Double> scores) {
        if (scores.isEmpty())
            return 100;
        double sum = 0;
        for (Double score : scores) {
            sum += score;
        }
        return sum / scores.size();
    }

    // Check if final exam score is higher than midterm score
    public boolean finalReplacesMidterm() {
        return finalExam > midterm;
    }

    // Check if final exam score is passing
    public boolean finalIsPassing() {
        return finalExam >= 60.0;
    }

    // Calculate total score by combining weighted scores from each category
    public double totalScore() {
        double total = 0;
        total += participation * participationWeight;
        total += unweightedReadingsScore() * readingsWeight;
        total += unweightedLabsScore() * labsWeight;
        total += unweightedExercisesScore() * exercisesWeight;
        total += unweightedProjectsScore() * projectsWeight;
        if (finalReplacesMidterm()) {
            total += finalExam * finalExamWeight;
        } else {
            total += midterm * midtermWeight;
        }
        return total;
    }

    // Determine letter grade corresponding to total score
    public String letterGrade() {
        if (!finalIsPassing()) {
        return "F";  // Return "F" if final exam is not passing
        }
        
        double score = totalScore();
        if (score >= 98)
            return "A+";
        else if (score >= 92)
            return "A";
        else if (score >= 90)
            return "A-";
        else if (score >= 88)
            return "B+";
        else if (score >= 82)
            return "B";
        else if (score >= 80)
            return "B-";
        else if (score >= 78)
            return "C+";
        else if (score >= 72)
            return "C";
        else if (score >= 70)
            return "C-";
        else if (score >= 60)
            return "D";
        else
            return "F";
    }

    // Provide formatted string representation of the object
    @Override
    public String toString() {
        String rv = "Name: " + studentName + "\n";
        rv += "G#: " + gNumber + "\n";
        rv += "Participation: " + participation + "\n";
        rv += "Readings: " + unweightedReadingsScore() + ", " + readings + "\n";
        rv += "Labs: " + unweightedLabsScore() + ", " + labs + "\n";
        rv += "Exercises: " + unweightedExercisesScore() + ", " + exercises + "\n";
        rv += "Projects: " + unweightedProjectsScore() + ", " + projects + "\n";
        rv += "Midterm: " + midterm + "\n";
        rv += "Final Exam: " + finalExam + "\n";
        rv += totalScore() + ", " + letterGrade() + "\n";
        return rv;
    }

    // Getters for studentName and gNumber
    public String getStudentName() {
        return studentName;
    }

    public String getgNumber() {
        return gNumber;
    }
}
