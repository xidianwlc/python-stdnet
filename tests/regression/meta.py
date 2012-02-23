import inspect

from stdnet import test, orm
from stdnet.utils import populate, pickle
from stdnet.exceptions import QuerySetError
from stdnet.orm import model_to_dict, model_iterator
from stdnet.orm.base import StdNetType

from examples.data import FinanceTest, Instrument, Fund, Position


class TestInspectionAndComparison(FinanceTest):
    
    def setUp(self):
        self.register()
        
    def testSimple(self):
        d = model_to_dict(Instrument)
        self.assertFalse(d)
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR').save()
        d = model_to_dict(inst)
        self.assertTrue(len(d),3)
        
    def testEqual(self):
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR').save()
        id = inst.id
        b = Instrument.objects.get(id = id)
        self.assertEqual(b.id,id)
        self.assertTrue(inst == b)
        self.assertFalse(inst != b)
        f = Fund(name = 'bla', ccy = 'EUR').save()
        self.assertFalse(inst == f)
        self.assertTrue(inst != f)
        
    def testNotEqual(self):
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR').save()
        inst2 = Instrument(name = 'edz14', type = 'future', ccy = 'USD').save()
        id = inst.id
        b = Instrument.objects.get(id = id)
        self.assertEqual(b.id,id)
        self.assertFalse(inst2 == b)
        self.assertTrue(inst2 != b)
        
    def testHash(self):
        '''Test model instance hash'''
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR')
        h0 = hash(inst)
        self.assertTrue(h0)
        inst.save()
        h = hash(inst)
        self.assertTrue(h)
        self.assertNotEqual(h,h0)
        
    def testmodelFromHash(self):
        m = orm.get_model_from_hash(Instrument._meta.hash)
        self.assertEqual(m, Instrument)
        
    def testUniqueId(self):
        '''Test model instance unique id across different model'''
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR')
        self.assertRaises(inst.DoesNotExist, lambda : inst.uuid)
        inst.save()
        v = inst.uuid.split('.') # <<model hash>>.<<instance id>>
        self.assertEqual(len(v),2)
        self.assertEqual(v[0],inst._meta.hash)
        self.assertEqual(v[1],str(inst.id))


class PickleSupport(test.TestCase):
    model = Instrument
    
    def setUp(self):
        self.register()
        
    def testSimple(self):
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR').save()
        p = pickle.dumps(inst)
        inst2 = pickle.loads(p)
        self.assertEqual(inst,inst2)
        self.assertEqual(inst.name,inst2.name)
        self.assertEqual(inst.type,inst2.type)
        self.assertEqual(inst.ccy,inst2.ccy)
        
    def testTempDictionary(self):
        inst = Instrument(name = 'erz12', type = 'future', ccy = 'EUR').save()
        self.assertTrue('cleaned_data' in inst._dbdata)
        p = pickle.dumps(inst)
        inst2 = pickle.loads(p)
        self.assertFalse('cleaned_data' in inst2._dbdata)
        inst2.save()
        self.assertTrue('cleaned_data' in inst._dbdata)
        

class TestRegistration(test.TestCase):
    
    def testModelIterator(self):
        g = model_iterator('examples')
        self.assertTrue(inspect.isgenerator(g))
        d = list(g)
        self.assertTrue(d)
        for m in d:
            self.assertTrue(inspect.isclass(m))
            self.assertTrue(isinstance(m,StdNetType))
