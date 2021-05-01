import unittest
import numerated_challenge

class TestNumeratedMethods(unittest.TestCase):

    def test_get_routes(self):
        filter_type = "0,1"
        all_routes = numerated_challenge.get_routes(filter_type)
        self.assertEqual(8, len(all_routes))

    def test_get_stops(self):
        route_id = "Blue"
        stops = numerated_challenge.get_stops(route_id)
        self.assertEqual(12, len(stops))

    def test_get_directions(self):
        route_id = "Blue"
        directions = numerated_challenge.get_directions(route_id)
        self.assertEqual(2, len(directions))
        self.assertEqual('west', directions[0])
        self.assertEqual('east', directions[1])
        

    def test_get_predictions(self):
        route_id = "Blue"
        direction_id = 1
        stop_id = "place-bomnl"

        #test prediction and getting the next time from prediction
        predictions = numerated_challenge.get_predictions(route_id, stop_id, direction_id)
        time = numerated_challenge.get_next_departure_time(predictions)
        self.assertTrue(predictions)
        self.assertTrue(time)

    def test_name_to_id_methods(self):
        # test for routes
        filter_type = "0,1"
        all_routes = numerated_challenge.get_routes(filter_type)
        route_id = numerated_challenge.name_to_route_id("Red Line", all_routes)
        self.assertEqual(route_id, "Red")

        # test for stops
        route_id = "Blue"
        stops = numerated_challenge.get_stops(route_id)
        stop_id = numerated_challenge.name_to_stop_id("Maverick", stops)
        self.assertEqual(stop_id, "place-mvbcl")

        # test for directions
        directions = numerated_challenge.get_directions(route_id)
        direction_id = numerated_challenge.name_to_direction_id("East", directions)
        self.assertEqual(direction_id, 1)


if __name__ == '__main__':
    unittest.main()