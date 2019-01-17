package ca.utoronto.utm.paint;

public interface ShapeDrawCommand {
	void accept(ShapeDrawCommandVisitor v);
}
