import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;

public class Cell {

    Player content;
    int row, col;

    public Cell(int row, int col) {
        this.row = row;
        this.col = col;
        setContent(Player.Empty);
    }

    public void paint(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        g2d.setStroke(new BasicStroke(GameMain.SYMBOL_STROKE_WIDTH, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));

        int x1 = col * GameMain.CELL_SIZE + GameMain.CELL_PADDING;
        int y1 = row * GameMain.CELL_SIZE + GameMain.CELL_PADDING;
        if (content == Player.Cross) {
            g2d.setColor(Color.RED);
            int x2 = (col + 1) * GameMain.CELL_SIZE - GameMain.CELL_PADDING;
            int y2 = (row + 1) * GameMain.CELL_SIZE - GameMain.CELL_PADDING;
            g2d.drawLine(x1, y1, x2, y2);
            g2d.drawLine(x2, y1, x1, y2);
        } else if (content == Player.Nought) {
            g2d.setColor(Color.BLUE);
            g2d.drawOval(x1, y1, GameMain.SYMBOL_SIZE, GameMain.SYMBOL_SIZE);
        }
    }

    public void clear() {
        setContent(Player.Empty);
    }

    public void setContent(Player player) {
        content = player;
    }
}
