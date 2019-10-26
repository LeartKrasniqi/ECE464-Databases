/* Specific queries for Problem 1 of Assignment 1 */

/* Q1: Select, for each boat, the sailor who made the highest number of reservations for that boat -- Thanks to Kevin Lin for help with this one */
SELECT temp.bid, temp.sid, MAX(count_res)
FROM ( SELECT R.bid as bid, R.sid as sid, COUNT(R.bid) as count_res
	   FROM reserves R, sailors S
	   WHERE R.sid = S.sid
	   GROUP BY R.bid, R.sid
	   ORDER BY count_res DESC
	 ) as temp
GROUP BY temp.bid
ORDER BY temp.bid;


/* Q2: List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name) */
SELECT B.bid, B.bname, COUNT(*) as Num_Res
FROM Boats B, Reserves R
WHERE B.bid = R.bid
GROUP BY B.bid
HAVING Num_Res > 0;


/* Q3: List those sailors who have reserved every red boat (list the id and the name) */
SELECT S.sid, S.sname
FROM sailors S, boats B
WHERE NOT EXISTS ( SELECT B.bid
		   FROM boats B
		   WHERE NOT EXISTS ( SELECT R.bid
				      FROM reserves R
				       WHERE R.bid = B.bid AND R.sid = S.sid and B.color = 'red'
				    )
		 ); 	 


/* Q4: List those sailors who have reserved only red boats */
SELECT DISTINCT S.sid, S.sname
FROM sailors S, reserves R, boats B
WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red' AND S.sid NOT IN ( SELECT S.sid
									     FROM sailors S, reserves R, boats B
									     WHERE S.sid = R.sid AND R.bid = B.bid AND B.color != 'red'
									   );


/* Q5: For which boat are there the most reservations? */
SELECT B.bid, B.bname, COUNT(*) as Num_Res
FROM boats B, reserves R
WHERE B.bid = R.bid
GROUP BY B.bid
ORDER BY Num_Res DESC
LIMIT 1;


/* Q6: Select all sailors who have never reserved a red boat -- need to union with those who never reserve any boat */
SELECT DISTINCT S.sid as sid, S.sname
FROM sailors S, reserves R, boats B
WHERE S.sid = R.sid AND R.bid = B.bid AND B.color != 'red' AND S.sid NOT IN ( SELECT S.sid
                                                                              FROM sailors S, reserves R, boats B
                                                                              WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red'
                                                                            )
UNION 
SELECT DISTINCT S.sid as sid, S.sname
FROM sailors S, reserves R
WHERE S.sid NOT IN ( SELECT R.sid FROM reserves R)
ORDER BY sid;

/* Q7: Find the average age of sailors with a rating of 10 */
SELECT AVG(S.age)
FROM sailors S
WHERE S.rating = 10;
