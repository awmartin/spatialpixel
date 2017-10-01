/**
 * Holds a single particle and draws a rotating line at the particle's center.
 */
class Node {
  Particle p;
  float angle;
  float radius;
  color c;
  
  Node(Particle p){
    this.p = p;
    
    angle = random( 0, TWO_PI );
    radius = random( MIN_RADIUS, MAX_RADIUS );
    c = color( random( 0, 255 ), 255, 255, ALPHA_VALUE );
  }
  
  void draw(){
    angle += ROTATION_SPEED;
    float x = radius * cos( angle ) + p.position().x();
    float y = radius * sin( angle ) + p.position().y();
    stroke(c);
    line( p.position().x(), p.position().y(), x, y );
  }
}

