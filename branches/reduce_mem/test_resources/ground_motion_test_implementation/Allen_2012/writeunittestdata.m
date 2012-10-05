% writeunittestdata.m

header = ['UNIT TEST DATA FOR ALLEN (2012) GMPE FOR EASTERN AUSTRALIA',char(10), ...
         'DATA ARE INDICATED IN 5% DAMPED RESPONSE SPECTRAL ACCELERATION AT DIFFERENT SPECTRAL PERIODS', ...
         char(10),'FORMAT: PERIOD (SEC) LOG10 PSA (CM/S/S)',char(10)];
m = [4.5 5.5 6.5 7.5];
r = [20 50 100 200];
h = [7 14];

dlmwrite('All12.unit_test_data.txt',header,'delimiter','');

for i = 1:length(m)
    for j = 1:length(r)
        for k = 1:length(h)
            [T A12] = plotAll12(m(i),r(j),h(k));
            testhead = ['MW = ',num2str(m(i),'%0.1f'), ...
                        '; Rrup = ',num2str(r(j)), ...
                         '; h = ',num2str(h(k))];
            dlmwrite('All12.unit_test_data.txt',testhead,'delimiter','', ...
                     '-append');
            dlmwrite('All12.unit_test_data.txt',[T log10(A12)],'delimiter','\t', ...
                     'precision','%0.4f','-append');
%             dlmwrite('All12.unit_test_data.txt',['',char(10)],'-append'); % new line
         end
     end
 end

