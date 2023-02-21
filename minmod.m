function c = minmod(a,b)
%MINMOD minmod function according to Nujic (1995)

ab = a.*b;
c = (ab>0).*( (abs(a)<abs(b)).*a + ~(abs(a)<abs(b)).*b );
