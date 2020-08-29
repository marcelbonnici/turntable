// inChar Resource: https://www.arduino.cc/en/Tutorial.StringToIntExample
// Stepper Motor Resource: https://github.com/ItKindaWorks/How-To-Wire-It/blob/master/stepper/stepper_demo/stepper_demo.ino
const int stepPin = 2;
const int dirPin = 3;
int steps;
String inString = "";

void setup(){
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  Serial.begin(9600);
}

void loop(){
    steps=0;
    while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (inChar!='\n') {//isDigit(inChar)
      // convert the incoming byte to a char and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
      Serial.print("Value:");
      steps=inString.toInt();
      Serial.println(steps);
      // clear the string for new input:
      inString = "";
    }
    if (steps>0){
      digitalWrite(dirPin,LOW);
    }
    if (steps<0){
      digitalWrite(dirPin,HIGH);
      steps=steps*-1;
    }
    for(int i = 0; i < steps; i++){
      digitalWrite(stepPin, HIGH);
      delay(1);
      digitalWrite(stepPin, LOW);
      delay(1);
    }
}
}
      
