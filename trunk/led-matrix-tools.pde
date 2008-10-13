/* SPI by Hand
Originally by by Sebastian Tomczak, 20 July 2007
Adelaide, Australia

Updated by Scott Kirkwood,
Belo Horizonte, Brazil
*/

int CS1 = 2; // Chip select
int CLK = 3; // set clock pin
int MOSI = 4; // set master out, slave in
byte OFF = B00; // command byte LED off
byte RED = B01; // command byte LED red on
byte GRE = B10; // command byte LED green on
byte ORA = B11; // BOTH red and green, orage.
int index = 0;

byte message[64] = {
  RED, GRE, ORA, OFF, RED, GRE, ORA, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
  OFF, RED, RED, GRE, GRE, RED, RED, OFF, 
};

void writeMessage(int pin, byte message[64]) {
  start(pin);
  for (int i = 0; i < 64; i++) {
    spi_transfer(message[i]);
  }
  stop(pin);
}

void start(int pin) {
  digitalWrite(pin, LOW);
  delay(1);
}

void stop(int pin) {
  delay(1);
  digitalWrite(pin, HIGH);
}

void spi_transfer(byte working) {
  for(int i = 0; i < 8; i++) { // setup a loop of 8 iterations, one for each bit
    delayMicroseconds(10);
    if (working > 127) { // test the most significant bit 
      digitalWrite(MOSI, HIGH); // if it is a 1 (ie. B1XXXXXXX), set the master out pin high
    }
    else {
      digitalWrite(MOSI, LOW); // if it is not 1 (ie. B0XXXXXXX), set the master out pin low
    }
    delayMicroseconds(10);
    digitalWrite(CLK,HIGH); // set clock high, the pot IC will read the bit into its register
    delayMicroseconds(10);
    digitalWrite(CLK,LOW); // set clock low, the pot IC will stop reading and prepare for the next iteration
    working = working << 1;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(CS1, OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(MOSI, OUTPUT);
  digitalWrite(CS1, HIGH);
  
  writeMessage(CS1, message); // High means ignore
  index = 0;
}

void loop() {
  byte chr;
  if (Serial.available()) {
    chr = Serial.read();
    byte b = OFF;
    switch (chr) {
      case 'R':
        b = RED;
        break;
      case 'G':
        b = GRE;
        break;
      case 'O':
        b = ORA;
        break;
      case '\n':
        index = 0;
        return;
        break;
    }
    message[index] = b;
    index++;
    if (index >= 64) {
      writeMessage(CS1, message);
      index = 0;
    }
  }
}
