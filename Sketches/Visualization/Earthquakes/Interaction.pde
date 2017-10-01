/**
 * Holds Processing event handlers.
 *
 * +/-     Changes the spacing between dots on the globe.
 * [space] Toggles the backface rendering of the globe.
 * t       Toggles between a globe and flat map.
 * r       Exports a PNG file of the current view.
 */
void keyPressed(){
  if (key == '+' || key == '='){
    globe.dotSpacing += 0.1;
    globe.build();
  
  } else if (key == '-') {
    globe.dotSpacing -= 0.1;
    globe.build();
    
  } else if (key == ' ') {
    globe.toggleShowThrough();
    
  } else if (key == 't') {
    if (transformState == NOT_TRANSFORMING && isSphere()) {
      transformState = TO_FLAT;
      transformFrame = 0;
      
    } else if (transformState == NOT_TRANSFORMING && isFlat()) {
      transformState = TO_SPHERE;
      transformFrame = 0;
      
    }
    
  } else if (key == 'r') {
    saveFrame("earthquake-####.png");
    
  }
}

