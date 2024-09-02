package ca.utoronto.utm.paint;
import javafx.scene.canvas.GraphicsContext;
import java.util.ArrayList;

public class SquiggleCommand extends PaintCommand implements ShapeSaveCommand, ShapeDrawCommand{
	private ArrayList<Point> points=new ArrayList<Point>();
	
	public void add(Point p){ 
		this.points.add(p); 
		this.setChanged();
		this.notifyObservers();
	}
	public ArrayList<Point> getPoints(){ return this.points; }
	
	
	@Override
	public void execute(GraphicsContext g) {
		ArrayList<Point> points = this.getPoints();
		g.setStroke(this.getColor());
		for(int i=0;i<points.size()-1;i++){
			Point p1 = points.get(i);
			Point p2 = points.get(i+1);
			g.strokeLine(p1.x, p1.y, p2.x, p2.y);
		}
		
	}
	
	public String getSaveFormat() {
		String s = "Squiggle\r\n";
		s += this.toStringInt();
		s += "\tpoints\r\n";
		ArrayList<Point> points = this.getPoints();
		for(int i=0;i<points.size()-1;i++) {
			s += "\t\tpoint:("+points.get(i).x+","+points.get(i).y+")\r\n";
		}
		s += "\tend points\r\n";
		s += "End Squiggle";
		return s;
	}
	@Override
	public String accept(ShapeSaveCommandVisitor v) {
		return v.visit(this);
	}
	@Override
	public void accept(ShapeDrawCommandVisitor v) {
		v.visit(this);
		
	}
	
}
