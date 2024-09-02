package ca.utoronto.utm.paint;

public class SaveVisitor implements ShapeSaveCommandVisitor{
	@Override
	public String visit(CircleCommand circle) {
		return circle.getSaveFormat();
	}
	
	@Override
	public String visit(RectangleCommand rectangle) {
		return rectangle.getSaveFormat();
	}
	
	@Override
	public String visit(SquiggleCommand squiggle) {
		return squiggle.getSaveFormat();
	}
}
