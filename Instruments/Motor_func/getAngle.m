function angle = getAngle()
%% Returns the current angle of the motor
    global h
    angle = h.GetPosition_Position(0);
end

