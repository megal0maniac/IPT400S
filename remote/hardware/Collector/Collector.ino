//Includes
#include "DHT.h" //Temp/humidity sensor

//Defines
#define DHTPIN 5 //Digital pin 5
#define WINDVANE 3 //Analogue 5
#define ANEMOMETER 2 //Interrupt pin
#define MARGIN 3 //Margin of error for wind vane
#define RAINGUAGE 3 //Digital 3 (Interrupt)

//Global variables (sorry Mr. Dixie)
//Temp sensor
DHT dht(DHTPIN, DHT22);
unsigned long lastReadWind = millis(), lastReadRain = millis();
float temp, humidity;
int rain = 0;

//Anemometer
unsigned long lastMillis, diff;
float currentws = 0;
float avgws[5] = {0,0,0,0,0};
unsigned int counter = 0;

//Wind vane
//const String cardinalPoints[] = {"N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"};
int windDirection[] = {786, 406, 461, 84, 93, 66, 185, 127, 287, 245, 630, 599, 945, 828, 887, 703};

//Aggregation
unsigned int avgCounterMinute = 0, avgCounterHour = 0, avgCounterDay = 0; //Array pointers
unsigned int lastSecond, lastMinute, lastHour;

void setup() {
	pinMode(WINDVANE, INPUT);
	pinMode(ANEMOMETER, INPUT_PULLUP);
	pinMode(RAINGUAGE, INPUT_PULLUP);
	attachInterrupt(digitalPinToInterrupt(ANEMOMETER), readAnemometer , FALLING);
	attachInterrupt(digitalPinToInterrupt(RAINGUAGE), readRain, FALLING);

	Serial.begin(115200);
	dht.begin();

}

void loop() {

	if(millis()%1000 == 0)
	{
	//Reset windspeed if no interrupts in 30s
		if(millis() - lastMillis > 30000) currentws = 0;
	}

	// if we get a byte of serial data, read analog ins:
	if (Serial.available() > 0) {
		// get incoming byte:
		Serial.read();

		Serial.print("{ 'wd' : ");
		Serial.print(readWindVane());
		Serial.print(", 'ws' : ");
		Serial.print(currentws);
		Serial.print(", 't' : ");
		Serial.print(readTemp());
		Serial.print(", 'h' : ");
		Serial.print(readHumidity());
		Serial.print(", 'rain' : ");
		Serial.print(rain);
		Serial.print(" }\r\n");
		rain = 0;
	}
}

//This function keeps a rolling buffer of the last 5 times and averages them.
//In the main loop, the buffer is reset if 30 seconds elapse with no wind detected.
void readAnemometer()
{
	diff = millis() - lastMillis;
	lastMillis = millis();

	if(diff > 10)
	{
		avgws[counter++%5] = 2400.0/diff;
		currentws = ((avgws[0]+avgws[1]+avgws[2]+avgws[3]+avgws[4])/5);
	}
}

void readRain()
{
	if ((millis() - lastReadRain) > 100)
	{
		rain++;
		lastReadRain = millis();
	}
}

//This function searches for the value in the lookup table which matches the reading.
//It allows for an error of +-MARGIN to account for noise, temperature etc.
int readWindVane()
{
	int i;
	for(i=0; i<16; i++)
	{
		int currentValue = analogRead(WINDVANE);
		if ((currentValue >= windDirection[i]-MARGIN) && (currentValue <= windDirection[i]+MARGIN))
		{
			return i; //Return array index for current wind direction
		}
	}
return NULL;
}

//Reads temperature from DHT22
float readTemp()
{
	cli();
	float t = dht.readTemperature();
	sei();

	if (isnan(t)) return NULL; //Check for read error
	else return t;
}

//Reads humidity from DHT22
float readHumidity()
{
	cli();
	float h = dht.readHumidity();
	sei();
	if (isnan(h)) return NULL; //Check for read error
	else return h;
}
