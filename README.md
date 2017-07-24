

Introduction 
	One way to analyze acquisition strategy and estimate marketing cost is to calculate the Lifetime Value (“LTV”) of a customer. Simply speaking, LTV is the projected revenue that customer will generate during their lifetime.

Business Scenario
	A.  TopXSimpleLTVCustomers(x, D) (Required)

		Return the top x customers with the highest Simple Lifetime Value from data D.
		Please note that the timeframe for this calculation should come from D. That is, use the data that was ingested into D to calculate the LTV to frame the start and end dates of your LTV calculation. You should not be using external data (in particular "now") for this calculation.
		Events

		Please use the following sample events the Data Warehouse collects from Shutterfly’s public sites. All events have a key and event_time, but are received with no guaranteed order and with fluctuating frequency.

	A.	Customer LTV based on date frame  for each user. (Required)
		So if user A has order events in week 1 and order events in the following week 2, but user B has only order events in week 1, then user B will have see a lower average revenue as his revenue is averaged with zero revenue in week 2.
		
		Calculation :
		    equation: 52 (a) x t  
			a    : average user expenditure per week
            weeks: max Event Date - min Event Date / 7
            			
		

	B.	Customer LTV based on count weeks that user visited or ordered. 
		So if user A has order events in week 1 and order events in the following week 2, but user B has only order events in week 1, then user A & B will have equal average visit per week and expenditures is main factor .
		equation: 52 (a) x t  
			a    : average user expenditure per week
            weeks: Number of weeks that user has site visit or order 
			
	C.	Customer Segmentation.
		 Segment users based on CLTV to Segment A, B, C, D, and E as segment  A is group of users have CLTV perentage 130% of Average CLTV, segment B include users have percentage between 105%-125%, segment C for those users in average CLTV , segment D are those users have 80% of average, and segment E for reset of users
         equation: Customer LTV / Average CLTV

		 Ingest(e, D)
    Ingest the event source into memory as set of object (Customer, Event, Site Visit, and etc)   
		See sample_input directory for a sample of each event.
		Customer

			type *
				CUSTOMER
			verb *
				NEW
				UPDATE
			Additional Data
				key(customer_id) *
				event_time *
				last_name
				adr_city
				adr_state

		Site Visit

			type *
				SITE_VISIT
			verb *
				NEW
			Additional Data
				key(page_id) *
				event_time *
				customer_id *
				tags (array of name/value properties)

		Image Upload

			type *
				IMAGE
			verb *
				UPLOAD
			Additional Data
				key(image_id) *
				event_time *
				customer_id *
				camera_make
				camera_model

		Order

			type *
				ORDER
			verb *
				NEW
				UPDATE
			Additional Data
				key(order_id) *
				event_time *
				customer_id *
				total_amount *  


Technical Approach:
    •	In memory data processing based on python standard libraries
	•	hash table (Key, value) data structure.
	•	OO design (Customer, Event, and etc) 

Complixity:
      	•	Complexity Algorithm
		•	 Ingest 
				Time :  O(N)
				Space:  O(N)
				
		•	 TopXSimpleLTVCustomers (X)
				Time :  O(N) + g(x)
			    Space:  O(X)
Data Sample:
        Total Events      :2850
		Total Clients     :50
		Total Visits      :984
		Total Orders      :800
		Total Bad Events  :0

Test case:
        Asseret top x client 

Output Files:
1- output_MMDDYYYY-HMS      : Top X CLTV users , customer segmentaion
2- DS_Analsis_MMDDYYYY-HMS  : Data set analysis How many clients, count of each event type and count of bad event 
3- Log_MMDDYYYY-HMS         : log actions and error
4- Bad_MMDDYYYY-HMS     	: bad event containt	

Output Sample
A-	Calculate Topx Customer Lifetime Value Timeframe
Total Count OF Clients               :50
Averge Customers CLTV                :$546,199.36
Averge Customers Weekly Visit        :1.0
Averge Customers Visit  Expenditure  :$1,050.38
Averge Customers Weekly Expenditure  :$1,050.38

  ID 	Name	Expendure Vist	Weekly Visit	Customer CLTV
1008	Anderson	$1,486.21	1.0	$772,829.08
1044	Lamb	$1,441.13	1.0	$749,387.77
1029	Church	$1,421.36	1.0	$739,105.43
1030	Mccarty	$1,384.87	1.0	$720,131.99
1022	Andrews	$1,327.13	1.0	$690,107.79
--------------------------------------------------------------------------------------


B-	Calculate Topx Customer Live Time Value Based on numbers of weeks that user already visited
Total Count OF Clients  :50
Averge Customers CLTV                :$546,199.36
Averge Customers Weekly Visit        :1
Averge Customers Visit  Expenditure  :$1,050.38
Averge Customers Weekly Expenditure  :$1,050.38


  ID 	Name	Expendure Vist	Weekly Visit	Customer CLTV
1029	Church	$1,233.97	2	$1,478,210.86
1030	Mccarty	$1,233.97	2	$1,440,263.98
1023	Spencer	$1,233.97	2	$1,283,324.90
1013	Morin	$1,233.97	2	$1,274,952.25
1010	UnKnown	$1,233.97	2	$1,099,445.13

--------------------------------------------------------------------------------------
C-	Customer Segmentation Based on Customer Lifetime Value 

  ID 	Name	Customer Segment


------------------ Segment A  ----------------------
1008	Anderson	A
1044	Lamb	A
1029	Church	A
1030	Mccarty	A
Total Customer in  Segment  A Is  : 3   Precentage : 6.0%

------------------ Segment B  ----------------------
1022	Andrews	B
1011	UnKnown	B
1028	Hyde	B
1025	Mendoza	B
1033	Turner	B
1023	Spencer	B
1013	Morin	B
1016	Holman	B
1035	Johns	B
1026	Kennedy	B
1045	Underwood	B
1003	Cochran	B
1001	UnKnown	B
1048	UnKnown	B
1021	Mills	B
1017	Talley	B
1031	Mitchell	B
1019	UnKnown	B
1020	UnKnown	B
1027	Kent	B
1009	Phillips	B
Total Customer in  Segment  B Is  : 20   Precentage : 40.0%

------------------ Segment C  ----------------------
1010	UnKnown	C
1038	UnKnown	C
1002	Walters	C
1042	Taylor	C
1018	Mcgowan	C
1041	UnKnown	C
1046	Hester	C
1014	Hensley	C
1043	Bean	C
1015	UnKnown	C
1005	UnKnown	C
1006	UnKnown	C
Total Customer in  Segment  C Is  : 11   Precentage : 22.0%

------------------ Segment D  ----------------------
1007	Gould	D
1032	UnKnown	D
1037	UnKnown	D
1036	Campbell	D
1039	Farrell	D
Total Customer in  Segment  D Is  : 4   Precentage : 8.0%

------------------ Segment E  ----------------------
1047	Whitehead	E
1034	Short	E
1004	UnKnown	E
1012	Potter	E
1049	UnKnown	E
1024	Forbes	E
1040	UnKnown	E
1000	Shields	E


DS_Analsis_MMDDYYYY - Sample

Total Events      :2850
Total Clients     :50
Total Visits      :984
Total Orders      :800
Total Bad Events  :0

Log Sample 
2017-07-24 04:46:16.273000	Success to read json file : D:\Projects\CLTV\input\ds50Customers.txt

