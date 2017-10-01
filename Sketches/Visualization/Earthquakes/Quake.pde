final int COLOR_SCALE = 192;

class Quake {
  float latitude;
  float longitude;
  float magnitude;
  float depth;
  
  Quake(String[] event, QuakeParseSchema schema){
    parseQuakeData(event, schema);
  }
  
  void parseQuakeData(String[] event, QuakeParseSchema schema){
    
    this.latitude = schema.getLatitude(event);
    this.longitude = schema.getLongitude(event);
    this.magnitude = schema.getMagnitude(event);
    this.depth = schema.getDepth(event);
  
  }
  
  float x(){
    return (this.longitude + 180) * globe.scalePixelsPerLongitude;
  }
  
  float y(){
    return (-this.latitude + 90) * globe.scalePixelsPerLatitude;
  }
  
  void draw(){
    stroke(COLOR_SCALE - this.magnitude / 10.0 * COLOR_SCALE, 255, 255);
    strokeWeight(this.magnitude / 10.0 + 1.0);
    
    pushMatrix();
    transformToSphere(this.x(), this.y());
    
    // Draw a line showing the magnitude of the Quake by length.
    line(0, 0, 0, 0, 0, pow(magnitude, 1.1) * 10);
    popMatrix();
  }
}

