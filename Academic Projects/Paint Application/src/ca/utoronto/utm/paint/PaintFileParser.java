package ca.utoronto.utm.paint;

import javafx.scene.paint.Color;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
/**
 * Parse a file in Version 1.0 PaintSaveFile format. An instance of this class
 * understands the paint save file format, storing information about
 * its effort to parse a file. After a successful parse, an instance
 * will have an ArrayList of PaintCommand suitable for rendering.
 * If there is an error in the parse, the instance stores information
 * about the error. For more on the format of Version 1.0 of the paint 
 * save file format, see the associated documentation.
 * 
 * @author 
 *
 */
public class PaintFileParser {
	private int lineNumber = 0; // the current line being parsed
	private String errorMessage =""; // error encountered during parse
	private PaintModel paintModel; 
	private boolean start=false;
	
	/**
	 * Below are Patterns used in parsing 
	 */
	private Pattern pFileStart=Pattern.compile("^PaintSaveFileVersion1.0$");
	private Pattern pFileEnd=Pattern.compile("^EndPaintSaveFile$");

	private Pattern pCircleStart=Pattern.compile("^Circle$");
	private Pattern pCenter=Pattern.compile("^center:[(]([0-9]+),([0-9]+)[)]$");
	private Pattern pRadius=Pattern.compile("^radius:([0-9]+)$");
	private Pattern pCircleEnd=Pattern.compile("^EndCircle$");
	
	private Pattern pRectangleStart=Pattern.compile("^Rectangle$");
	private Pattern pP1=Pattern.compile("^p1:[(]([0-9]+),([0-9]+)[)]$");
	private Pattern pP2=Pattern.compile("^p2:[(]([0-9]+),([0-9]+)[)]$");
	private Pattern pRectangleEnd=Pattern.compile("^EndRectangle$");
	
	private Pattern pSquiggleStart=Pattern.compile("^Squiggle$");
	private Pattern pPointStart= Pattern.compile("^points$");
	private Pattern pPoint=Pattern.compile("^point:[(]([0-9]+),([0-9]+)[)]$");
	private Pattern pPointEnd= Pattern.compile("^endpoints$");
	private Pattern pSquiggleEnd=Pattern.compile("^EndSquiggle$");
	
	private Pattern pColor=Pattern.compile("^color:([0-9]|[1-8][0-9]|9[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(,([0-9]|[1-8][0-9]|9[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])){2}$");
	private Pattern pFilled=Pattern.compile("^filled:(true|false)$");
	private Pattern pBlank=Pattern.compile("^$");
	
	String[] circleData = new String[4];
	String[] rectangleData = new String[4];
	String[] squiggleData = new String[2];
	ArrayList<String> pointData = new ArrayList<String>(); 
	private ArrayList<PaintCommand> commands = new ArrayList<PaintCommand>();
	
	public ArrayList<PaintCommand> getCommands(){
		return this.commands;
	}
	/**
	 * Store an appropriate error message in this, including 
	 * lineNumber where the error occurred.
	 * @param mesg
	 */
	private void error(String mesg){
		JFrame frame = new JFrame("Error");
		this.errorMessage = "Error in line "+(lineNumber-1)+" "+mesg;
		JOptionPane.showMessageDialog(frame, this.errorMessage);
	}
	
	/**
	 * 
	 * @return the error message resulting from an unsuccessful parse
	 */
	public String getErrorMessage(){
		return this.errorMessage;
	}
	
	/**
	 * Parse the inputStream as a Paint Save File Format file.
	 * The result of the parse is stored as an ArrayList of Paint command.
	 * If the parse was not successful, this.errorMessage is appropriately
	 * set, with a useful error message.
	 * 
	 * @param inputStream the open file to parse
	 * @param paintModel the paint model to add the commands to
	 * @return whether the complete file was successfully parsed
	 */
	public boolean parse(BufferedReader inputStream, PaintModel paintModel) {
		this.paintModel = paintModel;
		this.errorMessage="";
		
		// During the parse, we will be building one of the 
		// following commands. As we parse the file, we modify 
		// the appropriate command.
		
		CircleCommand circleCommand = null; 
		RectangleCommand rectangleCommand = null;
		SquiggleCommand squiggleCommand = null;
	
		try {	
			int state=0; Matcher m; String l;
			
			this.lineNumber=0;
			while ((l = inputStream.readLine()) != null) {
				this.lineNumber++;
				System.out.println(lineNumber+" "+l+" ");
				switch(state){
					case 0:
						m=pFileStart.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()){
							this.start = true;
							state=1;
							break;
						} else {
							state=9;
						}
					case 1: // Looking for the start of a new object or end of the save file else move to next shape if not circle
						m=pCircleStart.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()){
							state=5; 
							break;
						} else {
							state=2;
						}
						m=pBlank.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()) {
							break;
						}
					case 2: // Looking for rectangle start.if not move to next shape (squiggle)
						m=pRectangleStart.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()){
							state=6; 
							break;
						}
						else {
							state=3;
						}
						m=pBlank.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()) {
							break;
						}
					case 3: // looking for squiggle start. if not move back to circle and check other shapes
						m=pSquiggleStart.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()){
							state=7; 
							break;
						} else {
							state=4;
						}
						m=pBlank.matcher(l.replaceAll("\\s+", ""));
						if(m.matches()) {
							break;
						}
					case 4: // looking for file end
						m=pFileEnd.matcher(l.replaceAll("\\s+", "")); //empty
						if(m.matches()){
							if (this.start == true) {
								this.start=false;
								state=10;
								break;
							} else {
								state=9;
							}
						}
					case 5: // Extract data from circle
						m=pCircleEnd.matcher(l.replaceAll("\\s+", "")); //empty
						if(m.matches()){
							this.createCircle(circleData);
							circleData = new String[4];
							state=1; 
							break;
						}else {
							state=5;
							m=pColor.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (circleData[1]==null && circleData[2]==null && circleData[3]==null) {
									circleData[0] = l;
									state=5;
									break;
								} else {
									state=9;
								}
							}else {
								state=9;
							}
							m=pFilled.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (circleData[0]!=null && circleData[2]==null && circleData[3]==null) {
									circleData[1] = l;
									state=5;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pCenter.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								if (circleData[0]!=null && circleData[1]!=null && circleData[3]==null) {
									circleData[2] = l;
									state=5;
									break;
								} else {
									state=9; 
								} 
							}else {
								state=9;
							}
							m=pRadius.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								if (circleData[0]!=null && circleData[1]!=null && circleData[2]!=null) {
									circleData[3] = l;
									state=5;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pBlank.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								break;
							}
							break;
						}
					case 6: // Extract data from rectangle
						m=pRectangleEnd.matcher(l.replaceAll("\\s+", "")); //empty
						if(m.matches()){
							this.createRectangle(rectangleData);
							rectangleData = new String[4];
							state=1; 
							break;
						} else {
							m=pColor.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (rectangleData[1]==null && rectangleData[2]==null && rectangleData[3]==null) {
									rectangleData[0] = l;
									state=6;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pFilled.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (rectangleData[0]!=null && rectangleData[2]==null && rectangleData[3]==null) {
									rectangleData[1] = l;
									state=6;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pP1.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (rectangleData[0]!=null && rectangleData[1]!=null && rectangleData[3]==null) {
									rectangleData[2] = l;
									state=6;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pP2.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (rectangleData[0]!=null && rectangleData[1]!=null && rectangleData[2]!=null) {
									rectangleData[3] = l;
									state=6;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pBlank.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								break;
							}
							break;
						}
					case 7: // extract squiggle data. look for point start when extracting data
						m=pSquiggleEnd.matcher(l.replaceAll("\\s+", "")); //empty
						if(m.matches()){
							this.createSquiggle(squiggleData);
							squiggleData = new String[2];
							pointData = new ArrayList<String>();
							state=1; 
							break;
						} else {
							state=7;
							m=pColor.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (squiggleData[1]==null) {
									squiggleData[0] = l;
									state=7;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pFilled.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								if (squiggleData[0]!=null) {
									squiggleData[1] = l;
									state=7;
									break;
								} else {
									state=9; 
								}
							}else {
								state=9;
							}
							m=pPointStart.matcher(l.replaceAll("\\s+", ""));
							if (m.matches()) {
								state=8;
								break;
							}else {
								state=9;	 
							}
							m=pBlank.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								break;
							}
							break;
						}
					case 8: // extract points in a list
						m=pPointEnd.matcher(l.replaceAll("\\s+", "")); //empty
						if(m.matches()){
							state=7; 
							break;
						}else {
							state=8;
							m=pPoint.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								if (squiggleData[0]!=null && squiggleData[1]!=null) {
									pointData.add(l);
									state=8;
									break;
								}else {
									state=9;
								}
							}else {
								state=9;
							}
							m=pBlank.matcher(l.replaceAll("\\s+", ""));
							if(m.matches()) {
								break;
							}
							break;
						}
					case 9: // acceptor if any error in any state. should return false
						error("");
						return false;
					case 10: // ends the FSM if no more lines left
						if (l!=null) {
							state=9;
						}
						break;
				}
			}
		}  catch (Exception e){
			
		}
		return true;
	}
	
	public void createCircle(String[] circleValues) {
		int[] rgb = parseRGB(circleValues[0]);
		boolean filled = parseBool(circleValues[1]);
		Point center = parsePoint(circleValues[2]);
		int radius = 0;
		
		Pattern p = Pattern.compile("(\\d+)");
		Matcher m = p.matcher(circleValues[3]);
		if(m.find()) {
			radius = Integer.parseInt(m.group(1));
		}
		CircleCommand cir = new CircleCommand(center, radius);
		cir.setColor(Color.rgb(rgb[0], rgb[1], rgb[2]));
		cir.setFill(filled);
		this.commands.add(cir);
	}
	public void createRectangle(String[] rectangleValues) {
		int[] rgb = parseRGB(rectangleValues[0]);
		boolean filled = parseBool(rectangleValues[1]);
		Point p1 = parsePoint(rectangleValues[2]);
		Point p2 = parsePoint(rectangleValues[3]);
		
		RectangleCommand rect = new RectangleCommand(p1, p2);
		rect.setColor(Color.rgb(rgb[0], rgb[1], rgb[2]));
		rect.setFill(filled);
		this.commands.add(rect);
	}
	public void createSquiggle(String[] squiggleValues) {
		int[] rgb = parseRGB(squiggleValues[0]);
		boolean filled = parseBool(squiggleValues[1]);
		SquiggleCommand squig = new SquiggleCommand();
		squig.setColor(Color.rgb(rgb[0], rgb[1], rgb[2]));
		squig.setFill(filled);
		for(String s: pointData) {
			squig.add(parsePoint(s));
		}
		this.commands.add(squig);
	}
	
	public int[] parseRGB(String colors) {
		int[] rgb = new int[3];
		rgb[0]=0;
		rgb[1]=0;
		rgb[2]=0;
		Pattern p = Pattern.compile("(:\\d+)");
		Matcher m = p.matcher(colors);
		if(m.find()) {
			rgb[0] = Integer.parseInt(m.group(1).replaceAll(":", "")); //r
		}
		p = Pattern.compile("(,\\d+)");
		m = p.matcher(colors);
		if(m.find()) {
			rgb[1] = Integer.parseInt(m.group(1).replaceAll(",", "")); //g
		}
		p = Pattern.compile("(,\\d+){2}");
		m = p.matcher(colors);
		if(m.find()) {
			rgb[2] = Integer.parseInt(m.group(1).replaceAll(",", "")); //b
		}
		return rgb;
	}
	public boolean parseBool(String boolString) {
		boolean fill=false;
		Pattern p = Pattern.compile("(true|false)");
		Matcher m = p.matcher(boolString);
		if(m.find()) {
			fill = Boolean.parseBoolean(m.group(1));
		}
		return fill;
	}
	public Point parsePoint(String pointString) {
		int x=0;
		int y=0;
		Point point = new Point(x,y);
		
		Pattern p = Pattern.compile("(\\d+,\\d+)");
		Matcher m = p.matcher(pointString);
		if(m.find()) {
			String[] split = m.group(1).split(",");
			x = Integer.parseInt(split[0]);
			y = Integer.parseInt(split[1]);
			point.x = x;
			point.y =y;
		}
		return point;
	}
}
