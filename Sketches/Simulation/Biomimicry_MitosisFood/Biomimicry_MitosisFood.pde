import traer.physics.*;

ParticleSystem ps;
Interface controls;

ArrayList<Cell> cells = new ArrayList();
FoodSource food;

boolean ENABLE_LIFESPAN = false;
boolean ENABLE_COHESION = true;

void initialize() {
  cells.add(new Cell(width / 2, height / 2));
}

void setup() {
  size(1100, 800);
  colorMode(HSB, 1.0);
  
  food = new FoodSource();
  ps = new ParticleSystem(0, 1.5);
  
  initialize();
  
  controls = new Interface(this);
  
  if (ENABLE_LIFESPAN) {
    controls.addSlider("minLifespan");
    controls.addSlider("maxLifespan");
  }
  
//  controls.addSlider("minGrowthInterval");
//  controls.addSlider("maxGrowthInterval");

  controls.addSlider("maxCellPopulation", 1, 300);
  controls.addSlider("systemDrag", 0.0, 2.5, 1.5);
  controls.addSlider("eatRate", 0.0, 0.2, 0.01);
  controls.addSlider("reproduceAfterEating", 0.0, 0.75, 0.5);
  
  controls.addButton("reset");
  
  noStroke();
  fill(0);
}

void eatRate(float value){
  for (int i = 0; i < cells.size(); i ++) {
    Cell c = cells.get(i);
    c.eatRate = value;
  }
}

void reproduceAfterEating(float value){
  for (int i = 0; i < cells.size(); i ++) {
    Cell c = cells.get(i);
    c.reproduceAfterEating = value;
  }
}

void systemDrag(float newDrag) {
  ps.setDrag(newDrag);
}

void reset(float dummy) {
  cells.clear();
  ps.clear();
  food.reset();
  initialize();
}

void draw() {
  food.draw();
  
  for (int i = 0; i < cells.size(); i ++) {
    Cell c = cells.get(i);
    c.tick();
    c.draw();
  }
  
  for (int i = 0; i < cells.size(); i ++) {
    Cell c = cells.get(i);
    c.checkForDeath();
  }
  
  ps.tick();
}

boolean looping = true;
void keyPressed(){
  
  if( key == 'p' ){
    // Toggle the animation on or off.
    if (looping) {
      looping = false;
      noLoop();
    }
    else {
      looping = true;
      loop();
    }
  }
  
  if (key == 'r')
    reset(0.0);
}


