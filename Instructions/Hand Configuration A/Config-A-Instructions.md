# Hand Measurement Instructions for Configuration A

## Initial Hand Positioning

Position robot end-effector as if it were to grasp a cylinder on a table top (as shown in the Figure). This can be done with or without an actual cylindrical object --- the main point is that the hand is set up in this fashion. We will refer to this cylindrical object as the reference cylinder.

Using the reference cylinder, assign the axes to the hand. *Makes reference to sections in the methodology section for how to pick axes. How should we handle that here?*

## Precision Grasp Measurements

To measure the hand dimensions on a precision grasp, one must make three measurements at three different finger positions --- which we will use to build a complete span-depth profile of the hand throughout the hand's actuation.

All distal link measurements are made at the center point of the distal link.

To make these measurements, perform the following steps:

1. ***Initial Setup:*** Place hand in correct position, as described above.
2. ***Position 0:*** Open the end effector fingers as much as possible.
3. ***Max Span Limit:*** Measure the total distance in the span axis between the midpoint of the distal links that will grasp the cylinder on each side.
4. ***Measurement Image Set 0:*** Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear. 
5. ***Position 1:*** Close the fingers such that the end effector can grasp the largest reference cylinder that can fit between the distal links, ignoring that such a reference cylinder size could collide with the proximal or palm contacts. 
 	- **Note:** As a guideline, consider actuating the distal links such that they are as far apart as possible, and up to $~120\degree$ angle from the palm.
    - One could also consider that the distal link contacts on the reference cylinder should be below the mid-line of the cylinder face, as shown in both Config A and Config B Figures. 
6. ***Span Measurement 1:*** Measure the total distance in the span axis between the distal links, as before. 
7. ***Depth Measurement 1:*** Keeping the same position, now measure the total distance orthogonal to the palm up to the span line (remember, this is to the midpoint of the distal link where you measured span). 
8. ***Max Width Measurement:*** Measure the maximum width, choosing between the two width calculations described in section **axes** which apply best to the hand.
9. ***Min Width Measurement:*** Measure the minimum width, choosing between the two width calculations described in section **axes** which apply best to the hand.
	- If the fingers are positioned in such a way that they do not obstruct a taller object from bring grasped, add a plus sign after the measurement to indicate this.
    - See the top of Figures Config A and COnfig B as a reference.
9. ***Measurement Image Set 1***: Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear.

10. ***Position 2:*** Now minimize the distance between the distal links.
11. ***Span Measurement 2:*** Measure the span at this position.
12. ***Depth Measurement 2:*** Measure the depth at this position.
13. ***Measurement Image Set 2:*** Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear.
14. ***Positions and Measurements 3+:*** Now choose at least one more finger position between positions 1 and 2 to measure hand span and depth
15. ***Measurement Image Sets 3+:*** Make sure that for every measurement you take a top-down and side-profile image of the hand's pose.
16. ***Final Steps:*** Plot the span and depth values with span as the x-axis. Plot the Max Span Limit as a dotted line to indicate the how far the hand can open.

## Power Grasp Measurements

To measure the hand volume on a 2d, cylindrical power grasp, one must measure three cross-sectional volumes at three different finger positions. Each cross-sectional volume consists of three span-depth measurement pairs. The method to measure the span-depth measurement pairs differs between the cylindrical and spherical power grasps, although the general method of measuring the volumes is the same. In this section, first we will go over the general method to measuring the hand power grasp dimensions, and then follow up with the unique way to measure the span-depth measurements for the cylindrical and spherical power grasps separately.

As with the precision grasp measurements, all distal link measurements are made at the center point of the distal link.

The complete instructions for measuring the hand volume at each finger position is as follows:

1. ***Initial Setup:*** Place hand in correct position, as described above.
2. ***Position 0:*** Open the end effector fingers as much as  possible.
	- **Note:** All  finger  movements  should  be  performed using the end effector’s mode of actuation. There  should  be  no obstacles  which  should  restrict a finger’s free movement.
3. ***Position 1:*** Close the fingers such that the end effector can power grasp the largest object possible. 
    - As a guideline, consider closing the distal links at least to a 80 degrees angle from the palm as if it were grasping the reference cylinder in a power grasp (so there must be a palm contact).
    - Make sure that contact occurs past the mid-line of the cylinder face.
4. ***Volume Measurement 1:*** Using the volume measurement instructions for either the cylindrical or spherical power grasp (see sections below), measure the hand volume for tssshis finger position. 
5. ***Max Width Measurement:*** Measure the maximum width, choosing between the two width calculations described in section \ref{sec:axes} which apply best to the hand.
6. ***Min Width Measurement:*** Measure the minimum width, choosing between the two width calculations described in section \ref{sec:axes} which apply best to the hand.
	- If the fingers are positioned in such a way that they do not obstruct a taller object from bring grasped, add a plus sign after the measurement to indicate this.
    - See the top of Figures Config A and Config B as a reference.
7. **Measurement Image Set 1:** Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear.
8. ***Position 2:*** Close the fingers as much as possible.
9. ***Volume Measurement 2:*** Use the volume measurement instructions to measure the hand volume for this finger position. 
	- **Note:** Ignore any span-depth measurement pair that will not apply in this grasp (for instance, if the distal links don't make *contact* with the volume). If only one span-depth measurement will work, include the palm contact point so that a triangular cross-section can be reported. ***MAKE A FIGURE EXAMPLE FOR THIS***
10. **Measurement Image Set 2:** Take a top-down and side-profile image of the hand's pose, making sure that the 1mm grid in the background is also clear.
11. ***Position 3:*** Actuate the fingers between positions 1 and 2.
12. ***Volume Measurement 3:*** Measure the hand volume at this position.
13. **Measurement Image Sets 3:** Take a top-down and side-profile image of the hand's pose.
    - Repeat the steps for Position 3 for as many intermediate measurements as desired.

### Cylindrical Volume Measurement

For the cylindrical volume measurements, we approximate the volume inside the power grasp by making three span measurements at specific depth measurements.

One makes the set of three span-depth measurement pairs for the cylindrical power grasp as so:

1. **Finger Position Setup:** Set the end effector's fingers to whatever finger position is called for.
2. **Span-Depth Measurement 1:** Measure the span between the distal links and record the distance from the palm to the distal link in the depth axis.
3. **Span-Depth Measurement 2:** Measure the maximum span achieved between the two opposing fingers and record the distance from the palm to that point in the depth axis.
4. **Span-Depth Measurement 3:** Measure the smallest span achieved between the two opposing fingers (not at the distal links) and record the distance from the palm to that point in the depth axis.
5. **Final Steps:** From here one can reconstruct the approximation of the hand volume for the particular finger position.


