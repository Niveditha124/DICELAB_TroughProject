function string = tag2str(i)
%TAG2STR   like int2str, but format integer (from 0 to 999) with a constant length of 3
% 
% Prepared by Herve Capart

if i<10
  string = ['00' int2str(i)];
elseif i<100
  string = ['0' int2str(i)];
else
  string = int2str(i);
end;