package ca.utoronto.utm.paint;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Observable;
import java.util.Observer;

import javafx.scene.canvas.GraphicsContext;

public class PaintModel extends Observable implements Observer {

	public void save(PrintWriter writer) {
		SaveVisitor visitor = new SaveVisitor();
		writer.println("Paint Save File Version 1.0");
		for (PaintCommand c: this.commands) {
			writer.println(c.accept(visitor));
		}
		writer.println("End Paint Save File");
		writer.close();
	}
	public void reset(){
		for(PaintCommand c: this.commands){
			c.deleteObserver(this);
		}
		this.commands.clear();
		this.setChanged();
		this.notifyObservers();
	}
	
	public void addCommand(PaintCommand command){
		this.commands.add(command);
		command.addObserver(this);
		this.setChanged();
		this.notifyObservers();
	}
	
	public void setCommands(ArrayList<PaintCommand> commandL) {
		this.commands=commandL;
	}
	private ArrayList<PaintCommand> commands = new ArrayList<PaintCommand>();

	public void executeAll(GraphicsContext g) {
		DrawVisitor visitor = new DrawVisitor(g);
		for(PaintCommand c: this.commands){
			c.accept(visitor);
		}
	}
	
	/**
	 * We Observe our model components, the PaintCommands
	 */
	@Override
	public void update(Observable o, Object arg) {
		this.setChanged();
		this.notifyObservers();
	}
}
