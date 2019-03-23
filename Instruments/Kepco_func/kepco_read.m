function data = kepco_read(type)
%% Measure the current (type = 0) or voltage (type = 1) outputed by the KEPCO

    global kepco %Visa object that holds the kepco

    %Query the kepco for the relevant data
    if(type == 0)
        fprintf(kepco, 'MEAS:CURR?');
        data = fscanf(kepco);

    elseif(type == 1)
        fprintf(kepco, 'MEAS:VOLT?');
        data = fscanf(kepco);
    end

end

