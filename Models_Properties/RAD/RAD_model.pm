dtmc


const int ff = 17;
const int cc = 18;

//Useful labels
label "fail" = s=ff;
label "complete" = s=cc;
label "end" = s=19;
label "correction" = s=13;

const double p1 = 0.95;
//const double p_ovUser = 0.5;

module mainFlow

    s : [0..19] init 0;
    [LFG_s]  s=0 -> (s'=1); // Look For Garment
    [LFG_c]  s=1 -> (s'=2);
    [LFG_f]  s=1 -> (s'=ff);

    [MEE_s] s=2 -> (s'=3); // Move EE into place and pick up garment
    [MEE_c] s=3 -> (s'=4);
    [MEE_f] s=3 -> (s'=ff);


    [MVU_s] s=4 -> (s'=5); // Move towards user
    [MVU_c] s=5 -> (s'=6);
    [MVU_f] s=5 -> (s'=ff);

    [DTP_s] s=6 -> (s'=7); // Determine Pose
    [DTP_c] s=7 -> (s'=8);
    [DTP_f] s=7 -> (s'=ff);

    
    [TJP_s] s=8 -> (s'=9); // Trajectory Planning
    [TJP_c] s=9 -> (s'=10);
    [TJP_f] s=9 -> (s'=ff);

    [MVG_s] s=10 -> (s'=11); // Move garment
    [MVG_snag] s=11 -> (s'=12);
    [MVG_traj] s=11 -> (s'=8);
    [MVG_pose] s=11 -> (s'=6);
    [MVG_c] s=11 -> (s'=14);

    
    [PFC_s] s=12 -> (s'=13); // Perform Correction
    [PFC_c] s=13 -> (s'=14);
    [PFC_f] s=13 -> (s'=ff);

    [DComplete] s=14 -> p1:(s'=cc) + (1-p1):(s'=10);

 
    [Failed]   s=ff -> (s'=19); // This state means that the dressing failed
    [Complete] s=cc -> (s'=19);
    [End] s=19-> (s'=19);



endmodule



// ------------ STAGE 1 - Look for garment -----------------------
const double p2;//= 0.3; // probability of finding the garment at the first attempt
//const double p3;// = 0.5; // probability of finding the garment at the second attempt
//const double p4;// = 0.7; // probability of finding the garment at the third attempt

// for this module the robot tries to findthe garment a number of times before giving up
// Synchronises with the mainFlow on the [LFG_s, LFG_c]
// note that LFG_1/2 means look for garment retry number 1/2

module LookingForGarment_Robot
    tLook : [0..3] init 0;
    gFound : [0..1] init 0; // garment found: 0 false, 1 true
    [LFG_s] tLook=0 & gFound=0 -> p2:(gFound' = 1)+ (1-p2):(tLook' = 1); // found without help
    [LFG_1] tLook=1 & gFound=0 -> p2*1.4:(gFound' = 1)+ (1-(p2*1.4)):(tLook' = 2); // User asked to talk
    [LFG_2] tLook=2 & gFound=0 -> p2*1.7:(gFound' = 1)+ (1-(p2*1.7)):(tLook' = 3); // user asked to fetch
    [LFG_f] tLook = 3 -> (tLook'=3);
    [LFG_c] gFound = 1 -> (gFound'=1);
endmodule


// ------------ STAGE 2 - Move EE into place and pick up garment -----------------------
const double p3;// = 0.3; // probability of correctly handling garment at the first attempt
//const double p6 ;//= 0.5; // probability of correctly handling garment at the second attempt
//const double p7 ;//= 0.7; // probability of correctly handling garment at the third attempt


module moveEE_Robot
    reorient : [0..3] init 0;
    cMove : [0..1] init 0; // Completed move : 0 false, 1 true
    // We might not need to re-orient
    [MEE_s] reorient=0 & cMove=0 -> p3:(cMove' = 1)+ (1-p3):(reorient' = 1);
    // After reorienting once is it all OK?
    [MEE_1] reorient=1 & cMove=0 -> p3*1.3:(cMove' = 1)+ (1-(p3*1.3)):(reorient' = 2);
    // After reorienting twice is it all OK?
    [MEE_2] reorient=2 & cMove=0 -> p3*1.6:(cMove' = 1)+ (1-(p3*1.6)):(reorient' = 3);
    // Give up.
    [MEE_f] reorient = 3 -> (reorient'=3);
    [MEE_c] cMove = 1 -> (cMove'=1);
endmodule



// ------------ STAGE 3 - Move Towards the User  -----------------------
const double p4 = 0.95; // probability of moving correctly
const double p5 = 0.2;
module move2U_Robot
    moved : [0..3] init 0; // 0 moved requested, 1 move successful, 2 move failed, 3 give up
    [MVU_s] moved=0 -> p4:(moved'=1) + (1-p4):(moved'=2);
    [MVU_r] moved=2 -> (1-p5):(moved'=3) + (p4*p5):(moved'=1) + ((1-p4) *p5):(moved'=2);
    [MVU_f] moved = 3 -> (moved'=2);
    [MVU_c] moved = 1 -> (moved'=1); // No looks back here so no need to reset
endmodule


// ------------ STAGE 4 - Determine Pose -----------------------
const double p6;// = 0.6; // probability of correctly handling garment at the first attempt
//const double p11 ;//= 0.7; // probability of correctly handling garment at the second attempt
//const double p12 ;//= 0.9; // probability of correctly handling garment at the third attempt

module detectPose_Robot
    detectP : [0..3] init 0;
    cPose : [0..1] init 0; // Completed pose detection : 0 false, 1 true
    // We might not need to detect again
    [DTP_s] detectP=0 & cPose=0 -> p6:(cPose' = 1)+ (1-p6):(detectP' = 1);
    // 2nd attempt at detecting
    [DTP_1] detectP=1 & cPose=0 -> p6*1.2:(cPose' = 1)+ (1-p6*1.2):(detectP' = 2);
    // 3rd attempt at detecting
    [DTP_2] detectP=2 & cPose=0 -> p6*1.5:(cPose' = 1)+ (1-p6*1.5):(detectP' = 3);
    // Give up.
    [DTP_f] detectP = 3 -> (detectP'=0) & (cPose'=0); // reset in case we end up back here
    [DTP_c] cPose = 1 -> (detectP'=0) & (cPose'=0);
endmodule


module TrajectoryPlanning_Robot
    planStep : [0..3] init 0;
    cPlan : [0..1] init 0; // Completed plan : 0 false, 1 true
    // We might not need to detect again
    [TJP_s] planStep=0 & cPlan=0 -> p6:(cPlan' = 1)+ (1-p6):(planStep' = 1);
    // 2nd attempt at detectingp
    [TJP_1] planStep=1 & cPlan=0 -> p6*1.2:(cPlan' = 1)+ (1-p6*1.2):(planStep' = 2);
    // 3rd attempt at detecting
    [TJP_2] planStep=2 & cPlan=0 -> p6*1.4:(cPlan' = 1)+ (1-p6*1.4):(planStep' = 3);
    // Give up.
    [TJP_f] planStep = 3 -> (planStep'=3);
    [TJP_c] cPlan = 1 -> (cPlan'=0) & (planStep'=0); // reset in case we end up back here
endmodule



// ------------ STAGE 6 - Move Garment -----------------------

const double p7= 0.1;
const double p8 = 0.05;
const double p9 = 0.1;

module MoveGarment_Robot
    mvStep : [0..4] init 0;
    [MVG_s] mvStep=0 -> p7:(mvStep' = 1) + p8:(mvStep'=2) + p9:(mvStep'=3) + (1-p7-p8-p9):(mvStep'=4);
    [MVG_snag] mvStep = 1 -> (mvStep'=0); // reset
    [MVG_traj] mvStep = 2 -> (mvStep'=0); // reset
    [MVG_pose] mvStep = 3 -> (mvStep'=0); // reset
    [MVG_c] mvStep=4 -> (mvStep'=0); // reset
endmodule

rewards "lookingGarmentTime"
    [LFG_s] true : 1;// looking for a garment takes longer for each retry.
    [LFG_1] true : 2;
    [LFG_2] true : 3;
endrewards


rewards "orientationTime"
    [MEE_s] true : 1;// Time taken to orient the garment correctly by retries.
    [MEE_1] true : 4;
    [MEE_2] true : 6;
endrewards


rewards "totalTime"
    [LFG_s] true : 1;// looking for a garment takes longer for each retry.
    [LFG_1] true : 2;
    [LFG_2] true : 3;

    [MEE_s] true : 1;// Time taken to orient the garment correctly by retries.
    [MEE_1] true : 4;
    [MEE_2] true : 6;

    [MVU_s] true : 3; // time taken to move to the user.
    [MVU_r] true : 1;

    [DTP_s] true : 1;// Time taken to orient the garment correctly by retries.
    [DTP_1] true : 4;
    [DTP_2] true : 6;

endrewards


rewards "Disturbance"
    [LFG_1] true : 1; // the user is asked to say where the garment is
    [LFG_2] true : 3; // the user is asked to move

    [MEE_2] true : 2; // the user is asked to place the garment in the robot hand.


    [DTP_1] true : 1; // the user is asked to move
    [DTP_2] true : 2; // the user is asked to move again
endrewards
