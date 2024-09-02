package ca.utoronto.utm.paint;

public interface ShapeSaveCommand {
	String accept(ShapeSaveCommandVisitor v);
}
