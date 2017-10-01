/**
 * Earthquakes sketch
 * 
 * Visualizes earthquake events gathered by USGS a graphic globe.
 */

import peasy.*;
import processing.opengl.*;

PeasyCam cam;
Globe globe;


void setup(){
  size(1280, 900, OPENGL);
  smooth();
  colorMode(HSB);
  
  cam = new PeasyCam(this, 1400);
  globe = new Globe("equirectangular_projection.jpg");
  
  loadQuakesCSV("earthquakes_2010_10.csv");
  loadQuakesCSV("earthquakes_2012_05.csv");
  loadQuakesCSV("earthquakes_2013_12.csv");
}


void draw(){
  background(0);
  
  // Puts the default rotation over North America and ensures the flat map 
  // is oriented with respect to the western hemisphere.
  rotateX(-0.75 * PI * transformFactor);

  globe.draw();
  drawQuakes();
  
  handleTransform();
}


ArrayList<Quake> quakes = new ArrayList();

void drawQuakes(){
  for(int i = 0; i < quakes.size(); i++){
    Quake q = quakes.get(i);
    q.draw();
  }
}



