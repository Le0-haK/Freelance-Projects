// GradeChecker.java

import java.util.Scanner;
import java.io.File;

public class GradeChecker {
	public static void main(String[] args){
		double[] defaultWeights = {0.05, 0.05, 0.15, 0.09, 0.21, 0.2, 0.25};
		try{
			System.out.println(	"This driver class should let you test out much of the "+
								"functionality of the StudentGrades class, but you should "+
								"still write your own tests! For each grade you enter below "+
								"be sure to enter as a percentage out of 100. For example, "+
								"for an exercise score of 48/50 you should enter \"96.0\" "+
								"(without quotes). For lists of scores, enter as a comma "+
								"separated list: \"96.0, 85.1, 100.0\" (without quotes). "+
								"If you provide a filename as a command line argument, it "+
								"data will be pulled from that source rather than "+
								"interactively.");
			Scanner scan;
			if(args.length > 0){
				scan = new Scanner(new File(args[0]));
			} else {
				scan = new Scanner(System.in);
			}
			System.out.print("Enter a name (String): ");
			String studentName = scan.nextLine();
			System.out.print("Enter a G#: ");
			String gNumber = scan.nextLine();
			StudentGrades sg = new StudentGrades(studentName, gNumber, defaultWeights);
			//Participation
			String line;
			System.out.print("Enter participation: ");
			sg.setParticipation(Double.parseDouble(scan.nextLine()));
			//Readings
			System.out.print("Enter a list of scores (out of 100) for the readings, separated by commas: ");
			line = scan.nextLine();
			for(String scoreStr : line.split(",")){
				sg.addReading(Double.parseDouble(scoreStr.trim()));
			}
			//Labs
			System.out.print("Enter a list of scores (out of 100) for the labs, separated by commas: ");
			line = scan.nextLine();
			for(String scoreStr : line.split(",")){
				sg.addLab(Double.parseDouble(scoreStr.trim()));
			}
			//Exercises
			System.out.print("Enter a list of scores (out of 100) for the exercises, separated by commas: ");
			line = scan.nextLine();
			for(String scoreStr : line.split(",")){
				sg.addExercise(Double.parseDouble(scoreStr.trim()));
			}
			//Projects
			System.out.print("Enter a list of scores (out of 100) for the projects, separated by commas: ");
			line = scan.nextLine();
			for(String scoreStr : line.split(",")){
				sg.addProject(Double.parseDouble(scoreStr.trim()));
			}
			//Midterm
			System.out.print("Enter a score for the midterm: ");
			sg.setMidterm(Double.parseDouble(scan.nextLine()));
			//Final
			System.out.print("Enter a score for the final exam: ");
			sg.setFinalExam(Double.parseDouble(scan.nextLine()));
			//test output:
			System.out.println("Grades");
			System.out.println(sg);
		} catch(Exception e){
			throw new RuntimeException(e);
		}
	}
}
