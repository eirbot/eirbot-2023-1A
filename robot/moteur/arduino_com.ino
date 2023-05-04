// Authors: Charlène Vernant, Arthur Hausswald
// Control a stepper motor with A4988 stepper motor driver and Arduino without a library.


// Define stepper motor connections and steps per revolution:
// Personnal values to adapt
#include <Arduino.h>

#define NB_MOTORS 2
int step_pins[]={8, 4};
int dir_pins[]={4, 7};
#define stepsPerRevolution 100

// string received from serial
char compared_forward[]  = {'f','w','d','\0'};
char compared_backward[]  = {'b','w','d','\0'};

void spin_forward(int nb_revolution, int id_motor){
    digitalWrite(dir_pins[id_motor], LOW);
    for (int i = 0; i < nb_revolution * stepsPerRevolution; i++) {
        digitalWrite(step_pins[id_motor], HIGH);
    }
}

void spin_backward(int angle, int id_motor){
    digitalWrite(dir_pins[id_motor], HIGH);
    for (int i = 0; i < angle * stepsPerRevolution; i++) {
        digitalWrite(step_pins[id_motor], HIGH);
    }
}

#define MAX_ARG_VALUE 10
char* arguments[MAX_ARG_VALUE];
    
int parse_argument(char* str, const char * separators){
    int i=0;
    //on coupe l'array de char pour récupérer le premier élément (cette méthode ne fonctionne que sur des array de char)
    char * strToken = strtok ( str, separators );
    for(i=0; i<MAX_ARG_VALUE && strToken != NULL; i++ ){
        arguments[i] = strToken;
        strToken = strtok ( NULL, separators);
    }
    return i;
}  



void setup() {
    Serial.begin(9600);
    Serial.setTimeout(1);
    
    // Declare pins as output:
    for(int i=0; i< NB_MOTORS; i++){
        pinMode(step_pins[i], OUTPUT);
        pinMode(dir_pins[i], OUTPUT);
    }
}

void print_error(){
  Serial.println("Invalid command");
}

String response;

#define MAX_SIZE 256
char res[MAX_SIZE];

char * order;

void loop() {
    /*
    while(Serial.available()>0){

        // read the string until the newline character:
        response=Serial.readString();

        // copy the string to res and a string terminator
        strncpy(res, response.c_str(),MAX_SIZE-1);
        res[MAX_SIZE-1] = '\0';

        // parse the string and get the number of arguments
        int nb_arg = parse_argument(response, " ");

        if (nb_arg == NB_MOTORS+1){
            char* order = arguments[0];
            if (strcmp(order, compared_forward) == 0){
                for (int i=0; i < NB_MOTORS; i++){
                    int nb_revolution = atoi(arguments[i+1]);
                    int id_motor = i;
                    spin_forward(nb_revolution, id_motor);
                }
            }
            else if (strcmp(order, compared_backward) == 0){
                for (int i=0; i < NB_MOTORS; i++){
                    int nb_revolution = atoi(arguments[i+1]);
                    int id_motor = i;
                    spin_backward(nb_revolution, id_motor);
                }
            }
        }
    }*/
    spin_forward(5, 0);
    spin_forward(5, 1);
    delay(3000);
    spin_backward(5, 0);
    spin_backward(5, 1);
}
