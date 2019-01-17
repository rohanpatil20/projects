package ca.utoronto.utm.paint;

public interface ShapeSaveCommandVisitor {
	String visit(CircleCommand circle);
	String visit(RectangleCommand rectangle);
	String visit(SquiggleCommand squiggle);
}
