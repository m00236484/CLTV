

Introduction 
	One way to analyze acquisition strategy and estimate marketing cost is to calculate the Lifetime Value (“LTV”) of a customer. Simply speaking, LTV is the projected revenue that customer will generate during their lifetime.

Business Scenario
	to calculate customer live time value 
	A.	Customer LTV based on date frame  for each user. 
		So if user A has order events in week 1 and order events in the following week 2, but user B has only order events in week 1, then user B will have see a lower average revenue as his revenue is averaged with zero revenue in week 2.

	B.	Customer LTV based on count weeks that user visited or ordered. 
		So if user A has order events in week 1 and order events in the following week 2, but user B has only order events in week 1, then user A & B will have equal average visit per week and expenditures is main factor .
	C.	Customer Segmentation.
		 Segment users based on CLTV to Segment A, B, C and D, as segment  A is user   	 
 
Ingest(e, D)

Given event e, update data D
TopXSimpleLTVCustomers(x, D)

Return the top x customers with the highest Simple Lifetime Value from data D.

Please note that the timeframe for this calculation should come from D. That is, use the data that was ingested into D to calculate the LTV to frame the start and end dates of your LTV calculation. You should not be using external data (in particular "now") for this calculation.
Events

Please use the following sample events the Data Warehouse collects from Shutterfly’s public sites. All events have a key and event_time, but are received with no guaranteed order and with fluctuating frequency.

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

Programming Language 
A simple LTV can be calculated using the following equation: 52(a) x t. Where a is the average customer value per week (customer expenditures per visit (USD) x number of site visits per week) and t is the average customer lifespan. The average lifespan for Shutterfly is 10 years.
Code Requirements

Write a program that ingests event data and implements one analytic method, below. You are expected to write clean, well-documented and well-tested code. Be sure to think about performance - what the performance characteristic of the code is and how it could be improved in the future.

You may use one of the following OO languages: Java, Python, Scala.

* represents required data
