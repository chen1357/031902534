
import unittest
from main import chinese
from main import english
from main import search
from main import parament
from main import fileOpen

class functionTest(unittest.TestCase):
    def test_parament(self):
        try :
            parament()
        except Exception:
            self.assertTrue(True)
        else:
            self.asserttTrue(False)
      
    def test_fileOpen(self):
        try :
            fileOpen("a.txt")
        except IOError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_seperate(self):
        word="你好"
        org="亻尔女子"
        a=chinese(word)
        text,textlen=a.testing(org)
        self.assertEqual(text,"亻尔女子")

    def test_pinyin(self):
        word="你好"
        org="nhAo"
        a=chinese(word)
        text,textlen=a.testing(org)
        self.assertEqual(text,"nhAo")

    def test_insert(self):
        word="你好"
        org="你234a!@#$%^&*()_+=-`~好254早上好"
        a=chinese(word)
        text,textlen=a.testing(org)
        self.assertEqual(text,"你234a!@#$%^&*()_+=-`~好")

    def test_homophones(self):
        word="你好"
        org="昵郝吃饭"
        a=chinese(word)
        text,textlen=a.testing(org)
        self.assertEqual(text,"昵郝")

    def test_english(self):
        word="hello"
        org="Hel8!lo13"
        a=english(word)
        text,textlen=a.testing(org)
        self.assertEqual(text,"Hel8!lo")

    def test_search(self):
        org=["93ni^&%hao13h8ello4郝\n"]
        word_1="你好"
        word_2="hello"
        a=[chinese(word_1)]
        b=[english(word_2)]
        result,count=search(org,a,b)
        self.assertEqual(result,['Line1: <你好> ni^&%hao', 'Line1: <hello> h8ello'])
        self.assertEqual(count,2)



if __name__=='__main__':
    unittest.main()