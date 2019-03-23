function angle = moveAbs(pos)
%MOVEREL: Move the motor to the "pos" position and return the
%final angle "angle"
global h

h.SetRelMoveDist(0, pos);
h.MoveRelative(0,1==0);

%Wait until the move is complete by checking for whether the motor is still
%moving
while isMoving()
    pause(0.5)

angle = getAngle();

end