
boolean looping = true;
void keyPressed(){
  if( key == 'p' ){
    // Toggle the animation on or off.
    if( looping ){
      looping = false;
      noLoop();
    } else {
      looping = true;
      loop();
    }
    
  }
  else
  if (key == 'r'){
    // Resets the entire simulation.
    initialize();
    
  }
  else
  if (key == 'f'){
    // Reverses the attractive/repulsive forces.
    flip();
  }
}

/**
 * Reverses the attractive forces to become repulsive, and vice versa.
 */
void flip(){
  for( int i=0; i<ps.numberOfAttractions(); i++ ){
    Attraction a = ps.getAttraction(i);
    a.setStrength( -a.getStrength() );
  }
  
  jitter();
}

/**
 * This function adds a small random value to the x- and y-coordinates of all known
 * particles. This ensures that if any particles have converged to a single point, 
 * that they repel each other and diverge again. Otherwise, we get thickened paths
 * that imbalance the composition. 
 */
void jitter(){
  for ( int i = 0; i < ps.numberOfParticles(); ++i ){
    Particle p = ps.getParticle( i );
    p.position().set( p.position().x() + random(-1, 1), p.position().y() + random(-1, 1), 0.0 );
  }
}

