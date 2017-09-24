/** 
 * This module holds helpers that parse CSV data files and loads the Quakes.
 */


/**
 * Loads a list of earthquake events from a CSV file.
 */
void loadQuakesCSV(String filename){
  String[] quakeStrings = loadStrings(filename);
  
  String headerRow = quakeStrings[0];
  String[] headers = split(headerRow, ",");
  
  QuakeParseSchema schema = new QuakeParseSchema(headers);
  
  for(int i = 1; i < quakeStrings.length; i++){
    String[] quakeData = split(quakeStrings[i], ",");
    
    quakes.add(new Quake(quakeData, schema));
  }
}

/**
 * Return the index of a string in an array of strings.
 */
int indexOf(String[] haystack, String needle){
  // Search linearly instead of using java.util for future compatibility with Processing.js.
  for (int i=0; i<haystack.length; i++){
    if (haystack[i] == needle) return i;
  }
  return -1;
}

/**
 * Return the index of the first keyword found in an array of strings.
 */
int indexOfKeyword(String[] haystack, String[] keywords){
  for (int i = 0; i < keywords.length; i ++){
    int index = indexOf(haystack, keywords[i]);
    if (index != -1) return index;
  }
  return -1;
}

/**
 * Encapsulates the parsing logic that finds the columns needed to produce a list of quakes.
 * Ensures that we can handle multiple CSV formats coming from USGS.
 */
class QuakeParseSchema {
  String[] headers;
  
  int latitudeColumn;
  int longitudeColumn;
  int magnitudeColumn;
  int depthColumn;
  
  QuakeParseSchema(String[] headers){
    this.headers = headers;
    
    this.latitudeColumn = getLatitudeColumn();
    this.longitudeColumn = getLongitudeColumn();
    this.magnitudeColumn = getMagnitudeColumn();
    this.depthColumn = getDepthColumn();
  }
  
  int getLatitudeColumn(){
    String[] keywords = {"Latitude", "Lat", "latitude", "lat"};
    return indexOfKeyword(this.headers, keywords);
  }
  
  int getLongitudeColumn(){
    String[] keywords = {"Longitude", "Lon", "longitude", "lon"};
    return indexOfKeyword(this.headers, keywords);
  }
  
  int getMagnitudeColumn(){
    String[] keywords = {"Magnitude", "Mag", "mag", "magnitude"};
    return indexOfKeyword(this.headers, keywords);
  }
  
  int getDepthColumn(){
    String[] keywords = {"Depth", "depth"};
    return indexOfKeyword(this.headers, keywords);
  }
  
  float getLatitude(String[] event){
    return float(event[this.latitudeColumn]);
  }
  
  float getLongitude(String[] event){
    return float(event[this.longitudeColumn]);
  }
  
  float getMagnitude(String[] event){
    return float(event[this.magnitudeColumn]);
  }
  
  float getDepth(String[] event){
    return float(event[this.depthColumn]);
  }
}



