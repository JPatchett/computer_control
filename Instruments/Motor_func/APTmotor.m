%Script for controlling the ATP motor
clear; close all; clc;
global h;

fpos = get(0, 'DefaultFigurePosition');
fpos(3) = 650;
fpos(4) = 430;


f = figure('Position', fpos,...
            'Menu','None',...
            'Name','ATP GUI',...
            'Visible', 'on');
        
 h = actxcontrol('MGMOTOR.MGMotorCtrl.1', [20 20 600 400], f);

h.StartCtrl;

SN = 83848101;
set(h, 'HWSerialNum', SN);

h.Identify;
