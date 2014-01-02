import controlP5.*;

class Interface {
  ControlP5 cp5;
  int currentHorizontalPosition;
  int currentVerticalPosition;
  
  Interface(PApplet parent) {
    this.cp5 = new ControlP5(parent);
    this.cp5.enableShortcuts();
    
    this.currentHorizontalPosition = 20;
    this.currentVerticalPosition = 40;
  }
  
  void addSlider(String sliderName){
    int minValue = 0;
    int maxValue = 100;
    this.cp5.addSlider(sliderName)
      .setPosition(this.currentHorizontalPosition, this.currentVerticalPosition)
      .setRange(minValue, maxValue)
      .setColorLabel(color(64));
    this.currentVerticalPosition += 25;
  }
  
  void addSlider(String sliderName, float minValue, float maxValue) {
    this.cp5.addSlider(sliderName)
      .setPosition(this.currentHorizontalPosition, this.currentVerticalPosition)
      .setRange(minValue, maxValue)
      .setColorLabel(color(64));
    this.currentVerticalPosition += 25;
  }
  
  void addSlider(String sliderName, float minValue, float maxValue, float defaultValue) {
    this.cp5.addSlider(sliderName)
      .setPosition(this.currentHorizontalPosition, this.currentVerticalPosition)
      .setRange(minValue, maxValue)
      .setColorLabel(color(64))
      .setValue(defaultValue);
    this.currentVerticalPosition += 25;
  }
  
  void addButton(String buttonName){
    this.cp5.addButton(buttonName)
      .setPosition(this.currentHorizontalPosition, this.currentVerticalPosition)
      .setValue(0.0);
    this.currentVerticalPosition += 40;
  }
}

