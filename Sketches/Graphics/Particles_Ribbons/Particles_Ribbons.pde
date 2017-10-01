/**
 * A painterly particle simulation.
 */

import traer.physics.*;

// System parameters.
final int NUM_PARTICLES = 100;
final float PARTICLE_MASS = 3;
final float DRAG = 0.5;

// Attraction.
final float MIN_ATTRACTION = 0;
final float MAX_ATTRACTION = 100;
final float ATTRACTION_MULTIPLIER = 1;

// Node drawing parameters.
final float MIN_RADIUS = 10;
final float MAX_RADIUS = 100;      // 50
final float ROTATION_SPEED = 0.01; // radians

// Colors.
final color BACKGROUND_COLOR = color(0);
final int ALPHA_VALUE = 2;

// Globals.
ParticleSystem ps;
ArrayList<Node> nodes = new ArrayList();


// --------------------------------------------------------------------------------

void setup(){
  size( 1200, 600 );
  ps = new ParticleSystem( 0, DRAG );
  
  smooth();
  colorMode( HSB );
  
  initialize();
}

void draw(){
  for( int i=0; i<nodes.size(); i++ ){
    Node n = nodes.get(i);
    n.draw();
  }
  ps.tick();
}

// --------------------------------------------------------------------------------

void initialize(){
  background( BACKGROUND_COLOR );
  
  // Get rid of everthing, all particles, nodes, and forces.
  ps.clear();
  nodes.clear();
  
  // Make the particles.
  for( int i=0; i<NUM_PARTICLES; i++ ){
    Particle p = ps.makeParticle(
      PARTICLE_MASS,
      random(0, width),   // x
      random(0, height),  // y
      0                   // z
      );
    
    Node n = new Node(p);
    nodes.add(n);
  }
  
  // Make all the attractions between all particles, but not between a particle and itself.
  for( int j = 0; j < ps.numberOfParticles(); j++ ){
    for ( int i = 0; i < ps.numberOfParticles(); ++i ){
      
      Particle p = ps.getParticle( i );
      Particle q = ps.getParticle( j );
      
      if ( p != q  ){
        float attraction = random(MIN_ATTRACTION, MAX_ATTRACTION) * ATTRACTION_MULTIPLIER;
        ps.makeAttraction(p, q, attraction, 100);
      }
    }
  }
}


