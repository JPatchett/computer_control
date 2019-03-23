function kepco_set_volt(volt)
%% Set the voltage on the KEPCO
    global kepco

    fprintf(kepco, ['Volt ' num2str(volt)]);
    
end

