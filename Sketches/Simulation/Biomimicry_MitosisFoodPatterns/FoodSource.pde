class SpiralFood extends FoodSource {
  SpiralFood() {
    this.food = createGraphics(width, height);
    reset();
  }
  
  void setFood(){
    
    this.food.background(0.5, 0, 0);
    this.food.blendMode(BLEND);
    this.food.fill(1.0);
    this.food.noStroke();
    
    for (float r = 0; r < TWO_PI * 4; r += 0.01) {
      float x = 15 * r * cos(r) + width / 2;
      float y = 15 * r * sin(r) + height / 2;
      this.food.ellipse(x, y, 50, 50);
    }
    
  }
}

class CircularHoleFood extends FoodSource {
  CircularHoleFood() {
    this.food = createGraphics(width, height);
    reset();
  }
  
  void setFood(){
    this.food.background(1.0);
    this.food.blendMode(BLEND);
    this.food.fill(0.5, 0, 0);
    this.food.noStroke();
    
    int holeSize = 100;
    this.food.ellipse(width / 2 - holeSize / 2, height / 2 - holeSize / 2, holeSize, holeSize);
  }
}  

class FoodSource {
  PGraphics food;
  
  FoodSource() {
    this.food = createGraphics(width, height);
    reset();
  }
  
  void setFood(){
    this.food.background(1.0, 1.0, 1.0);
  }
  
  void reset(){
    this.food.beginDraw();
    this.food.colorMode(RGB, 1.0);
    this.food.noStroke();
    
    this.setFood();
    
    this.food.blendMode(DIFFERENCE);
    this.food.rectMode(CENTER);
    this.food.endDraw();
  }
  
  boolean isOnScreen(float x, float y){
    return x >= 0 && y >= 0 && x < width && y < height;
  }
  
  float getFoodAt(float x, float y){
    if (isOnScreen(x, y)) {
      this.food.loadPixels();
      color c = this.food.pixels[int(y) * width + int(x)];
      float tr = green(c);
      return tr;
    } else {
      return 0.0;
    }
  }
  
  void beginDraw(){
    this.food.beginDraw();
  }
  
  void endDraw(){
    this.food.endDraw();
  }
  
  void eatAt(float x, float y, float eatRate){
    this.food.fill(eatRate, eatRate, eatRate);
    this.food.ellipse(x, y, 5.0, 5.0);
  }
  
  void draw(){
    loadPixels();
    this.food.loadPixels();
    System.arraycopy( this.food.pixels, 0, pixels, 0, pixels.length );
    updatePixels();
  }

}



