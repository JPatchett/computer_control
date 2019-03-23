function  moving = isMoving
%ISMOVING: Returns whether or not the motor is moving or not

global h

%Get the status bits from the motor
StatusBits = h.GetStatusBits_Bits(0);

%Will return 1 if moving, 0 is stationary
moving = xor(bitget(abs(StatusBits),5),bitget(abs(StatusBits),6));

end

