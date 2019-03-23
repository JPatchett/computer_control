function open_kepco(address)
    %% Function that opens the KEPCO 

    %% Check there are no open connections, if there are, delete them

    connec = instrfind;
    if isempty(connec) == 0
        fclose(connec);
        delete(connec);
        clear connec
    end
    
    disp('Cleared connections');
    
    %% Connect to the KEPCO
    global kepco
    
    disp('Opening KEPCO')
    kepco = visa('ni',address);
    fopen(kepco);
    disp('Success')

    %% Test communication with the KEPCO
    %Query and display the ID
    fprintf(kepco, '*IDN?');
    disp(fscanf(kepco));

end

