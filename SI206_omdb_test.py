import unittest
from SI206_omdb import *



class TestDatabase(unittest.TestCase):

    def test_top200_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = 'SELECT Rank FROM Top200'
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertIn((2,), result_list)
        self.assertEqual(len(result_list), 200)

        statement = '''
            SELECT * FROM Top200 WHERE Rank < 10
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertEqual(len(result_list),9)
        self.assertEqual(result_list[8][3], '2002')
        self.assertEqual(result_list[0][1], 'PulpFiction')
        self.assertEqual(result_list[0][2], 1)
        self.assertEqual(result_list[0][3], '1994')
        conn.close()

    def test_MovieInfo_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Name FROM MovieInfo
            WHERE Rated = 'R'
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertIn(('PulpFiction',), result_list)

        statement = '''
            SELECT COUNT(*) FROM MovieInfo
        '''
        results = cur.execute(statement)
        count = results.fetchone()[0]
        self.assertEqual(count,200)
        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Year FROM Top200 JOIN MovieInfo
            ON MovieInfo.MovieId=Top200.Id
            WHERE Top200.Title='Se7en'
        '''
        results = cur.execute(statement)
        result = results.fetchone()
        self.assertEqual(('1995',),result)

        statement1 = '''
            SELECT Year FROM Top200 JOIN MovieInfo
            ON MovieInfo.MovieId=Top200.Id
        '''
        result1 = cur.execute(statement1)
        results1 = result1.fetchall()
        self.assertEqual(len(results1), 200)
        conn.close()

class TestMovie(unittest.TestCase):
    def testConstructor(self):
        movie1 = Movie('Pulp Fiction', 1, '1994')
        self.assertEqual(movie1.title, 'Pulp Fiction')
        self.assertEqual(movie1.rank, 1)
        self.assertEqual(movie1.year, '1994')

    def testStrConstructor(self):
        movie1 = Movie('The Departed', 2, '2006')
        self.assertEqual(movie1.__str__(), '2. The Departed is produced in 2006')



unittest.main()
