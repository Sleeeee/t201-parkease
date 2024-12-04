import unittest
from src.controllers import ParkingController
from src.models import PremiumCar, StandardCar

class TestParkingController(unittest.TestCase):
    def test_new_entry_free(self):
        pc = ParkingController(update_db=False)
        pc.parking_lot.add_spot({"id": 1, "spot_number": 1, "row_number": 1, "floor_number": 1})
        self.assertEqual(pc.new_entry(1, 1, 1, "ABC-123"), "[NEW ENTRY] Car ABC-123 was successfully parked at floor 1 - row 1 - spot 1")
        self.assertEqual(pc.parking_lot.floors[1].rows[1].spots[1].status, "occupied")
        pc.parking_lot.add_spot({"id": 2, "spot_number": 2, "row_number": 7, "floor_number": -1})
        self.assertEqual(pc.new_entry(-1, 7, 2, "JAX-726"), "[NEW ENTRY] Car JAX-726 was successfully parked at floor -1 - row 7 - spot 2")
        self.assertEqual(pc.parking_lot.floors[-1].rows[7].spots[2].status, "occupied")

    def test_new_entry_occupied(self):
        pc = ParkingController(update_db=False)
        pc.parking_lot.add_spot({"id": 2, "spot_number": 2, "row_number": 7, "floor_number": -1})
        pc.parking_lot.floors[-1].rows[7].spots[2].status = "occupied"
        self.assertEqual(pc.new_entry(-1, 7, 2, "PIP-126"), "[Error] This spot is already occupied")
        self.assertEqual(pc.parking_lot.floors[-1].rows[7].spots[2].status, "occupied")
        pc.parking_lot.add_spot({"id": 1, "spot_number": 1, "row_number": 1, "floor_number": 1})
        pc.parking_lot.floors[1].rows[1].spots[1].status = "occupied"
        self.assertEqual(pc.new_entry(1, 1, 1, "ABC-123"), "[Error] This spot is already occupied")
        self.assertEqual(pc.parking_lot.floors[1].rows[1].spots[1].status, "occupied")

    def test_new_entry_non_existing(self):
        pc = ParkingController(update_db=False)
        self.assertEqual(pc.new_entry(1, 1, 1, "ABC-123"), "[Error] This spot does not exist")
        self.assertEqual(pc.new_entry(2, 12, 9, "RFC-1010"), "[Error] This spot does not exist")
        pc.parking_lot.add_spot({"id": 5, "spot_number": 1, "row_number": 1, "floor_number": 3})
        pc.parking_lot.add_spot({"id": 6, "spot_number": 2, "row_number": 1, "floor_number": 3})
        pc.parking_lot.add_spot({"id": 7, "spot_number": 3, "row_number": 1, "floor_number": 3})
        self.assertEqual(pc.new_entry(3, 1, 6, "BOB-974"), "[Error] This spot does not exist")

    def test_new_exit_matching(self):
        pc = ParkingController(update_db=False)
        pc.parking_lot.add_spot({"id": 1, "spot_number": 1, "row_number": 1, "floor_number": 1})
        s1 = pc.parking_lot.floors[1].rows[1].spots[1]
        s1.status = "occupied"
        s1.linked_car = StandardCar("ABC-123")
        self.assertEqual(pc.new_exit(1, 1, 1, "ABC-123"), "[NEW EXIT] Car ABC-123 was successfully parked out of floor 1 - row 1 - spot 1")
        self.assertEqual(s1.status, "free")

    def test_new_exit_non_matching(self):
        pc = ParkingController(update_db=False)
        pc.parking_lot.add_spot({"id": 1, "spot_number": 2, "row_number": 7, "floor_number": -1})
        s1 = pc.parking_lot.floors[-1].rows[7].spots[2]
        s1.status = "occupied"
        s1.linked_car = PremiumCar("JAX-726")
        self.assertEqual(pc.new_exit(-1, 7, 2, "PIP-126"), "[Error] This spot is unoccupied or the registration plates don't match")
        self.assertEqual(s1.status, "occupied")

    def test_new_exit_non_occupied(self):
        pc = ParkingController(update_db=False)
        pc.parking_lot.add_spot({"id": 1, "spot_number": 5, "row_number": 2, "floor_number": 3})
        self.assertEqual(pc.new_exit(3, 2, 5, "ANY-123"), "[Error] This spot is unoccupied or the registration plates don't match")
        self.assertEqual(pc.parking_lot.floors[3].rows[2].spots[5].status, "free")
        pc.parking_lot.add_spot({"id": 2, "spot_number": 8, "row_number": 4, "floor_number": -2})
        self.assertEqual(pc.new_exit(-2, 4, 8, "DEF-456"), "[Error] This spot is unoccupied or the registration plates don't match")
        self.assertEqual(pc.parking_lot.floors[-2].rows[4].spots[8].status, "free")

    def test_new_exit_non_existing(self):
        pc = ParkingController(update_db=False)
        self.assertEqual(pc.new_exit(2, 3, 7, "ABC-123"), "[Error] This spot does not exist")
        pc.parking_lot.add_spot({"id": 1, "spot_number": 1, "row_number": 1, "floor_number": 1})
        pc.parking_lot.add_spot({"id": 2, "spot_number": 2, "row_number": 1, "floor_number": 1})
        self.assertEqual(pc.new_exit(1, 1, 3, "XYZ-123"), "[Error] This spot does not exist")

if __name__ == "__main__":
    unittest.main()
