function kepco_set_output(curr,volt)
%% Set the output current and voltage of the KEPCO

    global kepco

    fprintf(kepco, ['CURR ' num2str(curr) ';VOLT ' num2str(volt)]);

end

