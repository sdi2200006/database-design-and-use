
# 1

select title AS Title
from movie m, role r, actor a, movie_has_genre mhg, genre g
where a.last_name = "Allen" 
	  and g.genre_name = "Comedy" 
      and a.actor_id = r.actor_id 
      and m.movie_id = r.movie_id 
      and m.movie_id = mhg.movie_id 
      and g.genre_id = mhg.genre_id;
      
# 2
                        
select distinct d.last_name AS Last_name, m.title AS Title
from director d, movie m, actor a, movie_has_director mhd, movie_has_genre mhg
where exists
		(select a.last_name
		from role r
		where a.actor_id = r.actor_id 
			  and a.last_name = "Allen" 
              and r.movie_id = m.movie_id)
      and m.movie_id = mhd.movie_id
      and d.director_id = mhd.director_id
      and m.movie_id = mhg.movie_id
      and exists  
			(select d.director_id
			from movie_has_genre mhg, movie_has_director mhd2
			where mhd2.movie_id = mhg.movie_id 
				  and mhd2.director_id = d.director_id
			group by mhd.director_id
			having count(distinct mhg.genre_id) >= 2)
order by d.last_name asc, m.title asc;
            
# 3                                             
                                             
select distinct a.last_name AS Last_name
from actor a, movie m1, movie m2, director d1, director d2, role r1, role r2, movie_has_director mhd1, movie_has_director mhd2, movie_has_genre mhg
where
# παίζουν σε τουλάχιστον μια ταινία που έχει σκηνοθετηθεί από σκηνοθέτη με το ίδιο επώνυμο
      a.last_name = d1.last_name
      and r1.actor_id = a.actor_id
      and r1.movie_id = m1.movie_id
      and mhd1.director_id = d1.director_id
      and mhd1.movie_id = m1.movie_id
#δεύτερον, έχουν παίξει σε τουλάχιστον μια ταινία με σκηνοθέτη με διαφορετικό επώνυμο
      and a.last_name != d2.last_name
      and r2.actor_id = a.actor_id
      and r2.movie_id = m2.movie_id
      and mhd2.director_id = d2.director_id
      and mhd2.movie_id = m2.movie_id
#που έχει ίδιο είδος με αυτό άλλης ταινίας που δεν παίζουν αλλά έχει σκηνοθετήσει ο σκηνοθέτης με το ίδιο επώνυμο.
	  and mhg.movie_id = m2.movie_id
      and exists  
           (select mhg1.genre_id
           from movie_has_genre mhg1, movie m3, movie_has_director mhd3
           where mhd3.director_id = d1.director_id
           and m3.movie_id = mhd3.movie_id
           and mhg1.genre_id = mhg.genre_id
           and a.actor_id not in 
				(select r3.actor_id
				from role r3
				where a.actor_id != r3.actor_id 
					  and r3.movie_id = m3.movie_id));
                      
# 4

(select "yes" as answer
from movie m, movie_has_genre mhg, genre g  
where m.movie_id = mhg.movie_id 
	  and mhg.genre_id = g.genre_id
      and g.genre_name = "Drama"
      and m.year = "1995")
union 
(select "no" as answer
where not exists
		(select *
		from movie m, movie_has_genre mhg, genre g  
		where m.movie_id = mhg.movie_id 
			  and mhg.genre_id = g.genre_id
              and g.genre_name = "Drama"
              and m.year = "1995"));
              
# 5
           
select d1.last_name as Director_1 , d2.last_name as Director_2
from director d1, director d2, movie_has_director mhd1, movie_has_director mhd2, movie m, movie_has_genre mhg
where d1.director_id = mhd1.director_id
      and d2.director_id = mhd2.director_id
      and m.movie_id = mhg.movie_id 
      and m.movie_id = mhd1.movie_id
      and m.movie_id = mhd2.movie_id
      and d1.director_id < d2.director_id
      and (m.year >= "2000" and m.year <= "2006")
group by d1.last_name, d2.last_name
having count(distinct mhg.genre_id) >= 6;
      
# 6   
      
select a.first_name as Actor_name, a.last_name as Actor_surname, count(distinct mhd.director_id) as Count
from actor a, role r, movie_has_director mhd
where a.actor_id = r.actor_id
	  and mhd.movie_id = r.movie_id
      and  a.actor_id in  
               (select r1.actor_id 
               from role r1 
               group by r1.actor_id 
              having count(r1.actor_id) = 3)
group by (a.actor_id);

# 7

select mhg.genre_id as Genre_id , count(distinct mhd.director_id) as Count  
from movie_has_director mhd, movie_has_genre mhg
where mhd.movie_id = mhg.movie_id
      and mhg.genre_id  in
			(select mhg1.genre_id
            from movie_has_genre mhg1
            where (mhg1.movie_id,1) in 	#βαζουμε ",1" επειδη στο επομενο select εχουμε και το count το οποιο θελουμε να ειναι 1 
						(select mhg2.movie_id, count( mhg1.genre_id) as count1
                        from movie_has_genre mhg2
                        group by mhg2.movie_id
                        having  count1= 1))
group by mhg.genre_id;

# 8

select distinct a.actor_id as Actor_id
from actor a
where not exists
		(select g.genre_id
        from genre g
        where not exists
				(select r.actor_id
                from role r, movie_has_genre mhg
                where r.actor_id = a.actor_id
					  and mhg.genre_id = g.genre_id
                      and r.movie_id = mhg.movie_id));
                      
# 9

select mhg1.genre_id as Genre_id_1, mhg2.genre_id as Genre_id_2, count(distinct mhd1.director_id + mhd2.director_id) as Count
from movie_has_genre mhg1, movie_has_genre mhg2, movie_has_director mhd1, movie_has_director mhd2
where mhg1.movie_id = mhd1.movie_id
	  and mhg2.movie_id = mhd2.movie_id
      and mhd1.director_id = mhd2.director_id
      and mhg1.genre_id < mhg2.genre_id
group by mhg1.genre_id, mhg2.genre_id
order by mhg1.genre_id asc, mhg1.genre_id asc;

# 10

select mhg.genre_id as Genre, r.actor_id as Actor, count(distinct m.movie_id) as Count
from role r, movie_has_genre mhg, movie_has_director mhd, movie m
where m.movie_id = mhd.movie_id
      and m.movie_id = mhg.movie_id
      and m.movie_id = r.movie_id
	  and not exists 
			(select mhd1.movie_id 
            from movie_has_director mhd1, movie_has_genre mhg1
            where (mhd1.movie_id = mhg1.movie_id
				  and mhd1.director_id = mhd.director_id
                  and mhg1.genre_id != mhg.genre_id)
                  or 
                  (mhd1.movie_id = m.movie_id
                  and mhd1.movie_id = mhg1.movie_id
				  and mhd1.director_id != mhd.director_id
                  and mhg1.genre_id = mhg.genre_id))
group by r.actor_id, mhg.genre_id
order by mhg.genre_id asc, r.actor_id asc;