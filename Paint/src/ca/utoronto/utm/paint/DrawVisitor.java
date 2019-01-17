package ca.utoronto.utm.paint;

import javafx.scene.canvas.GraphicsContext;

public class DrawVisitor implements ShapeDrawCommandVisitor{
	private GraphicsContext g;
	public DrawVisitor(GraphicsContext g) {
		this.g = g;
	}
	@Override
	public void visit(CircleCommand circle) {
		circle.execute(this.g);
	}

	@Override
	public void visit(RectangleCommand rectangle) {
		rectangle.execute(this.g);
	}

	@Override
	public void visit(SquiggleCommand squiggle) {
		squiggle.execute(this.g);
	}

}
