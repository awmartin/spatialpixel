import traer.physics.*;

ParticleSystem ps;
Interface controls;

ArrayList<Cell> cells = new ArrayList();


void setup() {
  size(1100, 800);
  
  ps = new ParticleSystem(0, 1.5);
  
  initialize();
  
  controls = new Interface(this);
  controls.addSlider("minDeathTime");
  controls.addSlider("maxDeathTime");
  controls.addSlider("minGrowthInterval");
  controls.addSlider("maxGrowthInterval");
  controls.addSlider("maxNodePopulation", 1, 300);
  controls.addSlider("systemDrag", 0.0, 2.5, 1.5);
  controls.addButton("reset");
  
  noStroke();
  fill(0);
}

void initialize() {
  cells.add(new Cell(width / 2, height / 2));
}

void systemDrag(float newDrag) {
  ps.setDrag(newDrag);
}

void reset(float dummy) {
  cells.clear();
  ps.clear();
  initialize();
}

void draw() {
  background(255);
  
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

