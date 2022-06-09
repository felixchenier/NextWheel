#include "IMU.h"


IMU::IMU(unsigned char address)
:   m_i2c_address(address) {

}

void IMU::begin() {
    // Initialize the IMU
    m_bmx160.begin();

    // Set Range
    m_bmx160.setAccelRange(eAccelRange_8G);
    m_bmx160.setGyroRange(eGyroRange_2000DPS);


}

void IMU::update() {

  sBmx160SensorData_t Omagn, Ogyro, Oaccel;

  /* Get a new sensor event */
  m_bmx160.getAllData(&Omagn, &Ogyro, &Oaccel);

  /* Display the magnetometer results (magn is magnetometer in uTesla) */
  Serial.print("M ");
  Serial.print("X: "); Serial.print(Omagn.x); Serial.print("  ");
  Serial.print("Y: "); Serial.print(Omagn.y); Serial.print("  ");
  Serial.print("Z: "); Serial.print(Omagn.z); Serial.print("  ");
  Serial.println("uT");

  /* Display the gyroscope results (gyroscope data is in g) */
  Serial.print("G ");
  Serial.print("X: "); Serial.print(Ogyro.x); Serial.print("  ");
  Serial.print("Y: "); Serial.print(Ogyro.y); Serial.print("  ");
  Serial.print("Z: "); Serial.print(Ogyro.z); Serial.print("  ");
  Serial.println("g");

  /* Display the accelerometer results (accelerometer data is in m/s^2) */
  Serial.print("A ");
  Serial.print("X: "); Serial.print(Oaccel.x    ); Serial.print("  ");
  Serial.print("Y: "); Serial.print(Oaccel.y    ); Serial.print("  ");
  Serial.print("Z: "); Serial.print(Oaccel.z    ); Serial.print("  ");
  Serial.println("m/s^2");

  Serial.println("");
}


