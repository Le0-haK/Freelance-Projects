import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class KakuroSolver {
    private static final char BLANK = '0';
    private static final char FIXED = 'X';
    private static final char SUM_MARKER = '\\';
    private static int numRows;
    private static int numCols;
    private static char[][] board;

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java KakuroSolver <input_file>");
            return;
        }
        String inputFile = args[0];
        if (!inputFile.endsWith(".txt")) {
            System.out.println("Input file must be a text file (*.txt)");
            return;
        }

        if (!readBoardFromFile(inputFile)) {
            System.out.println("Failed to load the board.");
            return;
        }

        if (solveKakuro(0, 0)) {
            printBoard();
        } else {
            System.out.println("No solution found.");
        }
    }

    private static boolean solveKakuro(int row, int col) {
        if (col == numCols) {
            col = 0;
            row++;
        }
        if (row == numRows) {
            return true;
        }

        if (board[row][col] != BLANK) {
            return solveKakuro(row, col + 1);
        }

        for (char num = '1'; num <= '9'; num++) {
            if (isValidPlacement(row, col, num)) {
                board[row][col] = num;
                if (solveKakuro(row, col + 1)) {
                    return true;
                }
                board[row][col] = BLANK;
            }
        }
        return false;
    }

    private static boolean isValidPlacement(int row, int col, char num) {
        return isRowValid(row, num) && isColumnValid(col, num);
    }

    private static boolean isRowValid(int row, char num) {
        for (int j = 0; j < numCols; j++) {
            if (board[row][j] == num) {
                return false; // Duplicate number in the row
            }
        }
        return true;
    }

    private static boolean isColumnValid(int col, char num) {
        for (int i = 0; i < numRows; i++) {
            if (board[i][col] == num) {
                return false; // Duplicate number in the column
            }
        }
        return true;
    }

    private static boolean readBoardFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String[] dimensions = reader.readLine().split(" ");
            numRows = Integer.parseInt(dimensions[0]);
            numCols = Integer.parseInt(dimensions[1]);
            if (numRows < 3 || numRows > 10 || numCols < 3 || numCols > 10) {
                System.out.println("Invalid board size. Size must be between 3 and 10.");
                return false;
            }
            board = new char[numRows][numCols];
            for (int i = 0; i < numRows; i++) {
                String[] rowValues = reader.readLine().split(","); // Split each line by comma
                if (rowValues.length != numCols) {
                    System.out.println("Invalid number of elements in row " + (i + 1));
                    return false;
                }
                for (int j = 0; j < numCols; j++) {
                    char value = rowValues[j].charAt(0);
                    if (value == SUM_MARKER) {
                        board[i][j] = value;
                    } else if (value == BLANK) {
                        board[i][j] = BLANK; // Initialize empty cells with '0'
                    } else {
                        board[i][j] = value;
                    }
                }
            }
            return true;
        } catch (IOException | NumberFormatException | ArrayIndexOutOfBoundsException e) {
            e.printStackTrace();
            return false;
        }
    }

    private static void printBoard() {
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                System.out.print(board[i][j]);
                if (board[i][j] == SUM_MARKER && j < numCols - 1) {
                    System.out.print(",");
                } else if (j < numCols - 1) {
                    System.out.print(",");
                }
            }
            System.out.println();
        }
    }
}
