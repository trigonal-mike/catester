classdef CodeAbilityTestOutputSpecification < handle

    properties
        type                (1,:) char = ''
        version             (1,:) char = ''
        timeStamp           (1,:) char = ''

        name                (1,:) char = ''
        description         (1,:) char = ''

        status              (1,:) char {mustBeMember(status,{'','SCHEDULED','PENDING','RUNNING','CANCELLED','COMPLETED','FAILED','CRASHED'})} = ''
        result              (1,:) char {mustBeMember(result,{'','FAILED','PASSED','SKIPPED','TIMEDOUT'})} = ''

        summary             (1,1) struct % check is missing, see fields below  
            % total           (1,:) double
            % success         (1,:) double   
            % failed          (1,:) double
            % skipped         (1,:) double

        statusMessage       (1,:) char
        resultMessage       (1,:) char

        % qualification     (1,:) char      % removed
        details             (1,:) char

        setup               (1,:) char 
        teardown            (1,:) char 

        duration            (1,1) double 
        executionDuration   (1,1) double


        environment         (1,1) struct % free fieldnames
        testProperties      (1,1) struct % free fieldnames
        debug               (1,1) struct % free fieldnames
        
        % testMetaInformation % removed

        tests           CodeAbilityTestOutputSpecification
         
    end % properties

    methods

    end % methods

end % classdef
