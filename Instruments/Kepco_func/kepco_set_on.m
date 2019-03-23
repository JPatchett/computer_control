function kepco_set_on(on)

    global kepco 

    if(on == 1) %Turn on
       fprintf(kepco, 'OUTP ON');

    elseif(on == 0) %Turn off
        fprintf(kepco, 'OUTP OFF');

    end

end

