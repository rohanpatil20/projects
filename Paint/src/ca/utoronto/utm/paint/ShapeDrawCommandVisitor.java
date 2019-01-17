package ca.utoronto.utm.paint;

public interface ShapeDrawCommandVisitor {
	void visit(CircleCommand circle);
	void visit(RectangleCommand rectangle);
	void visit(SquiggleCommand squiggle);
}
