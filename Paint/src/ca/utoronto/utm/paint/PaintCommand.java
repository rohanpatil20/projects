package ca.utoronto.utm.paint;
import java.util.Observable;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public abstract class PaintCommand extends Observable {
	private Color color;
	private boolean fill;
	
	PaintCommand(){
		// Pick a random color for this
		int r = (int)(Math.random()*256);
		int g = (int)(Math.random()*256);
		int b= (int)(Math.random()*256);
		this.color = Color.rgb(r, g, b);
		
		this.fill = (1==(int)(Math.random()*2));
	}
	public Color getColor() {
		return color;
	}
	public void setColor(Color color) {
		this.color = color;
	}
	public boolean isFill() {
		return fill;
	}
	public void setFill(boolean fill) {
		this.fill = fill;
	}
	public String toString(){
		double r = this.color.getRed();
		double g = this.color.getGreen();
		double b = this.color.getBlue();

		String s = "";
		s+="\tcolor:"+r+","+g+","+b+"\r\n";
		s+="\tfilled:"+this.fill+"\r\n";
		return s;
	}
	
	public String toStringInt(){
		int r = (int) Math.round(this.color.getRed()*255);
		int g = (int) Math.round(this.color.getGreen()*255);
		int b = (int) Math.round(this.color.getBlue()*255);

		String s = "";
		s+="\t"+ "color:"+r+","+g+","+b+"\r\n";
		s+="\t"+ "filled:"+this.fill+"\r\n";
		return s;
	}
	public abstract void execute(GraphicsContext g);
	public abstract String getSaveFormat();
	public abstract String accept(ShapeSaveCommandVisitor v);
	public abstract void accept(ShapeDrawCommandVisitor v);
}
