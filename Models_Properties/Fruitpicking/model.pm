dtmc

const double t1;
const double t2;
const double t3;

const double e1;
const double e2;
const double e3;



const double p1 = 0.9;
const double p2 = 0.95;
const double p3 = 0.6;
const double alpha;
const double beta;

const int positioning      = 0;
const int picking          = 1;
const int pickingAbandoned = 2;
const int decision         = 3;
const int pickingsuccess   = 4;
const int done	           = 5;


module mainflow
    s:[0..5]init 0;

    []s  = positioning -> (1-(alpha*p1)):(s'=pickingAbandoned) + (alpha*p1):(s'=picking);
    []s  = picking -> (beta*p2):(s'=pickingsuccess) + (1-(beta*p2)):(s'=decision);
    []s  = decision-> p3:(s'=positioning) + (1-p3):(s'=pickingAbandoned); 	 
    []s  = pickingAbandoned -> 1:(s'=done); 
    []s  = pickingsuccess -> 1:(s'=done);
    []s  = done -> 1:(s'=done);  	
endmodule


rewards "totalTime"
	s=0:t1; s=1:t2; s=2:t3;
	
	
endrewards

rewards "totalCost"
	s=0:e1;
	s=1:e2;
	s=2:e3;
endrewards
