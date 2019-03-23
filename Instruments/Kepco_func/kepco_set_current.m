function kepco_set_current(curr)
%% Set's the current on the KEPCO

    global kepco

    fprintf(kepco, ['Curr ' num2str(curr)]);

end

