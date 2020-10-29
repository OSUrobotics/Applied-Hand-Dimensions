### Hand Measurement Instructions for Configuration A

## Initial Hand Positioning

Position robot end-effector as if it were to grasp a cylinder on a table top (as shown in the Figure). This can be done with or without an actual cylindrical object --- the main point is that the hand is set up in this fashion. We will refer to this cylindrical object as the reference cylinder.

Using the reference cylinder, assign the axes to the hand. *Makes reference to sections in the methodology section for how to pick axes. How should we handle that here*

## Precision Grasp Measurements

To measure the hand dimensions on a precision grasp, one must make three measurements at three different finger positions --- which we will use to build a complete span-depth profile of the hand throughout the hand's actuation.

All distal link measurements are made at the center point of the distal link.

To make these measurements, perform the following steps:

1. ***Initial Setup:*** Place hand in correct position, as described above.
2. ***Position 0:*** Open the end effector fingers as much as possible.
3. ***Max Span Limit:*** Measure the total distance in the span axis between the midpoint of the distal links that will grasp the cylinder on each side.
4. ***Measurement Image Set 0:*** Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear. 
    - **Position 1:** Close the fingers such that the end effector can grasp the largest reference cylinder that can fit between the distal links, ignoring that such a reference cylinder size could collide with the proximal or palm contacts. 
 		- **Note:** As a guideline, consider actuating the distal links such that they are as far apart as possible, and up to 120 degrees angle from the palm.
        - One could also consider that the distal link contacts on the reference cylinder should be below the mid-line of the cylinder face, as shown in both Config A and Config B Figures. 
5. ***Span Measurement 1:*** Measure the total distance in the span axis between the distal links, as before. 
6. ***Depth Measurement 1:*** Keeping the same position, now measure the total distance orthogonal to the palm up to the span line (remember, this is to the midpoint of the distal link where you measured span). 
7. 
