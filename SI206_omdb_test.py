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
        self.assertIn(('Pulp Fiction',), result_list)

        statement = '''
            SELECT COUNT(*) FROM MovieInfo
        '''
        results = cur.execute(statement)
        count = results.fetchone()[0]
        self.assertEqual(count,200)xs
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
        conn.close()



unittest.main()





    # def test_country_table(self):
    #     conn = sqlite3.connect(DBNAME)
    #     cur = conn.cursor()
    #
    #     sql = '''
    #         SELECT EnglishName
    #         FROM Countries
    #         WHERE Region="Oceania"
    #     '''
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn(('Australia',), result_list)
    #     self.assertEqual(len(result_list), 27)
    #
    #     sql = '''
    #         SELECT COUNT(*)
    #         FROM Countries
    #     '''
    #     results = cur.execute(sql)
    #     count = results.fetchone()[0]
    #     self.assertEqual(count, 250)
    #
    #     conn.close()

    # def test_joins(self):
    #     conn = sqlite3.connect(DBNAME)
    #     cur = conn.cursor()
    #
    #     sql = '''
    #         SELECT Alpha2
    #         FROM Bars
    #             JOIN Countries
    #             ON Bars.CompanyLocationId=Countries.Id
    #         WHERE SpecificBeanBarName="Hacienda Victoria"
    #             AND Company="Arete"
    #     '''
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn(('US',), result_list)
    #     conn.close()
