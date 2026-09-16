# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql

def connection():
    ''' User this function to create your connections '''    
    con =  pymysql.connect(host="127.0.0.1", port=3306, user="YOUR_USERNAME", passwd="YOUR_PASSWORD", db="YOUR_DATABASE")  #update with your settings
   
    return con

# ΕΡΩΤΗΜΑ 1
def updateRank(rank1, rank2, movieTitle):
    # Create a new connection
    con = connection()
    # Create a cursor on the connection
    cur = con.cursor()
    try:
        float(rank1)
    except ValueError:
        return [("status",), ("error",)]
    try:
        float(rank2)
    except ValueError:
        return [("status",), ("error",)]
    
    # Δημιουργία ερωτήματος και αναζήτηση της ταινίας με το δοσμένο τίτλο
    cur.execute('SELECT m.rank FROM movie m WHERE m.title = %s', (movieTitle))
    number = cur.fetchall()
    
    # Έλεγχος αν υπάρχει μοναδική ταινία 
    if len(number) != 1:     
        return [("status",), ("error",)]
    current = number[0][0]
    # Υπολογισμός μέσου όρου για κάθε περίπτωση
    if not current :
        new_rank = (float(rank1) + float(rank2)) / 2
    else:
        new_rank = (float(current) + float(rank1) + float(rank2)) / 3
    # Ενημέρωση της βαθμολογίας
    cur.execute('UPDATE movie m SET m.rank = %s WHERE m.title = %s', (new_rank, movieTitle))
    # Ενημέρωση της βαθμολογίας στη βάση δεδομένων και κλεισιμο σύνδεσης
    con.commit()
    return [("status",), ("ok",)]



# ΕΡΩΤΗΜΑ 2
# Τα ζευγάρια (a1,b1) και (b1,a1) τα θεωρούμε διαφορετικά
def colleaguesOfColleagues(actorId1, actorId2):
    # Create a new connection
    con = connection()
    # Create a cursor on the connection
    cur = con.cursor()
    
    # Έλεγχος ότι έχει δώσει 2 κωδικούς ηθοποιών
    if not actorId1 or not actorId2:
        return [("status",), ("You have to give 2 actor ID",)]
    elif actorId1 == actorId2:
        return [("status",), ("You gave the same ID two times",)]
    
    # Έλεγχος αν υπάρχουν οι ηθοποιοί με τους δοσμένους κωδικούς
    sql1 = '''SELECT 1 FROM actor a WHERE a.actor_id = %s'''
    cur.execute(sql1, (actorId1,))
    data1 = cur.fetchall()
    cur.execute(sql1, (actorId2,))
    data2 = cur.fetchall()
    if not data1 and not data2:
        return [("status",), ("There aren't the actors with these IDs",)]
    elif not data1:
        return [("status",), ("There isn't the first actor with this ID",)]
    elif not data2:
        return [("status",), ("There isn't the second actor with this ID",)]
    
    # Δημιουργία βασικού ερωτήματος
    sql = '''SELECT DISTINCT m1.title, %s AS actorId1, %s AS actorId2, c.actor_id AS c, d.actor_id AS d
             FROM movie m1, role c, role d
             WHERE %s != %s
             -- Παίζουν μαζί c & d
             AND c.movie_id = m1.movie_id
             AND d.movie_id = m1.movie_id
             -- O C παίζει με τον a
             AND c.actor_id IN (
                 SELECT r.actor_id
                 FROM role r
                 WHERE r.movie_id IN (
                     SELECT r2.movie_id
                     FROM role r2
                     WHERE r2.actor_id = %s
                 )
             )
             -- O b παίζει με τον d
             AND d.actor_id IN (
                 SELECT r.actor_id
                 FROM role r
                 WHERE r.movie_id IN (
                     SELECT r2.movie_id
                     FROM role r2
                     WHERE r2.actor_id = %s
                 )
             )
             AND c.actor_id <> d.actor_id
             AND %s <> c.actor_id
             AND %s <> d.actor_id        
             AND %s <> c.actor_id
             AND %s <> d.actor_id
             ORDER BY m1.title ASC'''
    cur.execute(sql, (actorId1, actorId2, actorId1, actorId2, actorId1, actorId2, actorId1, actorId1, actorId2, actorId2))
    rows = cur.fetchall()
    
    # Εάν δεν έχει κανένα αποτέλεσμα
    if not rows:
        return [("status",), ("There aren't actors with this connection",)]
    else:
        results = [["Title", "A", "B", "C", "D"]]
        for row in rows:
            results.append(row)
        return results

# ΕΡΩΤΗΜΑ 3
def actorPairs(actorId):
    # Create a new connection
    con = connection()
    # Create a cursor on the connection
    cur = con.cursor()
    
    # Έλεγχος ότι έδωσε κάποιο ID ηθοποιού
    if not actorId:
        return [("status",), ("You have to give the ID",)]
    
    # Έλεγχος αν υπάρχει ο ηθοποιός με τον κωδικό που έδωσε
    sql1 = '''SELECT 1 FROM actor a WHERE a.actor_id = %s'''
    cur.execute(sql1, (actorId,))
    data = cur.fetchall()
    if not data:
        return [("status",), ("There isn't an actor with this ID",)]
    
    # Δημιουργία βασικού ερωτήματος
    sql = '''SELECT DISTINCT b.actor_id
             FROM actor a, actor b
             WHERE a.actor_id = %s
               AND a.actor_id <> b.actor_id 
               AND b.actor_id IN (
                   SELECT rb.actor_id
                   FROM movie_has_genre ga, movie_has_genre gb, role ra, role rb
                   WHERE ga.movie_id = ra.movie_id
                    AND gb.movie_id = rb.movie_id
                    AND ra.actor_id = a.actor_id
                    AND rb.actor_id = b.actor_id
                    AND ga.genre_id <> gb.genre_id)
               AND b.actor_id IN (
                   SELECT rb.actor_id
                   FROM movie_has_genre g, role ra, role rb
                   WHERE g.movie_id = ra.movie_id
                    AND g.movie_id = rb.movie_id
                    AND ra.actor_id = a.actor_id
                    AND rb.actor_id = b.actor_id
                    GROUP BY rb.actor_id
                    HAVING COUNT(DISTINCT g.genre_id) >= 7)'''
    cur.execute(sql, (actorId,))
    rows = cur.fetchall()
    
    # Εάν δεν έχει κανένα αποτέλεσμα
    if not rows:
        return [("status",), ("There aren't actors with this connection",)]
    else:
        results = [["Actors Id"]]
        for row in rows:
            results.append(row)
        return results

# ΕΡΩΤΗΜΑ 4
def selectTopNactors(N):
    # Create a new connection
    con = connection()
    # Create a cursor on the connection
    cur = con.cursor()
     
    if not N :
        return [("status",), ("You have to give a number > 0",)]
    
    # Δημιουργια ερωτήματος για να πάρουμε τα ονόματα όλων των ειδών ταινιών
    cur.execute('SELECT DISTINCT genre_name FROM genre ORDER BY genre_name ASC')
    genres = cur.fetchall()
    
    #Αρχικοποίηση λίστας με την επικεφαλίδα 
    results = [["Genre", "Actor ID", "Movies' number"]]
    
    # Για κάθε είδος ταινίας θα βρούμε τους ηθοποιούς με τις περισσότερες ταινίες
    for genre in genres:
        genre_name = genre[0]
        # Δημιουργια βασικού ερωτήματος για το συγκεκριμένο είδος
        sql = '''SELECT DISTINCT  r.actor_id, COUNT(DISTINCT mhg.movie_id) AS c
                 FROM genre g, movie_has_genre mhg, role r
                 WHERE g.genre_id = mhg.genre_id
                   AND r.movie_id = mhg.movie_id
                   AND g.genre_name = %s
                 GROUP BY r.actor_id
                 ORDER BY c DESC'''
        cur.execute(sql, (genre_name,))
        actors = cur.fetchall()
        N = int(N)
        
        # Εισαγωγή των κορυφαίων N ηθοποιών στο αποτέλεσμα
        if len(actors) < N:
            min = len(actors)
        else:
            min = N

        for i in range(min):
            actor_id, movie_count = actors[i]
            results.append((genre_name, actor_id, movie_count))
    return results


# ΕΡΩΤΗΜΑ 5
def traceActorInfluence(actorId):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    return [("influencedActorId",),]
