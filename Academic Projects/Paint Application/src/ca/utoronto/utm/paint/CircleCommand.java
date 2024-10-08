package ca.utoronto.utm.paint;
import javafx.scene.canvas.GraphicsContext;

public class CircleCommand extends PaintCommand implements ShapeSaveCommand, ShapeDrawCommand{
	private Point centre;
	private int radius;
	
	public CircleCommand(Point centre, int radius){
		this.centre = centre;
		this.radius = radius;
	}
	public Point getCentre() { return centre; }
	public void setCentre(Point centre) { 
		this.centre = centre; 
		this.setChanged();
		this.notifyObservers();
	}
	public int getRadius() { return radius; }
	public void setRadius(int radius) { 
		this.radius = radius; 
		this.setChanged();
		this.notifyObservers();
	}
	public void execute(GraphicsContext g){
		int x = this.getCentre().x;
		int y = this.getCentre().y;
		int radius = this.getRadius();
		if(this.isFill()){
			g.setFill(this.getColor());
			g.fillOval(x-radius, y-radius, 2*radius, 2*radius);
		} else {
			g.setStroke(this.getColor());
			g.strokeOval(x-radius, y-radius, 2*radius, 2*radius);
		}
	}
	
	public String getSaveFormat() {
		String c = "Circle"+"\r\n";
		c += this.toStringInt();
		c += "\t"+ "center:("+this.getCentre().x+","+this.getCentre().y+")"+"\r\n";
		c += "\t"+ "radius:"+this.getRadius()+"\r\n";
		c += "End Circle";
		return c;
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
