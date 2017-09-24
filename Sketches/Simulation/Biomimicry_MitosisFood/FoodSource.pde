class FoodSource {
  float[] food;
  
  float[] eatPattern = {
    0.0, 1.0, 1.0, 1.0, 0.0,
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 1.0, 0.0
  };
  
  FoodSource() {
    this.food = new float[width * height];
    reset();
  }
  
  void reset(){
    for (int i=0; i < width * height; i ++)
      this.food[i] = 1.0;
  }
  
  boolean isOnScreen(float x, float y){
    return x >= 0 && y >= 0 && x < width && y < height;
  }
  
  float getFoodAt(float x, float y){
    if (isOnScreen(x, y)) {
      int index = int(y) * width + int(x);
      return this.food[index];
    } else {
      return 0.0;
    }
  }
  
  void eatAt(float x, float y, float eatRate){
    if (this.getFoodAt(x, y) - eatRate < 0.0){
      if (isOnScreen(x, y)){
        int index = int(y) * width + int(x);
        this.food[index] = 0.0;
      }
    } else {
      for (int k=0; k < eatPattern.length; k ++){
        int ex = int(k % 5) - 2;
        int ey = int(k / 5) - 2;
        if (isOnScreen(x + ex, y + ey)){
          int index = int(y + ey) * width + int(x + ex);
          this.food[index] -= eatPattern[k] * eatRate;
        }
      }
    }
  }
  
  void draw(){
    loadPixels();
    for (int i=0; i < width * height; i ++){
      pixels[i] = color(this.food[i], 0.8 * (1.0 - this.food[i]), 1.0);
    }
    updatePixels();
  }

}



