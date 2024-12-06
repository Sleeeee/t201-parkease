import unittest
from src.models import ParkingLot, ParkingFloor, ParkingRow, ParkingSpot, PremiumCar, StandardCar

class TestParkingLot(unittest.TestCase):
    def test_init_positive(self):
        p1, p2 = ParkingLot(2), ParkingLot(5)
        self.assertEqual(p1.lot_number, 2)
        self.assertEqual(p1.floors, {})
        self.assertEqual(p2.lot_number, 5)
        self.assertEqual(p2.floors, {})

    def test_init_negative(self):
        self.assertRaises(ValueError, ParkingLot, -1)
        self.assertRaises(ValueError, ParkingLot, -3)

    def test_init_zero(self):
        self.assertRaises(ValueError, ParkingLot, 0)

    def test_add_non_existing(self):
        p1 = ParkingLot(1)
        p1.add_spot({"id":12, "spot_number":1, "row_number":2, "floor_number": 3})
        s1 = p1.floors[3].rows[2].spots[1]
        self.assertEqual(s1.id, 12)
        self.assertEqual(s1.spot_number, 1)
        self.assertEqual(s1.status, "free")

        p2 = ParkingLot(2)
        p2.floors = {-1: ParkingFloor(-1)}
        p2.floors[-1].rows = {3: ParkingRow(3)}
        p2.floors[-1].rows[3].spots = {1: ParkingSpot(5, 1)}
        p2.add_spot({"id":7, "spot_number":8, "row_number":3, "floor_number":-1})
        s2_1 = p2.floors[-1].rows[3].spots[1]
        self.assertEqual(s2_1.id, 5)
        self.assertEqual(s2_1.spot_number, 1)
        self.assertEqual(s2_1.status, "free")
        s2_2 = p2.floors[-1].rows[3].spots[8]
        self.assertEqual(s2_2.id, 7)
        self.assertEqual(s2_2.spot_number, 8)
        self.assertEqual(s2_2.status, "free")

        p3 = ParkingLot(3)
        p3.floors = {3: ParkingFloor(3)}
        p3.floors[3].rows = {3: ParkingRow(3), 6: ParkingRow(6)}
        p3.floors[3].rows[3].spots = {1: ParkingSpot(5, 1)}
        p3.floors[3].rows[6].spots = {1: ParkingSpot(6, 1)}
        p3.add_spot({"id":10, "spot_number":1, "row_number": 1, "floor_number": 1})
        s3_1 = p3.floors[3].rows[3].spots[1]
        self.assertEqual(s3_1.id, 5)
        self.assertEqual(s3_1.spot_number, 1)
        self.assertEqual(s3_1.status, "free")
        s3_2 = p3.floors[3].rows[6].spots[1]
        self.assertEqual(s3_2.id, 6)
        self.assertEqual(s3_2.spot_number, 1)
        self.assertEqual(s3_2.status, "free")
        s3_3 = p3.floors[1].rows[1].spots[1]
        self.assertEqual(s3_3.id, 10)
        self.assertEqual(s3_3.spot_number, 1)
        self.assertEqual(s3_3.status, "free")

    def test_add_existing(self):
        p1 = ParkingLot(1)
        p1.floors = {-1: ParkingFloor(-1)}
        p1.floors[-1].rows = {3: ParkingRow(3)}
        p1.floors[-1].rows[3].spots = {1: ParkingSpot(5, 1)}
        self.assertRaises(ValueError, p1.add_spot, {"id":9, "spot_number":1, "row_number":3, "floor_number":-1})

    def test_add_wrong_format(self):
        p1 = ParkingLot(1)
        self.assertEqual(p1.floors, {})
        self.assertRaises(TypeError, p1.add_spot, {"id": 1, "spot_number": 1, "floor_number": 1})
        self.assertRaises(TypeError, p1.add_spot, {"id": 1, "spot_number": 1, "row_number": 1, "floor_number": 1, "lot_number": 1})
        self.assertEqual(p1.floors, {})

    def test_add_negative(self):
        p1 = ParkingLot(1)
        self.assertRaises(ValueError, p1.add_spot, {"id": -1, "spot_number": 1, "row_number": 4, "floor_number": 2})
        self.assertRaises(ValueError, p1.add_spot, {"id": 1, "spot_number": 0, "row_number": 4, "floor_number": 2})
        self.assertRaises(ValueError, p1.add_spot, {"id": 1, "spot_number": 1, "row_number": -4, "floor_number": 2})
        p1.add_spot({"id": 1, "spot_number": 1, "row_number": 4, "floor_number": -2})
        s1 = p1.floors[-2].rows[4].spots[1]
        self.assertEqual(s1.id, 1)
        self.assertEqual(s1.spot_number, 1)
        self.assertEqual(s1.status, "free")

    def test_remove_existing(self):
        p1 = ParkingLot(1)
        p1.floors = {1: ParkingFloor(1)}
        p1.floors[1].rows = {2: ParkingRow(2)}
        p1.floors[1].rows[2].spots = {5: ParkingSpot(12, 5)}
        p1.remove_spot({"spot_number": 5, "row_number": 2, "floor_number": 1})
        self.assertEqual(p1.floors, {})

        p2 = ParkingLot(2)
        p2.floors = {3: ParkingFloor(3)}
        p2.floors[3].rows = {4: ParkingRow(4)}
        p2.floors[3].rows[4].spots = {7: ParkingSpot(22, 7), 8: ParkingSpot(23, 8)}
        p2.remove_spot({"spot_number": 7, "row_number": 4, "floor_number": 3})
        s2 = p2.floors[3].rows[4].spots[8]
        self.assertEqual(s2.id, 23)
        self.assertEqual(s2.spot_number, 8)
        self.assertEqual(s2.status, "free")

        p3 = ParkingLot(3)
        p3.floors = {2: ParkingFloor(2)}
        p3.floors[2].rows = {3: ParkingRow(3), 4: ParkingRow(4)}
        p3.floors[2].rows[3].spots = {5: ParkingSpot(15, 5)}
        p3.floors[2].rows[4].spots = {1: ParkingSpot(5, 1)}
        p3.remove_spot({"spot_number": 5, "row_number": 3, "floor_number": 2})
        self.assertEqual(len(p3.floors[2].rows), 1)
        self.assertEqual(p3.floors[2].rows[4].row_number, 4)

    def test_remove_non_existing(self):
        p1 = ParkingLot(1)
        p1.floors = {2: ParkingFloor(2)}
        p1.floors[2].rows = {3: ParkingRow(3)}
        p1.floors[2].rows[3].spots = {1: ParkingSpot(9, 1)}
        self.assertRaises(ValueError, p1.remove_spot, {"spot_number": 5, "row_number": 3, "floor_number": 2})
        s1 = p1.floors[2].rows[3].spots[1]
        self.assertEqual(s1.id, 9)
        self.assertEqual(s1.spot_number, 1)
        self.assertEqual(s1.status, "free")

        p2 = ParkingLot(2)
        self.assertRaises(ValueError, p2.remove_spot, {"spot_number": 1, "row_number": 1, "floor_number": 1})
        self.assertEqual(p2.floors, {})

        p3 = ParkingLot(3)
        p3.floors = {1: ParkingFloor(1)}
        p3.floors[1].rows = {2: ParkingRow(2)}
        p3.floors[1].rows[2].spots = {1: ParkingSpot(10, 1)}
        self.assertRaises(ValueError, p3.remove_spot, {"spot_number": 5, "row_number": 2, "floor_number": 1})
        s3 = p3.floors[1].rows[2].spots[1]
        self.assertEqual(s3.id, 10)
        self.assertEqual(s3.spot_number, 1)
        self.assertEqual(s3.status, "free")

    def test_remove_wrong_format(self):
        p1 = ParkingLot(1)
        self.assertRaises(TypeError, p1.remove_spot, {"row_number": 2, "floor_number": 1})
        self.assertRaises(TypeError, p1.remove_spot, {"spot_number": "1", "row_number": 1, "floor_number": 1, "test": 1})
        self.assertEqual(p1.floors, {})

class TestParkingSpot(unittest.TestCase):

    def test_init(self):
        s1 = ParkingSpot(1, 2, "free")
        self.assertEqual(s1.spot_number, 2)
        self.assertEqual(s1.id, 1)
        self.assertEqual(s1.status, "free")
        self.assertEqual(s1.linked_car, None)


        s2 = ParkingSpot(2, 3, "occupied")
        self.assertEqual(s2.spot_number, 3)
        self.assertEqual(s2.id, 2)
        self.assertEqual(s2.status, "occupied")
        self.assertEqual(s2.linked_car, None)

        s3 = ParkingSpot(0, 1, "booked")
        self.assertEqual(s3.spot_number, 1)
        self.assertEqual(s3.id, 0)
        self.assertEqual(s3.status, "booked")
        self.assertEqual(s3.linked_car, None)

        with self.assertRaises(ValueError):
            ParkingSpot(1, 2, "test")

    def test_enter(self):

        #test erreur already occupied
        s2 = ParkingSpot(2, 3, "occupied")
        with self.assertRaises(AssertionError):
            s2.enter("abc",True)

        #test normal premium
        s1 = ParkingSpot(3, 4, "free")
        s1.enter("acd", True)
        self.assertEqual(s1.status, "occupied")
        self.assertEqual(s1.linked_car.registration_plate, "acd")
        self.assertIsInstance(s1.linked_car, PremiumCar)

        #test normal standard
        s3 = ParkingSpot(1, 2, "free")
        s3.enter("bcd", False)
        self.assertEqual(s3.status, "occupied")
        self.assertEqual(s3.linked_car.registration_plate, "bcd")
        self.assertIsInstance(s3.linked_car, StandardCar)


        s4 = ParkingSpot(4, 4, "booked")
        s4.linked_car = PremiumCar("prem")

        #test premium plate not matching
        with self.assertRaises(AssertionError):
            s4.enter("acd", True)

        #test premium car but isPremium false
        with self.assertRaises(AssertionError):
            s4.enter("prem", False)

        s4.enter("prem", True)
        self.assertEqual(s4.linked_car.registration_plate, "prem")
        self.assertEqual(s4.status, "occupied")

    def test_exit(self):
        s1 = ParkingSpot(1, 1, "free")
        s1.linked_car = StandardCar("abc")
        with self.assertRaises(AssertionError):
            s1.exit("abc")

        s2 = ParkingSpot(2, 2, "occupied")
        s2.linked_car = StandardCar("bcd")
        with self.assertRaises(AssertionError):
            s2.exit("flckqzdmqd")

        s3 = ParkingSpot(3, 3, "occupied")
        s3.linked_car = StandardCar("cde")
        s3.exit("cde")
        self.assertEqual(s3.status, "free")
        self.assertEqual(s3.linked_car, None)

    def test_booking(self):
        s1 = ParkingSpot(1, 1, "occupied")
        s2 = ParkingSpot(2, 2, "free")

        #test error status occupied
        with self.assertRaises(AssertionError):
            s1.book("abc",True)

        #test error is_premium false
        with self.assertRaises(AssertionError):
            s2.book("abc",False)

        #working test
        s2.book("prem", True)
        self.assertEqual(s2.status, "booked")
        self.assertEqual(s2.linked_car.registration_plate, "prem")
    def test_pay(self):
        s1 = ParkingSpot(1, 1, "free")
        s2 = ParkingSpot(2, 2, "occupied")
        s2.linked_car = PremiumCar("prem")
        #test status error
        with self.assertRaises(AssertionError):
            s1.pay("abc",6.0)

        #test wrong plate
        with self.assertRaises(AssertionError):
            s2.pay("abc",6.0)


        #test normal premium car
        self.assertEqual(s2.pay("prem",5.0),10.0)

        s3 = ParkingSpot(3, 3, "occupied")
        s3.linked_car = StandardCar("stand")

        #test normal standard car
        self.assertEqual(s3.pay("stand",5.0), 15.0)










if __name__ == "__main__":
    unittest.main()

