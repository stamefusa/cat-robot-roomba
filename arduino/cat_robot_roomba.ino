/**
 * https://4009.jp/post/archives/58 のコードを改変し流用
 */

#include <SoftwareSerial.h>

//指定されているオペレーションコードを設定
#define OP_START 128
#define OP_SAFE_MODE 131
#define OP_POWER 133
#define OP_DRIVE_PWM 146
#define OP_DIGIT_LED 164

//Arduinoへの接続ピン
#define rxPin 10
#define txPin 11
#define ddPin 2

int cnt = 0;  //ステップカウント用

SoftwareSerial iRobot(rxPin, txPin);

/*--------------------------------------------------------------------------*/
void setup() {

  //通信レートは初期値115200に設定
  iRobot.begin(115200);
  Serial.begin(115200);

  Serial.setTimeout(10); // SerialでのString受信のタイムアウト設定（ms）

  pinMode(ddPin, OUTPUT);

  //iRobot側の準備が出来るまでのWait設定
  delay(3000);

  Serial.println("iRobot Start");

  wakeUp();     //iRobot電源ON
  startSafe();  //セーフモードで起動

  Serial.println("Setup Completed");

  delay(1000);
}

/*--------------------------------------------------------------------------*/
void loop() {
  if (Serial.available() > 0) {
    String key = Serial.readStringUntil(';');
    key.trim();
    Serial.println(key);

    if (key == "w") {
      // 前進
      opDrivePWM(60, 60);
    } else if (key == "s") {
      // 後進
      opDrivePWM(-60, -60);
    } else if (key == "a") {
      // 左旋回
      opDrivePWM(60, 0);
    } else if (key == "d") {
      // 右旋回
      opDrivePWM(0, 60);
    } else if (key == "q") {
      // 停止
      opDrivePWM(0, 0);
    } else if (key == "z") {
      // 電源OFF
      powerOff();
    }
  }

 delay(100);
}

/*--------------------------------------------------------------------------*/
void wakeUp() {
  digitalWrite(ddPin, HIGH);
  delay(100);
  digitalWrite(ddPin, LOW);
  delay(500);
  digitalWrite(ddPin, HIGH);
  delay(2000);
}

/*--------------------------------------------------------------------------*/
void startSafe() {
  iRobot.write(OP_START);      //Start
  iRobot.write(OP_SAFE_MODE);  //Safe mode
  delay(1000);
}

/*--------------------------------------------------------------------------*/
void powerOff() {
  iRobot.write(OP_POWER);
}

/*--------------------------------------------------------------------------*/
void opDrivePWM(signed short rightPWM, signed short leftPWM) {

  iRobot.write(OP_DRIVE_PWM);
  iRobot.write(rightPWM >> 8);
  iRobot.write(rightPWM);
  iRobot.write(leftPWM >> 8);
  iRobot.write(leftPWM);
}