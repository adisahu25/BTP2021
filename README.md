The functions created are as follows:

1. Create_person() :
A person is created with array containing his information like state, home, work and current location.

2. createPopulation() :

•	In this function, we are using pop array which is a 2-D array of size n_pop x person_attr who’s each row represent a single person and columns specify the attributes of that person discussed above. The home locations are selected between 250(n_overlap) and 2750(n_loc) whereas work location is selected between 0 and 250(n_net).
•	Further we are using n_per_location which is also a 2-D array of size n_loc x n_states representing number of people in each state at a specific location.
•	In addition to them, another 2-D array people_linked_to of size n_loc x max_ppl talking about individuals in each location.

3.	Targeted_Run() :

•	We our running our simulation in this part for tf days with population as pop.

•	In this we added a Tpars array of size 2 x 4 where first row is for RAT test and second for PCR test. The columns contain information about sensitivity, specificity, test delay and fraction in mixture

•	Lock_homes Boolean variable tells us whether the home is quarantined or not.

•	Quarantine_when_sample_taken variable tells us about quarantine status of a person when sample is taken.

•	Quarantine_confined is created to decide if people who are quarantined have their infectivity reduced.

•	Begin_at variable is a percentage number which provides us information of population recovered when testing is started.

•	Test_frac variable is a percentage number telling us how much tests are to be conducted on a single day.


