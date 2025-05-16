
# Create your tests here.
for i in range(10):
	print(i)
class ExampleTestCase(TestCase):
	def test_example(self):
		self.assertEqual(1 + 1, 2)

	def test_another_example(self):
		self.assertTrue(True)
