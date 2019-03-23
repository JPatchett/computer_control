function output = kepco_query_on()
    %% Find out if the kepco is on or not
    
    global kepco
    
    fprintf(kepco, 'OUTP?');
    output = fscanf(kepco);
    
end

