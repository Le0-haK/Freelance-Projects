public class Main {
    public static void main(String[] args) {
        // Creating instances of StudentGrades
        StudentGrades john = new StudentGrades("John", "G001", new double[]{0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.3});
        john.setParticipation(90.0);
        john.addReading(100.0);
        john.addLab(85.0);
        john.addExercise(75.0);
        john.addProject(90.0);
        john.setMidterm(85.0);
        john.setFinalExam(75.0);

        StudentGrades alice = new StudentGrades("Alice", "G002", new double[]{0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.3});
        alice.setParticipation(80.0);
        alice.addReading(100.0);
        alice.addLab(75.0);
        alice.addExercise(85.0);
        alice.addProject(80.0);
        alice.setMidterm(75.0);
        alice.setFinalExam(85.0);

        StudentGrades bob = new StudentGrades("Bob", "G003", new double[]{0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.3});
        bob.setParticipation(70.0);
        bob.addReading(100.0);
        bob.addLab(65.0);
        bob.addExercise(75.0);
        bob.addProject(70.0);
        bob.setMidterm(65.0);
        bob.setFinalExam(75.0);

        // Creating a Gradebook instance
        Gradebook gradebook = new Gradebook();
        // Adding StudentGrades instances to the Gradebook
        gradebook.addGrade(john);
        gradebook.addGrade(alice);
        gradebook.addGrade(bob);

        // Printing the Gradebook
        System.out.println(gradebook);
    }
}
